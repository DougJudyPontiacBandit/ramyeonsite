// Clear Cart Data - Run this in browser console (F12)
console.log('🧹 Clearing all Ramyeon cart data...');

// Clear all cart-related localStorage
localStorage.removeItem('ramyeon_cart');
localStorage.removeItem('ramyeon_pending_order');
localStorage.removeItem('ramyeon_payment_history');
localStorage.removeItem('ramyeon_orders');
localStorage.removeItem('ramyeon_force_clear_cart');

// Clear user-specific orders
const keys = Object.keys(localStorage);
let clearedKeys = [];
keys.forEach(key => {
  if (key.startsWith('ramyeon_orders_')) {
    localStorage.removeItem(key);
    clearedKeys.push(key);
  }
});

console.log('✅ Cleared localStorage keys:');
console.log('  - ramyeon_cart');
console.log('  - ramyeon_pending_order');
console.log('  - ramyeon_payment_history');
console.log('  - ramyeon_orders');
console.log('  - ramyeon_force_clear_cart');
if (clearedKeys.length > 0) {
  console.log('  - User orders:', clearedKeys);
}

// Check what's left
const remainingKeys = Object.keys(localStorage).filter(key => key.startsWith('ramyeon_'));
if (remainingKeys.length > 0) {
  console.log('⚠️ Remaining ramyeon keys:', remainingKeys);
} else {
  console.log('✅ All ramyeon data cleared!');
}

console.log('🔄 Refresh the page to see the empty cart');



