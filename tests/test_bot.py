"""
Test script for FlexCode Twitter Bot.

This script allows you to test the bot functionality without needing
actual Twitter API credentials or real Twitter interactions.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from dotenv import load_dotenv

from src.services.x_handler import XHandler
from src.services.nlp_processor import NLPProcessor
from src.services.bet_converter import BetConverter
from src.bot.twitter_bot import FlexCodeTwitterBot

# Load environment variables
load_dotenv()


async def test_bot_processing():
    """
    Test the bot's message processing capabilities.
    """
    print("🤖 Testing FlexCode Bot Processing...")
    
    # Initialize services (with test credentials)
    x_handler = XHandler(
        api_key=os.getenv("X_API_KEY", "test_key"),
        api_secret=os.getenv("X_API_SECRET", "test_secret"),
        access_token=os.getenv("X_ACCESS_TOKEN", "test_token"),
        access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET", "test_token_secret")
    )
    
    nlp_processor = NLPProcessor(
        hugging_face_api_key=os.getenv("HUGGING_FACE_API_KEY", "test_hf_key")
    )
    
    bet_converter = BetConverter(
        api_key=os.getenv("CONVERT_BET_API_KEY", "test_convert_key")
    )
    
    # Create bot instance
    bot = FlexCodeTwitterBot(x_handler, nlp_processor, bet_converter)
    
    # Test cases
    test_cases = [
        {
            "name": "Single Code Conversion",
            "tweet_id": "test_tweet_1",
            "user_handle": "testuser1",
            "message": "@FlexCodeBot Convert Stake code ABC123 to SportyBet"
        },
        {
            "name": "Multiple Code Conversion",
            "tweet_id": "test_tweet_2",
            "user_handle": "testuser2",
            "message": "@FlexCodeBot Convert Stake code ABC123 to SportyBet and Bet9ja code XYZ789 to 1xBet"
        },
        {
            "name": "Missing Original Platform",
            "tweet_id": "test_tweet_3",
            "user_handle": "testuser3",
            "message": "@FlexCodeBot Convert ABC123 to SportyBet"
        },
        {
            "name": "No Codes Found",
            "tweet_id": "test_tweet_4",
            "user_handle": "testuser4",
            "message": "@FlexCodeBot Hello, how are you?"
        }
    ]
    
    print("\n" + "="*60)
    print("TESTING BOT MESSAGE PROCESSING")
    print("="*60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {test_case['name']}")
        print(f"📝 Message: {test_case['message']}")
        print("-" * 40)
        
        try:
            # Process the test mention
            await bot.process_manual_mention(
                test_case['tweet_id'],
                test_case['user_handle'],
                test_case['message']
            )
            print("✅ Test completed successfully")
            
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
        
        print("-" * 40)
    
    print("\n🎉 All tests completed!")


async def test_nlp_extraction():
    """
    Test NLP extraction capabilities.
    """
    print("\n" + "="*60)
    print("TESTING NLP EXTRACTION")
    print("="*60)
    
    nlp_processor = NLPProcessor(
        hugging_face_api_key=os.getenv("HUGGING_FACE_API_KEY", "test_hf_key")
    )
    
    test_messages = [
        "@FlexCodeBot Convert Stake code ABC123 to SportyBet",
        "@FlexCodeBot Convert Stake code ABC123 to SportyBet and Bet9ja code XYZ789 to 1xBet",
        "Convert ABC123 to SportyBet",
        "Hello world"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n🧪 NLP Test {i}")
        print(f"📝 Message: {message}")
        
        try:
            result = await nlp_processor.extract_betting_info(message)
            print(f"🔍 Extracted: {result}")
            
        except Exception as e:
            print(f"❌ NLP extraction failed: {str(e)}")


async def test_bet_conversion():
    """
    Test bet code conversion.
    """
    print("\n" + "="*60)
    print("TESTING BET CODE CONVERSION")
    print("="*60)
    
    bet_converter = BetConverter(
        api_key=os.getenv("CONVERT_BET_API_KEY", "test_convert_key")
    )
    
    test_conversions = [
        ("ABC123", "Stake", "SportyBet"),
        ("XYZ789", "Bet9ja", "1xBet"),
        ("INVALID", "UnsupportedPlatform", "SportyBet")
    ]
    
    for i, (code, orig_platform, target_platform) in enumerate(test_conversions, 1):
        print(f"\n🧪 Conversion Test {i}")
        print(f"🔄 Converting: {orig_platform} {code} → {target_platform}")
        
        try:
            result = await bet_converter.convert_code(code, orig_platform, target_platform)
            print(f"✅ Result: {result}")
            
        except Exception as e:
            print(f"❌ Conversion failed: {str(e)}")


def print_setup_instructions():
    """
    Print setup instructions for testing.
    """
    print("🚀 FlexCode Bot Test Suite")
    print("="*60)
    print("\n📋 SETUP INSTRUCTIONS:")
    print("1. Copy .env.example to .env")
    print("2. Add your API keys to .env file:")
    print("   - X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET")
    print("   - HUGGING_FACE_API_KEY")
    print("   - CONVERT_BET_API_KEY")
    print("3. Run: python tests/test_bot.py")
    print("\n💡 NOTE: Tests will run with mock data if API keys are not provided")
    print("="*60)


async def main():
    """
    Main test function.
    """
    print_setup_instructions()
    
    # Run all tests
    await test_nlp_extraction()
    await test_bet_conversion()
    await test_bot_processing()
    
    print("\n🎯 TESTING COMPLETE!")
    print("\n📚 Next Steps:")
    print("1. Set up your Twitter API credentials")
    print("2. Deploy to Render.com")
    print("3. Start the bot: POST /bot/start")
    print("4. Test with real Twitter mentions!")


if __name__ == "__main__":
    asyncio.run(main())