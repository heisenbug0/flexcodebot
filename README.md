# FlexCode Bot

FlexCode is a betting code conversion bot that processes X (Twitter) mentions and direct messages to convert betting codes between different platforms like Stake, SportyBet, Bet9ja, and more. Built for the Bolt hackathon using FastAPI, Hugging Face NLP, and X API.

## Overview

FlexCode Bot (@FlexCodeBot) automatically:
- **Monitors X mentions and DMs** for betting code conversion requests in real-time
- **Extracts multiple betting codes** and platforms from a single message using NLP
- **Converts codes** between platforms using external APIs
- **Replies automatically** with converted codes or asks for clarification when needed

## Features

- **Real-time Twitter Monitoring**: Automatically monitors @FlexCodeBot mentions and DMs
- **Multi-code Processing**: Handle multiple betting codes in a single message
- **NLP-Powered**: Uses Hugging Face's BERT model for entity extraction
- **Platform Support**: Supports 10+ betting platforms including Stake, SportyBet, Bet9ja, 1xBet
- **Smart Parsing**: Understands various message formats and conversion instructions
- **Auto-Response**: Automatically replies to users on Twitter
- **Error Handling**: Graceful error handling with user-friendly messages

## Supported Platforms

- Stake
- SportyBet
- Bet9ja
- 1xBet
- Betway
- NairaBet
- MerryBet
- BetKing
- BetNaija
- SupaBet

## How It Works

1. **User mentions** @FlexCodeBot on Twitter with a conversion request
2. **Bot monitors** Twitter for mentions in real-time
3. **NLP extracts** betting codes and platforms from the message
4. **API converts** codes between platforms
5. **Bot replies** automatically with converted codes

## API Endpoints

- `GET /health` - Health check endpoint
- `GET /bot/status` - Get Twitter bot status
- `POST /bot/start` - Start Twitter bot monitoring
- `POST /bot/stop` - Stop Twitter bot monitoring
- `POST /test/mention` - Test mention processing (development)
- `POST /process_mention` - Process X mentions (webhook)
- `POST /process_dm` - Process X direct messages (webhook)

## Setup Instructions

### Prerequisites

- Python 3.10+
- X (Twitter) Developer Account with API v2 access
- Hugging Face API Key
- Convert Bet Codes API Key

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd flexcode
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your API keys:
   ```env
   # X (Twitter) API Credentials
   X_API_KEY=your_x_api_key_here
   X_API_SECRET=your_x_api_secret_here
   X_ACCESS_TOKEN=your_x_access_token_here
   X_ACCESS_TOKEN_SECRET=your_x_access_token_secret_here

   # Hugging Face API Key
   HUGGING_FACE_API_KEY=your_hugging_face_api_key_here

   # Convert Bet Codes API Key
   CONVERT_BET_API_KEY=your_convert_bet_api_key_here

   # Environment
   ENVIRONMENT=development
   ```

4. **Run the application**
   ```bash
   uvicorn src.api.main:app --reload
   ```

   The API will be available at `http://localhost:8000`

5. **Test the bot**
   ```bash
   python test_bot.py
   ```

### API Keys Setup

