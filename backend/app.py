from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from dotenv import load_dotenv
import logging
import smtplib
from ticket_generator import generate_ticket_pdf
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import base64
from database import DatabaseHandler
from chatbot import chatbot_service
load_dotenv()

app = Flask(__name__)
CORS(app)

logger = logging.getLogger(__name__)

chatbot = chatbot_service
db = DatabaseHandler()

def send_ticket_email(email, ticket_data, pdf_path):
    try:
        # Email configuration
        sender_email = os.getenv('GMAIL_EMAIL')
        sender_password = os.getenv('GMAIL_APP_PASSWORD')

        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = 'Your Museum Visit Confirmation'

        # Email body
        html_content = f'''
            <h1>Thank you for booking your museum visit!</h1>
            <p>Dear {ticket_data['name']},</p>
            
            <h2>Booking Details:</h2>
            <ul>
                <li><strong>Booking Reference:</strong> {ticket_data['booking_ref']}</li>
                <li><strong>Visit Date:</strong> {ticket_data['visit_date']}</li>
                <li><strong>Contact Phone:</strong> {ticket_data['phone']}</li>
            </ul>

            <h2>Ticket Summary:</h2>
            <ul>
                <li><strong>Adult Tickets:</strong> {ticket_data['adult_tickets']}</li>
                <li><strong>Child Tickets:</strong> {ticket_data['child_tickets']}</li>
                <li><strong>Student Tickets:</strong> {ticket_data['student_tickets']}</li>
                <li><strong>Total Amount:</strong> ₹{ticket_data['total_amount']}</li>
            </ul>

            <p><strong>Important Information:</strong></p>
            <ul>
                <li>Please arrive 15 minutes before your scheduled time</li>
                <li>Bring a valid ID proof</li>
                <li>Your ticket is attached to this email</li>
                <li>Student ticket holders must present valid student ID</li>
            </ul>

            <p>We look forward to welcoming you to our museum!</p>
            <p>Best regards,<br>Museum Team</p>
        '''

        # Attach HTML content
        msg.attach(MIMEText(html_content, 'html'))

        # Attach PDF
        with open(pdf_path, 'rb') as f:
            pdf_attachment = MIMEApplication(f.read(), _subtype='pdf')
            pdf_attachment.add_header(
                'Content-Disposition', 
                'attachment', 
                filename=f"museum-ticket-{ticket_data['booking_ref']}.pdf"
            )
            msg.attach(pdf_attachment)

        # Send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print(f"Email sent successfully to {email}")
            return True

    except Exception as e:
        print(f"Error sending email: {str(e)}")
        logger.error(f"Error sending email: {e}")
        return False

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
        print("Received ticket generation request")
        ticket_data = request.get_json()
        print(f"Ticket data: {ticket_data}")
        
        if 'email' not in ticket_data:
            return jsonify({'error': 'Email is required'}), 400

        # Generate PDF ticket
        pdf_path = generate_ticket_pdf(ticket_data)
        print(f"Generated PDF at: {pdf_path}")

        # Send email with ticket
        email_sent = send_ticket_email(ticket_data['email'], ticket_data, pdf_path)
        
        if not email_sent:
            logger.error("Failed to send email")
            # Continue to return PDF even if email fails
        
        # Send the PDF file
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"museum-ticket-{ticket_data['booking_ref']}.pdf"
        )
        
    except Exception as e:
        print(f"Error in generate_ticket: {str(e)}")
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