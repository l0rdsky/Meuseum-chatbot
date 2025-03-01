import { useState, useEffect, useRef } from 'react';
import { Layout, Button } from 'antd';
import { HomeOutlined } from '@ant-design/icons';
import MessageBubble from './MessageBubble';
import '../index.css';

const { Content, Footer } = Layout;

const MuseumApp = () => {
  const [messages, setMessages] = useState([
    { text: 'Hello! How can I help you today?', isSent: false },
  ]);
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef(null);

  const handleSendMessage = () => {
    if (inputValue.trim()) {
      const userMessage = inputValue.trim();
      setMessages((prevMessages) => [...prevMessages, { text: userMessage, isSent: true }]);
      setInputValue('');
  
      // Show "Bot is typing..."
      setTimeout(() => {
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: "Bot is typing...", isSent: false, isTyping: true }
        ]);
  
        setTimeout(() => {
          let botResponse = "I'm sorry, I didn't understand that.";
  
          if (userMessage.toLowerCase().includes('book ticket')) {
            botResponse = "Sure! How many tickets would you like to book?";
          } else if (userMessage.match(/\d+\s*ticket/i)) {
            botResponse = "Please provide the date for your visit (e.g., 2025-03-10).";
          } else if (userMessage.match(/\d{4}-\d{2}-\d{2}/)) {
            botResponse = "Got it! How would you like to pay? We accept online payments.";
          } else if (userMessage.toLowerCase().includes('pay')) {
            botResponse = "Payment successful! Your tickets have been booked.";
          }
  
          // Remove "Bot is typing..." and add bot response
          setMessages((prevMessages) => [
            ...prevMessages.slice(0, -1), // Remove last "Bot is typing..."
            { text: botResponse, isSent: false }
          ]);
        }, 1000); // Bot response delay
      }, 500); // "Bot is typing..." delay
    }
  };
  

  useEffect(() => {
    setTimeout(() => {
      document.getElementById("chatbot-box").style.opacity = "1";
      document.getElementById("chatbot-box").style.transform = "translate(-50%, -50%) scale(1)";
    }, 200);
  }, []);
  

  return (
    <Layout style={{ minHeight: '100vh', background: "url('/museum-bg.jpg') center/cover no-repeat" }}>
      {/* Home Button */}
      <Button 
        type="default" 
        onClick={() => window.location.href = '/'} 
        style={{ position: 'absolute', top: '20px', right: '20px', zIndex: 1100 }}>
        <HomeOutlined /> Home
      </Button>

      {/* Chatbot (Always Open) */}
      {/* Chatbot (Always Open) */}
<div
  style={{
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%) scale(0.9)', /* Start smaller */
    width: '1050px',
    height: '600px',
    background: 'rgba(255, 255, 255, 0.8)',
    borderRadius: '10px',
    display: 'flex',
    flexDirection: 'column',
    boxShadow: '0px 4px 10px rgba(0, 0, 0, 0.2)',
    zIndex: 1200,
    opacity: 0, /* Initially hidden */
    transition: 'opacity 0.5s ease-out, transform 0.5s ease-out', /* Smooth animation */
  }}
  id="chatbot-box"
>

        <div style={{ padding: '10px', borderBottom: '1px solid #ccc', background: 'rgba(255, 255, 255, 0.5)' }}>
          <strong>Chatbot for Museum Ticket Booking</strong>
        </div>
        <div style={{ flex: 1, padding: '10px', overflowY: 'auto' }}>
          {messages.map((msg, index) => (
            <MessageBubble key={index} text={msg.text} isSent={msg.isSent} />
          ))}
          <div ref={messagesEndRef} />
        </div>
        <div style={{ padding: '10px', borderTop: '1px solid #ccc', display: 'flex' }}>
          <input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type your message..."
            onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
            style={{ flex: 1, padding: '8px', border: 'none', outline: 'none' }}
          />
          <Button type="primary" onClick={handleSendMessage} style={{ marginLeft: '10px' }}>
            Send
          </Button>
        </div>
      </div>

      {/* Footer */}
      <Footer style={{
        textAlign: 'center',
        position: 'absolute',
        bottom: '0',
        width: '100%',
        background: 'rgba(0, 0, 0, 0.7)',
        color: '#fff',
        padding: '10px',
      }}>
        © {new Date().getFullYear()} Museum Chatbot. Created by Sushant , Suruchi , Vaibhavi , Akash . All rights reserved.
      </Footer>
    </Layout>
  );
};

export default MuseumApp;
