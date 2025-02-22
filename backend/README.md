# Museum Chatbot Backend

This is the backend for the Museum Chatbot Ticketing System built using FastAPI and MongoDB. It provides:
- Real-time ticket availability
- Information about exhibitions and events
- Secure payment processing using Razorpay
- Interaction with Open LLM models for chatbot functionalities

---

## Tech Stack
- FastAPI (for building APIs)
- MongoDB (as the database)
- Razorpay (for payment processing)
- Open LLM Models (for chatbot functionalities)

---

## Prerequisites
- Python 3.8 or later
- MongoDB server running locally or on the cloud

---

## Installation and Setup
1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd backend
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/Scripts/activate  # On Mac: venv\bin\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the FastAPI server:
    ```bash
    uvicorn main:app --reload
    ```
    The API documentation will be available at `http://localhost:8000/docs`

---

## Project Structure

backend/
├── main.py                 # Entry point for FastAPI
├── models/                 # Database models
├── routes/                 # API routes
│   ├── chatbot.py          # Chatbot interaction endpoints
│   ├── tickets.py          # Ticket booking endpoints
│   └── payments.py         # Payment processing endpoints
├── services/               # Business logic and helper functions
├── utils/                  # Utility functions (e.g., database connection)
└── requirements.txt        # Dependencies list

---

## Environment Variables
Create a `.env` file in the root directory with the following:

MONGO_URI=mongodb://localhost:27017/museum-db 
Razorpay_SECRET_KEY=your_Razorpay_secret_key 
OPEN_LLM_MODAL_API_KEY=your_LLM_api_key


---

## API Endpoints
- `/api/tickets`: Check ticket availability and book tickets
- `/api/chatbot`: Interact with the chatbot for event and exhibition information
- `/api/payments`: Handle payment processing securely

---

## Features
- Real-time ticket availability
- Detailed information about exhibitions and events
- Secure payment processing using Razorpay
- Intelligent chatbot interactions using Open LLM models

---

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for suggestions.

---

## License
This project is licensed under the MIT License.


