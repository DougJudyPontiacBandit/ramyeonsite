<template>
  <div class="menu-page">
    <h1>Menu</h1>
    <div class="categories">
      <button
        v-for="category in categories"
        :key="category"
        :class="{ active: selectedCategory === category }"
        @click="selectCategory(category)"
      >
        {{ category }}
      </button>
    </div>
    <div class="products-grid">
      <div
        class="product-card"
        v-for="product in filteredProducts"
        :key="product.id"
      >
        <img :src="product.image" :alt="product.name" />
        <div class="product-info">
          <h3>{{ product.name }}</h3>
          <p>{{ product.description }}</p>
          <div class="price">${{ product.price }}</div>
        </div>
        <button class="add-btn" @click="addToCart(product)">+</button>
      </div>
    </div>
  </div>
</template>

<script>
import '../components/Menu.css';
import { api } from '../api.js';

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
      categories: ["All"],
      selectedCategory: "All",
      products: [],
      loading: false,
      error: null
    };
  },
  computed: {
    filteredProducts() {
      if (this.selectedCategory === "All") {
        return this.products;
      }
      return this.products.filter(
        (product) => product.category === this.selectedCategory
      );
    },
  },
  async mounted() {
    await this.loadCategories();
    await this.loadProducts();
  },
  methods: {
    async loadCategories() {
      try {
        const response = await api.categories.list();
        const backendCategories = response.data.map(cat => cat.name);
        this.categories = ["All", ...backendCategories];
      } catch (error) {
        console.error('Error loading categories:', error);
        // Fallback to default categories
        this.categories = ["All", "Noodles", "Rice Cake", "Side Dish", "Drinks"];
      }
    },

    async loadProducts() {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.products.list();
        // Transform backend products to frontend format
        this.products = response.data.map(product => ({
          id: product.id,
          name: product.name,
          category: product.category_name || product.category,
          price: product.price,
          description: product.description,
          image: product.image_url || this.getDefaultImage(product.category)
        }));
      } catch (error) {
        console.error('Error loading products:', error);
        this.error = 'Failed to load products. Please try again.';
        // Fallback to local products
        this.loadFallbackProducts();
      } finally {
        this.loading = false;
      }
    },

    getDefaultImage(category) {
      const imageMap = {
        'Noodles': require("../assets/Home/BigRamen.png"),
        'Rice Cake': require("../assets/Home/Invoice.png"),
        'Side Dish': require("../assets/Home/Pick up.png"),
        'Drinks': require("../assets/Home/Clock.png")
      };
      return imageMap[category] || require("../assets/Home/BigRamen.png");
    },

    loadFallbackProducts() {
      this.products = [
        {
          id: 1,
          name: "Shin Ramen",
          category: "Noodles",
          price: 150,
          description: "Made with Shin ramen, eggs, spring onions, oil and spices.",
          image: require("../assets/Home/BigRamen.png"),
        },
        {
          id: 2,
          name: "Neo Guri",
          category: "Noodles",
          price: 130,
          description: "Made with Neo guri, seaweed, and spices.",
          image: require("../assets/Home/bell.png"),
        },
        {
          id: 3,
          name: "Jin Ramen",
          category: "Noodles",
          price: 185,
          description: "Made with Jin ramen, egg yolk, mushroom, and other spices.",
          image: require("../assets/Home/Bigpin.png"),
        },
        {
          id: 4,
          name: "Ice Talk Drink",
          category: "Drinks",
          price: 55,
          description: "Can choose from coffee, kiwi, grapes, peach, blue lemonade and more.",
          image: require("../assets/Home/Clock.png"),
        },
        {
          id: 5,
          name: "Buldak",
          category: "Noodles",
          price: 130,
          description: "Made with Buldak, cheese, and spring onions.",
          image: require("../assets/Home/donut.png"),
        },
        {
          id: 6,
          name: "Tteok-bokki",
          category: "Rice Cake",
          price: 200,
          description: "Made with Korean rice cakes, fish cakes, dashi stock and gochujang.",
          image: require("../assets/Home/Invoice.png"),
        },
        {
          id: 7,
          name: "Fish cake",
          category: "Side Dish",
          price: 55,
          description: "Made with ground fish, starch, eggs, breadcrumbs, and seasonings.",
          image: require("../assets/Home/Pick up.png"),
        },
        {
          id: 8,
          name: "Corn Dog",
          category: "Side Dish",
          price: 120,
          description: "Made with dough, sausage, potato crust, salt, and sugar.",
          image: require("../assets/Home/Pick up 1.png"),
        },
      ];
    },

    selectCategory(category) {
      this.selectedCategory = category;
    },

    addToCart(product) {
      this.onAddToCart(product);
    },
  },
};
</script>
