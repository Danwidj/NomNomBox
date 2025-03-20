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

        <!-- Price Range Dropdown -->
        <div class="filter-group">
          <label>Price Range:</label>
          <select v-model="priceFilter">
            <option value="">All Prices</option>
            <option value="lessThan5">Less than 5</option>
            <option value="5to10">5-10</option>
            <option value="10to15">10-15</option>
            <option value="15to20">15-20</option>
            <option value="above25">Above 20</option>
          </select>
        </div>

        <!-- Clear Filters Button -->
        <button @click="clearFilters" class="clear-filters">Clear Filters</button>
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
            <div class="product-image"><img :src="product.imageURL" :alt="product.name" class="product-image" /></div>
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
              <button class="view-details" @click="viewProductDetail(product)">View Details</button>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>

  <!-- Product Detail Modal -->
  <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal" @click.stop>
        <h2>{{ selectedProduct.name }}</h2>
        <p><strong>Price:</strong> ${{ selectedProduct.price.toFixed(2) }}</p>
        <p><strong>Ingredients:</strong></p>
        <ul>
          <li v-for="ingredient in selectedProduct.ingredients" :key="ingredient">{{ ingredient }}</li>
        </ul>
        <p><strong>Preparation:</strong> {{ selectedProduct.preparation }}</p>
        <button class="close-modal" @click="closeModal">Close</button>
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
      priceFilter: "",  // New drop-down filter for price range
      products: [], // Initially empty, filled from API
      loading: true,
      showModal: false, // Controls modal visibility
      selectedProduct: {} // Stores the product selected for detail view
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

      // Price Filter using the dropdown selection
      if (this.priceFilter) {
        if (this.priceFilter === "lessThan5")
          result = result.filter(product => product.price < 5);
        else if (this.priceFilter === "5to10")
          result = result.filter(product => product.price >= 5 && product.price <= 10);
        else if (this.priceFilter === "10to15")
          result = result.filter(product => product.price >= 10 && product.price <= 15);
        else if (this.priceFilter === "15to20")
          result = result.filter(product => product.price >= 15 && product.price <= 20);
        else if (this.priceFilter === "above25")
          result = result.filter(product => product.price > 20);
      }

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
        const response = await fetch("http://127.0.0.1:5006/inventory"); // Fetch from Inventory API
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
         // Check if the user is logged in (this is a simple example; adapt as needed)
    const user = sessionStorage.getItem("customerId");
    if (!user) {
      // If the user isn't logged in, redirect them to the login page.
      // Using Vue Router's push method.
      this.$router.push("/login");
      return; // Stop further execution
    }

      let cart = JSON.parse(sessionStorage.getItem("shoppingCart")) || [];
      let existingItem = cart.find(item => item.id === product.id);

      if (existingItem) {
        existingItem.quantity++;
      } else {
        cart.push({ ...product, quantity: 1 });
      }

      sessionStorage.setItem("shoppingCart", JSON.stringify(cart));
      alert(`${product.name} added to cart!`);
    },
    clearFilters() {
      this.selectedTags = [];
      this.priceFilter = "";
    },
    viewProductDetail(product) {
      this.selectedProduct = product;
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.selectedProduct = {};
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
  width: 300px;
  padding: 15px;
  border-radius: 8px;
  background: #f9f9f9;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}

.filter-group {
  margin-bottom: 15px;
}

.multi-select,
.filters select {
  width: 100%;
  padding: 6px;
  font-size: 0.9rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

/* Clear Filters Button Styling */
.clear-filters {
  padding: 8px 12px;
  font-size: 0.9rem;
  border: none;
  border-radius: 4px;
  background: #ccc ;
  cursor: pointer;
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

.product-image {
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  width: 100%;
  height: 180px; /* Adjust height to maintain uniformity */
  border-radius: 10px; /* Soft rounded corners */
  background-color: #f4f4f4; /* Neutral background for consistency */
}

.product-image img {
  max-width: 100%;
  max-height: 100%;
  object-fit: cover; /* Ensures the image fills the container without distortion */
  border-radius: 10px; /* Matches container's rounded corners */
  transition: transform 0.3s ease-in-out; /* Smooth hover effect */
}

.product-image img:hover {
  transform: scale(1.05); /* Slight zoom effect on hover */
}

/* Add to Cart Button */
.add-to-cart, .view-details {
  background: #ff9900;
  border: none;
  color: white;
  padding: 8px 14px;
  font-size: 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: 0.3s;
}

.add-to-cart:hover, .view-details:hover {
  background: #e68a00;
}

/* View Details Button Styling */
.view-details {
  background: #4caf50;
  margin-top: 10px;
}

.view-details:hover {
  background: #45a049;
}

/* Modal Overlay Styling */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7); /* Darker overlay for a stronger focus effect */
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Modal Styling */
.modal {
  background: white;
  padding: 20px;
  border-radius: 12px;
  width: 70%;
  max-width: 700px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2); /* Softer shadow for a cleaner look */
}

/* Modal Header */
.modal h2 {
  font-size: 1.5rem;
  margin-bottom: 15px;
}

/* Close Button Styling */
.close-modal {
  padding: 10px 16px;
  font-size: 1rem;
  background: #ffcc00;
  border-radius: 6px;
  color: white;
  border: none;
  cursor: pointer;
  transition: 0.3s;
  text-align: center;
}

.close-modal:hover {
  background: #e6b800;
}

button {
  padding: 8px 14px;
  font-size: 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: 0.3s;
  border: none;
}
</style>
