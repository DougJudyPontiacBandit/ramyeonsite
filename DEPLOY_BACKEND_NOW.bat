@echo off
REM Deploy Backend with Online Orders Endpoint to Production
REM This will deploy the missing /api/v1/online/orders/create/ endpoint

echo ========================================
echo   DEPLOY BACKEND TO PRODUCTION
echo ========================================
echo.
echo This will deploy the backend code with the online orders endpoint to Render.
echo.
echo Target: https://pann-pos.onrender.com
echo Branch: 11/8/2025
echo.
echo ========================================
pause

echo.
echo Step 1: Staging backend files...
git add backend/app/kpi_views/online_transaction_views.py
git add backend/app/kpi_views/order_status_views.py  
git add backend/app/services/online_transactions_service.py
git add backend/app/urls.py
git add ORDER_CREATION_FIX.md

echo.
echo Step 2: Staging frontend changes (for documentation)...
git add frontend/src/components/Cart.vue
git add frontend/src/services/api.js

echo.
echo Step 3: Committing changes...
git commit -m "Deploy: Add online orders create endpoint to fix 404 error

- Add /api/v1/online/orders/create/ endpoint
- Fix order creation for customer website
- Update Cart.vue with latest order flow
- Deploy to production: pann-pos.onrender.com"

echo.
echo Step 4: Pushing to origin...
git push origin 11/8/2025

echo.
echo ========================================
echo   DEPLOYMENT IN PROGRESS
echo ========================================
echo.
echo Your code is being pushed to GitHub/GitLab.
echo.
echo NEXT STEPS:
echo 1. Go to your Render dashboard: https://dashboard.render.com
echo 2. Find your backend service (pann-pos)
echo 3. Wait for automatic deployment to complete (3-5 minutes)
echo.
echo OR manually trigger deployment:
echo 4. Click "Manual Deploy" -> "Deploy latest commit"
echo.
echo Once deployed, test by placing an order on your website.
echo.
echo ========================================
echo.
pause

