import json
from typing import List, Dict, Any
import re
import os
import sys
from datetime import datetime
import logging
from database import DatabaseHandler
import google.generativeai as genai

logger = logging.getLogger(__name__)

# Initialize the Google AI client
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

# Set up the model
model = genai.GenerativeModel('gemini-1.5-flash')

# Prices for different ticket types
TICKET_PRICES = {
    'adult': 500,    # Rs. 500 per adult
    'student': 250,  # Rs. 250 per student
    'child': 0       # Free for children
}

# Date formatting utility functions
def parse_date(date_str):
    """Convert various date formats to DD/MM/YYYY format"""
    date_str = date_str.lower().strip()
    
    # Remove common prefixes
    prefixes = ['on ', 'on the ', 'the ', 'visit on ', 'planning to visit on ', 'come on ']
    for prefix in prefixes:
        if date_str.startswith(prefix):
            date_str = date_str[len(prefix):]
    
    # Handle dates like "22nd may", "22 may", "22-may"
    month_names = {
        'january': '01', 'jan': '01',
        'february': '02', 'feb': '02',
        'march': '03', 'mar': '03',
        'april': '04', 'apr': '04',
        'may': '05',
        'june': '06', 'jun': '06',
        'july': '07', 'jul': '07',
        'august': '08', 'aug': '08',
        'september': '09', 'sep': '09', 'sept': '09',
        'october': '10', 'oct': '10',
        'november': '11', 'nov': '11',
        'december': '12', 'dec': '12'
    }
    
    # Regular expressions for different date patterns
    patterns = [
        # 22nd may, 2nd june, etc.
        r'(\d+)(st|nd|rd|th)?\s+([a-z]+)',
        # may 22, june 2
        r'([a-z]+)\s+(\d+)(st|nd|rd|th)?',
        # 22-05, 22/05, 22.05
        r'(\d{1,2})[\-\.\/](\d{1,2})',
        # 22-05-2023, 22/05/2023
        r'(\d{1,2})[\-\.\/](\d{1,2})[\-\.\/](\d{2,4})'
    ]
    
    # Try each pattern to see if it matches
    for pattern in patterns:
        match = re.search(pattern, date_str)
        if match:
            groups = match.groups()
            
            # For patterns like "22nd may"
            if len(groups) == 3 and any(m == groups[2].lower() for m in month_names):
                day = groups[0].zfill(2)
                month = month_names.get(groups[2].lower(), '01')  # Default to January if not found
                year = str(datetime.now().year)
                return f"{day}/{month}/{year}"
                
            # For patterns like "may 22"
            elif len(groups) >= 2 and any(m == groups[0].lower() for m in month_names):
                day = groups[1].zfill(2)
                month = month_names.get(groups[0].lower(), '01')
                year = str(datetime.now().year)
                return f"{day}/{month}/{year}"
                
            # For DD/MM format
            elif len(groups) == 2 and groups[0].isdigit() and groups[1].isdigit():
                day = groups[0].zfill(2)
                month = groups[1].zfill(2)
                year = str(datetime.now().year)
                return f"{day}/{month}/{year}"
                
            # For DD/MM/YYYY format
            elif len(groups) == 3 and all(g.isdigit() for g in groups):
                day = groups[0].zfill(2)
                month = groups[1].zfill(2)
                year = groups[2]
                # Handle 2-digit years
                if len(year) == 2:
                    year = '20' + year
                return f"{day}/{month}/{year}"
    
    # If no pattern matched, return the original string with a note
    # This allows the flow to continue even if we couldn't parse the date
    return date_str

