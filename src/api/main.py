"""
FlexCode Bot - Main FastAPI Application

A betting code conversion bot that processes X (Twitter) mentions and DMs
to convert betting codes between different platforms using NLP and external APIs.
"""

from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from typing import Dict, Any

from ..models.entities import (
    HealthResponse,
    ProcessMentionRequest,
    ProcessDMRequest,
    BetCodeResponse
)
from ..services.x_handler import XHandler
from ..services.nlp_processor import NLPProcessor
from ..services.bet_converter import BetConverter
from ..bot.twitter_bot import bot_manager
from ..utils.logger import get_logger
from .dependencies import (
    get_x_handler,
    get_nlp_processor,
    get_bet_converter
)

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    logger.info("FlexCode Bot starting up...")
    
    # Start the Twitter bot monitoring
    try:
        x_handler = get_x_handler()
        nlp_processor = get_nlp_processor()
        bet_converter = get_bet_converter()
        
        bot_manager.start_bot(x_handler, nlp_processor, bet_converter)
        logger.info("Twitter bot monitoring started")
    except Exception as e:
        logger.error(f"Failed to start Twitter bot: {str(e)}")
    
    yield
    
    # Stop the Twitter bot
    try:
        bot_manager.stop_bot()
        logger.info("Twitter bot monitoring stopped")
    except Exception as e:
        logger.error(f"Error stopping Twitter bot: {str(e)}")
    
    logger.info("FlexCode Bot shutting down...")


