<template>
  <div class="cart-page">
    <div class="cart-container">
      <!-- Cart Header -->
      <div class="cart-header">
        <h1>Your Cart</h1>
        <p v-if="cartItems.length === 0">Your cart is empty</p>
        <p v-else>{{ cartItems.length }} item{{ cartItems.length > 1 ? 's' : '' }} in your cart</p>
      </div>

      <div class="cart-content" v-if="cartItems.length > 0">
        <!-- Cart Items -->
        <div class="cart-items">
          <div class="cart-item" v-for="item in cartItems" :key="item.id">
            <img :src="item.image" :alt="item.name" class="item-image" />
            <div class="item-details">
              <h3>{{ item.name }}</h3>
              <p class="item-description">{{ item.description }}</p>
              <div class="item-price">₱{{ item.price }}</div>
            </div>
            <div class="item-controls">
              <button class="quantity-btn" @click="decreaseQuantity(item.id)">-</button>
              <span class="quantity">{{ item.quantity }}</span>
              <button class="quantity-btn" @click="increaseQuantity(item.id)">+</button>
            </div>
            <div class="item-total">₱{{ (item.price * item.quantity).toFixed(2) }}</div>
            <button class="remove-btn" @click="removeItem(item.id)">×</button>
          </div>
        </div>

        <!-- Order Summary -->
        <div class="order-summary">
          <h2>Order Summary</h2>
          <div class="summary-row">
            <span>Subtotal</span>
            <span>₱{{ subtotal.toFixed(2) }}</span>
          </div>
          <div class="summary-row">
            <span>Delivery Fee</span>
            <span>₱{{ deliveryFee.toFixed(2) }}</span>
          </div>
          <div class="summary-row">
            <span>Service Fee</span>
            <span>₱{{ serviceFee.toFixed(2) }}</span>
          </div>
          <div class="summary-row total">
            <span>Total</span>
            <span>₱{{ total.toFixed(2) }}</span>
          </div>
        </div>

        <!-- Delivery Options -->
        <div class="delivery-options">
          <h2>Delivery Options</h2>
          <div class="option-group">
            <label class="option-label">
              <input type="radio" v-model="deliveryType" value="delivery" />
              <div class="option-content">
                <div class="option-icon">🚚</div>
                <div class="option-text">
                  <h3>Delivery</h3>
                  <p>Get it delivered to your doorstep</p>
                  <span class="option-time">30-45 mins</span>
                </div>
              </div>
            </label>
            <label class="option-label">
              <input type="radio" v-model="deliveryType" value="pickup" />
              <div class="option-content">
                <div class="option-icon">🏪</div>
                <div class="option-text">
                  <h3>Pickup</h3>
                  <p>Pick up from our store</p>
                  <span class="option-time">15-20 mins</span>
                </div>
              </div>
            </label>
          </div>
        </div>

        <!-- Delivery Address (only show if delivery is selected) -->
        <div class="delivery-address" v-if="deliveryType === 'delivery'">
          <h2>Delivery Address</h2>
          <div class="address-input">
            <input 
              type="text" 
              v-model="deliveryAddress" 
              placeholder="Enter your delivery address"
              class="address-field"
            />
            <button class="map-btn" @click="openMap">📍 Use Map</button>
          </div>
          
          <!-- Google Map -->
          <div class="map-container" v-if="showMap">
            <p class="map-instructions">📍 Click anywhere on the map to set your delivery location</p>
            <div id="google-map" class="google-map"></div>
            <button class="close-map-btn" @click="closeMap">Close Map</button>
          </div>
        </div>

        <!-- Payment Methods -->
        <div class="payment-methods">
          <h2>Payment Method</h2>
          <div class="payment-options">
            <label class="payment-option">
              <input type="radio" v-model="paymentMethod" value="cash" />
              <div class="payment-content">
                <div class="payment-icon">💵</div>
                <span>Cash on Delivery</span>
              </div>
            </label>
            <label class="payment-option">
              <input type="radio" v-model="paymentMethod" value="gcash" />
              <div class="payment-content">
                <div class="payment-icon">📱</div>
                <span>GCash</span>
              </div>
            </label>
            <label class="payment-option">
              <input type="radio" v-model="paymentMethod" value="card" />
              <div class="payment-content">
                <div class="payment-icon">💳</div>
                <span>Credit/Debit Card</span>
              </div>
            </label>
            <label class="payment-option">
              <input type="radio" v-model="paymentMethod" value="paymaya" />
              <div class="payment-content">
                <div class="payment-icon">🏦</div>
                <span>PayMaya</span>
              </div>
            </label>
          </div>
        </div>

        <!-- Special Instructions -->
        <div class="special-instructions">
          <h2>Special Instructions</h2>
          <textarea 
            v-model="specialInstructions" 
            placeholder="Any special requests or instructions for your order..."
            class="instructions-field"
          ></textarea>
        </div>

        <!-- Checkout Button -->
        <div class="checkout-section">
          <button class="checkout-btn" @click="proceedToCheckout" :disabled="!canCheckout">
            <span v-if="isProcessing" class="loading-spinner"></span>
            {{ isProcessing ? 'Processing...' : `Place Order - ₱${total.toFixed(2)}` }}
          </button>
        </div>
      </div>

      <!-- Empty Cart State -->
      <div class="empty-cart" v-else>
        <div class="empty-cart-icon">🛒</div>
        <h2>Your cart is empty</h2>
        <p>Add some delicious ramyeon to get started!</p>
        <button class="browse-menu-btn" @click="$emit('setCurrentPage', 'Menu')">
          Browse Menu
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Cart',
  emits: ['setCurrentPage'],
  data() {
    return {
      cartItems: [
        // Sample cart items for demonstration
        {
          id: 1,
          name: 'Shin Ramen',
          description: 'Made with Shin ramen, eggs, spring onions, oil and spices.',
          price: 150,
          quantity: 2,
          image: require('../assets/Home/BigRamen.png')
        },
        {
          id: 2,
          name: 'Tteok-bokki',
          description: 'Made with Korean rice cakes, fish cakes, dashi stock and gochujang.',
          price: 200,
          quantity: 1,
          image: require('../assets/Home/Invoice.png')
        }
      ],
      deliveryType: 'delivery',
      deliveryAddress: '',
      paymentMethod: 'cash',
      specialInstructions: '',
      showMap: false,
      isProcessing: false,
      map: null,
      marker: null
    }
  },
  computed: {
    subtotal() {
      return this.cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    },
    deliveryFee() {
      return this.deliveryType === 'delivery' ? 50 : 0;
    },
    serviceFee() {
      return this.subtotal * 0.05; // 5% service fee
    },
    total() {
      return this.subtotal + this.deliveryFee + this.serviceFee;
    },
    canCheckout() {
      const hasItems = this.cartItems.length > 0;
      const hasPayment = this.paymentMethod !== '';
      const hasAddress = this.deliveryType === 'pickup' || (this.deliveryType === 'delivery' && this.deliveryAddress.trim() !== '');
      return hasItems && hasPayment && hasAddress && !this.isProcessing;
    }
  },
  methods: {
    increaseQuantity(itemId) {
      const item = this.cartItems.find(item => item.id === itemId);
      if (item) {
        item.quantity++;
      }
    },
    decreaseQuantity(itemId) {
      const item = this.cartItems.find(item => item.id === itemId);
      if (item && item.quantity > 1) {
        item.quantity--;
      }
    },
    removeItem(itemId) {
      this.cartItems = this.cartItems.filter(item => item.id !== itemId);
    },
    async openMap() {
      this.showMap = true;
      
      // Load Google Maps script dynamically
      if (!window.google) {
        try {
          await this.loadGoogleMapsScript();
        } catch (error) {
          console.error('Failed to load Google Maps:', error);
          alert('Unable to load Google Maps. Please check:\n1. Internet connection\n2. API key is valid\n3. Billing is enabled in Google Cloud Console\n\nYou can manually enter your address instead.');
          this.closeMap();
          return;
        }
      }
      
      this.$nextTick(() => {
        this.initializeMap();
      });
    },
    loadGoogleMapsScript() {
      return new Promise((resolve, reject) => {
        if (window.google) {
          resolve();
          return;
        }

        const script = document.createElement('script');
        script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyAmv6-w1GHQ7Z4Y7c_iOlr17iw6Z6pnmC0&libraries=places&callback=initMap';
        script.async = true;
        script.defer = true;
        
        window.initMap = () => {
          resolve();
          delete window.initMap;
        };
        
        script.onerror = () => {
          reject(new Error('Failed to load Google Maps script'));
        };
        
        document.head.appendChild(script);
      });
    },
    closeMap() {
      this.showMap = false;
    },
    initializeMap() {
      const mapElement = document.getElementById('google-map');
      if (!mapElement || !window.google) {
        console.error('Google Maps not loaded or map element not found');
        alert('Unable to load Google Maps. Please check your internet connection and try again.');
        this.closeMap();
        return;
      }

      try {
        // Default center (Philippines - you can change this to your preferred location)
        const defaultCenter = { lat: 8.1837, lng: 126.3162 }; // Bislig City, Philippines
        
        // Initialize the map
        this.map = new window.google.maps.Map(mapElement, {
          center: defaultCenter,
          zoom: 13,
          mapTypeControl: true,
          streetViewControl: false,
          fullscreenControl: false,
          mapId: 'DEMO_MAP_ID' // Required for advanced features
        });

        // Try to get user's current location
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(
            (position) => {
              const userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
              };
              this.map.setCenter(userLocation);
              this.placeMarker(userLocation);
            },
            (error) => {
              console.log('Geolocation error:', error);
              // If geolocation fails, use default location
              this.placeMarker(defaultCenter);
            }
          );
        } else {
          // Browser doesn't support geolocation
          this.placeMarker(defaultCenter);
        }

        // Add click listener to map
        this.map.addListener('click', (event) => {
          this.placeMarker(event.latLng);
        });
      } catch (error) {
        console.error('Map initialization error:', error);
        
        // Check if it's a billing error
        if (error.message && error.message.includes('Billing')) {
          alert('⚠️ Google Maps API Error: Billing is not enabled.\n\nPlease enable billing for this API key in Google Cloud Console:\n1. Go to console.cloud.google.com\n2. Select your project\n3. Enable billing\n4. Enable Maps JavaScript API');
        } else {
          alert('Unable to initialize Google Maps. Error: ' + error.message);
        }
        this.closeMap();
      }
    },
    placeMarker(location) {
      // Remove existing marker if any
      if (this.marker) {
        this.marker.setMap(null);
      }

      // Create new marker
      this.marker = new window.google.maps.Marker({
        position: location,
        map: this.map,
        animation: window.google.maps.Animation.DROP,
        title: 'Delivery Location'
      });

      // Get address from coordinates using Geocoding
      this.getAddressFromCoordinates(location);
    },
    getAddressFromCoordinates(location) {
      const geocoder = new window.google.maps.Geocoder();
      const latLng = {
        lat: typeof location.lat === 'function' ? location.lat() : location.lat,
        lng: typeof location.lng === 'function' ? location.lng() : location.lng
      };

      geocoder.geocode({ location: latLng }, (results, status) => {
        if (status === 'OK' && results[0]) {
          this.deliveryAddress = results[0].formatted_address;
          
          // Optionally show an info window
          if (this.marker) {
            const infoWindow = new window.google.maps.InfoWindow({
              content: `<div style="padding: 10px;">
                <strong>Selected Location:</strong><br/>
                ${results[0].formatted_address}
              </div>`
            });
            infoWindow.open(this.map, this.marker);
          }
        } else {
          console.error('Geocoder failed:', status);
          alert('Unable to get address for this location. Please try another location.');
        }
      });
    },
    async proceedToCheckout() {
      if (!this.canCheckout) return;
      
      this.isProcessing = true;
      
      try {
        // Simulate order processing
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        const orderData = {
          id: 'ORDER-' + Date.now(),
          items: this.cartItems,
          deliveryType: this.deliveryType,
          deliveryAddress: this.deliveryAddress,
          paymentMethod: this.paymentMethod,
          specialInstructions: this.specialInstructions,
          subtotal: this.subtotal,
          deliveryFee: this.deliveryFee,
          serviceFee: this.serviceFee,
          total: this.total,
          orderTime: new Date().toISOString(),
          status: 'confirmed'
        };
        
        // Store order in localStorage (in real app, this would be sent to backend)
        const orders = JSON.parse(localStorage.getItem('ramyeon_orders') || '[]');
        orders.push(orderData);
        localStorage.setItem('ramyeon_orders', JSON.stringify(orders));
        
        // Clear cart
        this.cartItems = [];
        
        // Show success message
        alert(`Order placed successfully! Order ID: ${orderData.id}\n\nEstimated ${this.deliveryType === 'delivery' ? 'delivery' : 'pickup'} time: ${this.deliveryType === 'delivery' ? '30-45' : '15-20'} minutes.`);
        
        // Redirect to profile or orders page
        this.$emit('setCurrentPage', 'Profile');
        
      } catch (error) {
        console.error('Checkout error:', error);
        alert('There was an error processing your order. Please try again.');
      } finally {
        this.isProcessing = false;
      }
    }
  },
  mounted() {
    // Load cart items from localStorage if available
    const savedCart = localStorage.getItem('ramyeon_cart');
    if (savedCart) {
      try {
        this.cartItems = JSON.parse(savedCart);
      } catch (error) {
        console.error('Error loading cart:', error);
      }
    }
  },
  watch: {
    cartItems: {
      handler(newCart) {
        // Save cart to localStorage whenever it changes
        localStorage.setItem('ramyeon_cart', JSON.stringify(newCart));
      },
      deep: true
    }
  }
}
</script>