class ChatbotService:
    def __init__(self):
        self.conversation_state = {
            'current_step': 'greeting',
            'booking_info': {},
            'conversation_ended': False
        }
        self.prices = TICKET_PRICES
        self.db = DatabaseHandler()
        self.chat_history = []
        
        # Initialize the conversation with system prompt
        self.system_prompt = """
        You are a helpful museum ticket booking assistant for the National Museum of India.
        Your job is to help visitors book tickets, answer questions about the museum, and provide information.
        
        Museum Details:
        - Name: National Museum of India
        - Location: Janpath, New Delhi, India
        - Opening Hours: Tuesday to Sunday, 10:00 AM - 6:00 PM (Closed on Mondays and National Holidays)
        - Contact: Phone: +91-11-23019272, Email: info@nationalmuseum.in
        - The museum houses over 200,000 works of art spanning 5,000 years of cultural heritage
        - The museum has collections from prehistoric era, ancient India, medieval period, and modern art
        - Popular exhibits include the Dancing Girl from Mohenjo-daro, the Ashoka Pillar, and miniature paintings
        
        Ticket Prices:
        - Adult: Rs. 500 per ticket
        - Student: Rs. 250 per ticket (with valid ID)
        - Child (under 12): Free
        
        Other Information:
        - Photography is allowed in most areas (no flash)
        - The museum offers guided tours in English and Hindi
        - There is a cafe and gift shop in the premises
        - Wheelchairs are available for visitors with mobility issues
        - Large bags must be checked at the entrance
        
        Booking Process:
        1. Get visitor's name
        2. Get visitor's email
        3. Get visitor's phone number
        4. Ask for visit date (in DD/MM/YYYY format)
        5. Ask for number of tickets (adult, student, child)
        6. Calculate total amount
        7. Show booking summary and confirm
        8. Process payment
        9. Generate booking reference
        
        IMPORTANT: When a user is in the booking process, they can change any information BEFORE the final confirmation. Be helpful and allow changes to name, email, phone, etc. during the booking flow. After payment confirmation, no changes are allowed.
        
        IMPORTANT: The date format should always be DD/MM/YYYY for storing in the system, but accept various date inputs from users.
        
        Keep responses conversational, friendly, and concise. When answering general questions, provide accurate information about the museum.
        When in the booking flow, stay on track but be helpful.
        
        If someone asks a general question during the booking process, answer it briefly then guide them back to the booking flow.
        """
        self.initialize_chat()

    def initialize_chat(self):
        self.chat = model.start_chat(history=[])
        self.chat.send_message(self.system_prompt)

    def reset_state(self):
        self.conversation_state = {
            'current_step': 'greeting',
            'booking_info': {},
            'conversation_ended': False
        }
        self.chat_history = []
        self.initialize_chat()

    def _validate_email(self, email: str) -> bool:
        return '@' in email and '.' in email.split('@')[1]

    def _validate_phone(self, phone: str) -> bool:
        digits = ''.join(filter(str.isdigit, phone))
        return len(digits) >= 10

    def generate_booking_ref(self) -> str:
        now = datetime.now()
        date_str = now.strftime('%Y%m%d')
        random_part = str(abs(hash(str(now.timestamp()))))[-3:]
        return f"MSM{date_str}{random_part}"
        
    def _is_change_request(self, message: str) -> tuple:
        """
        Check if the message is a request to change information
        Returns (is_change_request, field_to_change, new_value)
        """
        # Common patterns for change requests
        name_patterns = [
            r"change (?:my|the) name (?:to|from) (.+)",
            r"my name is (?:actually|not) (.+)",
            r"(?:update|correct) (?:my|the) name to (.+)"
        ]
        
        email_patterns = [
            r"change (?:my|the) email (?:to|from) (.+)",
            r"my email is (?:actually|not) (.+)",
            r"(?:update|correct) (?:my|the) email to (.+)"
        ]
        
        phone_patterns = [
            r"change (?:my|the) (?:phone|number) (?:to|from) (.+)",
            r"my (?:phone|number) is (?:actually|not) (.+)",
            r"(?:update|correct) (?:my|the) (?:phone|number) to (.+)"
        ]
        
        date_patterns = [
            r"change (?:my|the) (?:date|visit date) (?:to|from) (.+)",
            r"(?:visit|come) on (.+)",
            r"planning to visit on (.+)",
            r"(?:update|correct) (?:my|the) (?:date|visit date) to (.+)"
        ]
        
        # Check each pattern
        for pattern in name_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return True, 'name', match.group(1).strip()
                
        for pattern in email_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return True, 'email', match.group(1).strip()
                
        for pattern in phone_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return True, 'phone', match.group(1).strip()
                
        for pattern in date_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                date_value = match.group(1).strip()
                formatted_date = parse_date(date_value)
                return True, 'visit_date', formatted_date
                
        return False, None, None

    def process_ai_response(self, ai_response, current_step, message):
        """Process the AI-generated response based on the current state"""
        booking_info = self.conversation_state['booking_info']
        next_state = current_step
        
        # Check if this is a change request
        is_change, field, new_value = self._is_change_request(message)
        
        # Handle change requests before payment/confirmation
        if is_change and current_step not in ['payment', 'confirm_booking']:
            if field:
                booking_info[field] = new_value
                return {
                    'response': f"I've updated your {field} to '{new_value}'. " + ai_response,
                    'state': current_step
                }
        
        # Normal booking flow processing
        if current_step == 'asking_name':
            # Check if message looks like a general question
            if len(message.split()) > 3 and not is_change and not message.lower().startswith("my name"):
                # Just return the AI response without changing state
                return {
                    'response': ai_response,
                    'state': current_step
                }
                
            # Extract name from user message
            if message.lower().startswith("my name is "):
                name = message[11:].strip()
            elif message.lower().startswith("my full name is "):
                name = message[16:].strip()
            else:
                name = message.strip()
                
            booking_info['name'] = name
            next_state = 'asking_email'
            
        elif current_step == 'asking_email':
            email = message.strip()
            # Check if it's a general question
            if '@' not in email and len(message.split()) > 3 and not is_change and not message.lower().startswith("my email") and not message.lower().startswith("my mail"):
                # Just return the AI response without changing state
                return {
                    'response': ai_response,
                    'state': current_step
                }
             
            # Extract email if in a natural language response   
            if message.lower().startswith("my email is "):
                email = message[12:].strip()
            elif message.lower().startswith("my mail is "):
                email = message[11:].strip()
                
            if self._validate_email(email):
                booking_info['email'] = email
                next_state = 'asking_phone'
            else:
                return {
                    'response': "That doesn't look like a valid email address. Please provide a valid email.",
                    'state': 'asking_email'
                }
                
        elif current_step == 'asking_phone':
            phone = message.strip()
            # Check if it's a general question
            if not any(char.isdigit() for char in message) and len(message.split()) > 3 and not is_change and not message.lower().startswith("my phone"):
                # Just return the AI response without changing state
                return {
                    'response': ai_response,
                    'state': current_step
                }
                
            # Extract phone if in a natural language response
            if message.lower().startswith("my phone is "):
                phone = message[12:].strip()
            elif message.lower().startswith("my number is "):
                phone = message[13:].strip()
            
            # Extract numbers only from the phone
            phone_digits = ''.join(filter(str.isdigit, phone))
                
            if self._validate_phone(phone_digits):
                booking_info['phone'] = phone_digits
                next_state = 'asking_visit_date'
            else:
                return {
                    'response': "Please provide a valid phone number with at least 10 digits.",
                    'state': 'asking_phone'
                }
                
        elif current_step == 'asking_visit_date':
            # Process and format the date
            if not is_change:
                formatted_date = parse_date(message.strip())
                booking_info['visit_date'] = formatted_date
            
            next_state = 'asking_adult_tickets'
            
        elif current_step == 'asking_adult_tickets':
            try:
                # Check if it's a general question
                if not any(char.isdigit() for char in message) and len(message.split()) > 3 and not is_change and not "adult" in message.lower() and not "ticket" in message.lower():
                    # Just return the AI response without changing state
                    return {
                        'response': ai_response,
                        'state': current_step
                    }
                
                # Try to extract a number from the message
                match = re.search(r'\d+', message)
                if not match:
                    return {
                        'response': "Please enter a valid number for adult tickets.",
                        'state': 'asking_adult_tickets'
                    }
                    
                adult_tickets = int(match.group())
                booking_info['adult_tickets'] = adult_tickets
                next_state = 'asking_student_tickets'
                
                # If this was a response indicating they want all adult tickets
                if "adult" in message.lower() and not "student" in message.lower() and not "child" in message.lower():
                    booking_info['student_tickets'] = 0
                    booking_info['child_tickets'] = 0
                    
                    # Calculate total amount
                    total = adult_tickets * self.prices['adult']
                    booking_info['total_amount'] = total
                    
                    # Skip to confirmation
                    summary = self._generate_confirmation_message(booking_info)
                    return {
                        'response': summary,
                        'state': 'confirm_booking',
                        'options': [
                            {'text': 'Confirm & Pay', 'value': 'confirm'},
                            {'text': 'Cancel', 'value': 'cancel'}
                        ]
                    }
                
            except (ValueError, AttributeError):
                return {
                    'response': "Please enter a valid number for adult tickets.",
                    'state': 'asking_adult_tickets'
                }
                
        elif current_step == 'asking_student_tickets':
            try:
                # Check if it's a general question
                if not any(char.isdigit() for char in message) and len(message.split()) > 3 and not is_change and not "student" in message.lower() and not "ticket" in message.lower():
                    # Just return the AI response without changing state
                    return {
                        'response': ai_response,
                        'state': current_step
                    }
                    
                # Try to extract a number from the message
                match = re.search(r'\d+', message)
                if not match:
                    student_tickets = 0  # Assume 0 if no number found
                else:
                    student_tickets = int(match.group())
                    
                booking_info['student_tickets'] = student_tickets
                next_state = 'asking_child_tickets'
            except (ValueError, AttributeError):
                return {
                    'response': "Please enter a valid number for student tickets.",
                    'state': 'asking_student_tickets'
                }
                
        elif current_step == 'asking_child_tickets':
            try:
                # Check if it's a general question
                if not any(char.isdigit() for char in message) and len(message.split()) > 3 and not is_change and not "child" in message.lower() and not "ticket" in message.lower():
                    # Just return the AI response without changing state
                    return {
                        'response': ai_response,
                        'state': current_step
                    }
                    
                # Try to extract a number from the message
                match = re.search(r'\d+', message)
                if not match:
                    child_tickets = 0  # Assume 0 if no number found
                else:
                    child_tickets = int(match.group())
                    
                booking_info['child_tickets'] = child_tickets
                
                # Calculate total amount
                total = (
                    booking_info.get('adult_tickets', 0) * self.prices['adult'] +
                    booking_info.get('student_tickets', 0) * self.prices['student'] +
                    booking_info.get('child_tickets', 0) * self.prices['child']
                )
                booking_info['total_amount'] = total
                
                # Generate a booking summary
                summary = self._generate_confirmation_message(booking_info)
                return {
                    'response': summary,
                    'state': 'confirm_booking',
                    'options': [
                        {'text': 'Confirm & Pay', 'value': 'confirm'},
                        {'text': 'Cancel', 'value': 'cancel'}
                    ]
                }
            except (ValueError, AttributeError):
                return {
                    'response': "Please enter a valid number for child tickets.",
                    'state': 'asking_child_tickets'
                }
                
        elif current_step == 'confirm_booking':
            if message.lower() == 'confirm' or "yes" in message.lower() or "proceed" in message.lower():
                return {
                    'response': "Please proceed with the payment of ₹" + str(booking_info['total_amount']),
                    'state': 'payment',
                    'show_payment': True
                }
            elif message.lower() == 'cancel' or "no" in message.lower() or "stop" in message.lower():
                self.reset_state()
                return {
                    'response': "Booking canceled. How can I help you today?",
                    'state': 'greeting'
                }
            elif message.lower() == 'book tickets':
                # Handle edge case where user accidentally clicks Book Tickets button
                return {
                    'response': "Please proceed with the payment of ₹" + str(booking_info['total_amount']),
                    'state': 'payment',
                    'show_payment': True
                }
        
        # Return the next step in the conversation
        self.conversation_state['current_step'] = next_state
        return {'response': ai_response, 'state': next_state}

    def get_response(self, message: str, current_state: str = None) -> Dict[str, Any]:
        try:
            if current_state:
                self.conversation_state['current_step'] = current_state
                
            current_step = self.conversation_state['current_step']
            booking_info = self.conversation_state['booking_info']
            
            # Handle payment completion
            if current_step == 'payment' and message == 'payment_completed':
                # Generate booking reference if not already present
                if 'booking_ref' not in booking_info:
                    booking_info['booking_ref'] = self.generate_booking_ref()
                
                booking_info['status'] = 'paid'
                booking_info['payment_date'] = datetime.now().isoformat()
                
                # Save to database
                if self.db.save_booking(booking_info):
                    ticket_data = {
                        'booking_ref': booking_info['booking_ref'],
                        'name': booking_info.get('name'),
                        'email': booking_info.get('email'),
                        'phone': booking_info.get('phone'),
                        'visit_date': booking_info.get('visit_date'),
                        'adult_tickets': booking_info.get('adult_tickets', 0),
                        'student_tickets': booking_info.get('student_tickets', 0),
                        'child_tickets': booking_info.get('child_tickets', 0),
                        'total_amount': booking_info.get('total_amount', 0)
                    }
                    
                    self.conversation_state['conversation_ended'] = True
                    return {
                        'response': f"""
                        Payment completed successfully!
                        
                        Booking Reference: {ticket_data['booking_ref']}
                        Name: {ticket_data['name']}
                        Email: {ticket_data['email']}
                        Phone: {ticket_data['phone']}
                        Visit Date: {ticket_data['visit_date']}
                        
                        Adult Tickets: {ticket_data['adult_tickets']}
                        Student Tickets: {ticket_data['student_tickets']}
                        Child Tickets: {ticket_data['child_tickets']}
                        Total Amount: ₹{ticket_data['total_amount']}
                        
                        Thank you for booking with us! You can download your ticket below.
                        """,
                        'state': 'booking_completed',
                        'ticket_data': ticket_data,
                        'show_download': True,
                        'conversation_ended': True
                    }

            # If conversation has ended, only allow starting a new conversation
            if self.conversation_state['conversation_ended']:
                if message.lower() == 'start_new':
                    self.reset_state()
                    return {
                        'response': "Welcome! How can I assist you with museum tickets today?",
                        'state': 'initial_options',
                        'options': [
                            {'text': 'Museum Information', 'value': 'info'},
                            {'text': 'Book Tickets', 'value': 'book'}
                        ]
                    }
                return {
                    'response': "Our conversation has ended. Click 'Start New Chat' to begin a new conversation.",
                    'state': 'ended',
                    'options': [{'text': 'Start New Chat', 'value': 'start_new'}]
                }

            # Initial greeting with options
            if current_step == 'greeting':
                return {
                    'response': "Welcome to the National Museum of India! How may I assist you today?",
                    'state': 'initial_options',
                    'options': [
                        {'text': 'Museum Information', 'value': 'info'},
                        {'text': 'Book Tickets', 'value': 'book'}
                    ]
                }
            
            # Handle museum info request or booking initiation
            if current_step == 'initial_options':
                if message == 'info':
                    return {
                        'response': """
                        Welcome to the National Museum of India!
                        
                        About:
                        The National Museum of India houses over 200,000 works of art spanning 5,000 years of cultural heritage.
                        
                        Opening Hours:
                        Tuesday to Sunday: 10:00 AM - 6:00 PM
                        Closed on Mondays and National Holidays
                        
                        Location:
                        Janpath, New Delhi, India
                        
                        Contact:
                        Phone: +91-11-23019272
                        Email: info@nationalmuseum.in
                        
                        Would you like to book tickets now?
                        """,
                        'state': 'after_info',
                        'options': [
                            {'text': 'Book Tickets', 'value': 'book'},
                            {'text': 'No, thanks', 'value': 'end'}
                        ]
                    }
                elif message == 'book':
                    return {
                        'response': "Great! Let's start your booking. Please provide your name.",
                        'state': 'asking_name'
                    }

            # Handle after info options
            if current_step == 'after_info':
                if message == 'book':
                    return {
                        'response': "Great! Let's start your booking. Please provide your name.",
                        'state': 'asking_name'
                    }
                elif message == 'end':
                    self.conversation_state['conversation_ended'] = True
                    return {
                        'response': "Thank you for your interest in the National Museum. Have a great day!",
                        'state': 'ended',
                        'options': [{'text': 'Start New Chat', 'value': 'start_new'}]
                    }
            
            # For payment and confirmation stage - check if attempting to change details
            if current_step == 'payment':
                # Pattern to detect requests to change information
                change_patterns = [
                    r'change (my|the) (name|email|phone|visit date|date|tickets|number)',
                    r'update (my|the) (name|email|phone|visit date|date|tickets|number)',
                    r'modify (my|the) (name|email|phone|visit date|date|tickets|number)',
                    r'edit (my|the) (name|email|phone|visit date|date|tickets|number)',
                    r'different (name|email|phone|visit date|date|tickets|number)'
                ]
                
                if any(re.search(pattern, message.lower()) for pattern in change_patterns):
                    return {
                        'response': "I'm sorry, but once you've started the payment process, the booking details cannot be changed. If you need to make changes, you'll need to cancel this booking and start a new one.",
                        'state': current_step
                    }
                    
            # Special handling for the visit date step
            if current_step == 'asking_visit_date':
                # Check for date related change request
                is_change, field, new_value = self._is_change_request(message)
                
                if field == 'visit_date':
                    booking_info['visit_date'] = new_value
                    return {
                        'response': f"I've set your visit date to {new_value}. How many adult tickets would you like to book? (Rs. 500 each)",
                        'state': 'asking_adult_tickets'
                    }
                elif not is_change:
                    # Not a change request, treat as new date
                    formatted_date = parse_date(message.strip())
                    booking_info['visit_date'] = formatted_date
                    return {
                        'response': f"Thanks! I've scheduled your visit for {formatted_date}. How many adult tickets would you like to book? (Rs. 500 each)",
                        'state': 'asking_adult_tickets',
                    }
            
            # Check for change requests before processing with AI
            is_change, field, new_value = self._is_change_request(message)
            if is_change and current_step != 'payment' and field and current_step not in ['initial_options', 'greeting', 'after_info']:
                # Handle changes before confirmation
                old_value = booking_info.get(field, "")
                booking_info[field] = new_value
                
                # For visit date changes, show a more specific message
                if field == 'visit_date':
                    return {
                        'response': f"I've updated your visit date to {new_value}. Let's continue with your booking.",
                        'state': current_step 
                    }
                
                return {
                    'response': f"I've updated your {field} from '{old_value}' to '{new_value}'. Let's continue with your booking.",
                    'state': current_step 
                }
            
            # For booking flow steps or general queries, use Gemini AI
            prompt = f"The user says: '{message}'. Current step: {current_step}."
            
            # Add context about the booking flow stage to guide the AI
            if current_step == 'asking_name':
                prompt += " Ask for their email address in a friendly way. If they asked a general question, answer it briefly and then guide them back to providing their name for the booking."
            elif current_step == 'asking_email':
                prompt += " Ask for their phone number. If they asked a general question, answer it briefly and then guide them back to providing their email for the booking."
            elif current_step == 'asking_phone':
                prompt += " Ask for the date they'd like to visit the museum in DD/MM/YYYY format. If they asked a general question, answer it briefly and then guide them back to providing their phone number for the booking."
            elif current_step == 'asking_visit_date':
                prompt += " Ask how many adult tickets they'd like to purchase (Rs. 500 each). If they asked a general question, answer it briefly and then guide them back to providing their visit date for the booking."
            elif current_step == 'asking_adult_tickets':
                prompt += " Ask how many student tickets they'd like to purchase (Rs. 250 each). If they asked a general question, answer it briefly and then guide them back to providing the number of adult tickets for the booking."
            elif current_step == 'asking_student_tickets':
                prompt += " Ask how many child tickets they'd like (free for children under 12). If they asked a general question, answer it briefly and then guide them back to providing the number of student tickets for the booking."
            elif current_step == 'payment':
                prompt += " Remind them to complete the payment. If they asked to change details, explain that it's not possible at this stage and they would need to cancel and start a new booking."
            elif current_step == 'confirm_booking':
                prompt += " Ask them to confirm the booking."
            else:
                # For general conversation or initial stages, allow more flexibility
                prompt += " Answer their question in a helpful way, providing accurate information about the museum."
            
            # Send message to Gemini API
            ai_response = self.chat.send_message(prompt).text
            
            # If in one of the booking flow steps, process the structured response
            if current_step in ['asking_name', 'asking_email', 'asking_phone', 'asking_visit_date', 
                                'asking_adult_tickets', 'asking_student_tickets', 'asking_child_tickets',
                                'confirm_booking']:
                return self.process_ai_response(ai_response, current_step, message)
            
            # For general queries, just return the AI response
            return {
                'response': ai_response,
                'state': current_step
            }
            
        except Exception as e:
            logger.error(f"Chatbot error: {str(e)}", file=sys.stderr)
            return {
                'response': "I apologize, but I encountered an error. Please try again.",
                'state': current_step or 'greeting'
            }
    
    def _generate_confirmation_message(self, booking_data: Dict) -> str:
        """Generate a confirmation message with booking details"""
        adult_tickets = booking_data.get('adult_tickets', 0)
        student_tickets = booking_data.get('student_tickets', 0)
        child_tickets = booking_data.get('child_tickets', 0)
        total_amount = booking_data.get('total_amount', 0)
        
        return f"""
        Please confirm your booking details:
        
        Name: {booking_data.get('name')}
        Email: {booking_data.get('email')}
        Phone: {booking_data.get('phone')}
        Visit Date: {booking_data.get('visit_date')}
        
        Adult Tickets: {adult_tickets} x ₹{self.prices['adult']} = ₹{adult_tickets * self.prices['adult']}
        Student Tickets: {student_tickets} x ₹{self.prices['student']} = ₹{student_tickets * self.prices['student']}
        Child Tickets: {child_tickets} (Free)
        
        Total Amount: ₹{total_amount}
        
        Would you like to confirm this booking and proceed to payment?
        """

