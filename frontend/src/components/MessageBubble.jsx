import React from 'react';

const MessageBubble = ({ text, isSent }) => {
  return (
    <div style={{ 
      display: 'flex', 
      justifyContent: isSent ? 'flex-end' : 'flex-start', 
      marginBottom: '10px', 
      alignItems: 'center'
    }}>
      {!isSent && (
        <img 
          src="/bot-avatar.png" 
          alt="Bot" 
          style={{ width: '40px', height: '40px', borderRadius: '50%', marginRight: '10px' }}
        />
      )}
      <div style={{
        background: isSent ? '#d6556c' : '#e2c5ca',
        color: isSent ? '#fff' : '#000',
        padding: '10px',
        borderRadius: '10px',
        maxWidth: '70%',
      }}>
        {text}
      </div>
      {isSent && (
        <img 
          src="/user-avatar.png" 
          alt="User" 
          style={{ width: '40px', height: '40px', borderRadius: '50%', marginLeft: '10px' }}
        />
      )}
    </div>
  );
};

export default MessageBubble;
