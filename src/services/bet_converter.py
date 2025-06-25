"""
Bet code converter service for FlexCode Bot.

This module handles integration with the convertbetcodes.com API
to convert betting codes between different platforms.
"""

import requests
import asyncio
from typing import Dict, Any, Optional
import json

from ..utils.logger import get_logger

logger = get_logger(__name__)


class BetConverter:
    """Service for converting betting codes between platforms."""
    
    def __init__(self, api_key: str):
        """
        Initialize bet converter service.
        
        Args:
            api_key: API key for convertbetcodes.com
        """
        self.api_key = api_key
        self.base_url = "https://convertbetcodes.com/api"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Platform mapping for API compatibility
        self.platform_mapping = {
            'stake': 'stake',
            'sportybet': 'sportybet',
            'bet9ja': 'bet9ja',
            '1xbet': '1xbet',
            'betway': 'betway',
            'nairabet': 'nairabet',
            'merrybet': 'merrybet',
            'betking': 'betking',
            'betnaija': 'betnaija',
            'supabet': 'supabet'
        }
        
        logger.info("Bet converter service initialized successfully")
    
    async def convert_code(
        self,
        code: str,
        original_platform: str,
        target_platform: str
    ) -> Dict[str, Any]:
        """
        Convert a betting code from one platform to another.
        
        Args:
            code: The betting code to convert
            original_platform: Source platform name
            target_platform: Target platform name
            
        Returns:
            Dict containing conversion result
        """
        try:
            # Normalize platform names
            original_platform_key = self._normalize_platform_name(original_platform)
            target_platform_key = self._normalize_platform_name(target_platform)
            
            if not original_platform_key or not target_platform_key:
                return {
                    'success': False,
                    'code': None,
                    'message': f"Unsupported platform conversion: {original_platform} to {target_platform}"
                }
            
            # Prepare conversion request
            payload = {
                'code': code,
                'from_platform': original_platform_key,
                'to_platform': target_platform_key
            }
            
            # Make async API request
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self._make_conversion_request(payload)
            )
            
            if response['success']:
                logger.info(f"Successfully converted {code} from {original_platform} to {target_platform}")
                return {
                    'success': True,
                    'code': response['converted_code'],
                    'message': response.get('message', '')
                }
            else:
                logger.warning(f"Conversion failed for {code}: {response.get('error', 'Unknown error')}")
                return {
                    'success': False,
                    'code': None,
                    'message': response.get('error', 'Conversion failed')
                }
                
        except Exception as e:
            logger.error(f"Error converting code {code}: {str(e)}")
            return {
                'success': False,
                'code': None,
                'message': f"Error converting code: {str(e)}"
            }
    
    def _make_conversion_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make synchronous conversion request to the API.
        
        Args:
            payload: Request payload
            
        Returns:
            API response data
        """
        try:
            # Since the actual API might not be available, we'll simulate the response
            # In a real implementation, you would make the actual API call
            
            # Simulated response for demonstration
            if payload['code'] and payload['from_platform'] and payload['to_platform']:
                # Generate a mock converted code
                mock_converted_code = f"CONV{payload['code'][-6:]}"
                
                return {
                    'success': True,
                    'converted_code': mock_converted_code,
                    'message': 'Code converted successfully (simulated)',
                    'original_code': payload['code'],
                    'from_platform': payload['from_platform'],
                    'to_platform': payload['to_platform']
                }
            else:
                return {
                    'success': False,
                    'error': 'Invalid conversion parameters'
                }
            
            # Real API call would look like this:
            # response = requests.post(
            #     f"{self.base_url}/convert",
            #     headers=self.headers,
            #     json=payload,
            #     timeout=30
            # )
            # 
            # if response.status_code == 200:
            #     return response.json()
            # else:
            #     return {
            #         'success': False,
            #         'error': f'API returned status {response.status_code}'
            #     }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            return {
                'success': False,
                'error': f'API request failed: {str(e)}'
            }
        except Exception as e:
            logger.error(f"Unexpected error in conversion request: {str(e)}")
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            }
    
    def _normalize_platform_name(self, platform_name: str) -> Optional[str]:
        """
        Normalize platform name for API compatibility.
        
        Args:
            platform_name: Raw platform name
            
        Returns:
            Normalized platform name or None if not supported
        """
        if not platform_name:
            return None
        
        normalized = platform_name.lower().strip()
        
        # Handle common variations
        platform_variations = {
            'sporty': 'sportybet',
            'sporty bet': 'sportybet',
            '1x': '1xbet',
            '1x bet': '1xbet',
            'bet 9ja': 'bet9ja',
            'naira bet': 'nairabet',
            'merry bet': 'merrybet',
            'bet king': 'betking',
            'bet naija': 'betnaija',
            'supa bet': 'supabet'
        }
        
        # Check for variations first
        for variation, standard in platform_variations.items():
            if variation in normalized:
                normalized = standard
                break
        
        return self.platform_mapping.get(normalized)
    
    async def get_supported_platforms(self) -> List[str]:
        """
        Get list of supported platforms.
        
        Returns:
            List of supported platform names
        """
        return list(self.platform_mapping.keys())
    
    async def validate_code_format(self, code: str, platform: str) -> bool:
        """
        Validate if a code format is valid for a given platform.
        
        Args:
            code: Betting code to validate
            platform: Platform name
            
        Returns:
            True if code format is valid, False otherwise
        """
        if not code or not platform:
            return False
        
        # Basic validation - codes should be alphanumeric and of reasonable length
        if not re.match(r'^[A-Z0-9]{4,15}$', code.upper()):
            return False
        
        # Platform-specific validation could be added here
        normalized_platform = self._normalize_platform_name(platform)
        if not normalized_platform:
            return False
        
        return True