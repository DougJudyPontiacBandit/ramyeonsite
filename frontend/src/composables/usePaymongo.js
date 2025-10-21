/**
 * PayMongo API Composable
 * Handles payment processing for GCash, PayMaya, and Card payments
 */

// Get PayMongo API keys from environment variables
// Handle both Vue CLI (process.env) and Vite (import.meta.env) environments
const getEnvVar = (key, defaultValue = null) => {
  try {
    // Try Vue CLI environment first (process.env)
    if (typeof process !== 'undefined' && process.env && process.env[key]) {
      return process.env[key];
    }
    // Try Vite environment (import.meta.env)
    if (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env[key]) {
      return import.meta.env[key];
    }
    return defaultValue;
  } catch (error) {
    console.warn(`Could not access environment variable ${key}:`, error);
    return defaultValue;
  }
};

// Get environment variables dynamically
const getPayMongoKeys = () => {
  // Try multiple ways to get the keys
  const publicKey = getEnvVar('VUE_APP_PAYMONGO_PUBLIC_KEY') || 
                   getEnvVar('VITE_PAYMONGO_PUBLIC_KEY') ||
                   // Fallback to hardcoded values for testing (remove in production)
                   'pk_test_8NmDEEMt6wN5LSGSiTShjoSs';
                   
  const secretKey = getEnvVar('VUE_APP_PAYMONGO_SECRET_KEY') || 
                   getEnvVar('VITE_PAYMONGO_SECRET_KEY') ||
                   // Fallback to hardcoded values for testing (remove in production)
                   'sk_test_33DPJG17cScDA11mDi5RoHyu';
                   
  const mode = getEnvVar('VUE_APP_PAYMONGO_MODE') || 
              getEnvVar('VITE_PAYMONGO_MODE', 'test');
              
  return { publicKey, secretKey, mode };
};

// Get keys dynamically rather than at module load time
let PAYMONGO_PUBLIC_KEY, PAYMONGO_SECRET_KEY, PAYMONGO_MODE;

// Initialize keys and debug
const initKeys = () => {
  const keys = getPayMongoKeys();
  PAYMONGO_PUBLIC_KEY = keys.publicKey;
  PAYMONGO_SECRET_KEY = keys.secretKey;
  PAYMONGO_MODE = keys.mode;
  
  // Debug: Log environment variables (remove in production)
  console.log('PayMongo Config:', {
    hasProcessEnv: typeof process !== 'undefined' && !!process.env,
    hasImportMeta: typeof import.meta !== 'undefined' && !!import.meta.env,
    hasPublicKey: !!PAYMONGO_PUBLIC_KEY,
    hasSecretKey: !!PAYMONGO_SECRET_KEY,
    mode: PAYMONGO_MODE,
    publicKeyPreview: PAYMONGO_PUBLIC_KEY ? `${PAYMONGO_PUBLIC_KEY.substring(0, 10)}...` : 'undefined',
    processEnvKeys: typeof process !== 'undefined' && process.env ? Object.keys(process.env).filter(k => k.includes('PAYMONGO')) : 'no process.env',
    importMetaEnvKeys: typeof import.meta !== 'undefined' && import.meta.env ? Object.keys(import.meta.env).filter(k => k.includes('PAYMONGO')) : 'no import.meta.env',
    usingFallbackKeys: !getEnvVar('VUE_APP_PAYMONGO_SECRET_KEY') && !getEnvVar('VITE_PAYMONGO_SECRET_KEY')
  });
};

// Initialize keys
initKeys();

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
 * Get PayMongo secret key dynamically
 * @returns {string} PayMongo secret key
 */
const getSecretKey = () => {
  // Always get fresh keys dynamically
  const keys = getPayMongoKeys();
  const secretKey = keys.secretKey;
    
  if (!secretKey) {
    console.error('PayMongo secret key is undefined. Please check your .env file.');
    console.error('Process env keys:', typeof process !== 'undefined' && process.env ? Object.keys(process.env).filter(k => k.includes('PAYMONGO')) : 'no process.env');
    console.error('Import meta env keys:', typeof import.meta !== 'undefined' && import.meta.env ? Object.keys(import.meta.env).filter(k => k.includes('PAYMONGO')) : 'no import.meta.env');
    throw new Error('PayMongo secret key is not configured. Please check your environment variables.');
  }
  
  return secretKey;
};

/**
 * Create authorization header for PayMongo API
 * @returns {string} Base64 encoded authorization header
 */
const getAuthHeader = () => {
  const secretKey = getSecretKey();
  const encodedKey = btoa(secretKey + ':');
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
 * @returns {Promise<Object>} PayMongo payment link object with redirect URL
 */
export const processCardPayment = async ({ amount, orderId }) => {
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
