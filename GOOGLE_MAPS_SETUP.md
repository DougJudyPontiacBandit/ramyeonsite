# Google Maps API Setup Guide

## Current Issue: Billing Not Enabled

The error you're seeing is because **Google Maps JavaScript API requires billing to be enabled** in Google Cloud Console, even if you stay within the free tier.

## 🔧 How to Fix the Billing Error

### Step 1: Go to Google Cloud Console
1. Visit: https://console.cloud.google.com
2. Sign in with your Google account

### Step 2: Select or Create a Project
1. Click on the project dropdown (top left)
2. Select the project associated with your API key
   - OR create a new project if needed

### Step 3: Enable Billing
1. Go to **Billing** in the left sidebar
2. Click **"Link a billing account"**
3. If you don't have a billing account:
   - Click **"Create billing account"**
   - Enter your payment information
   - **Note**: Google provides $200 free credit per month for Maps API
   - You likely won't be charged unless you exceed the free tier

### Step 4: Enable Required APIs
1. Go to **APIs & Services** > **Library**
2. Search for and enable these APIs:
   - ✅ **Maps JavaScript API**
   - ✅ **Geocoding API** (for address lookup)
   - ✅ **Places API** (optional, for place search)

### Step 5: Verify API Key Restrictions
1. Go to **APIs & Services** > **Credentials**
2. Click on your API key: `AIzaSyAmv6-w1GHQ7Z4Y7c_iOlr17iw6Z6pnmC0`
3. Under **API restrictions**:
   - Select **"Restrict key"**
   - Check: Maps JavaScript API, Geocoding API, Places API
4. Under **Application restrictions**:
   - Add your website domain (e.g., `localhost:8080`, `yourdomain.com`)

### Step 6: Wait & Test
1. Changes may take a few minutes to propagate
2. Refresh your website
3. Try the map feature again

---

## 💰 Pricing Information

### Free Tier (Monthly)
- **Maps JavaScript API**: $200 credit = ~28,000 map loads
- **Geocoding API**: $200 credit = ~40,000 requests
- Most small/medium websites stay within free tier

### Cost Per Request (after free tier)
- Map Load: $0.007 per load
- Geocoding: $0.005 per request

**You'll get alerts before being charged!**

---

## 🔑 Alternative: Get a New API Key

If you can't enable billing on the current key:

1. Go to: https://console.cloud.google.com/google/maps-apis/start
2. Create a new project
3. Enable billing (required)
4. Get new API key
5. Replace the key in: `frontend/src/components/Cart.vue`
   - Look for: `AIzaSyAmv6-w1GHQ7Z4Y7c_iOlr17iw6Z6pnmC0`
   - Replace with your new key

---

## 🛠️ Temporary Workaround (No Map)

If you can't enable billing right now, you can still use the cart by:

1. **Manually entering the address** in the text field
2. The map button will show an error, but address input still works
3. Users can type their full address without using the map

---

## ✅ Testing Checklist

After enabling billing:

- [ ] Refresh the page completely (Ctrl+Shift+R / Cmd+Shift+R)
- [ ] Open browser console (F12)
- [ ] Click "📍 Use Map" button
- [ ] Check for any error messages
- [ ] Click on the map to test pin placement
- [ ] Verify address appears in the input field

---

## 📞 Need Help?

**Google Maps Platform Support:**
- Documentation: https://developers.google.com/maps/documentation
- Support: https://developers.google.com/maps/support

**Common Errors:**
- `BillingNotEnabledMapError` → Enable billing (this guide)
- `ApiNotActivatedMapError` → Enable Maps JavaScript API
- `RefererNotAllowedMapError` → Add your domain to API restrictions
- `InvalidKeyMapError` → Check API key is correct

---

## 🔄 Updated Implementation

The cart now has:
- ✅ Async Google Maps loading (better performance)
- ✅ Error handling with helpful messages
- ✅ Fallback to manual address entry
- ✅ Geolocation support (asks for permission)
- ✅ Click-to-pin functionality
- ✅ Automatic address geocoding

**Location of code:** `frontend/src/components/Cart.vue`