app = FastAPI(
    title="FlexCode Bot",
    description="A betting code conversion bot for X (Twitter) mentions and DMs",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint to verify server status.
    
    Returns:
        HealthResponse: Server status information
    """
    logger.info("Health check requested")
    bot_status = bot_manager.get_bot_status()
    
    return HealthResponse(
        status="ok", 
        message=f"FlexCode Bot is running. Twitter bot status: {bot_status['status']}"
    )


@app.get("/bot/status")
async def get_bot_status() -> Dict[str, Any]:
    """
    Get Twitter bot status.
    
    Returns:
        Dict with bot status information
    """
    return bot_manager.get_bot_status()


@app.post("/bot/start")
async def start_bot(
    x_handler: XHandler = Depends(get_x_handler),
    nlp_processor: NLPProcessor = Depends(get_nlp_processor),
    bet_converter: BetConverter = Depends(get_bet_converter)
) -> Dict[str, str]:
    """
    Manually start the Twitter bot.
    
    Returns:
        Status message
    """
    try:
        bot_manager.start_bot(x_handler, nlp_processor, bet_converter)
        return {"message": "Twitter bot started successfully"}
    except Exception as e:
        logger.error(f"Failed to start bot: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/bot/stop")
async def stop_bot() -> Dict[str, str]:
    """
    Manually stop the Twitter bot.
    
    Returns:
        Status message
    """
    try:
        bot_manager.stop_bot()
        return {"message": "Twitter bot stopped successfully"}
    except Exception as e:
        logger.error(f"Failed to stop bot: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/test/mention")
async def test_mention_processing(
    tweet_id: str,
    user_handle: str,
    message_text: str
) -> Dict[str, str]:
    """
    Test mention processing manually (for development/testing).
    
    Args:
        tweet_id: Test tweet ID
        user_handle: Test user handle
        message_text: Test message text
    
    Returns:
        Processing result
    """
    if not bot_manager.bot:
        raise HTTPException(status_code=400, detail="Bot is not running")
    
    try:
        await bot_manager.bot.process_manual_mention(tweet_id, user_handle, message_text)
        return {"message": "Mention processed successfully"}
    except Exception as e:
        logger.error(f"Failed to process test mention: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/process_mention", response_model=BetCodeResponse)
async def process_mention(
    request: ProcessMentionRequest,
    background_tasks: BackgroundTasks,
    x_handler: XHandler = Depends(get_x_handler),
    nlp_processor: NLPProcessor = Depends(get_nlp_processor),
    bet_converter: BetConverter = Depends(get_bet_converter)
) -> BetCodeResponse:
    """
    Process X (Twitter) mentions for betting code conversion.
    
    Args:
        request: The mention processing request
        background_tasks: FastAPI background tasks
        x_handler: X API handler service
        nlp_processor: NLP processing service
        bet_converter: Bet conversion service
    
    Returns:
        BetCodeResponse: Processing result with converted codes or error message
    """
    try:
        logger.info(f"Processing mention from user: {request.user_handle}")
        
        # Extract betting codes and platforms using NLP
        extracted_data = await nlp_processor.extract_betting_info(request.message_text)
        
        if not extracted_data:
            error_msg = "No betting codes or platforms found in your message. Please include codes and specify platforms."
            background_tasks.add_task(
                x_handler.reply_to_mention,
                request.tweet_id,
                request.user_handle,
                error_msg
            )
            return BetCodeResponse(
                success=False,
                message=error_msg,
                converted_codes=[]
            )
        
        # Check for missing platforms
        missing_platforms = [
            item for item in extracted_data 
            if not item.get('original_platform') or not item.get('target_platform')
        ]
        
        if missing_platforms:
            codes_str = ", ".join([item['code'] for item in missing_platforms])
            clarification_msg = f"Please specify the original and target platforms for code(s): {codes_str}"
            background_tasks.add_task(
                x_handler.reply_to_mention,
                request.tweet_id,
                request.user_handle,
                clarification_msg
            )
            return BetCodeResponse(
                success=False,
                message=clarification_msg,
                converted_codes=[]
            )
        
        # Convert betting codes
        converted_results = []
        for item in extracted_data:
            try:
                converted_code = await bet_converter.convert_code(
                    item['code'],
                    item['original_platform'],
                    item['target_platform']
                )
                converted_results.append({
                    'original_code': item['code'],
                    'original_platform': item['original_platform'],
                    'target_platform': item['target_platform'],
                    'converted_code': converted_code['code'],
                    'message': converted_code.get('message', '')
                })
            except Exception as e:
                logger.error(f"Failed to convert code {item['code']}: {str(e)}")
                converted_results.append({
                    'original_code': item['code'],
                    'original_platform': item['original_platform'],
                    'target_platform': item['target_platform'],
                    'converted_code': None,
                    'message': f"Failed to convert code {item['code']}"
                })
        
        # Format reply message
        reply_parts = []
        for result in converted_results:
            if result['converted_code']:
                part = f"{result['original_platform']} {result['original_code']} to {result['target_platform']}: {result['converted_code']}"
                if result['message']:
                    part += f" ({result['message']})"
            else:
                part = f"{result['original_platform']} {result['original_code']}: {result['message']}"
            reply_parts.append(part)
        
        reply_message = f"Converted codes: {'; '.join(reply_parts)}"
        
        # Send reply in background
        background_tasks.add_task(
            x_handler.reply_to_mention,
            request.tweet_id,
            request.user_handle,
            reply_message
        )
        
        return BetCodeResponse(
            success=True,
            message="Codes processed successfully",
            converted_codes=converted_results
        )
        
    except Exception as e:
        logger.error(f"Error processing mention: {str(e)}")
        error_msg = "Sorry, I encountered an error processing your request. Please try again."
        background_tasks.add_task(
            x_handler.reply_to_mention,
            request.tweet_id,
            request.user_handle,
            error_msg
        )
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/process_dm", response_model=BetCodeResponse)
async def process_dm(
    request: ProcessDMRequest,
    background_tasks: BackgroundTasks,
    x_handler: XHandler = Depends(get_x_handler),
    nlp_processor: NLPProcessor = Depends(get_nlp_processor),
    bet_converter: BetConverter = Depends(get_bet_converter)
) -> BetCodeResponse:
    """
    Process X (Twitter) direct messages for betting code conversion.
    
    Args:
        request: The DM processing request
        background_tasks: FastAPI background tasks
        x_handler: X API handler service
        nlp_processor: NLP processing service
        bet_converter: Bet conversion service
    
    Returns:
        BetCodeResponse: Processing result with converted codes or error message
    """
    try:
        logger.info(f"Processing DM from user: {request.user_handle}")
        
        # Extract betting codes and platforms using NLP
        extracted_data = await nlp_processor.extract_betting_info(request.message_text)
        
        if not extracted_data:
            error_msg = "No betting codes or platforms found in your message. Please include codes and specify platforms."
            background_tasks.add_task(
                x_handler.send_dm,
                request.user_id,
                error_msg
            )
            return BetCodeResponse(
                success=False,
                message=error_msg,
                converted_codes=[]
            )
        
        # Check for missing platforms
        missing_platforms = [
            item for item in extracted_data 
            if not item.get('original_platform') or not item.get('target_platform')
        ]
        
        if missing_platforms:
            codes_str = ", ".join([item['code'] for item in missing_platforms])
            clarification_msg = f"Please specify the original and target platforms for code(s): {codes_str}"
            background_tasks.add_task(
                x_handler.send_dm,
                request.user_id,
                clarification_msg
            )
            return BetCodeResponse(
                success=False,
                message=clarification_msg,
                converted_codes=[]
            )
        
        # Convert betting codes
        converted_results = []
        for item in extracted_data:
            try:
                converted_code = await bet_converter.convert_code(
                    item['code'],
                    item['original_platform'],
                    item['target_platform']
                )
                converted_results.append({
                    'original_code': item['code'],
                    'original_platform': item['original_platform'],
                    'target_platform': item['target_platform'],
                    'converted_code': converted_code['code'],
                    'message': converted_code.get('message', '')
                })
            except Exception as e:
                logger.error(f"Failed to convert code {item['code']}: {str(e)}")
                converted_results.append({
                    'original_code': item['code'],
                    'original_platform': item['original_platform'],
                    'target_platform': item['target_platform'],
                    'converted_code': None,
                    'message': f"Failed to convert code {item['code']}"
                })
        
        # Format reply message
        reply_parts = []
        for result in converted_results:
            if result['converted_code']:
                part = f"{result['original_platform']} {result['original_code']} to {result['target_platform']}: {result['converted_code']}"
                if result['message']:
                    part += f" ({result['message']})"
            else:
                part = f"{result['original_platform']} {result['original_code']}: {result['message']}"
            reply_parts.append(part)
        
        reply_message = f"Converted codes: {'; '.join(reply_parts)}"
        
        # Send DM reply in background
        background_tasks.add_task(
            x_handler.send_dm,
            request.user_id,
            reply_message
        )
        
        return BetCodeResponse(
            success=True,
            message="Codes processed successfully",
            converted_codes=converted_results
        )
        
    except Exception as e:
        logger.error(f"Error processing DM: {str(e)}")
        error_msg = "Sorry, I encountered an error processing your request. Please try again."
        background_tasks.add_task(
            x_handler.send_dm,
            request.user_id,
            error_msg
        )
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)