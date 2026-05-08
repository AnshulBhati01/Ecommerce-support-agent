import React, { useState } from 'react';
import axios from 'axios';

export const EscalationPrompt = ({ conversationId, customerId, onEscalate, onDismiss }) => {
  const [loading, setLoading] = useState(false);
  const [reason, setReason] = useState('');
  const [priority, setPriority] = useState('medium');
  const [error, setError] = useState('');

  const handleEscalate = async () => {
    if (!reason.trim()) {
      setError('Please provide a reason for escalation');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const response = await axios.post('/api/v1/escalations/tickets', {
        conversation_id: conversationId,
        customer_id: customerId,
        reason: reason,
        priority: priority
      });

      setLoading(false);
      if (onEscalate) {
        onEscalate(response.data);
      }
    } catch (err) {
      console.error('Error escalating:', err);
      setError('Failed to escalate. Please try again.');
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-lg max-w-md w-full p-6">
        <h2 className="text-lg font-bold mb-4">Escalate to Support Agent</h2>
        
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-3 py-2 rounded mb-4 text-sm">
            {error}
          </div>
        )}

        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">Priority Level</label>
          <select
            value={priority}
            onChange={e => setPriority(e.target.value)}
            className="w-full border border-gray-300 rounded px-3 py-2"
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
            <option value="urgent">Urgent</option>
          </select>
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">Reason for Escalation</label>
          <textarea
            value={reason}
            onChange={e => setReason(e.target.value)}
            placeholder="Please explain why you need to escalate to an agent..."
            className="w-full border border-gray-300 rounded px-3 py-2 h-24 resize-none"
          />
        </div>

        <div className="flex gap-2">
          <button
            onClick={handleEscalate}
            disabled={loading}
            className="flex-1 bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 disabled:bg-gray-400 transition font-medium"
          >
            {loading ? 'Escalating...' : 'Escalate'}
          </button>
          <button
            onClick={onDismiss}
            disabled={loading}
            className="flex-1 bg-gray-300 text-gray-800 px-4 py-2 rounded hover:bg-gray-400 disabled:bg-gray-400 transition"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default EscalationPrompt;
