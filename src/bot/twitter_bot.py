"""
Twitter Bot for FlexCode - Real-time monitoring and response.

This module implements the actual Twitter bot that monitors mentions and DMs,
processes them through the backend services, and responds automatically.
"""

import asyncio
import tweepy
import threading
import time
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from ..services.x_handler import XHandler
from ..services.nlp_processor import NLPProcessor
from ..services.bet_converter import BetConverter
from ..utils.logger import get_logger

logger = get_logger(__name__)


class FlexCodeTwitterBot:
    """
    Main Twitter bot class that monitors mentions and DMs.
    """
    
    def __init__(
        self,
        x_handler: XHandler,
        nlp_processor: NLPProcessor,
        bet_converter: BetConverter
    ):
        """
        Initialize the Twitter bot.
        
        Args:
            x_handler: X API handler
            nlp_processor: NLP processing service
            bet_converter: Bet conversion service
        """
        self.x_handler = x_handler
        self.nlp_processor = nlp_processor
        self.bet_converter = bet_converter
        
        # Track processed tweets to avoid duplicates
        self.processed_mentions = set()
        self.processed_dms = set()
        
        # Bot status
        self.is_running = False
        self.last_mention_id = None
        
        logger.info("FlexCode Twitter Bot initialized")
    
    async def start_monitoring(self):
        """
        Start monitoring Twitter for mentions and DMs.
        """
        logger.info("Starting Twitter bot monitoring...")
        self.is_running = True
        
        # Validate credentials first
        if not self.x_handler.validate_credentials():
            logger.error("Invalid Twitter credentials. Bot cannot start.")
            return
        
        # Start monitoring tasks
        mention_task = asyncio.create_task(self._monitor_mentions())
        dm_task = asyncio.create_task(self._monitor_dms())
        
        try:
            await asyncio.gather(mention_task, dm_task)
        except Exception as e:
            logger.error(f"Error in bot monitoring: {str(e)}")
        finally:
            self.is_running = False
    
    def stop_monitoring(self):
        """
        Stop the Twitter bot monitoring.
        """
        logger.info("Stopping Twitter bot monitoring...")
        self.is_running = False
    
    async def _monitor_mentions(self):
        """
        Monitor Twitter mentions in a loop.
        """
        logger.info("Starting mention monitoring...")
        
        while self.is_running:
            try:
                # Get recent mentions
                mentions = await self.x_handler.get_mentions(
                    since_id=self.last_mention_id,
                    max_results=10
                )
                
                if mentions:
                    logger.info(f"Found {len(mentions)} new mentions")
                    
                    for mention in mentions:
                        if mention['tweet_id'] not in self.processed_mentions:
                            await self._process_mention(mention)
                            self.processed_mentions.add(mention['tweet_id'])
                            self.last_mention_id = mention['tweet_id']
                
                # Wait before next check (avoid rate limits)
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Error monitoring mentions: {str(e)}")
                await asyncio.sleep(60)  # Wait longer on error
    
    async def _monitor_dms(self):
        """
        Monitor Twitter DMs in a loop.
        """
        logger.info("Starting DM monitoring...")
        
        while self.is_running:
            try:
                # Note: DM monitoring would require additional implementation
                # For now, we'll log that it's running
                logger.debug("DM monitoring active (implementation pending)")
                
                # Wait before next check
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Error monitoring DMs: {str(e)}")
                await asyncio.sleep(120)  # Wait longer on error
    
    async def _process_mention(self, mention: Dict[str, Any]):
        """
        Process a Twitter mention.
        
        Args:
            mention: Mention data from Twitter API
        """
        try:
            tweet_id = mention['tweet_id']
            author_id = mention['author_id']
            text = mention['text']
            
            logger.info(f"Processing mention {tweet_id} from user {author_id}")
            
            # Get user info
            user_info = await self.x_handler.get_user_info(author_id)
            if not user_info:
                logger.warning(f"Could not get user info for {author_id}")
                return
            
            user_handle = user_info['username']
            
            # Extract betting codes and platforms using NLP
            extracted_data = await self.nlp_processor.extract_betting_info(text)
            
            if not extracted_data:
                error_msg = "No betting codes or platforms found in your message. Please include codes and specify platforms."
                await self.x_handler.reply_to_mention(tweet_id, user_handle, error_msg)
                return
            
            # Check for missing platforms
            missing_platforms = [
                item for item in extracted_data 
                if not item.get('original_platform') or not item.get('target_platform')
            ]
            
            if missing_platforms:
                codes_str = ", ".join([item['code'] for item in missing_platforms])
                clarification_msg = f"Please specify the original and target platforms for code(s): {codes_str}"
                await self.x_handler.reply_to_mention(tweet_id, user_handle, clarification_msg)
                return
            
            # Convert betting codes
            converted_results = []
            for item in extracted_data:
                try:
                    converted_code = await self.bet_converter.convert_code(
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
            
            # Send reply
            await self.x_handler.reply_to_mention(tweet_id, user_handle, reply_message)
            
            logger.info(f"Successfully processed mention {tweet_id}")
            
        except Exception as e:
            logger.error(f"Error processing mention: {str(e)}")
            try:
                error_msg = "Sorry, I encountered an error processing your request. Please try again."
                await self.x_handler.reply_to_mention(tweet_id, user_handle, error_msg)
            except:
                pass  # Don't fail if we can't send error message
    
    async def process_manual_mention(self, tweet_id: str, user_handle: str, message_text: str):
        """
        Manually process a mention (for testing).
        
        Args:
            tweet_id: Tweet ID
            user_handle: User handle
            message_text: Message text
        """
        mention_data = {
            'tweet_id': tweet_id,
            'author_id': 'test_user_id',
            'text': message_text
        }
        
        # Mock user info for testing
        original_get_user_info = self.x_handler.get_user_info
        self.x_handler.get_user_info = lambda user_id: {'username': user_handle}
        
        try:
            await self._process_mention(mention_data)
        finally:
            # Restore original method
            self.x_handler.get_user_info = original_get_user_info


class TwitterBotManager:
    """
    Manager class to handle bot lifecycle.
    """
    
    def __init__(self):
        self.bot: Optional[FlexCodeTwitterBot] = None
        self.bot_thread: Optional[threading.Thread] = None
    
    def start_bot(
        self,
        x_handler: XHandler,
        nlp_processor: NLPProcessor,
        bet_converter: BetConverter
    ):
        """
        Start the Twitter bot in a separate thread.
        
        Args:
            x_handler: X API handler
            nlp_processor: NLP processor
            bet_converter: Bet converter
        """
        if self.bot and self.bot.is_running:
            logger.warning("Bot is already running")
            return
        
        self.bot = FlexCodeTwitterBot(x_handler, nlp_processor, bet_converter)
        
        def run_bot():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(self.bot.start_monitoring())
            except Exception as e:
                logger.error(f"Bot thread error: {str(e)}")
            finally:
                loop.close()
        
        self.bot_thread = threading.Thread(target=run_bot, daemon=True)
        self.bot_thread.start()
        
        logger.info("Twitter bot started in background thread")
    
    def stop_bot(self):
        """
        Stop the Twitter bot.
        """
        if self.bot:
            self.bot.stop_monitoring()
            self.bot = None
        
        if self.bot_thread:
            self.bot_thread.join(timeout=5)
            self.bot_thread = None
        
        logger.info("Twitter bot stopped")
    
    def get_bot_status(self) -> Dict[str, Any]:
        """
        Get bot status information.
        
        Returns:
            Dict with bot status
        """
        if not self.bot:
            return {"status": "stopped", "is_running": False}
        
        return {
            "status": "running" if self.bot.is_running else "stopped",
            "is_running": self.bot.is_running,
            "processed_mentions": len(self.bot.processed_mentions),
            "processed_dms": len(self.bot.processed_dms)
        }


# Global bot manager instance
bot_manager = TwitterBotManager()