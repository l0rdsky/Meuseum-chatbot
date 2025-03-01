from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from chatbot import chatbot_service
from database import DatabaseHandler
from ticket_generator import generate_ticket_pdf
import os
from dotenv import load_dotenv
import logging

load_dotenv()

app = Flask(__name__)
CORS(app)

logger = logging.getLogger(__name__)

chatbot = chatbot_service
db = DatabaseHandler()

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
            
        user_message = data['message']
        current_state = data.get('currentState', 'greeting')
        
        response = chatbot.get_response(user_message, current_state)
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Server Error: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500

@app.route('/generate-ticket', methods=['POST'])
def generate_ticket():
    try:
        ticket_data = request.get_json()
        
        # Generate PDF ticket
        pdf_path = generate_ticket_pdf(ticket_data)
        
        # Send the PDF file
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"museum-ticket-{ticket_data['booking_ref']}.pdf"
        )
        
    except Exception as e:
        logger.error(f"Error generating ticket: {e}")
        return jsonify({
            'error': 'Failed to generate ticket',
            'details': str(e)
        }), 500

@app.route('/tickets/<ticket_id>.pdf')
def get_ticket(ticket_id):
    pdf_path = f'tickets/{ticket_id}.pdf'
    return send_file(pdf_path, mimetype='application/pdf')

if __name__ == '__main__':
    if not os.path.exists('tickets'):
        os.makedirs('tickets')
    app.run(debug=True, port=5000)