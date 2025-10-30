# 📱 POS Order Status Quick Guide

## Quick Reference for Staff

---

## 🎯 Order Status Buttons

When you receive an online order, update its status using these buttons:

### 1️⃣ **Order Received** → Click: ✅ **Confirm Order**
```
Status: pending → confirmed
Tell customer: "Order confirmed! We're preparing it now."
```

### 2️⃣ **Start Gathering Items** → Click: 📦 **Start Preparing**
```
Status: confirmed → preparing
Tell customer: "We're gathering your items."
```

### 3️⃣ **Start Cooking** → Click: 👨‍🍳 **Start Cooking**
```
Status: preparing → cooking
Tell customer: "Your food is being prepared."
```

### 4️⃣ **Food Ready** → Click: ✨ **Mark Ready**
```
Status: cooking → ready
Tell customer: "Your order is ready!"
For pickup: Customer can come get it
For delivery: Driver can pick it up
```

### 5️⃣ **Driver Takes Order** → Click: 🚚 **Out for Delivery**
```
Status: ready → out_for_delivery
Tell customer: "Your order is on the way!"
Optional: Add driver name in notes
```

### 6️⃣ **Order Delivered** → Click: 📦 **Delivered**
```
Status: out_for_delivery → delivered
Tell customer: "Your order has been delivered!"
```

### 7️⃣ **Transaction Complete** → Click: 🎉 **Complete**
```
Status: delivered → completed
Order is finished!
```

---

## ⏱️ Typical Timeline

| Status | When | Time |
|--------|------|------|
| **Pending** | Order just placed | 0 min |
| ↓ | | |
| **Confirmed** | Staff accepts order | +2 min |
| ↓ | | |
| **Preparing** | Start gathering items | +3 min |
| ↓ | | |
| **Cooking** | Kitchen starts cooking | +5 min |
| ↓ | | |
| **Ready** | Food complete | +15 min |
| ↓ | | |
| **Out for Delivery** | Driver assigned | +18 min |
| ↓ | | |
| **Delivered** | Customer receives | +35 min |
| ↓ | | |
| **Completed** | Transaction closed | +36 min |

**Total Time:** ~35-40 minutes for delivery orders

---

## 🚨 Important Rules

### ✅ DO:
- Update status as soon as action happens
- Add notes for special situations
- Confirm order within 2-3 minutes
- Mark ready when food is actually ready
- Update to delivered when driver confirms

### ❌ DON'T:
- Skip status updates
- Mark ready before food is complete
- Mark delivered before actual delivery
- Leave orders in "pending" status
- Forget to update when driver leaves

---

## 📝 Adding Notes (Optional)

You can add notes when updating status:

**Good Examples:**
- "Chef John is preparing your order"
- "Extra spicy as requested"
- "Driver: Mike, ETA 15 minutes"
- "Packed with extra utensils"
- "Special instructions followed"

**When to Add Notes:**
- Special requests
- Delays
- Driver information
- Important customer messages

---

## 📱 Customer Experience

**What customers see:**

```
┌──────────────────────────────────┐
│  🕐 Order Pending                │
│  Your order is waiting...        │
│  ████░░░░░░░░░░░░░░ 10%         │
└──────────────────────────────────┘
        ↓ (You click confirm)
┌──────────────────────────────────┐
│  ✅ Order Confirmed              │
│  We're preparing your order!     │
│  ████████░░░░░░░░░░ 20%         │
└──────────────────────────────────┘
        ↓ (You click cooking)
┌──────────────────────────────────┐
│  👨‍🍳 Cooking                     │
│  Your food is being prepared     │
│  ████████████░░░░░░ 60%         │
└──────────────────────────────────┘
```

**Customers can see:**
- Current status with icon
- Progress percentage
- Estimated completion
- Full timeline of updates
- Any notes you add

**Auto-refresh:** Customer page updates every 30 seconds automatically!

---

## 🎓 Training Scenarios

### Scenario 1: Regular Delivery Order

```
1. Order appears on POS screen → Click "Confirm" immediately
2. Kitchen starts gathering ingredients → Click "Preparing"
3. Chef starts cooking → Click "Cooking"
4. Food is ready, packed in bag → Click "Ready"
5. Driver takes the order → Click "Out for Delivery"
   (Add note: "Driver: John")
6. Driver confirms delivery → Click "Delivered"
7. Close order → Click "Completed"
```

