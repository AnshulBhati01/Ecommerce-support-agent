import React, { useState } from 'react';
import axios from 'axios';

export const OrderContext = ({ customerId }) => {
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(false);
  const [orderID, setOrderID] = useState('');
  const [error, setError] = useState('');

  const fetchOrder = async () => {
    if (!orderID.trim()) {
      setError('Please enter an order ID');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const response = await axios.get(
        `/api/v1/orders/${orderID}`,
        { params: { customer_id: customerId } }
      );
      setOrder(response.data);
    } catch (err) {
      console.error('Error fetching order:', err);
      setError('Order not found. Please check the ID and try again.');
      setOrder(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-50 p-4 rounded-lg mb-4 border border-gray-200">
      <h3 className="font-bold mb-3 text-lg">Order Lookup</h3>
      <div className="flex gap-2 mb-4">
        <input
          type="text"
          value={orderID}
          onChange={e => setOrderID(e.target.value)}
          onKeyPress={e => e.key === 'Enter' && !loading && fetchOrder()}
          placeholder="Enter Order ID"
          className="flex-1 border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-blue-500"
        />
        <button
          onClick={fetchOrder}
          disabled={loading}
          className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 disabled:bg-gray-400 transition"
        >
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-3 py-2 rounded mb-3 text-sm">
          {error}
        </div>
      )}

      {order && (
        <div className="bg-white p-3 rounded border border-gray-200 text-sm">
          <div className="grid grid-cols-2 gap-2">
            <div>
              <p className="text-gray-600">Status</p>
              <p className="font-semibold text-green-600">{order.status}</p>
            </div>
            <div>
              <p className="text-gray-600">Total Amount</p>
              <p className="font-semibold">${order.total_amount?.toFixed(2)}</p>
            </div>
            <div>
              <p className="text-gray-600">Tracking</p>
              <p className="font-semibold">{order.tracking_number || 'N/A'}</p>
            </div>
            <div>
              <p className="text-gray-600">Expected Delivery</p>
              <p className="font-semibold">
                {order.expected_delivery ? new Date(order.expected_delivery).toLocaleDateString() : 'TBD'}
              </p>
            </div>
          </div>
          
          {order.items && order.items.length > 0 && (
            <div className="mt-3 pt-3 border-t">
              <p className="font-semibold mb-2">Items:</p>
              {order.items.map((item, idx) => (
                <div key={idx} className="text-xs bg-gray-50 p-2 rounded mb-1">
                  <p>{item.product_name} x {item.quantity}</p>
                  <p className="text-gray-600">${item.total_price?.toFixed(2)}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default OrderContext;
