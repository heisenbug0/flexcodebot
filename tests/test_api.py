"""
Tests for FastAPI endpoints.

This module contains unit tests for the FastAPI application endpoints,
testing request/response handling and integration between services.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

from src.api.main import app
from src.models.entities import ProcessMentionRequest, ProcessDMRequest


class TestHealthEndpoint:
    """Test cases for health check endpoint."""
    
    def test_health_check(self):
        """Test health check endpoint."""
        client = TestClient(app)
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["message"] == "FlexCode Bot is running"
        assert "timestamp" in data


class TestProcessMentionEndpoint:
    """Test cases for process mention endpoint."""
    
    @patch('src.api.main.get_x_handler')
    @patch('src.api.main.get_nlp_processor')
    @patch('src.api.main.get_bet_converter')
    def test_process_mention_success(self, mock_bet_converter, mock_nlp_processor, mock_x_handler):
        """Test successful mention processing."""
        # Mock services
        mock_nlp = Mock()
        mock_nlp.extract_betting_info = AsyncMock(return_value=[
            {
                'code': 'ABC123',
                'original_platform': 'Stake',
                'target_platform': 'SportyBet'
            }
        ])
        mock_nlp_processor.return_value = mock_nlp
        
        mock_converter = Mock()
        mock_converter.convert_code = AsyncMock(return_value={
            'success': True,
            'code': 'CONV123456',
            'message': 'Converted successfully'
        })
        mock_bet_converter.return_value = mock_converter
        
        mock_x = Mock()
        mock_x.reply_to_mention = AsyncMock(return_value={'status': 'sent'})
        mock_x_handler.return_value = mock_x
        
        # Test request
        client = TestClient(app)
        request_data = {
            "tweet_id": "123456789",
            "user_handle": "testuser",
            "user_id": "987654321",
            "message_text": "@FlexCodeBot Convert Stake code ABC123 to SportyBet"
        }
        
        response = client.post("/process_mention", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["converted_codes"]) == 1
        assert data["converted_codes"][0]["original_code"] == "ABC123"
        assert data["converted_codes"][0]["converted_code"] == "CONV123456"
    
    @patch('src.api.main.get_x_handler')
    @patch('src.api.main.get_nlp_processor')
    @patch('src.api.main.get_bet_converter')
    def test_process_mention_no_codes(self, mock_bet_converter, mock_nlp_processor, mock_x_handler):
        """Test mention processing with no codes found."""
        # Mock services
        mock_nlp = Mock()
        mock_nlp.extract_betting_info = AsyncMock(return_value=[])
        mock_nlp_processor.return_value = mock_nlp
        
        mock_x = Mock()
        mock_x.reply_to_mention = AsyncMock(return_value={'status': 'sent'})
        mock_x_handler.return_value = mock_x
        
        # Test request
        client = TestClient(app)
        request_data = {
            "tweet_id": "123456789",
            "user_handle": "testuser",
            "user_id": "987654321",
            "message_text": "@FlexCodeBot Hello there"
        }
        
        response = client.post("/process_mention", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "No betting codes" in data["message"]
    
    @patch('src.api.main.get_x_handler')
    @patch('src.api.main.get_nlp_processor')
    @patch('src.api.main.get_bet_converter')
    def test_process_mention_missing_platforms(self, mock_bet_converter, mock_nlp_processor, mock_x_handler):
        """Test mention processing with missing platform information."""
        # Mock services
        mock_nlp = Mock()
        mock_nlp.extract_betting_info = AsyncMock(return_value=[
            {
                'code': 'ABC123',
                'original_platform': None,
                'target_platform': 'SportyBet'
            }
        ])
        mock_nlp_processor.return_value = mock_nlp
        
        mock_x = Mock()
        mock_x.reply_to_mention = AsyncMock(return_value={'status': 'sent'})
        mock_x_handler.return_value = mock_x
        
        # Test request
        client = TestClient(app)
        request_data = {
            "tweet_id": "123456789",
            "user_handle": "testuser",
            "user_id": "987654321",
            "message_text": "@FlexCodeBot Convert ABC123 to SportyBet"
        }
        
        response = client.post("/process_mention", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "specify the original and target platforms" in data["message"]


class TestProcessDMEndpoint:
    """Test cases for process DM endpoint."""
    
    @patch('src.api.main.get_x_handler')
    @patch('src.api.main.get_nlp_processor')
    @patch('src.api.main.get_bet_converter')
    def test_process_dm_success(self, mock_bet_converter, mock_nlp_processor, mock_x_handler):
        """Test successful DM processing."""
        # Mock services
        mock_nlp = Mock()
        mock_nlp.extract_betting_info = AsyncMock(return_value=[
            {
                'code': 'XYZ789',
                'original_platform': 'Bet9ja',
                'target_platform': '1xBet'
            }
        ])
        mock_nlp_processor.return_value = mock_nlp
        
        mock_converter = Mock()
        mock_converter.convert_code = AsyncMock(return_value={
            'success': True,
            'code': 'CONV789123',
            'message': 'Converted successfully'
        })
        mock_bet_converter.return_value = mock_converter
        
        mock_x = Mock()
        mock_x.send_dm = AsyncMock(return_value={'status': 'sent'})
        mock_x_handler.return_value = mock_x
        
        # Test request
        client = TestClient(app)
        request_data = {
            "message_id": "dm123456789",
            "user_handle": "testuser",
            "user_id": "987654321",
            "message_text": "Convert Bet9ja code XYZ789 to 1xBet"
        }
        
        response = client.post("/process_dm", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["converted_codes"]) == 1
        assert data["converted_codes"][0]["original_code"] == "XYZ789"
        assert data["converted_codes"][0]["converted_code"] == "CONV789123"
    
    def test_process_dm_invalid_request(self):
        """Test DM processing with invalid request data."""
        client = TestClient(app)
        
        # Missing required fields
        request_data = {
            "user_handle": "testuser",
            "message_text": "Convert ABC123 to SportyBet"
            # Missing message_id and user_id
        }
        
        response = client.post("/process_dm", json=request_data)
        
        assert response.status_code == 422  # Validation error


class TestRequestValidation:
    """Test cases for request validation."""
    
    def test_mention_request_validation(self):
        """Test mention request validation."""
        client = TestClient(app)
        
        # Valid request
        valid_request = {
            "tweet_id": "123456789",
            "user_handle": "testuser",
            "user_id": "987654321",
            "message_text": "Convert ABC123 to SportyBet"
        }
        
        # This should not raise validation error (though it may fail in processing)
        response = client.post("/process_mention", json=valid_request)
        assert response.status_code != 422
        
        # Invalid request - missing required fields
        invalid_request = {
            "user_handle": "testuser",
            "message_text": "Convert ABC123 to SportyBet"
            # Missing tweet_id and user_id
        }
        
        response = client.post("/process_mention", json=invalid_request)
        assert response.status_code == 422
    
    def test_dm_request_validation(self):
        """Test DM request validation."""
        client = TestClient(app)
        
        # Valid request
        valid_request = {
            "message_id": "dm123456789",
            "user_handle": "testuser",
            "user_id": "987654321",
            "message_text": "Convert ABC123 to SportyBet"
        }
        
        # This should not raise validation error (though it may fail in processing)
        response = client.post("/process_dm", json=valid_request)
        assert response.status_code != 422
        
        # Invalid request - empty message text
        invalid_request = {
            "message_id": "dm123456789",
            "user_handle": "testuser",
            "user_id": "987654321",
            "message_text": ""
        }
        
        response = client.post("/process_dm", json=invalid_request)
        # Should still be valid as empty string is allowed, but processing will handle it
        assert response.status_code != 422


class TestErrorHandling:
    """Test cases for error handling."""
    
    @patch('src.api.main.get_nlp_processor')
    def test_nlp_service_error(self, mock_nlp_processor):
        """Test handling of NLP service errors."""
        # Mock NLP service to raise exception
        mock_nlp = Mock()
        mock_nlp.extract_betting_info = AsyncMock(side_effect=Exception("NLP service error"))
        mock_nlp_processor.return_value = mock_nlp
        
        client = TestClient(app)
        request_data = {
            "tweet_id": "123456789",
            "user_handle": "testuser",
            "user_id": "987654321",
            "message_text": "Convert ABC123 to SportyBet"
        }
        
        response = client.post("/process_mention", json=request_data)
        
        assert response.status_code == 500
    
    @patch('src.api.main.get_x_handler')
    @patch('src.api.main.get_nlp_processor')
    @patch('src.api.main.get_bet_converter')
    def test_conversion_service_error(self, mock_bet_converter, mock_nlp_processor, mock_x_handler):
        """Test handling of conversion service errors."""
        # Mock services
        mock_nlp = Mock()
        mock_nlp.extract_betting_info = AsyncMock(return_value=[
            {
                'code': 'ABC123',
                'original_platform': 'Stake',
                'target_platform': 'SportyBet'
            }
        ])
        mock_nlp_processor.return_value = mock_nlp
        
        mock_converter = Mock()
        mock_converter.convert_code = AsyncMock(side_effect=Exception("Conversion service error"))
        mock_bet_converter.return_value = mock_converter
        
        mock_x = Mock()
        mock_x.reply_to_mention = AsyncMock(return_value={'status': 'sent'})
        mock_x_handler.return_value = mock_x
        
        client = TestClient(app)
        request_data = {
            "tweet_id": "123456789",
            "user_handle": "testuser",
            "user_id": "987654321",
            "message_text": "Convert Stake code ABC123 to SportyBet"
        }
        
        response = client.post("/process_mention", json=request_data)
        
        # Should handle the error gracefully and still return a response
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True  # Overall success, but individual conversion failed
        assert len(data["converted_codes"]) == 1
        assert data["converted_codes"][0]["converted_code"] is None
        assert "Failed to convert" in data["converted_codes"][0]["message"]


if __name__ == "__main__":
    pytest.main([__file__])