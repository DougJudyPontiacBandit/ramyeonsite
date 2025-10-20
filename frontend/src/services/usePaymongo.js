/**
 * PayMongo API Service
 * Handles payment processing for GCash, PayMaya, and Card payments
 */

// Get PayMongo API keys from environment variables
// eslint-disable-next-line no-unused-vars
const PAYMONGO_PUBLIC_KEY = process.env.VUE_APP_PAYMONGO_PUBLIC_KEY;
const PAYMONGO_SECRET_KEY = process.env.VUE_APP_PAYMONGO_SECRET_KEY;
// eslint-disable-next-line no-unused-vars
const PAYMONGO_MODE = process.env.VUE_APP_PAYMONGO_MODE || 'test';

// PayMongo API base URL
const PAYMONGO_API_URL = 'https://api.paymongo.com/v1';

/**
 * Convert amount to centavos (PayMongo requires amounts in smallest currency unit)
 * @param {number} amount - Amount in pesos
 * @returns {number} Amount in centavos
 */
const convertToCentavos = (amount) => {
  return Math.round(amount * 100);
};

/**
 * Create authorization header for PayMongo API
 * @returns {string} Base64 encoded authorization header
 */
const getAuthHeader = () => {
  const encodedKey = btoa(PAYMONGO_SECRET_KEY + ':');
  return `Basic ${encodedKey}`;
};

/**
 * Process GCash payment
 * @param {Object} params - Payment parameters
 * @param {number} params.amount - Amount in pesos
 * @param {string} params.orderId - Order ID
 * @param {string} params.customerEmail - Customer email
 * @param {string} params.customerName - Customer name
 * @returns {Promise<Object>} PayMongo source object
 */
export const processGCashPayment = async ({ amount, orderId, customerEmail, customerName }) => {
  try {
    const response = await fetch(`${PAYMONGO_API_URL}/sources`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': getAuthHeader()
      },
      body: JSON.stringify({
        data: {
          attributes: {
            type: 'gcash',
            amount: convertToCentavos(amount),
            currency: 'PHP',
            redirect: {
              success: `${window.location.origin}/#/cart?payment=success&order=${orderId}`,
              failed: `${window.location.origin}/#/cart?payment=failed&order=${orderId}`
            },
            billing: {
              name: customerName,
              email: customerEmail
            },
            metadata: {
              order_id: orderId
            }
          }
        }
      })
    });

    if (!response.ok) {
      const error = await response.json();
      console.error('GCash API error response:', error);
      throw new Error(error.errors?.[0]?.detail || 'Failed to create GCash payment');
    }

    const data = await response.json();
    console.log('GCash payment source created:', data);
    return data;
  } catch (error) {
    console.error('GCash payment error:', error);
    throw error;
  }
};

/**
 * Process PayMaya payment
 * @param {Object} params - Payment parameters
 * @param {number} params.amount - Amount in pesos
 * @param {string} params.orderId - Order ID
 * @param {string} params.customerEmail - Customer email
 * @param {string} params.customerName - Customer name
 * @returns {Promise<Object>} PayMongo source object
 */
export const processPayMayaPayment = async ({ amount, orderId, customerEmail, customerName }) => {
  try {
    const response = await fetch(`${PAYMONGO_API_URL}/sources`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': getAuthHeader()
      },
      body: JSON.stringify({
        data: {
          attributes: {
            type: 'paymaya',
            amount: convertToCentavos(amount),
            currency: 'PHP',
            redirect: {
              success: `${window.location.origin}/#/cart?payment=success&order=${orderId}`,
              failed: `${window.location.origin}/#/cart?payment=failed&order=${orderId}`
            },
            billing: {
              name: customerName,
              email: customerEmail
            },
            metadata: {
              order_id: orderId
            }
          }
        }
      })
    });

    if (!response.ok) {
      const error = await response.json();
      console.error('PayMaya API error response:', error);
      throw new Error(error.errors?.[0]?.detail || 'Failed to create PayMaya payment');
    }

    const data = await response.json();
    console.log('PayMaya payment source created:', data);
    return data;
  } catch (error) {
    console.error('PayMaya payment error:', error);
    throw error;
  }
};

/**
 * Process Card payment using Payment Links (redirects to PayMongo checkout)
 * PayMongo doesn't support 'card' as a source type - we need to use Payment Links
 * @param {Object} params - Payment parameters
 * @param {number} params.amount - Amount in pesos
 * @param {string} params.orderId - Order ID
 * @param {string} params.customerEmail - Customer email
 * @param {string} params.customerName - Customer name
 * @returns {Promise<Object>} PayMongo payment link object with redirect URL
 */
