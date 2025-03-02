from typing import Dict, Any
from datetime import datetime
import pymongo
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)
load_dotenv()

class DatabaseHandler:
    def __init__(self):
        self.client = pymongo.MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client['museum']
        self.bookings = self.db['bookings']
        self.museum_info = self.db['museum_info']

    def save_booking(self, booking_data: Dict[str, Any]) -> bool:
        try:
            booking_data['created_at'] = datetime.now().isoformat()
            result = self.bookings.insert_one(booking_data)
            booking_data['_id'] = str(result.inserted_id)
            return bool(result.inserted_id)
        except Exception as e:
            logger.error(f"Error saving booking: {e}")
            return False

    def get_booking(self, booking_ref: str) -> Dict[str, Any]:
        try:
            return self.bookings.find_one({'booking_ref': booking_ref})
        except Exception as e:
            logger.error(f"Error fetching booking: {e}")
            return None

    def get_museum_info(self) -> Dict[str, Any]:
        try:
            return self.museum_info.find_one({})
        except Exception as e:
            logger.error(f"Error fetching museum info: {e}")
            return None

    def save_ticket(self, ticket_data: dict) -> str:
        ticket_data['created_at'] = datetime.utcnow()
        result = self.db.tickets.insert_one(ticket_data)
        return str(result.inserted_id)
    
    def get_ticket(self, ticket_id: str) -> dict:
        return self.db.tickets.find_one({'_id': ticket_id})
    
    def save_transaction(self, transaction_data: dict) -> str:
        transaction_data['created_at'] = datetime.utcnow()
        result = self.db.transactions.insert_one(transaction_data)
        return str(result.inserted_id)
