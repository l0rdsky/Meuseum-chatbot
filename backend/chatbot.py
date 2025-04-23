import json
from typing import List, Dict, Any
import ollama
import re
import os
import sys
from datetime import datetime
import logging
from database import DatabaseHandler

logger = logging.getLogger(__name__)

def chatbot(user_message, current_state='greeting'):
    try:
        # Define conversation states and their corresponding responses
        states = {
            'greeting': {
                'next_state': 'asking_name',
                'response': "I'll help you book your museum tickets. Could you please provide your name?"
            },
            'asking_name': {
                'next_state': 'asking_email',
                'response': "Thank you! Please provide your email address."
            },
            'asking_email': {
                'next_state': 'asking_phone',
                'response': "Great! Now, please share your phone number."
            },
            'asking_phone': {
                'next_state': 'asking_adult_tickets',
                'response': "How many adult tickets would you like? (Price: $20 per ticket)"
            },
            'asking_adult_tickets': {
                'next_state': 'asking_student_tickets',
                'response': "How many student tickets would you like? (Price: $15 per ticket)"
            },
            'asking_student_tickets': {
                'next_state': 'asking_child_tickets',
                'response': "And finally, how many children's tickets? (Age below 12, Price: $10 per ticket)"
            }
        }

        if current_state == 'greeting' and 'book' in user_message.lower():
            return {
                'response': states['greeting']['response'],
                'state': states['greeting']['next_state']
            }
        if current_state in states:
            return {
                'response': states[current_state]['response'],
                'state': states[current_state]['next_state']
            }

        # Default response for unknown states or general queries
        return {
            'response': "I can help you book museum tickets. Would you like to start the booking process?",
            'state': 'greeting'
        }

    except Exception as e:
        print(f"Chatbot error: {str(e)}", file=sys.stderr)
        return {
            'response': "I apologize, but I encountered an error. Please try again.",
            'state': 'greeting'
        }

