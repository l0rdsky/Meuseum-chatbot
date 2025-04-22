# Museum Ticket Booking Chatbot

A intelligent chatbot system powered by Google Gemini AI for booking museum tickets and answering visitor queries.

## Features

- Interactive chat interface for ticket bookings
- Answers general questions about the museum
- Handles complete booking flow from personal details to payment
- Generates PDF tickets for confirmed bookings
- Remembers conversation context for natural interactions

## Setup

1. Make sure you have Python 3.8+ installed
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
   
   Or use the setup script:
   ```
   python setup.py
   ```

3. Set up your environment variables in a `.env` file:
   ```
   MONGODB_URI="your_mongodb_connection_string"
   MUSEUM_NAME="National Museum of India"
   GEMINI_API_KEY="your_gemini_api_key"
   ```

4. Make sure to get a valid Google Gemini API key from:
   https://ai.google.dev/

## Running the Application

1. Start the backend server:
   ```
   python app.py
   ```

2. The server will run on http://localhost:5000
3. The frontend should be configured to connect to this address

## API Endpoints

- `/chat` - POST - Send and receive chat messages
- `/generate-ticket` - POST - Generate a PDF ticket
- `/tickets/<ticket_id>.pdf` - GET - Retrieve a generated ticket 