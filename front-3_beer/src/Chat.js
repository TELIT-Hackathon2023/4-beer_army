import React, { useState, useEffect, useRef } from 'react';
import './App.css';


function Chat() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

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
      setIsLoading(true)
      const response = await fetch('http://127.0.0.1:5000/api/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });
      const data = await response.json();
      return data.response; 
    } catch (error) {
      console.error('Fetch error:', error);
      return 'Fetching error.'
    } finally{
      setIsLoading(false)
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

      {
  isLoading ?
    <div className="loading-container">
      {/* You can use a spinner or a simple loading message */}
      <div>Loading...</div>
      {/* Alternatively, you can use an image or a CSS-based spinner */}
    </div>
  :
    <div className="input-container">
      <input
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && sendMessage()}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
}
    </div>
  );
}

export default Chat;
