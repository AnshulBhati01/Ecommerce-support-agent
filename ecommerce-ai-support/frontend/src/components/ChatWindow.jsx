import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import MessageBubble from './MessageBubble';

export const ChatWindow = ({ customerId, conversationId }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [showEscalation, setShowEscalation] = useState(false);
  const [error, setError] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Load conversation history on mount
  useEffect(() => {
    if (conversationId) {
      loadConversationHistory();
    }
  }, [conversationId]);

  const loadConversationHistory = async () => {
    try {
      const response = await axios.get(`/api/v1/chat/conversation/${conversationId}`);
      const loadedMessages = response.data.messages.map(msg => ({
        id: msg.message_id,
        sender: msg.sender_type,
        text: msg.message_text,
        timestamp: new Date(msg.created_at),
        intent: msg.intent,
        requiresEscalation: msg.intent === 'escalation'
      }));
      setMessages(loadedMessages);
    } catch (err) {
      console.error('Error loading conversation:', err);
      setError('Failed to load conversation history');
    }
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = {
      id: Date.now(),
      sender: 'customer',
      text: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    setError('');

    try {
      const response = await axios.post('/api/v1/chat/message', {
        conversation_id: conversationId,
        customer_id: customerId,
        message: input
      });

      const aiMessage = {
        id: response.data.message_id,
        sender: 'ai',
        text: response.data.response,
        timestamp: new Date(),
        intent: response.data.intent,
        requiresEscalation: response.data.requires_escalation
      };

      setMessages(prev => [...prev, aiMessage]);

      if (response.data.requires_escalation) {
        setShowEscalation(true);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setError('Failed to send message. Please try again.');
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        sender: 'ai',
        text: 'Sorry, something went wrong. Please try again.',
        timestamp: new Date()
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-white">
      {/* Header */}
      <div className="bg-blue-600 text-white p-4">
        <h1 className="text-xl font-bold">Customer Support Chat</h1>
        <p className="text-sm text-blue-100">Conversation ID: {conversationId}</p>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3">
          {error}
        </div>
      )}

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 py-8">
            <p>No messages yet. Start the conversation!</p>
          </div>
        )}
        {messages.map(msg => (
          <MessageBubble
            key={msg.id}
            message={msg}
            isUser={msg.sender === 'customer'}
          />
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-200 rounded-lg px-4 py-2">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-600 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-600 rounded-full animate-bounce delay-100"></div>
                <div className="w-2 h-2 bg-gray-600 rounded-full animate-bounce delay-200"></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Escalation Prompt */}
      {showEscalation && (
        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mx-4 mb-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="font-bold text-yellow-800">Would you like to escalate to a human agent?</p>
              <p className="text-yellow-700 text-sm">We can connect you with a specialist for better assistance.</p>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => {
                  // Escalate logic
                  setShowEscalation(false);
                }}
                className="bg-yellow-600 text-white px-4 py-2 rounded hover:bg-yellow-700"
              >
                Escalate
              </button>
              <button
                onClick={() => setShowEscalation(false)}
                className="bg-gray-300 text-gray-800 px-4 py-2 rounded hover:bg-gray-400"
              >
                Continue
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="border-t p-4 bg-gray-50">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyPress={e => e.key === 'Enter' && !loading && sendMessage()}
            placeholder="Type your message..."
            className="flex-1 border border-gray-300 rounded px-4 py-2 focus:outline-none focus:border-blue-500"
            disabled={loading}
          />
          <button
            onClick={sendMessage}
            disabled={loading}
            className="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600 disabled:bg-gray-400 transition"
          >
            {loading ? 'Sending...' : 'Send'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatWindow;
