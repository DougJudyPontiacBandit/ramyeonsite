<template>
  <div class="menu-page">
    <h1>Menu</h1>
    
    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <p>Loading menu...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
      <button @click="fetchData">Retry</button>
    </div>

    <!-- Menu Content -->
    <div v-else>
      <div class="categories">
        <button
          :class="{ active: selectedCategory === 'All' }"
          @click="selectCategory('All', null)"
        >
          All
        </button>
        <button
          v-for="category in categories"
          :key="category.id"
          :class="{ active: selectedCategory === category.id }"
          @click="selectCategory(category.id, category.name)"
        >
          {{ category.name }}
        </button>
      </div>

      <div v-if="loadingProducts" class="loading-products">
        <p>Loading products...</p>
      </div>

      <div v-else-if="products.length === 0" class="no-products">
        <p>No products available in this category.</p>
      </div>

      <div v-else class="products-grid">
        <div
          class="product-card"
          v-for="product in products"
          :key="product.id"
        >
          <img 
            :src="product.image || require('../assets/Home/BigRamen.png')" 
            :alt="product.name"
            @error="handleImageError"
          />
          <div class="product-info">
            <h3>{{ product.name }}</h3>
            <p>{{ product.description }}</p>
            <div class="price">₱{{ product.price.toFixed(2) }}</div>
          </div>
          <button class="add-btn" @click="addToCart(product)">+</button>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="pagination.total_pages > 1" class="pagination">
        <button 
          @click="goToPage(pagination.current_page - 1)" 
          :disabled="pagination.current_page === 1"
        >
          Previous
        </button>
        <span>Page {{ pagination.current_page }} of {{ pagination.total_pages }}</span>
        <button 
          @click="goToPage(pagination.current_page + 1)" 
          :disabled="pagination.current_page === pagination.total_pages"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import './Menu.css';
import { categoriesAPI } from '../services/apiCategories.js';
import { productsAPI } from '../services/apiProducts.js';

export default {
  name: "MenuPage",
  props: {
    onAddToCart: {
      type: Function,
      required: true,
    },
  },
  data() {
    return {
      categories: [],
      selectedCategory: 'All',
      selectedCategoryName: null,
      products: [],
      loading: true,
      loadingProducts: false,
      error: null,
      pagination: {
        current_page: 1,
        total_pages: 1,
        total_items: 0,
        items_per_page: 20
      }
    };
  },
  async mounted() {
    await this.fetchData();
  },
  methods: {
    async fetchData() {
      this.loading = true;
      this.error = null;
      
      try {
        // Fetch categories
        await this.fetchCategories();
        
        // Fetch all products initially
        await this.fetchProducts();
        
        this.loading = false;
      } catch (err) {
        console.error('Error fetching menu data:', err);
        this.error = err.message || 'Failed to load menu. Please try again.';
        this.loading = false;
      }
    },

    async fetchCategories() {
      try {
        const response = await categoriesAPI.getAll();
        
        if (response.success && response.data && response.data.categories) {
          this.categories = response.data.categories.map(cat => ({
            id: cat._id,
            name: cat.category_name,
            description: cat.description,
            productCount: cat.product_count,
            image: cat.image_url
          }));
        }
      } catch (err) {
        console.error('Error fetching categories:', err);
        throw new Error('Failed to load categories');
      }
    },

    async fetchProducts(page = 1) {
      this.loadingProducts = true;
      
      try {
        let response;
        
        if (this.selectedCategory === 'All') {
          // Fetch all products
          response = await productsAPI.getAll({
            page: page,
            limit: this.pagination.items_per_page
          });
        } else {
          // Fetch products by category
          response = await productsAPI.getByCategory(
            this.selectedCategory,
            null,
            page,
            this.pagination.items_per_page
          );
        }
        
        if (response.success && response.data) {
          // Map products to component format
          this.products = (response.data.products || []).map(product => ({
            id: product.product_id,
            name: product.product_name,
            price: parseFloat(product.selling_price),
            description: product.description || 'No description available',
            image: product.image_url,
            category: product.category_name,
            subcategory: product.subcategory_name,
            stock: product.stock_quantity
          }));

          // Update pagination
          if (response.data.pagination) {
            this.pagination = {
              current_page: response.data.pagination.current_page,
              total_pages: response.data.pagination.total_pages,
              total_items: response.data.pagination.total_items,
              items_per_page: response.data.pagination.items_per_page
            };
          }
        }
        
        this.loadingProducts = false;
      } catch (err) {
        console.error('Error fetching products:', err);
        this.products = [];
        this.loadingProducts = false;
      }
    },

    async selectCategory(categoryId, categoryName) {
      this.selectedCategory = categoryId;
      this.selectedCategoryName = categoryName;
      this.pagination.current_page = 1; // Reset to first page
      await this.fetchProducts(1);
    },

    async goToPage(page) {
      if (page >= 1 && page <= this.pagination.total_pages) {
        await this.fetchProducts(page);
        // Scroll to top of products
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    },

    addToCart(product) {
      this.onAddToCart(product);
    },

    handleImageError(event) {
      // Fallback image when product image fails to load
      event.target.src = require('../assets/Home/BigRamen.png');
    }
  },
};
</script>
