"""
Tests for bet code converter functionality.

This module contains unit tests for the bet converter service,
testing code conversion capabilities and API integration.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from typing import Dict, Any

from src.services.bet_converter import BetConverter


class TestBetConverter:
    """Test cases for bet converter."""
    
    @pytest.fixture
    def bet_converter(self):
        """Create bet converter instance for testing."""
        return BetConverter(api_key="test_api_key")
    
    def test_initialization(self, bet_converter):
        """Test bet converter initialization."""
        assert bet_converter.api_key == "test_api_key"
        assert bet_converter.base_url == "https://convertbetcodes.com/api"
        assert "Authorization" in bet_converter.headers
        assert len(bet_converter.platform_mapping) > 0
    
    def test_normalize_platform_name(self, bet_converter):
        """Test platform name normalization."""
        # Test exact matches
        assert bet_converter._normalize_platform_name("stake") == "stake"
        assert bet_converter._normalize_platform_name("Stake") == "stake"
        assert bet_converter._normalize_platform_name("STAKE") == "stake"
        
        # Test variations
        assert bet_converter._normalize_platform_name("sporty") == "sportybet"
        assert bet_converter._normalize_platform_name("Sporty Bet") == "sportybet"
        assert bet_converter._normalize_platform_name("1x") == "1xbet"
        assert bet_converter._normalize_platform_name("1X Bet") == "1xbet"
        
        # Test unsupported platforms
        assert bet_converter._normalize_platform_name("unknown") is None
        assert bet_converter._normalize_platform_name("") is None
        assert bet_converter._normalize_platform_name(None) is None
    
    def test_make_conversion_request_success(self, bet_converter):
        """Test successful conversion request."""
        payload = {
            'code': 'ABC123',
            'from_platform': 'stake',
            'to_platform': 'sportybet'
        }
        
        result = bet_converter._make_conversion_request(payload)
        
        assert result['success'] is True
        assert 'converted_code' in result
        assert result['converted_code'].startswith('CONV')
        assert result['original_code'] == 'ABC123'
    
    def test_make_conversion_request_invalid_params(self, bet_converter):
        """Test conversion request with invalid parameters."""
        payload = {
            'code': '',
            'from_platform': 'stake',
            'to_platform': 'sportybet'
        }
        
        result = bet_converter._make_conversion_request(payload)
        
        assert result['success'] is False
        assert 'error' in result
    
    @pytest.mark.asyncio
    async def test_convert_code_success(self, bet_converter):
        """Test successful code conversion."""
        with patch.object(bet_converter, '_make_conversion_request') as mock_request:
            mock_request.return_value = {
                'success': True,
                'converted_code': 'CONV123456',
                'message': 'Code converted successfully'
            }
            
            result = await bet_converter.convert_code('ABC123', 'Stake', 'SportyBet')
            
            assert result['success'] is True
            assert result['code'] == 'CONV123456'
            assert 'message' in result
            mock_request.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_convert_code_failure(self, bet_converter):
        """Test failed code conversion."""
        with patch.object(bet_converter, '_make_conversion_request') as mock_request:
            mock_request.return_value = {
                'success': False,
                'error': 'Code not found'
            }
            
            result = await bet_converter.convert_code('INVALID', 'Stake', 'SportyBet')
            
            assert result['success'] is False
            assert result['code'] is None
            assert 'Code not found' in result['message']
            mock_request.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_convert_code_unsupported_platform(self, bet_converter):
        """Test conversion with unsupported platform."""
        result = await bet_converter.convert_code('ABC123', 'UnsupportedPlatform', 'SportyBet')
        
        assert result['success'] is False
        assert result['code'] is None
        assert 'Unsupported platform' in result['message']
    
    @pytest.mark.asyncio
    async def test_convert_code_exception_handling(self, bet_converter):
        """Test exception handling in code conversion."""
        with patch.object(bet_converter, '_make_conversion_request', side_effect=Exception("Test error")):
            result = await bet_converter.convert_code('ABC123', 'Stake', 'SportyBet')
            
            assert result['success'] is False
            assert result['code'] is None
            assert 'Error converting code' in result['message']
    
    @pytest.mark.asyncio
    async def test_get_supported_platforms(self, bet_converter):
        """Test getting supported platforms."""
        platforms = await bet_converter.get_supported_platforms()
        
        assert isinstance(platforms, list)
        assert len(platforms) > 0
        assert 'stake' in platforms
        assert 'sportybet' in platforms
        assert 'bet9ja' in platforms
    
    @pytest.mark.asyncio
    async def test_validate_code_format(self, bet_converter):
        """Test code format validation."""
        # Valid codes
        assert await bet_converter.validate_code_format('ABC123', 'stake') is True
        assert await bet_converter.validate_code_format('12345678', 'sportybet') is True
        assert await bet_converter.validate_code_format('XYZ789ABC', 'bet9ja') is True
        
        # Invalid codes
        assert await bet_converter.validate_code_format('', 'stake') is False
        assert await bet_converter.validate_code_format('AB', 'stake') is False  # Too short
        assert await bet_converter.validate_code_format('ABCDEFGHIJKLMNOP', 'stake') is False  # Too long
        assert await bet_converter.validate_code_format('ABC-123', 'stake') is False  # Invalid characters
        
        # Invalid platform
        assert await bet_converter.validate_code_format('ABC123', 'invalid') is False
        assert await bet_converter.validate_code_format('ABC123', '') is False


# Test data for different conversion scenarios
CONVERSION_TEST_CASES = [
    {
        'code': 'ABC123',
        'original_platform': 'Stake',
        'target_platform': 'SportyBet',
        'should_succeed': True
    },
    {
        'code': 'XYZ789',
        'original_platform': 'Bet9ja',
        'target_platform': '1xBet',
        'should_succeed': True
    },
    {
        'code': 'DEF456',
        'original_platform': 'Betway',
        'target_platform': 'NairaBet',
        'should_succeed': True
    },
    {
        'code': 'INVALID',
        'original_platform': 'UnsupportedPlatform',
        'target_platform': 'SportyBet',
        'should_succeed': False
    },
    {
        'code': 'ABC123',
        'original_platform': 'Stake',
        'target_platform': 'UnsupportedPlatform',
        'should_succeed': False
    }
]


@pytest.mark.parametrize("test_case", CONVERSION_TEST_CASES)
@pytest.mark.asyncio
async def test_conversion_scenarios(test_case):
    """Test various conversion scenarios."""
    bet_converter = BetConverter(api_key="test_api_key")
    
    result = await bet_converter.convert_code(
        test_case['code'],
        test_case['original_platform'],
        test_case['target_platform']
    )
    
    if test_case['should_succeed']:
        # For supported platforms, the mock should return success
        if (bet_converter._normalize_platform_name(test_case['original_platform']) and 
            bet_converter._normalize_platform_name(test_case['target_platform'])):
            assert result['success'] is True
            assert result['code'] is not None
        else:
            assert result['success'] is False
    else:
        assert result['success'] is False
        assert result['code'] is None


class TestBetConverterIntegration:
    """Integration tests for bet converter."""
    
    @pytest.mark.asyncio
    async def test_multiple_conversions(self):
        """Test converting multiple codes."""
        bet_converter = BetConverter(api_key="test_api_key")
        
        conversions = [
            ('ABC123', 'Stake', 'SportyBet'),
            ('XYZ789', 'Bet9ja', '1xBet'),
            ('DEF456', 'Betway', 'NairaBet')
        ]
        
        results = []
        for code, orig_platform, target_platform in conversions:
            result = await bet_converter.convert_code(code, orig_platform, target_platform)
            results.append(result)
        
        # All should succeed with valid platforms
        successful_results = [r for r in results if r['success']]
        assert len(successful_results) == len(conversions)
    
    @pytest.mark.asyncio
    async def test_platform_case_insensitivity(self):
        """Test that platform names are case insensitive."""
        bet_converter = BetConverter(api_key="test_api_key")
        
        # Test different case variations
        variations = [
            ('ABC123', 'stake', 'sportybet'),
            ('ABC123', 'STAKE', 'SPORTYBET'),
            ('ABC123', 'Stake', 'SportyBet'),
            ('ABC123', 'StAkE', 'SpOrTyBeT')
        ]
        
        results = []
        for code, orig_platform, target_platform in variations:
            result = await bet_converter.convert_code(code, orig_platform, target_platform)
            results.append(result)
        
        # All should succeed regardless of case
        successful_results = [r for r in results if r['success']]
        assert len(successful_results) == len(variations)


if __name__ == "__main__":
    pytest.main([__file__])