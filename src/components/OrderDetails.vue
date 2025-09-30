<template>
  <div class="order-details-page">
    <div class="container">
      <button class="back-btn" @click="$emit('setCurrentPage', 'Orders')">← Back to Orders</button>
      <h1>Order Details</h1>
      <div v-if="loading" class="loading">Loading...</div>
      <div v-else-if="error" class="error">{{ error }}</div>

      <div v-else-if="order" class="order-card">
        <div class="row header">
          <div>Order: {{ orderId }}</div>
          <div>{{ formatDate(order.transaction_date || order.orderTime) }}</div>
        </div>
        <div class="row">
          <div class="label">Status</div>
          <div class="value">{{ order.status || 'completed' }}</div>
        </div>
        <div class="row">
          <div class="label">Payment</div>
          <div class="value">{{ order.payment_method || 'cash' }}</div>
        </div>
        <div class="row" v-if="order.delivery">
          <div class="label">Delivery</div>
          <div class="value">{{ order.delivery.delivery_type }} • {{ order.delivery.delivery_address }}</div>
        </div>
        <div class="items">
          <div class="item" v-for="it in items" :key="it.id">
            <div class="name">{{ it.name }}</div>
            <div class="qty">x{{ it.quantity }}</div>
            <div class="price">₱{{ (it.price * it.quantity).toFixed(2) }}</div>
          </div>
        </div>
        <div class="totals">
          <div>Subtotal</div>
          <div>₱{{ subtotal.toFixed(2) }}</div>
        </div>
        <div class="totals grand">
          <div>Total</div>
          <div>₱{{ (order.total_amount || subtotal).toFixed(2) }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OrderDetails',
  props: {
    orderId: { type: [String, Number], required: true }
  },
  emits: ['setCurrentPage'],
  data() {
    return { loading: false, error: '', order: null }
  },
  computed: {
    items() {
      const inv = this.order || {}
      const rawItems = inv.items || inv.item_list || []
      if (Array.isArray(rawItems)) {
        return rawItems.map(it => ({
          id: it.product_id || it.sku || it.id,
          name: it.product_name || it.item_name || it.name,
          price: it.price || it.unit_price || 0,
          quantity: it.quantity || 1
        }))
      }
      return []
    },
    subtotal() {
      return this.items.reduce((s, i) => s + (Number(i.price) * Number(i.quantity)), 0)
    }
  },
  methods: {
    formatDate(v) { 
      try { 
        return new Date(v).toLocaleString() 
      } catch { 
        return '' 
      } 
    }
  },
  async mounted() {
    this.loading = true
    this.error = ''
    try {
      const { api } = await import('../api.js')
      const resp = await api.sales.get(this.orderId)
      this.order = resp.data?.invoice || resp.data || null
      if (!this.order) this.error = 'Order not found.'
    } catch (e) {
      this.error = 'Failed to load order.'
    } finally {
      this.loading = false
    }
  }
}
</script>

<style scoped>
.order-details-page { 
  min-height: 60vh; 
  padding: 20px; 
}
.container { 
  max-width: 800px; 
  margin: 0 auto; 
  font-family: 'Poppins', sans-serif; 
}
.back-btn { 
  margin-bottom: 10px; 
  border: none; 
  background: transparent; 
  cursor: pointer; 
  color: #ff4757; 
  font-weight: 600; 
}
.order-card { 
  background: #fff; 
  border-radius: 14px; 
  padding: 16px; 
  box-shadow: 0 6px 18px rgba(0,0,0,0.08); 
}
.row { 
  display: flex; 
  justify-content: space-between; 
  padding: 6px 0; 
}
.row.header { 
  font-weight: 700; 
  border-bottom: 1px solid #eee; 
  margin-bottom: 8px; 
}
.label { 
  color: #666; 
}
.items { 
  margin-top: 10px; 
  border-top: 1px dashed #eee; 
  padding-top: 10px; 
  display: grid; 
  gap: 6px; 
}
.item { 
  display: grid; 
  grid-template-columns: 1fr auto auto; 
  gap: 8px; 
  align-items: center; 
}
.totals { 
  display: flex; 
  justify-content: space-between; 
  padding-top: 10px; 
}
.totals.grand { 
  font-weight: 800; 
  font-size: 1.1rem; 
}
.loading, .error { 
  padding: 12px; 
}
</style>