<template>
  <div class="orders-page">
    <div class="orders-container">
      <h1>Your Orders</h1>

      <div v-if="loading" class="loading">Loading orders...</div>
      <div v-else-if="error" class="error">{{ error }}</div>

      <div v-else>
        <div v-if="orders.length === 0" class="empty-orders">
          <div class="empty-icon">📦</div>
          <h2>No orders yet</h2>
          <p>Browse our menu and place your first order.</p>
          <button class="browse-menu-btn" @click="$emit('setCurrentPage', 'Menu')">Browse Menu</button>
        </div>

        <div v-else class="orders-list">
          <div class="order-card" v-for="order in orders" :key="order.id || order.transactionId" @click="$emit('setCurrentPage', 'OrderDetails', order.id || order.transactionId)" style="cursor: pointer;">
            <div class="order-header">
              <div class="order-id">Order: {{ order.id || order.transactionId }}</div>
              <div class="order-date">{{ formatDate(order.orderTime || order.timestamp) }}</div>
            </div>
            <div class="order-body">
              <div class="order-items">
                <div class="order-item" v-for="item in order.items" :key="item.id">
                  <span class="item-name">{{ item.name }}</span>
                  <span class="item-qty">x{{ item.quantity }}</span>
                  <span class="item-price">₱{{ (item.price * item.quantity).toFixed(2) }}</span>
                </div>
              </div>
              <div class="order-total">Total: ₱{{ (order.total || calcTotal(order.items)).toFixed(2) }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Orders',
  emits: ['setCurrentPage'],
  data() {
    return {
      loading: false,
      error: '',
      orders: []
    }
  },
  methods: {
    formatDate(val) {
      try {
        const d = new Date(val)
        return d.toLocaleString()
      } catch (e) {
        return ''
      }
    },
    calcTotal(items) {
      if (!Array.isArray(items)) return 0
      return items.reduce((sum, i) => sum + (Number(i.price) * Number(i.quantity || 1)), 0)
    }
  },
  async mounted() {
    this.loading = true
    this.error = ''
    try {
      // Try backend invoices; fallback to local orders
      const { api } = await import('../api.js')
      try {
        // Prefer current user's invoices if available
        const resp = await api.sales.mine()
        const data = Array.isArray(resp.data) ? resp.data : (resp.data?.invoices || [])
        if (Array.isArray(data) && data.length) {
          this.orders = data.slice(0, 20).map((inv) => ({
            id: inv.invoice_id || inv.id,
            items: (inv.items || []).map(it => ({
              id: it.product_id || it.sku || it.id,
              name: it.product_name || it.name,
              price: it.price || it.unit_price || 0,
              quantity: it.quantity || 1
            })),
            total: inv.total_amount || inv.total || 0,
            orderTime: inv.created_at || inv.timestamp
          }))
        }
      } catch (e) {
        try {
          const resp2 = await api.sales.list()
          const data2 = Array.isArray(resp2.data) ? resp2.data : (resp2.data?.invoices || [])
          if (Array.isArray(data2) && data2.length) {
            this.orders = data2.slice(0, 20).map((inv) => ({
              id: inv.invoice_id || inv.id,
              items: (inv.items || []).map(it => ({
                id: it.product_id || it.sku || it.id,
                name: it.product_name || it.name,
                price: it.price || it.unit_price || 0,
                quantity: it.quantity || 1
              })),
              total: inv.total_amount || inv.total || 0,
              orderTime: inv.created_at || inv.timestamp
            }))
          }
        } catch (ignored) {
          // Ignore fallback API errors
        }
      }

      if (this.orders.length === 0) {
        const saved = localStorage.getItem('ramyeon_orders')
        if (saved) {
          try {
            this.orders = JSON.parse(saved)
          } catch (e) {
            this.orders = []
          }
        }
      }
    } catch (err) {
      this.error = 'Failed to load orders.'
    } finally {
      this.loading = false
    }
  }
}
</script>

<style scoped>
.orders-page { min-height: 60vh; padding: 20px; }
.orders-container { max-width: 900px; margin: 0 auto; font-family: 'Poppins', sans-serif; }
.loading, .error { padding: 12px; }
.empty-orders { text-align: center; padding: 40px 0; }
.empty-icon { font-size: 48px; margin-bottom: 10px; }
.browse-menu-btn { margin-top: 10px; padding: 10px 16px; border: none; border-radius: 8px; background: #ff4757; color: #fff; cursor: pointer; }
.orders-list { display: grid; gap: 16px; }
.order-card { background: #fff; border-radius: 14px; padding: 16px; box-shadow: 0 6px 18px rgba(0,0,0,0.08); }
.order-header { display: flex; justify-content: space-between; font-weight: 600; margin-bottom: 10px; }
.order-items { display: grid; gap: 6px; }
.order-item { display: grid; grid-template-columns: 1fr auto auto; gap: 8px; align-items: center; }
.order-total { text-align: right; margin-top: 10px; font-weight: 700; }
</style>