<style scoped>
.cart-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  padding: 20px;
  font-family: 'Poppins', sans-serif;
}

.cart-container {
  max-width: 1200px;
  margin: 0 auto;
}

.cart-header {
  text-align: center;
  margin-bottom: 30px;
}

.cart-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 10px;
  background: linear-gradient(135deg, #ff4757, #ff3742);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.cart-header p {
  color: #666;
  font-size: 1.1rem;
}

.cart-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
  align-items: start;
}

.cart-items {
  background: white;
  border-radius: 20px;
  padding: 25px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.cart-item {
  display: grid;
  grid-template-columns: 80px 1fr auto auto auto;
  gap: 15px;
  align-items: center;
  padding: 20px 0;
  border-bottom: 1px solid #eee;
}

.cart-item:last-child {
  border-bottom: none;
}

.item-image {
  width: 80px;
  height: 80px;
  border-radius: 15px;
  object-fit: cover;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.item-details h3 {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
}

.item-description {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 8px;
}

.item-price {
  font-weight: 600;
  color: #ff4757;
  font-size: 1.1rem;
}

.item-controls {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #f8f9fa;
  border-radius: 25px;
  padding: 5px;
}

.quantity-btn {
  width: 35px;
  height: 35px;
  border: none;
  border-radius: 50%;
  background: #ff4757;
  color: white;
  font-size: 1.2rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.quantity-btn:hover {
  background: #ff3742;
  transform: scale(1.1);
}

.quantity {
  font-weight: 600;
  font-size: 1.1rem;
  min-width: 30px;
  text-align: center;
}

.item-total {
  font-weight: 700;
  font-size: 1.2rem;
  color: #333;
}

.remove-btn {
  width: 30px;
  height: 30px;
  border: none;
  border-radius: 50%;
  background: #dc3545;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.remove-btn:hover {
  background: #c82333;
  transform: scale(1.1);
}

.order-summary {
  background: white;
  border-radius: 20px;
  padding: 25px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  position: sticky;
  top: 20px;
}

.order-summary h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  font-size: 1rem;
}

.summary-row.total {
  border-top: 2px solid #eee;
  padding-top: 15px;
  font-weight: 700;
  font-size: 1.2rem;
  color: #ff4757;
}

.delivery-options,
.payment-methods,
.special-instructions {
  background: white;
  border-radius: 20px;
  padding: 25px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.delivery-options h2,
.payment-methods h2,
.special-instructions h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
}

.option-group {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.option-label {
  display: block;
  cursor: pointer;
}

.option-content {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  border: 2px solid #eee;
  border-radius: 15px;
  transition: all 0.3s ease;
}

.option-label input[type="radio"]:checked + .option-content {
  border-color: #ff4757;
  background: rgba(255, 71, 87, 0.05);
}

.option-icon {
  font-size: 2rem;
}

.option-text h3 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
}

.option-text p {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 5px;
}

.option-time {
  color: #ff4757;
  font-weight: 600;
  font-size: 0.9rem;
}

.delivery-address {
  background: white;
  border-radius: 20px;
  padding: 25px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.delivery-address h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
}

.address-input {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.address-field {
  flex: 1;
  padding: 15px 20px;
  border: 2px solid #eee;
  border-radius: 15px;
  font-size: 1rem;
  font-family: 'Poppins', sans-serif;
  transition: all 0.3s ease;
}

.address-field:focus {
  outline: none;
  border-color: #ff4757;
  box-shadow: 0 0 0 3px rgba(255, 71, 87, 0.1);
}

.map-btn {
  padding: 15px 25px;
  background: #ff4757;
  color: white;
  border: none;
  border-radius: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.map-btn:hover {
  background: #ff3742;
  transform: translateY(-2px);
}

.map-container {
  position: relative;
}

.map-instructions {
  color: #666;
  font-size: 0.95rem;
  margin-bottom: 15px;
  padding: 10px 15px;
  background: #f8f9fa;
  border-radius: 10px;
  border-left: 3px solid #ff4757;
}

.google-map {
  height: 400px;
  width: 100%;
  border-radius: 15px;
  overflow: hidden;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.close-map-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: white;
  border: none;
  padding: 10px 15px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.payment-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.payment-option {
  display: block;
  cursor: pointer;
}

.payment-content {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  border: 2px solid #eee;
  border-radius: 15px;
  transition: all 0.3s ease;
}

.payment-option input[type="radio"]:checked + .payment-content {
  border-color: #ff4757;
  background: rgba(255, 71, 87, 0.05);
}

.payment-icon {
  font-size: 1.5rem;
}

.instructions-field {
  width: 100%;
  min-height: 100px;
  padding: 15px 20px;
  border: 2px solid #eee;
  border-radius: 15px;
  font-size: 1rem;
  font-family: 'Poppins', sans-serif;
  resize: vertical;
  transition: all 0.3s ease;
}

.instructions-field:focus {
  outline: none;
  border-color: #ff4757;
  box-shadow: 0 0 0 3px rgba(255, 71, 87, 0.1);
}

.checkout-section {
  background: white;
  border-radius: 20px;
  padding: 25px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.checkout-btn {
  width: 100%;
  padding: 20px;
  background: linear-gradient(135deg, #ff4757, #ff3742);
  color: white;
  border: none;
  border-radius: 15px;
  font-size: 1.2rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.checkout-btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 15px 35px rgba(255, 71, 87, 0.4);
}

.checkout-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.loading-spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 2px solid #ffffff;
  border-radius: 50%;
  border-top-color: transparent;
  animation: spin 1s ease-in-out infinite;
  margin-right: 10px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.empty-cart {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.empty-cart-icon {
  font-size: 4rem;
  margin-bottom: 20px;
  opacity: 0.5;
}

.empty-cart h2 {
  font-size: 2rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
}

.empty-cart p {
  color: #666;
  font-size: 1.1rem;
  margin-bottom: 30px;
}

.browse-menu-btn {
  padding: 15px 30px;
  background: linear-gradient(135deg, #ff4757, #ff3742);
  color: white;
  border: none;
  border-radius: 15px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.browse-menu-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(255, 71, 87, 0.3);
}

/* Responsive Design */
@media (max-width: 992px) {
  .cart-content {
    grid-template-columns: 1fr;
  }
  
  .order-summary {
    position: static;
  }
}

@media (max-width: 768px) {
  .cart-item {
    grid-template-columns: 60px 1fr;
    gap: 10px;
  }
  
  .item-image {
    width: 60px;
    height: 60px;
  }
  
  .item-controls,
  .item-total,
  .remove-btn {
    grid-column: 2;
    justify-self: end;
    margin-top: 10px;
  }
  
  .payment-options {
    grid-template-columns: 1fr;
  }
  
  .address-input {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .cart-page {
    padding: 10px;
  }
  
  .cart-header h1 {
    font-size: 2rem;
  }
  
  .cart-items,
  .order-summary,
  .delivery-options,
  .payment-methods,
  .special-instructions,
  .checkout-section {
    padding: 20px;
  }
}
</style>
