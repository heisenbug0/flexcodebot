"""
NLP processor for extracting betting codes and platforms from text.

This module uses Hugging Face's Inference API to perform named entity recognition
and extract betting codes, original platforms, and target platforms from user messages.
"""

import re
import requests
import asyncio
from typing import List, Dict, Any, Optional
import json

from ..utils.logger import get_logger

logger = get_logger(__name__)


class NLPProcessor:
    """NLP processor for betting code and platform extraction."""
    
    def __init__(self, hugging_face_api_key: str):
        """
        Initialize NLP processor.
        
        Args:
            hugging_face_api_key: Hugging Face API key for inference
        """
        self.api_key = hugging_face_api_key
        self.api_url = "https://api-inference.huggingface.co/models/dslim/bert-base-NER"
        self.headers = {"Authorization": f"Bearer {hugging_face_api_key}"}
        
        # Known betting platforms for better matching
        self.known_platforms = {
            'stake', 'sportybet', 'bet9ja', '1xbet', 'betway', 'nairabet',
            'merrybet', 'betking', 'betnaija', 'supabet', 'betbonanza',
            'accessbet', 'betpawa', 'msport', 'parimatch', 'betfair'
        }
        
        logger.info("NLP processor initialized successfully")
    
    async def extract_betting_info(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract betting codes and platforms from text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            List of dictionaries containing code, original_platform, and target_platform
        """
        try:
            # Clean and preprocess text
            cleaned_text = self._preprocess_text(text)
            
            # Extract betting codes using regex
            codes = self._extract_codes(cleaned_text)
            
            # Extract platforms using NLP and keyword matching
            platforms = await self._extract_platforms(cleaned_text)
            
            # Parse conversion instructions
            conversion_pairs = self._parse_conversion_instructions(cleaned_text, codes, platforms)
            
            logger.info(f"Extracted {len(conversion_pairs)} betting code conversion pairs")
            return conversion_pairs
            
        except Exception as e:
            logger.error(f"Error in NLP extraction: {str(e)}")
            return []
    
    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess text for better extraction.
        
        Args:
            text: Raw input text
            
        Returns:
            Cleaned text
        """
        # Remove mentions and hashtags for cleaner processing
        text = re.sub(r'@\w+', '', text)
        text = re.sub(r'#\w+', '', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _extract_codes(self, text: str) -> List[str]:
        """
        Extract betting codes using regex patterns.
        
        Args:
            text: Input text
            
        Returns:
            List of extracted betting codes
        """
        # Common betting code patterns
        patterns = [
            r'\b[A-Z0-9]{6,12}\b',  # Alphanumeric codes 6-12 chars
            r'\b\d{8,15}\b',        # Numeric codes 8-15 digits
            r'\b[A-Z]{2,4}\d{4,8}\b',  # Letter prefix + numbers
        ]
        
        codes = []
        for pattern in patterns:
            matches = re.findall(pattern, text.upper())
            codes.extend(matches)
        
        # Remove duplicates while preserving order
        unique_codes = []
        for code in codes:
            if code not in unique_codes:
                unique_codes.append(code)
        
        logger.debug(f"Extracted codes: {unique_codes}")
        return unique_codes
    
    async def _extract_platforms(self, text: str) -> List[str]:
        """
        Extract betting platforms using NLP and keyword matching.
        
        Args:
            text: Input text
            
        Returns:
            List of extracted platform names
        """
        platforms = []
        
        # First, try keyword matching for known platforms
        text_lower = text.lower()
        for platform in self.known_platforms:
            if platform in text_lower:
                platforms.append(platform.title())
        
        # Use NLP for additional entity extraction
        try:
            nlp_platforms = await self._nlp_extract_entities(text)
            platforms.extend(nlp_platforms)
        except Exception as e:
            logger.warning(f"NLP entity extraction failed: {str(e)}")
        
        # Remove duplicates while preserving order
        unique_platforms = []
        for platform in platforms:
            if platform not in unique_platforms:
                unique_platforms.append(platform)
        
        logger.debug(f"Extracted platforms: {unique_platforms}")
        return unique_platforms
    
    async def _nlp_extract_entities(self, text: str) -> List[str]:
        """
        Use Hugging Face NER model to extract entities.
        
        Args:
            text: Input text
            
        Returns:
            List of extracted platform names
        """
        try:
            payload = {"inputs": text}
            
            # Make async request to Hugging Face API
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: requests.post(self.api_url, headers=self.headers, json=payload)
            )
            
            if response.status_code != 200:
                logger.warning(f"Hugging Face API returned status {response.status_code}")
                return []
            
            entities = response.json()
            
            # Extract organization names that might be betting platforms
            platforms = []
            for entity in entities:
                if entity.get('entity_group') == 'ORG' or entity.get('entity') in ['B-ORG', 'I-ORG']:
                    word = entity.get('word', '').replace('##', '').strip()
                    if word and len(word) > 2:
                        platforms.append(word.title())
            
            return platforms
            
        except Exception as e:
            logger.error(f"NLP entity extraction error: {str(e)}")
            return []
    
    def _parse_conversion_instructions(
        self,
        text: str,
        codes: List[str],
        platforms: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Parse conversion instructions to map codes to platforms.
        
        Args:
            text: Input text
            codes: Extracted betting codes
            platforms: Extracted platform names
            
        Returns:
            List of conversion mappings
        """
        conversion_pairs = []
        text_lower = text.lower()
        
        # Pattern matching for conversion instructions
        conversion_patterns = [
            r'convert\s+(\w+)\s+code\s+(\w+)\s+to\s+(\w+)',
            r'(\w+)\s+code\s+(\w+)\s+to\s+(\w+)',
            r'from\s+(\w+)\s+(\w+)\s+to\s+(\w+)',
            r'(\w+)\s+(\w+)\s+to\s+(\w+)'
        ]
        
        for pattern in conversion_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                groups = match.groups()
                if len(groups) >= 3:
                    # Try to identify which group is the code
                    potential_code = None
                    original_platform = None
                    target_platform = None
                    
                    for group in groups:
                        if group.upper() in [code.upper() for code in codes]:
                            potential_code = group.upper()
                        elif group.title() in platforms or group.lower() in self.known_platforms:
                            if original_platform is None:
                                original_platform = group.title()
                            else:
                                target_platform = group.title()
                    
                    if potential_code:
                        conversion_pairs.append({
                            'code': potential_code,
                            'original_platform': original_platform,
                            'target_platform': target_platform
                        })
        
        # If no specific patterns found, try to match codes with platforms sequentially
        if not conversion_pairs and codes:
            for i, code in enumerate(codes):
                original_platform = platforms[i * 2] if i * 2 < len(platforms) else None
                target_platform = platforms[i * 2 + 1] if i * 2 + 1 < len(platforms) else None
                
                conversion_pairs.append({
                    'code': code,
                    'original_platform': original_platform,
                    'target_platform': target_platform
                })
        
        # If still no pairs and we have codes, create entries with missing platforms
        if not conversion_pairs and codes:
            for code in codes:
                conversion_pairs.append({
                    'code': code,
                    'original_platform': None,
                    'target_platform': None
                })
        
        return conversion_pairs