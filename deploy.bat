@echo off
REM Deploy Order History Fix to Production
REM Run this file to deploy your changes

echo ========================================
echo   Deploy Order History Fix
echo ========================================
echo.

echo Step 1: Adding files to git...
git add backend/app/kpi_views/online_transaction_views.py
git add backend/app/kpi_views/order_status_views.py  
git add backend/app/services/online_transactions_service.py
git add frontend/src/components/OrderHistory.vue
git add frontend/src/services/api.js

echo.
echo Step 2: Committing changes...
git commit -m "Fix: Add order history endpoint and real-time status updates - Deploy to production to fix 404 error"

echo.
echo Step 3: Pushing to repository...
git push origin TEST_BRANCH

echo.
echo ========================================
echo   Deployment Initiated!
echo ========================================
echo.
echo Your changes are now being deployed to:
echo https://pann-pos.onrender.com
echo.
echo Please wait 3-5 minutes for deployment to complete.
echo.
echo Then test by visiting your Order History page.
echo.
echo ========================================
pause

