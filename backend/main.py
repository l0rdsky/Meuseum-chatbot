from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import DatabaseHandler
from chatbot import chatbot_service
from ticket_generator import generate_ticket_pdf
from fastapi.responses import FileResponse
import os
from dotenv import load_dotenv
import logging

load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

logger = logging.getLogger(__name__)
db = DatabaseHandler()

@app.get("/museum-info")
async def get_museum_info():
    try:
        museum_info = db.get_museum_info()
        if not museum_info:
            raise HTTPException(status_code=404, detail="Museum information not found")
        return museum_info
    except Exception as e:
        logger.error(f"Error fetching museum info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(request: dict):
    try:
        if 'message' not in request:
            raise HTTPException(status_code=400, detail="No message provided")
            
        user_message = request['message']
        current_state = request.get('currentState', 'greeting')
        
        response = chatbot_service.get_response(user_message, current_state)
        return response
        
    except Exception as e:
        logger.error(f"Server Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-ticket")
async def generate_ticket(ticket_data: dict):
    try:
        pdf_path = generate_ticket_pdf(ticket_data)
        return FileResponse(
            pdf_path,
            media_type='application/pdf',
            filename=f"museum-ticket-{ticket_data['booking_ref']}.pdf"
        )
    except Exception as e:
        logger.error(f"Error generating ticket: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000) 