# Initialize the chatbot service as a singleton instance
chatbot_service = ChatbotService()

class ChatbotHandler:
    def __init__(self):
        self.model = "deepseek-r1:1.5b"
        self.museum_name = os.getenv('MUSEUM_NAME', 'Museum')
        self.prices = {
            'adult': 20,
            'student': 15,
            'child': 10
        }
        
    async def get_response(self, user_message: str, chat_history: List[Dict], current_state: str, booking_data: Dict):
        if not self._is_museum_related(user_message) and current_state == 'greeting':
            return {
                'content': "I apologize, but I can only assist with museum-related queries. Please ask me about ticket booking or museum information.",
                'state': 'greeting'
            }

        response = self._process_message(user_message, current_state, booking_data)
        return response

    def _is_museum_related(self, message: str) -> bool:
        museum_keywords = ['museum', 'ticket', 'booking', 'visit', 'exhibition', 'gallery', 'art', 'tour']
        return any(keyword in message.lower() for keyword in museum_keywords)

    def _process_message(self, message: str, current_state: str, booking_data: Dict):
        if current_state == 'greeting':
            if self._contains_booking_intent(message):
                return {
                    'content': f"I'll help you book tickets for {self.museum_name}. Could you please provide the name under which you'd like to make the booking?",
                    'state': 'asking_name'
                }
            return {
                'content': f"Welcome to {self.museum_name}! I can help you with ticket booking. Would you like to book tickets?",
                'state': 'greeting'
            }

        states = {
            'asking_name': {
                'next': 'asking_email',
                'message': "Great! Could you please provide your email address?"
            },
            'asking_email': {
                'next': 'asking_phone',
                'message': "Thank you! Now, please provide your phone number."
            },
            'asking_phone': {
                'next': 'asking_tickets',
                'message': "How many tickets would you like to book in total?"
            },
            'asking_tickets': {
                'next': 'asking_adults',
                'message': "How many adult tickets do you need? (Price: $20 per ticket)"
            },
            'asking_adults': {
                'next': 'asking_students',
                'message': "How many student tickets do you need? (Price: $15 per ticket)"
            },
            'asking_students': {
                'next': 'asking_children',
                'message': "How many children tickets do you need? (Age below 12, Price: $10 per ticket)"
            },
            'asking_children': {
                'next': 'confirmation',
                'message': self._generate_confirmation_message
            }
        }

        if current_state in states:
            next_state = states[current_state]['next']
            message_func = states[current_state]['message']
            
            if callable(message_func):
                response_message = message_func(booking_data)
            else:
                response_message = message_func

            return {
                'content': response_message,
                'state': next_state
            }

        return {
            'content': "I'm sorry, I didn't understand that. Could you please try again?",
            'state': current_state
        }

    def _contains_booking_intent(self, message: str) -> bool:
        booking_keywords = ['book', 'ticket', 'buy', 'purchase', 'reserve']
        return any(keyword in message.lower() for keyword in booking_keywords)

    def _generate_confirmation_message(self, booking_data: Dict) -> str:
        total = (
            self.prices['adult'] * booking_data.get('adults', 0) +
            self.prices['student'] * booking_data.get('students', 0) +
            self.prices['child'] * booking_data.get('children', 0)
        )
        
        return f"""Please confirm your booking details:
        Name: {booking_data.get('name')}
        Email: {booking_data.get('email')}
        Phone: {booking_data.get('phone')}
        Visit Date: {booking_data.get('visit_date')}
        Adult tickets: {booking_data.get('adults', 0)} (${self.prices['adult']} each)
        Student tickets: {booking_data.get('students', 0)} (${self.prices['student']} each)
        Children tickets: {booking_data.get('children', 0)} (${self.prices['child']} each)
        Total amount: ${total}
        
        Would you like to confirm this booking?"""

    def _format_chat_history(self, history):
        return [{"role": "user" if msg["isUser"] else "assistant", 
                 "content": msg["content"]} for msg in history]

    def _determine_state(self, response):
        # Implement logic to determine the current state of conversation
        # (greeting, asking_name, asking_email, etc.)
        pass