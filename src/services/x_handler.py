"""
X (Twitter) API handler for FlexCode Bot.

This module handles all interactions with the X API including:
- Monitoring mentions and DMs
- Sending replies and DMs
- Authentication and rate limiting
"""

import tweepy
import asyncio
from typing import Optional, Dict, Any
import logging

from ..utils.logger import get_logger

logger = get_logger(__name__)


class XHandler:
    """Handler for X (Twitter) API operations."""
    
    def __init__(
        self,
        api_key: str,
        api_secret: str,
        access_token: str,
        access_token_secret: str
    ):
        """
        Initialize X API handler.
        
        Args:
            api_key: X API key
            api_secret: X API secret
            access_token: X access token
            access_token_secret: X access token secret
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        
        # Initialize Tweepy client
        self.client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            wait_on_rate_limit=True
        )
        
        # Initialize API v1.1 for DMs (if needed)
        auth = tweepy.OAuth1UserHandler(
            api_key, api_secret, access_token, access_token_secret
        )
        self.api_v1 = tweepy.API(auth, wait_on_rate_limit=True)
        
        logger.info("X API handler initialized successfully")
    
    async def reply_to_mention(
        self,
        tweet_id: str,
        user_handle: str,
        message: str
    ) -> Optional[Dict[str, Any]]:
        """
        Reply to a mention on X.
        
        Args:
            tweet_id: ID of the tweet to reply to
            user_handle: Handle of the user to mention in reply
            message: Reply message content
            
        Returns:
            Dict containing reply information or None if failed
        """
        try:
            # Format reply with user mention
            reply_text = f"@{user_handle} {message}"
            
            # Ensure reply is within character limit
            if len(reply_text) > 280:
                reply_text = reply_text[:277] + "..."
            
            # Send reply
            response = self.client.create_tweet(
                text=reply_text,
                in_reply_to_tweet_id=tweet_id
            )
            
            logger.info(f"Successfully replied to mention from @{user_handle}")
            return {
                "tweet_id": response.data["id"],
                "text": reply_text,
                "user_handle": user_handle
            }
            
        except Exception as e:
            logger.error(f"Failed to reply to mention from @{user_handle}: {str(e)}")
            return None
    
    async def send_dm(
        self,
        user_id: str,
        message: str
    ) -> Optional[Dict[str, Any]]:
        """
        Send a direct message to a user.
        
        Args:
            user_id: ID of the user to send DM to
            message: DM content
            
        Returns:
            Dict containing DM information or None if failed
        """
        try:
            # Note: DM functionality requires additional permissions
            # This is a placeholder implementation
            logger.info(f"DM functionality not fully implemented. Would send to user {user_id}: {message}")
            
            # In a real implementation, you would use:
            # response = self.api_v1.send_direct_message(recipient_id=user_id, text=message)
            
            return {
                "user_id": user_id,
                "message": message,
                "status": "simulated"
            }
            
        except Exception as e:
            logger.error(f"Failed to send DM to user {user_id}: {str(e)}")
            return None
    
    async def get_mentions(
        self,
        since_id: Optional[str] = None,
        max_results: int = 10
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get recent mentions of the bot.
        
        Args:
            since_id: Only return mentions after this tweet ID
            max_results: Maximum number of mentions to return
            
        Returns:
            List of mention data or None if failed
        """
        try:
            # Get bot's user ID first
            me = self.client.get_me()
            if not me.data:
                logger.error("Failed to get bot user information")
                return None
            
            # Search for mentions
            mentions = self.client.get_users_mentions(
                id=me.data.id,
                since_id=since_id,
                max_results=max_results,
                tweet_fields=["created_at", "author_id", "in_reply_to_user_id"],
                user_fields=["username"]
            )
            
            if not mentions.data:
                return []
            
            mention_list = []
            for mention in mentions.data:
                mention_data = {
                    "tweet_id": mention.id,
                    "text": mention.text,
                    "author_id": mention.author_id,
                    "created_at": mention.created_at,
                    "in_reply_to_user_id": mention.in_reply_to_user_id
                }
                mention_list.append(mention_data)
            
            logger.info(f"Retrieved {len(mention_list)} mentions")
            return mention_list
            
        except Exception as e:
            logger.error(f"Failed to get mentions: {str(e)}")
            return None
    
    async def get_user_info(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user information by user ID.
        
        Args:
            user_id: X user ID
            
        Returns:
            Dict containing user information or None if failed
        """
        try:
            user = self.client.get_user(id=user_id)
            if not user.data:
                return None
            
            return {
                "id": user.data.id,
                "username": user.data.username,
                "name": user.data.name
            }
            
        except Exception as e:
            logger.error(f"Failed to get user info for {user_id}: {str(e)}")
            return None
    
    def validate_credentials(self) -> bool:
        """
        Validate X API credentials.
        
        Returns:
            True if credentials are valid, False otherwise
        """
        try:
            me = self.client.get_me()
            if me.data:
                logger.info(f"X API credentials validated for user: @{me.data.username}")
                return True
            return False
        except Exception as e:
            logger.error(f"X API credential validation failed: {str(e)}")
            return False