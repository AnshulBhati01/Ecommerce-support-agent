import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Chat services
export const chatService = {
  startConversation: (customerId) =>
    apiClient.post('/api/v1/chat/conversation/start', { customer_id: customerId }),
  
  sendMessage: (conversationId, customerId, message) =>
    apiClient.post('/api/v1/chat/message', {
      conversation_id: conversationId,
      customer_id: customerId,
      message
    }),
  
  getConversation: (conversationId) =>
    apiClient.get(`/api/v1/chat/conversation/${conversationId}`),
  
  endConversation: (conversationId, satisfactionScore) =>
    apiClient.post(`/api/v1/chat/conversation/${conversationId}/end`, {
      satisfaction_score: satisfactionScore
    })
};

// Order services
export const orderService = {
  getOrder: (orderId, customerId) =>
    apiClient.get(`/api/v1/orders/${orderId}`, { params: { customer_id: customerId } }),
  
  getCustomerOrders: (customerId, limit = 10) =>
    apiClient.get(`/api/v1/orders/customer/${customerId}`, { params: { limit } }),
  
  createOrder: (orderData) =>
    apiClient.post('/api/v1/orders/', orderData),
  
  updateOrderStatus: (orderId, newStatus) =>
    apiClient.put(`/api/v1/orders/${orderId}/status`, { new_status: newStatus })
};

// Escalation services
export const escalationService = {
  createTicket: (conversationId, customerId, reason, priority = 'medium') =>
    apiClient.post('/api/v1/escalations/tickets', {
      conversation_id: conversationId,
      customer_id: customerId,
      reason,
      priority
    }),
  
  getTicket: (ticketId) =>
    apiClient.get(`/api/v1/escalations/tickets/${ticketId}`),
  
  updateTicketStatus: (ticketId, newStatus, resolution) =>
    apiClient.put(`/api/v1/escalations/tickets/${ticketId}/status`, {
      new_status: newStatus,
      resolution
    }),
  
  assignTicket: (ticketId, agentId) =>
    apiClient.put(`/api/v1/escalations/tickets/${ticketId}/assign`, {
      agent_id: agentId
    }),
  
  getPendingTickets: (priority, limit = 10) =>
    apiClient.get('/api/v1/escalations/pending', { params: { priority, limit } })
};

// Health check
export const healthService = {
  check: () =>
    apiClient.get('/health')
};

export default apiClient;
