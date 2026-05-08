import React, { useState, useEffect } from 'react';
import ChatWindow from '../components/ChatWindow';
import OrderContext from '../components/OrderContext';
import EscalationPrompt from '../components/EscalationPrompt';
import { chatService } from '../services/api';

export const ChatPage = () => {
  const [customerId, setCustomerId] = useState('');
  const [conversationId, setConversationId] = useState(null);
  const [showEscalationPrompt, setShowEscalationPrompt] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [customerEmail, setCustomerEmail] = useState('');

  const startNewConversation = async () => {
    if (!customerId.trim()) {
      setError('Please enter a customer ID');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await chatService.startConversation(customerId);
      setConversationId(response.data.conversation_id);
      setLoading(false);
    } catch (err) {
      console.error('Error starting conversation:', err);
      setError('Failed to start conversation. Please try again.');
      setLoading(false);
    }
  };

  if (!conversationId) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
        <div className="bg-white rounded-lg shadow-lg p-8 max-w-md w-full">
          <h1 className="text-3xl font-bold mb-2 text-center text-blue-600">
            E-Commerce Support Chat
          </h1>
          <p className="text-gray-600 text-center mb-6">
            Get instant help with orders, returns, and more
          </p>

          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Customer ID
            </label>
            <input
              type="text"
              value={customerId}
              onChange={e => setCustomerId(e.target.value)}
              onKeyPress={e => e.key === 'Enter' && !loading && startNewConversation()}
              placeholder="Enter your customer ID"
              className="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:border-blue-500"
            />
          </div>

          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email (Optional)
            </label>
            <input
              type="email"
              value={customerEmail}
              onChange={e => setCustomerEmail(e.target.value)}
              placeholder="your.email@example.com"
              className="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:border-blue-500"
            />
          </div>

          <button
            onClick={startNewConversation}
            disabled={loading}
            className="w-full bg-blue-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-blue-700 disabled:bg-gray-400 transition text-lg"
          >
            {loading ? 'Starting Conversation...' : 'Start Chat'}
          </button>

          <p className="text-xs text-gray-500 text-center mt-4">
            Our AI assistant is available 24/7 to help you
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex gap-4 h-screen bg-gray-100 p-4">
      <div className="flex-1">
        <ChatWindow customerId={customerId} conversationId={conversationId} />
      </div>

      <div className="w-80 flex flex-col gap-4">
        <OrderContext customerId={customerId} />
        
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="font-bold mb-3">Quick Actions</h3>
          <button
            onClick={() => setShowEscalationPrompt(true)}
            className="w-full bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition mb-2"
          >
            Escalate to Agent
          </button>
          <button
            onClick={() => {
              setConversationId(null);
              setCustomerId('');
            }}
            className="w-full bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500 transition"
          >
            End Chat
          </button>
        </div>
      </div>

      {showEscalationPrompt && (
        <EscalationPrompt
          conversationId={conversationId}
          customerId={customerId}
          onEscalate={(ticket) => {
            console.log('Escalated:', ticket);
            setShowEscalationPrompt(false);
          }}
          onDismiss={() => setShowEscalationPrompt(false)}
        />
      )}
    </div>
  );
};

export default ChatPage;
