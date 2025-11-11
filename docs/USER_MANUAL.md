# Ramyeon Corner Website — User Manual

Welcome to Ramyeon Corner’s online ordering site! This guide walks you through every major feature so you can browse the menu, order, and track your purchases with ease. No technical background is needed—just follow the simple steps below.

---

## 1. Getting Started

### Open the site
- Local testing: `http://localhost:8080`
- Production (once deployed): the Ramyeon Corner URL shared by your team.

You’ll see a welcoming home page with featured dishes, current promotions, and navigation links.

---

## 2. Creating an Account / Logging In

You need an account to place orders, view past orders, and earn loyalty points.

### Option A – Email & Password
1. Click **Login** (top-right) or **Create now** on the login panel.
2. For a new account, fill in your name, email, password, and accept the terms.
3. Press **Create Account**. You’ll be logged in automatically.

### Option B – Sign in with Google
1. On the login panel, click **Continue with Google**.
2. Choose your Google account and approve access.
3. You’ll be redirected back and signed in—no password required.

*Passwordless tip*: Google logins create a “Social” account in the system. You can always log in with Google again later—no password needed.

---

## 3. Navigating the Site

Use the top navigation bar to move around:

- **Home** – hero section, promotions, featured items.
- **Menu** – full list of dishes with categories, search, and “Add to Cart” buttons.
- **Promotions** – vouchers, flash sales, and special bundles.
- **Contact** – store location, business hours, and contact numbers.
- **Profile** – your personal dashboard (available when logged in).
- **Cart** – items ready for checkout.

The site is fully responsive—on tablets/phones you’ll see a mobile-friendly layout.

---

## 4. Browsing & Adding Items to Cart

1. Go to **Menu**.
2. Scroll through categories or use the search bar.
3. Click **Add to Cart** on any item.
4. View the cart anytime by clicking the cart icon or **Cart** in the navigation bar.

**Cart Page Summary**
- List of items, quantities, individual prices.
- Update or remove items.
- Apply vouchers (when available).
- See your subtotal, tax, and total.

---

## 5. Applying Promotions & Loyalty Points

Inside the cart:

- **Vouchers**: Click *Apply Promotion*, choose a code, and apply.
- **Points**: Enter how many loyalty points you’d like to redeem (if you have a balance). The site tells you how many points you currently have.

---

## 6. Checkout & Payment

1. Review your cart and press **Proceed to Checkout**.
2. Fill delivery information (address, contact number) or confirm pickup.
3. Select payment method:
   - **Cash** (pay on delivery/pickup)
   - **GCash** or **PayMaya** (redirects to the payment gateway)
4. Confirm your order. For online payments you’ll be taken to the provider to complete payment; afterward the site will return you to a status screen.

You’ll see a confirmation page with your order number. Keep this handy if you contact support.

---

## 7. Tracking Orders & History

- Open **Profile** → **Order History** to see your past purchases, totals, and statuses (Preparing, On the Way, Completed, etc.).
- From here you can view details, reorder items, or download receipts if enabled.

---

## 8. Profile Management

Inside **Profile** you can:

- View account details (name, email, loyalty points, verification status).
- Trigger **Send Code** if you need to verify your email manually (a modal walks you through it).
- Log out securely when you’re done.

---

## 9. Notifications & Status Messages

- Success and error messages appear as banners or pop-up toasts (e.g., “Added to cart,” “Payment failed,” etc.).
- OAuth errors (like invalid credentials) show a popup—follow the instructions or try again if prompted.

---

## 10. Helpful Tips

- **Remember Me**: On the login panel, tick “Remember me” so the site recalls your email next time.
- **Google Login Issues**: While the app is in testing mode, make sure your Google account is listed under authorized test users.
- **Passwords**: For social logins, password fields stay blank; you don’t need to set one unless you want to switch to email/password later.
- **Multiple Sessions**: You can sign in on multiple devices—your cart and history stick with your account.

---

## 11. Logging Out

Click **Profile → Sign Out** or the **Sign Out** link in the top bar. Confirm the dialog; access and refresh tokens plus the saved user session are cleared from the browser.

---

## 12. Getting Help

- **Support**: Use the details on the Contact page (email, phone).
- **Order Issues**: Provide your order number (shown in profile history and the confirmation screen).
- **Technical Errors**: Capture the on-screen message or popups; the team can diagnose quickly with that info.

---

Enjoy ordering from Ramyeon Corner! Whether you’re using a desktop, tablet, or phone, the site is designed to make browsing, buying, and tracking your favorite dishes fast and easy.
