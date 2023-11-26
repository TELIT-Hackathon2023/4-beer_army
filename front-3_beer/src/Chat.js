import React, { useState, useEffect, useRef } from 'react';
import './App.css';


function Chat() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const storedMessages = JSON.parse(localStorage.getItem('chatHistory')) || [];
    setMessages(storedMessages);
  }, []);

  const storeMessage = (newMessage) => {
    const existingMessages = JSON.parse(localStorage.getItem('chatHistory')) || [];
    const updatedMessages = [...existingMessages, newMessage];
    localStorage.setItem('chatHistory', JSON.stringify(updatedMessages));
    
  };

  const fetchMessage = async (message) => {
    try {
      const response = await fetch('YOUR_BACKEND_API_URL', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });

      const data = await response.json();
      return data.answer; 
    } catch (error) {
      console.error('Fetch error:', error);
      return 'Fetching error.'
    }
  };

  const sendMessage = async () => {
    if (!input) return;

    const newMessages = [...messages, { text: input, sender: 'user' }];
    setMessages(newMessages);

    const response = await fetchMessage(input);

    setMessages([...newMessages, { text: response, sender: 'bot' }]);
  
    storeMessage({ text: input, sender: 'user' });
    storeMessage({ text: response, sender: 'bot' });

    setInput('');
  };

  return (
    <div className="chat-container">
      <div className="messages-container">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`message ${message.sender}`}
          >
            {message.text}
          </div>
        ))}
      </div>


      <div className="input-container">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && sendMessage()}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default Chat;