export const processCardPayment = async ({ amount, orderId, customerEmail, customerName }) => {
  try {
    const successUrl = `${window.location.origin}/#/cart?payment=success&order=${orderId}`;
    const failedUrl = `${window.location.origin}/#/cart?payment=failed&order=${orderId}`;

    // Create a payment link for card payments
    const response = await fetch(`${PAYMONGO_API_URL}/links`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': getAuthHeader()
      },
      body: JSON.stringify({
        data: {
          attributes: {
            amount: convertToCentavos(amount),
            currency: 'PHP',
            description: `Order #${orderId} - Ramyeon Order`,
            remarks: `Order ${orderId}`,
            redirect: {
              success: successUrl,
              failed: failedUrl
            }
          }
        }
      })
    });

    if (!response.ok) {
      const error = await response.json();
      console.error('Card payment API error:', error);
      throw new Error(error.errors?.[0]?.detail || 'Failed to create card payment link');
    }

    const data = await response.json();
    console.log('Card payment link created:', data);
    
    // Convert payment link response to match source response format
    return {
      data: {
        id: data.data.id,
        type: 'payment_link',
        attributes: {
          redirect: {
            checkout_url: data.data.attributes.checkout_url,
            success: successUrl,
            failed: failedUrl
          },
          status: data.data.attributes.status
        }
      }
    };
  } catch (error) {
    console.error('Card payment error:', error);
    throw error;
  }
};

/**
 * Process GrabPay QR payment
 * @param {Object} params - Payment parameters
 * @param {number} params.amount - Amount in pesos
 * @param {string} params.orderId - Order ID
 * @param {string} params.customerEmail - Customer email
 * @param {string} params.customerName - Customer name
 * @returns {Promise<Object>} PayMongo source object with redirect URL
 */
export const processGrabPayPayment = async ({ amount, orderId, customerEmail, customerName }) => {
  try {
    const response = await fetch(`${PAYMONGO_API_URL}/sources`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': getAuthHeader()
      },
      body: JSON.stringify({
        data: {
          attributes: {
            type: 'grab_pay',
            amount: convertToCentavos(amount),
            currency: 'PHP',
            redirect: {
              success: `${window.location.origin}/#/cart?payment=success&order=${orderId}`,
              failed: `${window.location.origin}/#/cart?payment=failed&order=${orderId}`
            },
            billing: {
              name: customerName,
              email: customerEmail
            },
            metadata: {
              order_id: orderId
            }
          }
        }
      })
    });

    if (!response.ok) {
      const error = await response.json();
      console.error('GrabPay API error response:', error);
      throw new Error(error.errors?.[0]?.detail || 'Failed to create GrabPay payment');
    }

    const data = await response.json();
    console.log('GrabPay payment source created:', data);
    return data;
  } catch (error) {
    console.error('GrabPay payment error:', error);
    throw error;
  }
};

/**
 * Retrieve payment source status
 * @param {string} sourceId - PayMongo source ID
 * @returns {Promise<Object>} PayMongo source object with current status
 */
export const getSourceStatus = async (sourceId) => {
  try {
    const response = await fetch(`${PAYMONGO_API_URL}/sources/${sourceId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': getAuthHeader()
      }
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.errors?.[0]?.detail || 'Failed to get source status');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Get source status error:', error);
    throw error;
  }
};

/**
 * Retrieve payment intent status
 * @param {string} paymentIntentId - PayMongo payment intent ID
 * @returns {Promise<Object>} PayMongo payment intent object with current status
 */
export const getPaymentIntentStatus = async (paymentIntentId) => {
  try {
    const response = await fetch(`${PAYMONGO_API_URL}/payment_intents/${paymentIntentId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': getAuthHeader()
      }
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.errors?.[0]?.detail || 'Failed to get payment intent status');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Get payment intent status error:', error);
    throw error;
  }
};

// Export all functions as a default object
export default {
  processGCashPayment,
  processPayMayaPayment,
  processCardPayment,
  processGrabPayPayment,
  getSourceStatus,
  getPaymentIntentStatus
};

// Named export for convenience
export const paymongoAPI = {
  processGCashPayment,
  processPayMayaPayment,
  processCardPayment,
  processGrabPayPayment,
  getSourceStatus,
  getPaymentIntentStatus
};


