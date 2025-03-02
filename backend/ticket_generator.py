from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont, Font
import os
from datetime import datetime

def generate_ticket_pdf(ticket_data):
    if not os.path.exists('tickets'):
        os.makedirs('tickets')
        
    filename = f"tickets/museum-ticket-{ticket_data['booking_ref']}.pdf"
    
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Theme colors
    primary_color = colors.Color(0.29, 0.22, 0.16)  # Dark brown
    secondary_color = colors.Color(0.77, 0.64, 0.52)  # Gold
    
    # Use Rs. instead of ₹ symbol for better compatibility
    try:
        # Register a font that supports rupee symbol
        font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'NotoSans-Regular.ttf')
        pdfmetrics.registerFont(TTFont('NotoSans', font_path))
        use_rupee_symbol = True
    except:
        use_rupee_symbol = False
    
    rupee = "₹" if use_rupee_symbol else "Rs."
    
    # Header
    c.setFillColor(primary_color)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width/2, height-1.5*inch, "NATIONAL MUSEUM OF INDIA")
    
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width/2, height-2*inch, "ENTRY TICKET")
    
    # Decorative line
    c.setStrokeColor(secondary_color)
    c.setLineWidth(2)
    c.line(2*inch, height-2.5*inch, width-2*inch, height-2.5*inch)
    
    # Ticket details
    y = height-3*inch
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, y, "BOOKING DETAILS")
    y -= 0.5*inch
    
    c.setFont("Helvetica", 12)
    details = [
        f"Booking Reference: {ticket_data['booking_ref']}",
        f"Visit Date: {ticket_data['visit_date']}",
        f"Name: {ticket_data['name']}",
        f"Email: {ticket_data['email']}",
        f"Phone: {ticket_data['phone']}"
    ]
    
    # Add ticket quantities and calculate price breakdown
    ticket_counts = []
    price_breakdown = []
    total_amount = 0

    if ticket_data['adult_tickets'] > 0:
        adult_amount = ticket_data['adult_tickets'] * 500
        ticket_counts.append(f"Adult Tickets: {ticket_data['adult_tickets']}")
        price_breakdown.append(f"Adult: {ticket_data['adult_tickets']} x {rupee}500 = {rupee}{adult_amount}")
        total_amount += adult_amount

    if ticket_data['student_tickets'] > 0:
        student_amount = ticket_data['student_tickets'] * 250
        ticket_counts.append(f"Student Tickets: {ticket_data['student_tickets']}")
        price_breakdown.append(f"Student: {ticket_data['student_tickets']} x {rupee}250 = {rupee}{student_amount}")
        total_amount += student_amount

    if ticket_data.get('child_tickets', 0) > 0 and ticket_data['adult_tickets'] > 0:
        ticket_counts.append(f"Child Tickets: {ticket_data['child_tickets']} (Free)")
    
    # Add booking details
    for line in details:
        c.drawString(1*inch, y, line)
        y -= 0.3*inch
    
    # Add ticket information
    y -= 0.2*inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, y, "TICKET DETAILS")
    y -= 0.3*inch
    
    c.setFont("Helvetica", 12)
    for count in ticket_counts:
        c.drawString(1*inch, y, count)
        y -= 0.3*inch
    
    # Add price breakdown
    y -= 0.2*inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, y, "PRICE BREAKDOWN")
    y -= 0.3*inch
    
    c.setFont("NotoSans" if use_rupee_symbol else "Helvetica", 12)
    for price in price_breakdown:
        c.drawString(1*inch, y, price)
        y -= 0.3*inch
    
    y -= 0.2*inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, y, f"Total Amount: {rupee}{total_amount}")
    
    # Instructions section
    y -= 0.6*inch
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, y, "IMPORTANT INSTRUCTIONS")
    y -= 0.4*inch
    
    c.setFont("Helvetica", 11)
    instructions = [
        "• Please arrive 15 minutes before your scheduled visit time",
        "• Present this ticket at the entrance (digital or printed)",
        "• Photography is allowed without flash",
        "• No food and beverages allowed inside",
        "• Please maintain silence in the museum premises"
    ]
    
    for instruction in instructions:
        c.drawString(1*inch, y, instruction)
        y -= 0.3*inch
    
    # Footer
    c.setFont("Helvetica", 10)  # Changed from Helvetica-Italic to Helvetica
    c.drawCentredString(width/2, 0.5*inch, "Thank you for visiting National Museum of India")
    
    c.save()
    return filename
