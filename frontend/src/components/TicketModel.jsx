import React from 'react';

const TicketModel = ({ bookingData, onClose }) => {
    if (!bookingData) return null;

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <div className="ticket">
                    <h2>🎫 Museum Entry Ticket</h2>
                    <div className="ticket-details">
                        <p><strong>Booking Reference:</strong> {bookingData.booking_ref}</p>
                        <p><strong>Name:</strong> {bookingData.name}</p>
                        <p><strong>Email:</strong> {bookingData.email}</p>
                        <p><strong>Phone:</strong> {bookingData.phone}</p>
                        <div className="ticket-counts">
                            <p><strong>Adult Tickets:</strong> {bookingData.adult_tickets}</p>
                            <p><strong>Student Tickets:</strong> {bookingData.student_tickets}</p>
                            <p><strong>Child Tickets:</strong> {bookingData.child_tickets}</p>
                        </div>
                        <p className="total-amount"><strong>Total Amount:</strong> Rs. {bookingData.total_amount}</p>
                    </div>
                    <div className="ticket-footer">
                        <p>Please show this ticket at the museum entrance</p>
                        <p>Valid for one-time entry</p>
                    </div>
                </div>
                <button className="close-button" onClick={onClose}>Close</button>
            </div>
        </div>
    );
};

export default TicketModel;
