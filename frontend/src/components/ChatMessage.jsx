import React from 'react';

const ChatMessage = ({ message, onOptionClick, disableOptions }) => {
    const messageClass = message.isUser ? 'chat-message user-message' : 'chat-message bot-message';

    return (
        <div className={messageClass}>
            {message.content}
            {message.type === 'options' && message.options && !disableOptions && (
                <div className="message-options">
                    {message.options.map((option, index) => (
                        <button
                            key={index}
                            onClick={() => onOptionClick(option.value)}
                            className="option-button"
                        >
                            {option.text}
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
};

export default ChatMessage;
