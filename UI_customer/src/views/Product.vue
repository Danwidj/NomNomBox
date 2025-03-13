<template>
  <div class="product-page">
    <div class="page-layout">
      <!-- Left Sidebar: Filters -->
      <aside class="filters">
        <h2>Filters</h2>

        <!-- Dietary Tags Multi-Select Dropdown -->
        <div class="filter-group">
          <label>Dietary Tags:</label>
          <select multiple v-model="selectedTags" class="multi-select">
            <option v-for="tag in uniqueDietaryTags" :key="tag" :value="tag">
              {{ tag }}
            </option>
          </select>
        </div>

        <div class="filter-group">
          <label>Price Range:</label>
          <div class="price-range">
            <input v-model.number="minPrice" type="number" placeholder="Min Price" />
            <input v-model.number="maxPrice" type="number" placeholder="Max Price" />
          </div>
        </div>
      </aside>

      <!-- Right Content: Search/Sort and Products Grid -->
      <main class="content">
        <div class="top-bar">
          <div class="search-sort">
            <input v-model="searchTerm" type="text" placeholder="Search meal kits..." />
            <select v-model="sortOption">
              <option value="default">Sort by</option>
              <option value="priceLowToHigh">Price: Low to High</option>
              <option value="priceHighToLow">Price: High to Low</option>
            </select>
          </div>
        </div>

        <div v-if="loading" class="loading">Loading products...</div>
        <div v-else-if="filteredProducts.length === 0" class="no-results">
          No products match your filters.
        </div>
        <div v-else class="grid-container">
          <div v-for="product in filteredProducts" :key="product.id" class="product-card">
            <img :src="product.imageURL" :alt="product.name" class="product-image" />
            <div class="product-info">
              <h3 class="product-title">{{ product.name }}</h3>
              <p class="product-description">{{ product.description }}</p>

              <!-- Dietary Tags Display -->
              <div class="dietary-tags-container">
                <span v-for="tag in product.dietaryTags" :key="tag" class="dietary-tag">
                  {{ tag }}
                </span>
              </div>

              <p class="product-price">$ {{ product.price.toFixed(2) }}</p>
              <button class="add-to-cart" @click="addToCart(product)">Add to Cart</button>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProductPage",
  data() {
    return {
      searchTerm: "",
      sortOption: "default",
      selectedTags: [], // Stores selected dietary tags
      minPrice: null,
      maxPrice: null,
      products: [], // Initially empty, filled from API
      loading: true
    };
  },
  computed: {
    uniqueDietaryTags() {
      // Get all unique dietary tags from all products
      const allTags = this.products.flatMap(product => product.dietaryTags || []);
      return [...new Set(allTags)];
    },
    filteredProducts() {
      let result = this.products;

      // Search Filter
      if (this.searchTerm.trim() !== "")
        result = result.filter(product =>
          product.name.toLowerCase().includes(this.searchTerm.toLowerCase())
        );

      // Price Filter
      if (this.minPrice !== null && this.minPrice !== "")
        result = result.filter(product => product.price >= this.minPrice);
      if (this.maxPrice !== null && this.maxPrice !== "")
        result = result.filter(product => product.price <= this.maxPrice);

      // Dietary Tags Filter (show if product has at least one selected tag)
      if (this.selectedTags.length > 0) {
        result = result.filter(product =>
          product.dietaryTags.some(tag => this.selectedTags.includes(tag))
        );
      }

      // Sorting
      if (this.sortOption === "priceLowToHigh")
        result = result.slice().sort((a, b) => a.price - b.price);
      else if (this.sortOption === "priceHighToLow")
        result = result.slice().sort((a, b) => b.price - a.price);

      return result;
    }
  },
  created() {
    this.fetchProducts();
  },
  methods: {
    async fetchProducts() {
      try {
        const response = await fetch("http://127.0.0.1:5002/inventory"); // Fetch from Inventory API
        const data = await response.json();
        if (data.code === 200) {
          this.products = data.data; // Populate products from API response
        } else {
          console.error("No products available");
        }
      } catch (error) {
        console.error("Error fetching inventory:", error);
      } finally {
        this.loading = false;
      }
    },
    addToCart(product) {
      let cart = JSON.parse(sessionStorage.getItem("shoppingCart")) || [];
      let existingItem = cart.find(item => item.id === product.id);

      if (existingItem) {
        existingItem.quantity++;
      } else {
        cart.push({ ...product, quantity: 1 });
      }

      sessionStorage.setItem("shoppingCart", JSON.stringify(cart));
      alert(`${product.name} added to cart!`);
    }
  }
};
</script>

<style scoped>
/* General Page Styling */
.product-page {
  font-family: Arial, sans-serif;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
.page-layout {
  display: flex;
  gap: 15px;
}

/* Filters Sidebar */
.filters {
  width: 200px;
  padding: 15px;
  border-radius: 8px;
  background: #f9f9f9;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}

.filter-group {
  margin-bottom: 15px;
}

.multi-select {
  width: 100%;
  padding: 6px;
  font-size: 0.9rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

/* Dietary Tags inside Product Card */
.dietary-tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-top: 5px;
}

.dietary-tag {
  background: #ffcc80;
  color: #333;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.8rem;
}

/* Right Content */
.content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.top-bar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 15px;
}

.search-sort {
  display: flex;
  gap: 10px;
  align-items: center;
}

.search-sort input,
.search-sort select {
  padding: 8px;
  font-size: 0.9rem;
  border-radius: 4px;
  border: 1px solid #ccc;
}

/* Product Grid */
.grid-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
}

/* Product Card */
.product-card {
  border-radius: 8px;
  padding: 15px;
  background: white;
  transition: 0.3s;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.product-card:hover {
  transform: scale(1.03);
  box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.15);
}

/* Add to Cart Button */
.add-to-cart {
  background: #ff9900;
  border: none;
  color: white;
  padding: 8px 14px;
  font-size: 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: 0.3s;
}

.add-to-cart:hover {
  background: #e68a00;
}
</style>
