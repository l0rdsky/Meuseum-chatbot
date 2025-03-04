import React, { useState, useRef, useEffect } from 'react';
import { Paper, Box, TextField, Button, Container } from '@mui/material';
import ChatMessage from './ChatMessage';
import TicketModal from './TicketModal';
import axios from 'axios';
import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";

const Chat = () => {
    const [messages, setMessages] = useState([{
        content: 'Welcome! How can I assist you with museum tickets today?',
        isUser: false,
        type: 'options',
        options: [
            { text: 'Museum Information', value: 'info' },
            { text: 'Book Tickets', value: 'book' }
        ]
    }]);
    const [inputMessage, setInputMessage] = useState('');
    const [currentState, setCurrentState] = useState('initial_options');
    const [bookingData, setBookingData] = useState({});
    const [showPaymentButton, setShowPaymentButton] = useState(false);
    const [isProcessingPayment, setIsProcessingPayment] = useState(false);
    const [showTicketModal, setShowTicketModal] = useState(false);
    const chatContainerRef = useRef(null);
    const [selectedDate, setSelectedDate] = useState(null);
    const [showDatePicker, setShowDatePicker] = useState(false);
    const [showConfirmButtons, setShowConfirmButtons] = useState(false);
    const [showDownloadButton, setShowDownloadButton] = useState(false);
    const [ticketData, setTicketData] = useState(null);
    const [showInitialOptions, setShowInitialOptions] = useState(false);
    const [showBookingOption, setShowBookingOption] = useState(false);
    const [disabledMessageIndexes, setDisabledMessageIndexes] = useState(new Set());

    const handleOptionClick = async (value) => {
        // Disable the clicked options immediately
        setMessages(prev => {
            const lastIndex = prev.length - 1;
            setDisabledMessageIndexes(prevDisabled => new Set([...prevDisabled, lastIndex]));
            return [...prev, {
                content: value === 'info' ? 'Museum Information' : 'Book Tickets',
                isUser: true,
                type: 'text'
            }];
        });

        try {
            const response = await axios.post('http://localhost:5000/chat', {
                message: value,
                currentState: currentState
            });

            if (response.data) {
                setCurrentState(response.data.state);
                setShowInitialOptions(!!response.data.show_initial_buttons);
                setShowBookingOption(!!response.data.show_booking_option);
                
                if (response.data.booking_info) {
                    setBookingData(response.data.booking_info);
                }

                setShowPaymentButton(!!response.data.show_payment);
                setShowDatePicker(!!response.data.show_date_picker);
                setShowConfirmButtons(!!response.data.show_confirmation_buttons);
                setShowDownloadButton(!!response.data.show_download);

                if (response.data.ticket_data) {
                    setTicketData(response.data.ticket_data);
                }

                // Add new message with fresh options
                if (response.data.options) {
                    setMessages(prev => [...prev, {
                        content: response.data.response,
                        isUser: false,
                        type: 'options',
                        options: response.data.options
                    }]);
                } else {
                    setMessages(prev => [...prev, {
                        content: response.data.response,
                        isUser: false,
                        type: 'text'
                    }]);
                }
            }
        } catch (error) {
            console.error('Error:', error);
            setMessages(prev => [...prev, {
                content: "Sorry, I encountered an error. Please try again.",
                isUser: false,
                type: 'text'
            }]);
        }
    };

    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (!inputMessage.trim()) return;

        const userMessageContent = inputMessage.trim();
        setInputMessage('');

        // Add user message to messages
        setMessages(prev => [...prev, {
            content: userMessageContent,
            isUser: true,
            type: 'text'
        }]);

        try {
            // Direct API call instead of using handleOptionClick
            const response = await axios.post('http://localhost:5000/chat', {
                message: userMessageContent,
                currentState: currentState
            });

            if (response.data) {
                setCurrentState(response.data.state);
                
                if (response.data.booking_info) {
                    setBookingData(response.data.booking_info);
                }

                setShowPaymentButton(!!response.data.show_payment);
                setShowDatePicker(!!response.data.show_date_picker);
                setShowConfirmButtons(!!response.data.show_confirmation_buttons);
                setShowDownloadButton(!!response.data.show_download);

                if (response.data.ticket_data) {
                    setTicketData(response.data.ticket_data);
                }

                // Add bot response
                if (response.data.options) {
                    setMessages(prev => [...prev, {
                        content: response.data.response,
                        isUser: false,
                        type: 'options',
                        options: response.data.options
                    }]);
                } else {
                    setMessages(prev => [...prev, {
                        content: response.data.response,
                        isUser: false,
                        type: 'text'
                    }]);
                }
            }
        } catch (error) {
            console.error('Error:', error);
            setMessages(prev => [...prev, {
                content: "Sorry, I encountered an error. Please try again.",
                isUser: false,
                type: 'text'
            }]);
        }
    };

    const handlePayment = async () => {
        setIsProcessingPayment(true);
        try {
            // Simulate payment processing
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            const response = await axios.post('http://localhost:5000/chat', {
                message: 'payment_completed',
                currentState: currentState
            });

            if (response.data) {
                setCurrentState(response.data.state);
                
                if (response.data.ticket_data) {
                    setTicketData(response.data.ticket_data);
                }

                // Add payment success message
                setMessages(prev => [...prev, {
                    content: response.data.response,
                    isUser: false,
                    type: 'text'
                }]);

                // Show download button
                setShowDownloadButton(true);
                setShowPaymentButton(false);
            }
        } catch (error) {
            console.error('Error:', error);
            setMessages(prev => [...prev, {
                content: "Sorry, there was an error processing your payment. Please try again.",
                isUser: false,
                type: 'text'
            }]);
        } finally {
            setIsProcessingPayment(false);
        }
    };

    const handleDateSelect = (date) => {
        const formattedDate = date.toISOString().split('T')[0];
        setSelectedDate(date);
        
        handleOptionClick(formattedDate);
        setShowDatePicker(false);
    };

    const handleConfirmation = (confirmed) => {
        const message = confirmed ? 'confirm' : 'cancel';
        // Add user's confirmation to messages
        setMessages(prev => [...prev, {
            content: confirmed ? 'Confirm' : 'Cancel',
            isUser: true,
            type: 'text'
        }]);
        handleOptionClick(message);
        setShowConfirmButtons(false);
    };

    const handleDownloadTicket = async () => {
        try {
            if (!ticketData) {
                throw new Error('No ticket data available');
            }

            const response = await axios.post(
                'http://localhost:5000/generate-ticket', 
                ticketData,
                { responseType: 'blob' }
            );
            
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `museum-ticket-${ticketData.booking_ref}.pdf`);
            document.body.appendChild(link);
            link.click();
            window.URL.revokeObjectURL(url);
            link.remove();
        } catch (error) {
            console.error('Error downloading ticket:', error);
            setMessages(prev => [...prev, {
                content: "Sorry, there was an error downloading your ticket. Please try again.",
                isUser: false,
                type: 'text'
            }]);
        }
    };

    // Scroll to bottom when messages change
    useEffect(() => {
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
        }
    }, [messages]);

    return (
        <Container maxWidth="md">
            <Paper elevation={3} className="chat-container">
                <Box className="chat-messages" ref={chatContainerRef}>
                    {messages.map((message, index) => (
                        <ChatMessage 
                            key={index} 
                            message={message} 
                            onOptionClick={handleOptionClick}
                            disableOptions={disabledMessageIndexes.has(index)}
                        />
                    ))}
                </Box>

                <div className="chat-input-container">
                    {showDatePicker && (
                        <div className="date-picker-container">
                            <DatePicker
                                selected={selectedDate}
                                onChange={handleDateSelect}
                                minDate={new Date()}
                                inline
                                className="date-picker"
                            />
                        </div>
                    )}

                    {showConfirmButtons && (
                        <div className="confirmation-buttons">
                            <button
                                className="confirm-button"
                                onClick={() => handleConfirmation(true)}
                            >
                                Confirm Booking
                            </button>
                            <button
                                className="cancel-button"
                                onClick={() => handleConfirmation(false)}
                            >
                                Cancel
                            </button>
                        </div>
                    )}

                    {showDownloadButton && (
                        <button
                            className="download-button"
                            onClick={handleDownloadTicket}
                        >
                            Download Ticket PDF
                        </button>
                    )}

                    {!showDatePicker && !showConfirmButtons && !showPaymentButton && !showDownloadButton && (
                        <form onSubmit={handleSendMessage} className="chat-input-form">
                            <input
                                type="text"
                                value={inputMessage}
                                onChange={(e) => setInputMessage(e.target.value)}
                                placeholder="Type your message..."
                                className="chat-input"
                            />
                            <button type="submit" className="send-button">
                                Send
                            </button>
                        </form>
                    )}

                    {showPaymentButton && (
                        <button
                            className="payment-button"
                            onClick={handlePayment}
                            disabled={isProcessingPayment}
                        >
                            {isProcessingPayment ? 'Processing...' : 'Pay Now'}
                        </button>
                    )}
                </div>
            </Paper>
            {showTicketModal && ticketData && (
                <TicketModal 
                    bookingData={ticketData} 
                    onClose={() => setShowTicketModal(false)} 
                />
            )}
        </Container>
    );
};

export default Chat;