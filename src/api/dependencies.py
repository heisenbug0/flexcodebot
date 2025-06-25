"""
Dependency injection for shared services in FlexCode Bot.

This module provides dependency injection functions for FastAPI endpoints
to ensure proper service instantiation and lifecycle management.
"""

from functools import lru_cache
import os
from dotenv import load_dotenv

from ..services.x_handler import XHandler
from ..services.nlp_processor import NLPProcessor
from ..services.bet_converter import BetConverter
from ..utils.logger import get_logger

# Load environment variables
load_dotenv()

logger = get_logger(__name__)


@lru_cache()
def get_x_handler() -> XHandler:
    """
    Get X (Twitter) handler service instance.
    
    Returns:
        XHandler: Configured X API handler
    """
    return XHandler(
        api_key=os.getenv("X_API_KEY"),
        api_secret=os.getenv("X_API_SECRET"),
        access_token=os.getenv("X_ACCESS_TOKEN"),
        access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET")
    )


@lru_cache()
def get_nlp_processor() -> NLPProcessor:
    """
    Get NLP processor service instance.
    
    Returns:
        NLPProcessor: Configured NLP processor
    """
    return NLPProcessor(
        hugging_face_api_key=os.getenv("HUGGING_FACE_API_KEY")
    )


@lru_cache()
def get_bet_converter() -> BetConverter:
    """
    Get bet converter service instance.
    
    Returns:
        BetConverter: Configured bet code converter
    """
    return BetConverter(
        api_key=os.getenv("CONVERT_BET_API_KEY")
    )