# TODO List

## Immediate Redirect on Add to Cart (Not Logged In)
- [x] Modify `src/App.vue`: Remove alert from `addToCart` method to redirect immediately to login page without showing permission dialog.

## Add Back to Home Button on Auth Pages
- [x] Modify `src/components/Login.vue`: Add "Back to Home" button that emits 'backToHome' event.
- [x] Modify `src/components/SignUp.vue`: Add "Back to Home" button that emits 'backToHome' event.
- [x] Modify `src/App.vue`: Handle 'backToHome' event from Login and SignUp components to navigate to Home page.

## Testing
- [x] Test adding item to cart without login redirects immediately to login page.
- [x] Test "Back to Home" button on login page navigates to home.
- [x] Test "Back to Home" button on signup page navigates to home.
