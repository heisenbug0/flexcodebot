"""
Pydantic models for FlexCode Bot requests and responses.

This module defines all the data models used for API request/response validation
and internal data structures.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Server status")
    message: str = Field(..., description="Status message")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")


class ProcessMentionRequest(BaseModel):
    """Request model for processing X mentions."""
    tweet_id: str = Field(..., description="ID of the tweet containing the mention")
    user_handle: str = Field(..., description="Handle of the user who mentioned the bot")
    user_id: str = Field(..., description="ID of the user who mentioned the bot")
    message_text: str = Field(..., description="Text content of the mention")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp of the mention")


class ProcessDMRequest(BaseModel):
    """Request model for processing X direct messages."""
    message_id: str = Field(..., description="ID of the direct message")
    user_handle: str = Field(..., description="Handle of the user who sent the DM")
    user_id: str = Field(..., description="ID of the user who sent the DM")
    message_text: str = Field(..., description="Text content of the DM")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp of the DM")


class BetCodeInfo(BaseModel):
    """Model for betting code information."""
    code: str = Field(..., description="The betting code")
    original_platform: Optional[str] = Field(None, description="Original betting platform")
    target_platform: Optional[str] = Field(None, description="Target betting platform")


class ConvertedCode(BaseModel):
    """Model for converted betting code result."""
    original_code: str = Field(..., description="Original betting code")
    original_platform: str = Field(..., description="Original betting platform")
    target_platform: str = Field(..., description="Target betting platform")
    converted_code: Optional[str] = Field(None, description="Converted betting code")
    message: str = Field(default="", description="Additional message about the conversion")


class BetCodeResponse(BaseModel):
    """Response model for betting code processing."""
    success: bool = Field(..., description="Whether the processing was successful")
    message: str = Field(..., description="Response message")
    converted_codes: List[ConvertedCode] = Field(default_factory=list, description="List of converted codes")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")


class NLPExtractionResult(BaseModel):
    """Model for NLP extraction results."""
    codes: List[str] = Field(default_factory=list, description="Extracted betting codes")
    original_platforms: List[str] = Field(default_factory=list, description="Extracted original platforms")
    target_platforms: List[str] = Field(default_factory=list, description="Extracted target platforms")
    entities: List[Dict[str, Any]] = Field(default_factory=list, description="Raw NLP entities")


class ConversionRequest(BaseModel):
    """Model for bet code conversion request."""
    code: str = Field(..., description="Betting code to convert")
    original_platform: str = Field(..., description="Original betting platform")
    target_platform: str = Field(..., description="Target betting platform")


class ConversionResponse(BaseModel):
    """Model for bet code conversion response."""
    success: bool = Field(..., description="Whether the conversion was successful")
    code: Optional[str] = Field(None, description="Converted betting code")
    message: str = Field(default="", description="Conversion message or error details")
    original_code: str = Field(..., description="Original betting code")
    original_platform: str = Field(..., description="Original betting platform")
    target_platform: str = Field(..., description="Target betting platform")