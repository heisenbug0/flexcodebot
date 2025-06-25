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
    yield
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
    return HealthResponse(status="ok", message="FlexCode Bot is running")


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