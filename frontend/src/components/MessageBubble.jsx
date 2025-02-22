// import React from 'react';
import { Typography } from 'antd';
import PropTypes from 'prop-types';

const { Text } = Typography;

const MessageBubble = ({ message, isSent }) => {
  return (
    <div style={{
      display: 'flex',
      justifyContent: isSent ? 'flex-end' : 'flex-start',
      marginBottom: '10px'
    }}>
      <div style={{
        margin: '20px',
        maxWidth: '60%',
        padding: '15px',
        borderRadius: '10px',
        background: isSent ? '#1890ff' : '#f1f1f1',
        color: isSent ? '#fff' : '#000'
      }}>
        <Text>{message}</Text>
      </div>
    </div>
  );
};
MessageBubble.propTypes = {
  message: PropTypes.string.isRequired,
  isSent: PropTypes.bool.isRequired,
};

export default MessageBubble;