1. **X (Twitter) API**
   - Go to [developer.x.com](https://developer.x.com/)
   - Create a new app and get your API keys
   - Ensure you have read/write permissions for tweets and DMs
   - Enable API v2 access

2. **Hugging Face API**
   - Sign up at [huggingface.co](https://huggingface.co/)
   - Go to Settings > Access Tokens
   - Create a new token with read permissions

3. **Convert Bet Codes API**
   - Contact hi@convertbetcodes.com to request an API key
   - Follow their documentation for integration

## Testing the Bot

### 1. Local Testing (Without Twitter API)
```bash
python test_bot.py
```

This will test:
- NLP extraction capabilities
- Bet code conversion logic
- Message processing flow

### 2. API Testing
Visit `http://localhost:8000/docs` for interactive API documentation.

Test endpoints:
- `GET /health` - Check if bot is running
- `GET /bot/status` - Check Twitter monitoring status
- `POST /test/mention` - Test mention processing

### 3. Live Twitter Testing

Once deployed with real API keys:

1. **Start the bot monitoring**:
   ```bash
   curl -X POST http://your-app-url.com/bot/start
   ```

2. **Tweet at your bot**:
   ```
   @FlexCodeBot Convert Stake code ABC123 to SportyBet
   ```

3. **Check bot status**:
   ```bash
   curl http://your-app-url.com/bot/status
   ```

## Deployment on Render.com

1. **Connect your GitHub repository to Render**

2. **Create a new Web Service**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`

3. **Set Environment Variables**
   Add all the environment variables from your `.env` file in the Render dashboard

4. **Deploy**
   Render will automatically deploy your application

5. **Start the bot**
   After deployment, make a POST request to `/bot/start` to begin monitoring

## Usage Examples

### X Mentions

**Single Code Conversion:**
```
@FlexCodeBot Convert Stake code ABC123 to SportyBet
```

**Multiple Code Conversion:**
```
@FlexCodeBot Convert Stake code ABC123 to SportyBet and Bet9ja code XYZ789 to 1xBet
```

### Direct Messages

**Simple Conversion:**
```
Convert ABC123 from Stake to SportyBet
```

**Missing Platform (Bot will ask for clarification):**
```
Convert ABC123 to SportyBet
```

### Expected Responses

**Successful Conversion:**
```
@user Converted codes: Stake ABC123 to SportyBet: DEF456; Bet9ja XYZ789 to 1xBet: GHI789
```

**Clarification Request:**
```
@user Please specify the original and target platforms for code(s): ABC123
```

**Error Response:**
```
@user Sorry, I encountered an error processing your request. Please try again.
```

## Bot Monitoring

The bot automatically:
- ✅ Monitors Twitter mentions every 30 seconds
- ✅ Processes DMs every minute
- ✅ Tracks processed messages to avoid duplicates
- ✅ Handles rate limits gracefully
- ✅ Logs all activities for debugging

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run specific test files
pytest tests/test_nlp.py
pytest tests/test_converter.py
pytest tests/test_api.py

# Run with coverage
pytest --cov=src tests/

# Test bot functionality
python test_bot.py
```

### Sample Test Inputs

1. **Valid Multi-code Mention:**
   ```
   @FlexCodeBot Convert Stake code ABC123 to SportyBet and Bet9ja code XYZ789 to 1xBet
   ```

2. **Missing Original Platform:**
   ```
   Convert ABC123 to SportyBet
   ```

3. **Invalid Code:**
   ```
   @FlexCodeBot Convert INVALID to SportyBet
   ```

## Project Structure

```
flexcode/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app and endpoints
│   │   ├── dependencies.py      # Dependency injection
│   ├── bot/
│   │   ├── __init__.py
│   │   ├── twitter_bot.py       # Twitter bot monitoring and response
│   ├── services/
│   │   ├── __init__.py
│   │   ├── x_handler.py         # X API logic
│   │   ├── nlp_processor.py     # NLP processing
│   │   ├── bet_converter.py     # Bet code conversion
│   ├── models/
│   │   ├── __init__.py
│   │   ├── entities.py          # Pydantic models
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py            # Logging configuration
│   │   ├── helpers.py           # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_nlp.py              # NLP tests
│   ├── test_converter.py        # Converter tests
│   ├── test_api.py              # API tests
├── logs/
├── test_bot.py                  # Bot testing script
├── .env.example                 # Environment variables template
├── requirements.txt             # Dependencies
├── Procfile                     # Render.com deployment
├── runtime.txt                  # Python version
└── README.md                    # This file
```

## Architecture

The application follows a clean, modular architecture:

- **API Layer**: FastAPI endpoints for health checks and manual controls
- **Bot Layer**: Twitter monitoring and automatic response handling
- **Service Layer**: Business logic for X integration, NLP processing, and bet conversion
- **Model Layer**: Pydantic models for request/response validation
- **Utils Layer**: Logging, helpers, and utility functions

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **Tweepy**: X (Twitter) API client library
- **Hugging Face Transformers**: NLP model for entity extraction
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for running the application
- **Pytest**: Testing framework
- **Asyncio**: Asynchronous programming for real-time monitoring

## Troubleshooting

### Common Issues

1. **Bot not responding to mentions**
   - Check bot status: `GET /bot/status`
   - Verify Twitter API credentials
   - Check logs for rate limit issues

2. **NLP extraction not working**
   - Verify Hugging Face API key
   - Check message format
   - Review logs for API errors

3. **Code conversion failing**
   - Verify Convert Bet Codes API key
   - Check supported platforms
   - Review conversion logs

### Debugging

1. Check application logs in `logs/app.log`
2. Use the test script: `python test_bot.py`
3. Monitor bot status via `/bot/status` endpoint
4. Test individual components via API endpoints

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is built for the Bolt hackathon and follows all hackathon rules including the use of authorized third-party APIs.

## Support

For issues or questions:
1. Check the logs in `logs/app.log`
2. Run the test script: `python test_bot.py`
3. Review the troubleshooting section
4. Verify that all API keys are correctly configured
5. Ensure that all dependencies are installed

## Hackathon Compliance

This project complies with Bolt hackathon rules:
- ✅ New project created specifically for the hackathon
- ✅ Uses authorized third-party APIs (X API, Hugging Face, Convert Bet Codes)
- ✅ Clean, production-ready code with proper documentation
- ✅ Comprehensive testing suite
- ✅ Real-time Twitter bot functionality
- ✅ Deployment-ready configuration

## Quick Start Guide

1. **Setup**: Copy `.env.example` to `.env` and add your API keys
2. **Install**: `pip install -r requirements.txt`
3. **Test**: `python test_bot.py`
4. **Run**: `uvicorn src.api.main:app --reload`
5. **Deploy**: Push to Render.com and start the bot via `/bot/start`
6. **Use**: Tweet `@FlexCodeBot Convert Stake code ABC123 to SportyBet`

The bot will automatically monitor Twitter and respond to mentions! 🚀