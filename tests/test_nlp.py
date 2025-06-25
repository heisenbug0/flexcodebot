"""
Tests for NLP processor functionality.

This module contains unit tests for the NLP processor service,
testing betting code and platform extraction capabilities.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from typing import List, Dict, Any

from src.services.nlp_processor import NLPProcessor


class TestNLPProcessor:
    """Test cases for NLP processor."""
    
    @pytest.fixture
    def nlp_processor(self):
        """Create NLP processor instance for testing."""
        return NLPProcessor(hugging_face_api_key="test_key")
    
    def test_preprocess_text(self, nlp_processor):
        """Test text preprocessing functionality."""
        # Test mention removal
        text = "@FlexCodeBot Convert Stake code ABC123 to SportyBet"
        cleaned = nlp_processor._preprocess_text(text)
        assert "@FlexCodeBot" not in cleaned
        assert "Convert Stake code ABC123 to SportyBet" in cleaned
        
        # Test hashtag removal
        text = "Convert #Stake code ABC123 to #SportyBet"
        cleaned = nlp_processor._preprocess_text(text)
        assert "#Stake" not in cleaned
        assert "#SportyBet" not in cleaned
        
        # Test whitespace normalization
        text = "Convert    Stake   code   ABC123   to   SportyBet"
        cleaned = nlp_processor._preprocess_text(text)
        assert "  " not in cleaned
    
    def test_extract_codes(self, nlp_processor):
        """Test betting code extraction."""
        # Test alphanumeric codes
        text = "Convert Stake code ABC123 to SportyBet"
        codes = nlp_processor._extract_codes(text)
        assert "ABC123" in codes
        
        # Test numeric codes
        text = "Convert code 12345678 from Bet9ja to 1xBet"
        codes = nlp_processor._extract_codes(text)
        assert "12345678" in codes
        
        # Test multiple codes
        text = "Convert ABC123 and XYZ789 from Stake to SportyBet"
        codes = nlp_processor._extract_codes(text)
        assert "ABC123" in codes
        assert "XYZ789" in codes
        
        # Test no codes
        text = "Hello world"
        codes = nlp_processor._extract_codes(text)
        assert len(codes) == 0
    
    @pytest.mark.asyncio
    async def test_extract_platforms(self, nlp_processor):
        """Test platform extraction."""
        # Test known platforms
        text = "Convert Stake code ABC123 to SportyBet"
        platforms = await nlp_processor._extract_platforms(text)
        assert "Stake" in platforms
        assert "Sportybet" in platforms
        
        # Test platform variations
        text = "Convert from Sporty Bet to 1x Bet"
        platforms = await nlp_processor._extract_platforms(text)
        assert any("sporty" in p.lower() for p in platforms)
        assert any("1x" in p.lower() for p in platforms)
    
    @patch('requests.post')
    @pytest.mark.asyncio
    async def test_nlp_extract_entities(self, mock_post, nlp_processor):
        """Test NLP entity extraction with mocked API."""
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                'entity_group': 'ORG',
                'word': 'Stake',
                'start': 0,
                'end': 5
            },
            {
                'entity_group': 'ORG',
                'word': 'SportyBet',
                'start': 10,
                'end': 19
            }
        ]
        mock_post.return_value = mock_response
        
        text = "Stake to SportyBet"
        platforms = await nlp_processor._nlp_extract_entities(text)
        
        assert "Stake" in platforms
        assert "Sportybet" in platforms
        mock_post.assert_called_once()
    
    @patch('requests.post')
    @pytest.mark.asyncio
    async def test_nlp_extract_entities_api_failure(self, mock_post, nlp_processor):
        """Test NLP entity extraction with API failure."""
        # Mock API failure
        mock_response = Mock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        
        text = "Stake to SportyBet"
        platforms = await nlp_processor._nlp_extract_entities(text)
        
        assert platforms == []
        mock_post.assert_called_once()
    
    def test_parse_conversion_instructions(self, nlp_processor):
        """Test conversion instruction parsing."""
        # Test explicit conversion pattern
        text = "convert Stake code ABC123 to SportyBet"
        codes = ["ABC123"]
        platforms = ["Stake", "SportyBet"]
        
        pairs = nlp_processor._parse_conversion_instructions(text, codes, platforms)
        
        assert len(pairs) == 1
        assert pairs[0]['code'] == "ABC123"
        assert pairs[0]['original_platform'] == "Stake"
        assert pairs[0]['target_platform'] == "SportyBet"
        
        # Test multiple conversions
        text = "convert Stake code ABC123 to SportyBet and Bet9ja code XYZ789 to 1xBet"
        codes = ["ABC123", "XYZ789"]
        platforms = ["Stake", "SportyBet", "Bet9ja", "1xBet"]
        
        pairs = nlp_processor._parse_conversion_instructions(text, codes, platforms)
        
        assert len(pairs) >= 1
        assert any(p['code'] == "ABC123" for p in pairs)
    
    @pytest.mark.asyncio
    async def test_extract_betting_info_complete(self, nlp_processor):
        """Test complete betting info extraction."""
        with patch.object(nlp_processor, '_nlp_extract_entities', return_value=[]):
            text = "@FlexCodeBot Convert Stake code ABC123 to SportyBet and Bet9ja code XYZ789 to 1xBet"
            
            result = await nlp_processor.extract_betting_info(text)
            
            assert len(result) >= 1
            assert any(item['code'] == "ABC123" for item in result)
    
    @pytest.mark.asyncio
    async def test_extract_betting_info_missing_platforms(self, nlp_processor):
        """Test extraction with missing platform information."""
        with patch.object(nlp_processor, '_nlp_extract_entities', return_value=[]):
            text = "Convert ABC123 to SportyBet"  # Missing original platform
            
            result = await nlp_processor.extract_betting_info(text)
            
            assert len(result) >= 1
            assert any(item['code'] == "ABC123" for item in result)
            # Should have missing platform info
            assert any(item.get('original_platform') is None for item in result)
    
    @pytest.mark.asyncio
    async def test_extract_betting_info_no_codes(self, nlp_processor):
        """Test extraction with no betting codes."""
        text = "Hello, how are you?"
        
        result = await nlp_processor.extract_betting_info(text)
        
        assert len(result) == 0
    
    @pytest.mark.asyncio
    async def test_extract_betting_info_error_handling(self, nlp_processor):
        """Test error handling in betting info extraction."""
        with patch.object(nlp_processor, '_extract_codes', side_effect=Exception("Test error")):
            text = "Convert Stake code ABC123 to SportyBet"
            
            result = await nlp_processor.extract_betting_info(text)
            
            assert result == []


# Sample test data for integration testing
SAMPLE_INPUTS = [
    {
        'text': "@FlexCodeBot Convert Stake code ABC123 to SportyBet",
        'expected_codes': ["ABC123"],
        'expected_platforms': ["Stake", "SportyBet"]
    },
    {
        'text': "@FlexCodeBot Convert Stake code ABC123 to SportyBet and Bet9ja code XYZ789 to 1xBet",
        'expected_codes': ["ABC123", "XYZ789"],
        'expected_platforms': ["Stake", "SportyBet", "Bet9ja", "1xBet"]
    },
    {
        'text': "Convert ABC123 to SportyBet",  # Missing original platform
        'expected_codes': ["ABC123"],
        'expected_platforms': ["SportyBet"]
    },
    {
        'text': "@FlexCodeBot Convert INVALID to SportyBet",  # Invalid code format
        'expected_codes': [],
        'expected_platforms': ["SportyBet"]
    }
]


@pytest.mark.parametrize("sample", SAMPLE_INPUTS)
@pytest.mark.asyncio
async def test_sample_inputs(sample):
    """Test NLP processor with sample inputs."""
    nlp_processor = NLPProcessor(hugging_face_api_key="test_key")
    
    with patch.object(nlp_processor, '_nlp_extract_entities', return_value=[]):
        result = await nlp_processor.extract_betting_info(sample['text'])
        
        # Extract codes from result
        extracted_codes = [item['code'] for item in result]
        
        # Check if expected codes are found (allowing for some flexibility)
        for expected_code in sample['expected_codes']:
            if expected_code != "INVALID":  # Skip invalid codes
                assert any(expected_code in code for code in extracted_codes), \
                    f"Expected code {expected_code} not found in {extracted_codes}"


if __name__ == "__main__":
    pytest.main([__file__])