class ChatbotService:
    def __init__(self):
        self.conversation_state = {
            'current_step': 'greeting',
            'booking_info': {},
            'conversation_ended': False  # New flag to track conversation end
        }
        self.prices = {
            'adult': 500,    # Rs. 500 per adult
            'student': 250,  # Rs. 250 per student
            'child': 0      # Free for children
        }
        self.db = DatabaseHandler()

    def reset_state(self):
        self.conversation_state = {
            'current_step': 'greeting',
            'booking_info': {},
            'conversation_ended': False
        }

    def _validate_email(self, email: str) -> bool:
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email))

    def _validate_phone(self, phone: str) -> bool:
        # Remove any non-digit characters
        digits = ''.join(filter(str.isdigit, phone))
        # Check if exactly 10 digits for Indian phone numbers
        return len(digits) == 10

    def generate_booking_ref(self) -> str:
        now = datetime.now()
        date_str = now.strftime('%Y%m%d')
        random_part = str(abs(hash(str(now.timestamp()))))[-3:]
        return f"MSM{date_str}{random_part}"

    def get_response(self, message: str, current_state: str = None) -> Dict[str, Any]:
        try:
            if current_state:
                self.conversation_state['current_step'] = current_state
                
            current_step = self.conversation_state['current_step']
            booking_info = self.conversation_state['booking_info']
            
            message = message.strip().lower()

            # Handle confirmation and cancellation
            if current_step == 'confirm_booking':
                if message == 'confirm':
                    return {
                        'response': "Great! Your booking is confirmed. Please proceed with the payment.",
                        'state': 'payment',
                        'booking_info': booking_info,
                        'show_payment': True,
                        'hide_options': True
                    }
                elif message == 'cancel':
                    return {
                        'response': "Booking cancelled. What would you like to do?",
                        'state': 'after_cancellation',
                        'options': [
                            {'text': 'Start New Chat', 'value': 'start_new'},
                            {'text': 'Edit Booking Info', 'value': 'edit_info'}
                        ]
                    }
                else:
                    return {
                        'response': "Please select either 'confirm' or 'cancel' to proceed.",
                        'state': 'confirm_booking',
                        'show_confirmation_buttons': True
                    }

            # Handle after cancellation options
            if current_step == 'after_cancellation':
                if message == 'start_new':
                    self.reset_state()
                    return {
                        'response': "Welcome! How can I assist you with museum tickets today?",
                        'state': 'initial_options',
                        'options': [
                            {'text': 'Museum Information', 'value': 'info'},
                            {'text': 'Book Tickets', 'value': 'book'}
                        ]
                    }
                elif message == 'edit_info':
                    self.conversation_state['current_step'] = 'asking_adult_tickets'
                    return {
                        'response': "Let's start over with the number of tickets. How many adult tickets would you like?",
                        'state': 'asking_adult_tickets'
                    }
                else:
                    return {
                        'response': "Please select an option to proceed.",
                        'state': 'after_cancellation',
                        'options': [
                            {'text': 'Start New Chat', 'value': 'start_new'},
                            {'text': 'Edit Booking Info', 'value': 'edit_info'}
                        ]
                    }

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

            logger.info(f"Current step: {current_step}, Message: {message}")

            # Initial greeting with options (only shown once)
            if current_step == 'greeting':
                return {
                    'response': "Welcome to the National Museum of India! How may I assist you today?",
                    'state': 'initial_options',
                    'options': [
                        {'text': 'Museum Information', 'value': 'info'},
                        {'text': 'Book Tickets', 'value': 'book'}
                    ]
                }
            
            # Handle museum info request
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
                if message == 'end':
                    self.conversation_state['conversation_ended'] = True
                    return {
                        'response': "Thank you for your interest in the National Museum! Have a great day. Feel free to start a new chat if you'd like to book tickets later.",
                        'state': 'ended',
                        'options': [{'text': 'Start New Chat', 'value': 'start_new'}]
                    }
                elif message == 'book':
                    return {
                        'response': "Great! Let's start your booking. Please provide your name.",
                        'state': 'asking_name'
                    }

            # Handle booking flow
            if current_step == 'asking_name':
                booking_info['name'] = message
                return {
                    'response': "Thank you! Please provide your email address.",
                    'state': 'asking_email'
                }

            # Handle email validation
            if current_step == 'asking_email':
                if not self._validate_email(message):
                    return {
                        'response': "Please enter a valid email address (e.g., example@domain.com)",
                        'state': 'asking_email'
                    }
                booking_info['email'] = message
                return {
                    'response': "Great! Now, please share your phone number.",
                    'state': 'asking_phone'
                }

            # Handle phone validation
            if current_step == 'asking_phone':
                if not self._validate_phone(message):
                    return {
                        'response': "Please enter a valid 10-digit Indian phone number (e.g., 9876543210)",
                        'state': 'asking_phone'
                    }
                booking_info['phone'] = message
                return {
                    'response': f"How many adult tickets would you like? (Price: ₹{self.prices['adult']} per ticket)",
                    'state': 'asking_adult_tickets'
                }

            if current_step == 'asking_adult_tickets':
                try:
                    adult_tickets = int(message)
                    if adult_tickets < 0:
                        return {
                            'response': "Please enter a valid number (0 or more) for adult tickets.",
                            'state': 'asking_adult_tickets'
                        }
                    booking_info['adult_tickets'] = adult_tickets
                    
                    # If no adult tickets, must have student tickets
                    if adult_tickets == 0:
                        return {
                            'response': f"How many student tickets would you like? (Price: ₹{self.prices['student']} per ticket)\nNote: At least one adult or student ticket is required.",
                            'state': 'asking_student_tickets'
                        }
                    else:
                        return {
                            'response': f"How many student tickets would you like? (Price: ₹{self.prices['student']} per ticket)",
                            'state': 'asking_student_tickets'
                        }
                except ValueError:
                    return {
                        'response': "Please enter a valid number for adult tickets.",
                        'state': 'asking_adult_tickets'
                    }

            if current_step == 'asking_student_tickets':
                try:
                    student_tickets = int(message)
                    if student_tickets < 0:
                        return {
                            'response': "Please enter a valid number (0 or more) for student tickets.",
                            'state': 'asking_student_tickets'
                        }
                    
                    # Check if at least one ticket is booked when no adult tickets
                    if booking_info.get('adult_tickets', 0) == 0 and student_tickets == 0:
                        return {
                            'response': """
                            You need to book at least one ticket to proceed.
                            Thank you for your interest! Would you like to start a new booking?
                            """,
                            'state': 'initial_options',
                            'show_initial_buttons': True,
                            'options': [
                                {'text': 'Start New Booking', 'value': 'book'},
                                {'text': 'Museum Information', 'value': 'info'}
                            ]
                        }
                        
                    booking_info['student_tickets'] = student_tickets
                    
                    # Calculate total amount here when skipping child tickets
                    if booking_info.get('adult_tickets', 0) == 0:
                        # Only student tickets
                        total = student_tickets * self.prices['student']
                        booking_info['total_amount'] = total
                        booking_info['child_tickets'] = 0  # Set child tickets to 0
                        
                        return {
                            'response': "Please select your preferred visit date.",
                            'state': 'asking_date',
                            'show_date_picker': True
                        }
                    else:
                        # If there are adult tickets, proceed to ask for child tickets
                        return {
                            'response': "How many children's tickets? (Age below 12, Free entry)",
                            'state': 'asking_child_tickets'
                        }
                except ValueError:
                    return {
                        'response': "Please enter a valid number for student tickets.",
                        'state': 'asking_student_tickets'
                    }

            if current_step == 'asking_child_tickets':
                try:
                    child_tickets = int(message)
                    booking_info['child_tickets'] = child_tickets
                    
                    # Calculate total amount
                    total = (booking_info['adult_tickets'] * self.prices['adult'] +
                            booking_info['student_tickets'] * self.prices['student'])
                    booking_info['total_amount'] = total
                    
                    return {
                        'response': "Please select your preferred visit date.",
                        'state': 'asking_date',
                        'show_date_picker': True
                    }
                except ValueError:
                    return {
                        'response': "Please enter a valid number for children's tickets.",
                        'state': 'asking_child_tickets'
                    }

            # Update the confirmation step
            if current_step == 'asking_date':
                booking_info['visit_date'] = message
                booking_info['booking_ref'] = self.generate_booking_ref()
                
                return {
                    'response': f"""
                    Booking Summary:
                    Name: {booking_info['name']}
                    Email: {booking_info['email']}
                    Phone: {booking_info['phone']}
                    Adult Tickets: {booking_info['adult_tickets']} x ₹{self.prices['adult']}
                    Student Tickets: {booking_info['student_tickets']} x ₹{self.prices['student']}
                    Child Tickets: {booking_info['child_tickets']} (Free)
                    Visit Date: {booking_info['visit_date']}
                    
                    Total Amount: ₹{booking_info['total_amount']}
                    
                    Would you like to confirm this booking?
                    """,
                    'state': 'confirm_booking',
                    'booking_info': booking_info,
                    'show_confirmation_buttons': True
                }

            # Default response (should rarely be reached in production)
            return {
                'response': "I apologize, but I'm not sure how to help with that. Would you like to start a new conversation?",
                'state': 'ended',
                'options': [{'text': 'Start New Chat', 'value': 'start_new'}]
            }

        except Exception as e:
            logger.error(f"Error in get_response: {e}")
            self.reset_state()
            return {
                'response': "I encountered an error. Would you like to start a new conversation?",
                'state': 'error',
                'options': [{'text': 'Start New Chat', 'value': 'start_new'}]
            }

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