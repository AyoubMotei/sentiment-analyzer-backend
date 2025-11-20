# Sentiment Analyzer Backend

## Description

A FastAPI-based backend service for sentiment analysis using Hugging Face models. This API provides authentication and prediction endpoints to analyze the sentiment of text inputs, returning scores and sentiment labels (positive, neutral, negative).

## Features

- **Sentiment Analysis**: Utilizes the `nlptown/bert-base-multilingual-uncased-sentiment` model from Hugging Face for multilingual sentiment classification.
- **Authentication**: JWT-based authentication with simple user database.
- **CORS Support**: Configured for integration with frontend applications (e.g., Next.js on localhost:3000).
- **Error Handling**: Robust error handling for API key issues, model loading, and invalid requests.
- **Testing**: Includes unit and integration tests for API endpoints and sentiment analysis logic.

## Prerequisites

- Python 3.8 or higher
- Hugging Face API key (obtain from [Hugging Face](https://huggingface.co/settings/tokens))

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd sentiment-analyzer-backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add the required environment variables (see Environment Variables section).

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
HF_API_KEY=your_hugging_face_api_key_here
JWT_SECRET=your_jwt_secret_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

- `HF_API_KEY`: Your Hugging Face API token for accessing the inference API.
- `JWT_SECRET`: A secret key for signing JWT tokens.
- `ALGORITHM`: The algorithm used for JWT (default: HS256).
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time in minutes (default: 30).

## Usage

1. Activate the virtual environment (if not already activated).

2. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

3. The API will be available at `http://127.0.0.1:8000`.

4. Access the interactive API documentation at `http://127.0.0.1:8000/docs` (Swagger UI).

## API Endpoints

### GET /
Returns a welcome message.

**Response:**
```json
{
  "message": "Sentiment Analysis API"
}
```

### POST /login
Authenticates a user and returns a JWT token.

**Request Body:**
```json
{
  "username": "user",
  "password": "password"
}
```

**Response:**
```json
{
  "access_token": "jwt_token_here",
  "username": "user"
}
```

### POST /predict
Analyzes the sentiment of the provided text. Requires a valid JWT token in the Authorization header.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request Body:**
```json
{
  "text": "I love this product!"
}
```

**Response:**
```json
{
  "text": "I love this product!",
  "score": 5,
  "sentiment": "positif",
  "user": "username"
}
```

### GET /test-env
Tests if environment variables are configured correctly.

**Response:**
```json
{
  "hf_key_configured": true,
  "jwt_secret_configured": true,
  "hf_key_preview": "hf_xxxxxx..."
}
```

## Testing

Run the tests using pytest:

```bash
pytest app/test_api.py
```

The tests include:
- Integration tests for login and prediction endpoints.
- Unit tests for the sentiment analysis function.
- Authentication checks for protected endpoints.

## Project Structure

```
sentiment-analyzer-backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # Main FastAPI application
│   ├── auth.py          # Authentication logic
│   ├── test_api.py      # Tests
│   └── services/
│       └── ai_service.py # Sentiment analysis service
├── requirements.txt     # Python dependencies
├── .gitignore           # Git ignore rules
├── .env                 # Environment variables (not committed)
└── README.md            # This file
```

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make your changes and add tests.
4. Run tests to ensure everything works.
5. Submit a pull request.

## License

This project is licensed under the MIT License.