### Scenario 2: Pickup Order

```
1. Order appears → Click "Confirm"
2. Start preparing → Click "Preparing"
3. Start cooking → Click "Cooking"
4. Food is ready → Click "Ready"
5. Customer picks up → Click "Delivered"
   (Skip "Out for Delivery" for pickup)
6. Transaction complete → Click "Completed"
```

### Scenario 3: Delayed Order

```
1. Order confirmed → Click "Confirmed"
2. Start preparing → Click "Preparing"
3. Issue in kitchen (e.g., out of ingredient)
   → Add note: "Slight delay, substituting ingredient"
4. Cooking resumes → Click "Cooking"
   → Add note: "Back on track, preparing now"
5. Continue normally...
```

---

## 🔧 Troubleshooting

### Q: What if I click the wrong status?
**A:** Just click the correct status. The system keeps a history, but shows the latest status.

### Q: Can I go backwards (e.g., ready → cooking)?
**A:** Yes, but avoid it. If you must, click the correct status.

### Q: Order stuck in "pending" for 10 minutes?
**A:** Update it ASAP! Customer is waiting.

### Q: Driver can't find address?
**A:** Add note: "Driver calling customer" and keep status as "Out for Delivery"

### Q: Customer cancels order?
**A:** Use special "Cancel" button (if available) or contact supervisor.

### Q: Multiple orders at once?
**A:** Update each order as you work on it. Don't wait to do them all at once.

---

## 📊 Performance Goals

### Target Times:
- **Confirm order**: Within 2 minutes ⏱️
- **Start cooking**: Within 5 minutes 👨‍🍳
- **Mark ready**: Within 20 minutes ✨
- **Total delivery time**: 30-40 minutes 🚚

### Your Metrics:
Staff performance is tracked by:
- ✅ How quickly you confirm orders
- ✅ Accuracy of status updates
- ✅ Customer satisfaction
- ✅ On-time completion rate

---

## 💡 Pro Tips

1. **Confirm Immediately** - First impression matters
2. **Update Regularly** - Don't leave gaps
3. **Add Helpful Notes** - Customers appreciate communication
4. **Check Orders Often** - Don't miss updates
5. **Keep Customers Informed** - They're watching the status

---

## 📞 Need Help?

**Technical Issues:**
- Screen not loading → Refresh browser
- Can't update status → Check internet connection
- Button not working → Try again or contact IT

**Order Issues:**
- Contact supervisor
- Check order management system
- Review order details

---

## ✅ Daily Checklist

**Start of Shift:**
- [ ] Log into POS system
- [ ] Check pending orders
- [ ] Confirm any waiting orders

**During Shift:**
- [ ] Update status as orders progress
- [ ] Add notes for special situations
- [ ] Monitor order timeline
- [ ] Communicate with kitchen/drivers

**End of Shift:**
- [ ] Ensure all orders updated
- [ ] Complete any delivered orders
- [ ] Hand off pending orders to next shift

---

## 🎯 Remember

### The Golden Rule:
**Update status as soon as something happens!**

Customers are watching their orders in real-time. Quick, accurate updates = happy customers! 😊

---

**Questions?** Ask your supervisor or manager.

**Quick Access:** Bookmark this guide on your POS device!

---

## 📱 Visual Quick Reference

```
ORDER STATUS WORKFLOW - AT A GLANCE

     📱 Customer Orders
            ↓
     🕐 PENDING (Auto)
            ↓
    [You Click CONFIRM]
            ↓
     ✅ CONFIRMED
            ↓
   [You Click PREPARING]
            ↓
     📦 PREPARING
            ↓
   [You Click COOKING]
            ↓
     👨‍🍳 COOKING
            ↓
    [You Click READY]
            ↓
     ✨ READY
            ↓
  [Driver Takes Order]
            ↓
     🚚 OUT FOR DELIVERY
            ↓
  [Driver Confirms]
            ↓
     📦 DELIVERED
            ↓
   [You Click COMPLETE]
            ↓
     🎉 COMPLETED
```

---

**Print This Guide and Keep It Near Your POS Station!** 📌


