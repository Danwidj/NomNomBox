<template>
  <div class="product-page">
    <div class="page-layout">
      <!-- Left Sidebar: Filters -->
      <aside class="filters">
        <h2>Filters</h2>
        <div class="filter-group">
          <label for="category">Category:</label>
          <select id="category" v-model="selectedCategory">
            <option value="">All Categories</option>
            <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
          </select>
        </div>
        <div class="filter-group">
          <label>Price Range:</label>
          <div class="price-range">
            <input v-model.number="minPrice" type="number" placeholder="Min" />
            <input v-model.number="maxPrice" type="number" placeholder="Max" />
          </div>
        </div>
        <div class="filter-group">
          <label for="rating">Rating:</label>
          <select id="rating" v-model.number="minRating">
            <option value="0">All</option>
            <option value="1">1+ Stars</option>
            <option value="2">2+ Stars</option>
            <option value="3">3+ Stars</option>
            <option value="4">4+ Stars</option>
          </select>
        </div>
        <button @click="resetFilters">Reset Filters</button>
      </aside>

      <!-- Right Content: Search/Sort and Products Grid -->
      <main class="content">
        <div class="top-bar">
          <div class="search-sort">
            <input v-model="searchTerm" type="text" placeholder="Search products..." />
            <select v-model="sortOption">
              <option value="default">Sort by</option>
              <option value="priceLowToHigh">Price: Low to High</option>
              <option value="priceHighToLow">Price: High to Low</option>
            </select>
          </div>
        </div>
        <div class="grid-container">
          <div v-for="product in filteredProducts" :key="product.id" class="product-card">
            <img :src="product.image" :alt="product.name" class="product-image" />
            <div class="product-info">
              <h3 class="product-title">{{ product.name }}</h3>
              <p class="product-description">{{ product.description }}</p>
              <div class="product-rating">
                <span
                  v-for="n in 5"
                  :key="n"
                  class="star"
                  :class="{ filled: n <= product.rating }"
                >★</span>
              </div>
              <p class="product-price">$ {{ product.price.toFixed(2) }}</p>
              <button class="add-to-cart">Add to Cart</button>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProductPage',
  data() {
    return {
      searchTerm: '',
      sortOption: 'default',
      selectedCategory: '',
      minPrice: null,
      maxPrice: null,
      minRating: 0,
      products: [
        { id: 1, name: 'Italian Pasta Kit', description: 'Enjoy authentic Italian flavors with our pasta kit.', price: 25.0, rating: 4, category: 'Italian', image: 'pasta.jpg' },
        { id: 2, name: 'Mexican Taco Kit', description: 'Spice up your dinner with our taco kit.', price: 20.0, rating: 5, category: 'Mexican', image: 'taco.jpg' },
        { id: 3, name: 'Sushi Making Kit', description: 'Everything you need for a sushi night at home.', price: 30.0, rating: 4, category: 'Japanese', image: 'sushi.jpg' },
        { id: 4, name: 'Indian Curry Kit', description: 'A complete kit to create rich, flavorful curries.', price: 28.0, rating: 4, category: 'Indian', image: 'curry.jpg' },
        { id: 5, name: 'Mediterranean Mezze Kit', description: 'Enjoy a variety of dips and appetizers Mediterranean style.', price: 32.0, rating: 5, category: 'Mediterranean', image: 'mezze.jpg' },
        { id: 6, name: 'BBQ Grill Kit', description: 'All the essentials for a perfect BBQ experience.', price: 35.0, rating: 3, category: 'American', image: 'bbq.jpg' },
        { id: 7, name: 'Vegan Delight Kit', description: 'Delicious and healthy vegan meal kit options.', price: 22.0, rating: 4, category: 'Vegan', image: 'vegan.jpg' },
        { id: 8, name: 'French Bistro Kit', description: 'Create classic French bistro dishes in your own kitchen.', price: 40.0, rating: 5, category: 'French', image: 'french.jpg' },
        { id: 9, name: 'Thai Curry Kit', description: 'Experience the bold flavors of Thai cuisine with this kit.', price: 27.0, rating: 4, category: 'Thai', image: 'thai.jpg' },
        { id: 10, name: 'Healthy Salad Kit', description: 'Fresh ingredients for a nutritious and tasty salad.', price: 18.0, rating: 3, category: 'Healthy', image: 'salad.jpg' }
      ]
    };
  },
  computed: {
    categories() {
      return [...new Set(this.products.map(product => product.category))];
    },
    filteredProducts() {
      let result = this.products;
      if (this.searchTerm.trim() !== '')
        result = result.filter(product => product.name.toLowerCase().includes(this.searchTerm.toLowerCase()));
      if (this.selectedCategory)
        result = result.filter(product => product.category === this.selectedCategory);
      if (this.minPrice !== null && this.minPrice !== '')
        result = result.filter(product => product.price >= this.minPrice);
      if (this.maxPrice !== null && this.maxPrice !== '')
        result = result.filter(product => product.price <= this.maxPrice);
      if (this.minRating > 0)
        result = result.filter(product => product.rating >= this.minRating);
      if (this.sortOption === 'priceLowToHigh')
        result = result.slice().sort((a, b) => a.price - b.price);
      else if (this.sortOption === 'priceHighToLow')
        result = result.slice().sort((a, b) => b.price - a.price);
      return result;
    }
  },
  methods: {
    resetFilters() {
      this.selectedCategory = '';
      this.minPrice = null;
      this.maxPrice = null;
      this.minRating = 0;
      this.searchTerm = '';
      this.sortOption = 'default';
    }
  }
};
</script>

<style scoped>
.product-page {
  font-family: Arial, sans-serif;
  max-width: 1200px;
  margin: 0 auto;
  padding: 10px;
}
.page-layout {
  display: flex;
  gap: 10px;
}
/* Left Sidebar fixed to 150px with smaller padding */
.filters {
  width: 150px;
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 4px;
  height: fit-content;
}
.filters h2 {
  margin-top: 0;
  font-size: 1.1rem;
}
.filter-group {
  margin-bottom: 10px;
  display: flex;
  flex-direction: column;
}
.filter-group label {
  margin-bottom: 4px;
  font-weight: bold;
  font-size: 0.9rem;
}
.filter-group input,
.filter-group select {
  width: 100%;
  padding: 4px;
  font-size: 0.9rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.price-range {
  display: flex;
  flex-direction: column;
  gap: 4px;
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
  margin-bottom: 10px;
}
.search-sort {
  display: flex;
  gap: 6px;
  align-items: center;
}
.search-sort input,
.search-sort select {
  padding: 6px;
  font-size: 0.9rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
/* Products Grid: 4 per row with smaller gap */
.grid-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}
.product-card {
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 10px;
  background: #fff;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: box-shadow 0.3s ease;
}
.product-card:hover {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.product-image {
  width: 100%;
  height: auto;
  border-bottom: 1px solid #eee;
  margin-bottom: 5px;
}
.product-info {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}
.product-title {
  font-size: 1rem;
  margin: 5px 0;
}
.product-description {
  font-size: 0.8rem;
  color: #555;
  flex-grow: 1;
}
.product-rating {
  margin: 5px 0;
}
.star {
  color: #ccc;
  font-size: 0.8rem;
}
.star.filled {
  color: #f5a623;
}
.product-price {
  font-size: 1rem;
  font-weight: bold;
  margin-bottom: 5px;
}
.add-to-cart {
  background-color: #ff9900;
  border: none;
  color: #fff;
  padding: 6px;
  font-size: 0.9rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.add-to-cart:hover {
  background-color: #e68a00;
}
</style>
