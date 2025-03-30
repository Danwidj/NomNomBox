<template>
  <div class="nom-container py-8 nom-fade-in">
    <div class="flex flex-col lg:flex-row gap-6">
      <!-- Left Sidebar: Enhanced Filters -->
      <aside class="w-full lg:w-64 shrink-0">
        <div class="nom-card sticky top-24">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-xl font-semibold">Filters</h2>
            <button 
              @click="clearFilters" 
              class="text-sm text-primary hover:underline font-medium"
            >
              Reset
            </button>
          </div>

          <!-- Enhanced Dietary Tags Multi-Select -->
          <div class="mb-6">
            <label class="nom-label">Dietary Tags:</label>
            <div class="bg-background border border-input rounded-md p-2">
              <div v-if="selectedTags.length > 0" class="flex flex-wrap gap-2 mb-2">
                <span 
                  v-for="tag in selectedTags" 
                  :key="tag"
                  class="nom-badge-primary flex items-center"
                >
                  {{ tag }}
                  <button 
                    @click="removeTag(tag)" 
                    class="ml-1 hover:text-primary/70"
                  >×</button>
                </span>
              </div>
              <select 
                multiple 
                v-model="selectedTags" 
                class="w-full border-0 bg-transparent p-1 focus:ring-0 text-sm focus:outline-none"
              >
                <option v-for="tag in uniqueDietaryTags" :key="tag" :value="tag">
                  {{ tag }}
                </option>
              </select>
            </div>
          </div>

          <!-- Enhanced Price Range with Slider -->
          <div class="mb-6">
            <div class="flex justify-between mb-2">
              <label class="nom-label">Price Range:</label>
              <span class="text-sm font-medium" v-if="priceDisplay">
                {{ priceDisplay }}
              </span>
            </div>
            
            <div class="space-y-4">
              <select 
                v-model="priceFilter"
                class="nom-select"
              >
                <option value="">All Prices</option>
                <option value="lessThan5">Less than $5</option>
                <option value="5to10">$5 - $10</option>
                <option value="10to15">$10 - $15</option>
                <option value="15to20">$15 - $20</option>
                <option value="above25">Above $20</option>
              </select>
            </div>
          </div>

          <!-- Ratings Filter (New) -->
          <div class="mb-6">
            <label class="nom-label">Meal Type:</label>
            <div class="space-y-2 mt-2">
              <label class="flex items-center space-x-2 cursor-pointer">
                <input type="checkbox" class="rounded text-primary focus:ring-primary" value="Breakfast" v-model="mealTypes">
                <span>Breakfast</span>
              </label>
              <label class="flex items-center space-x-2 cursor-pointer">
                <input type="checkbox" class="rounded text-primary focus:ring-primary" value="Lunch" v-model="mealTypes">
                <span>Lunch</span>
              </label>
              <label class="flex items-center space-x-2 cursor-pointer">
                <input type="checkbox" class="rounded text-primary focus:ring-primary" value="Dinner" v-model="mealTypes">
                <span>Dinner</span>
              </label>
            </div>
          </div>

          <!-- Clear Filters Button -->
          <button 
            @click="clearFilters" 
            class="w-full py-2 px-4 bg-muted text-muted-foreground rounded-md hover:bg-muted/80 transition-all duration-200 font-medium"
          >
            Clear All Filters
          </button>
        </div>
      </aside>

      <!-- Right Content: Search/Sort and Products Grid -->
      <main class="flex-1">
        <div class="mb-6">
          <h1 class="text-2xl font-bold mb-6">Browse Meal Kits</h1>
          <div class="flex flex-col sm:flex-row gap-4">
            <div class="flex-1 relative">
              <div class="absolute inset-y-0 left-3 flex items-center pointer-events-none">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-muted-foreground">
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
              </div>
              <input 
                v-model="searchTerm" 
                type="text" 
                placeholder="Search meal kits..." 
                class="nom-input pl-10"
              />
            </div>
            <div class="w-full sm:w-48">
              <select 
                v-model="sortOption"
                class="nom-select"
              >
                <option value="default">Sort by</option>
                <option value="priceLowToHigh">Price: Low to High</option>
                <option value="priceHighToLow">Price: High to Low</option>
                <option value="nameAZ">Name: A-Z</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="py-16 text-center">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          <p class="mt-4 text-lg text-muted-foreground">Loading delicious meals...</p>
        </div>
        
        <!-- Empty State -->
        <div v-else-if="filteredProducts.length === 0" class="py-16 text-center">
          <div class="w-16 h-16 bg-muted/30 rounded-full flex items-center justify-center mx-auto mb-4 text-muted-foreground">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="8" y1="12" x2="16" y2="12"></line>
            </svg>
          </div>
          <p class="text-xl text-muted-foreground mb-2">No products match your filters.</p>
          <p class="text-muted-foreground mb-4">Try adjusting your search criteria.</p>
          <button @click="clearFilters" class="nom-btn-primary">Clear All Filters</button>
        </div>
        
        <!-- Product Grid -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div 
            v-for="product in filteredProducts" 
            :key="product.id" 
            class="nom-card nom-card-hover nom-scale-hover nom-fade-in relative group"
          >
            <!-- New Item Badge (if applicable) -->
            <div v-if="product.isNew" class="absolute top-3 right-3 z-10">
              <span class="nom-badge-secondary">
                New
              </span>
            </div>

            <!-- Image with hover overlay -->
            <div class="relative h-48 rounded-md mb-4 overflow-hidden">
              <img 
                :src="product.imageURL" 
                :alt="product.name" 
                class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
              />
              <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </div>
            
            <!-- Content -->
            <div class="space-y-3">
              <h3 class="text-lg font-semibold">{{ product.name }}</h3>
              <p class="text-muted-foreground text-sm line-clamp-2">{{ product.description }}</p>

              <!-- Dietary Tags -->
              <div class="flex flex-wrap gap-1.5">
                <span 
                  v-for="tag in product.dietaryTags" 
                  :key="tag" 
                  class="nom-badge"
                >
                  {{ tag }}
                </span>
              </div>

              <div class="flex justify-between items-center">
                <p class="text-xl font-bold text-primary">${{ product.price.toFixed(2) }}</p>
                <p v-if="product.servings" class="text-xs text-muted-foreground">{{ product.servings }} servings</p>
              </div>
              
              <div class="pt-2 grid grid-cols-2 gap-3">
                <button 
                  @click="addToCart(product)" 
                  class="nom-btn-primary py-2"
                >
                  Add to Cart
                </button>
                <button 
                  @click="viewProductDetail(product)" 
                  class="nom-btn-outline"
                >
                  Details
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>

  <!-- Enhanced Product Detail Modal -->
  <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 backdrop-blur-sm nom-fade-in">
    <div 
      @click.stop 
      class="bg-card text-card-foreground rounded-lg shadow-lg p-6 max-w-md w-full max-h-[90vh] overflow-auto nom-slide-up"
    >
      <div class="mb-6">
        <h2 class="text-2xl font-bold">{{ selectedProduct.name }}</h2>
        <p class="text-xl text-primary font-bold mt-2">${{ selectedProduct.price.toFixed(2) }}</p>
      </div>

      <div class="space-y-4 mb-6">
        <div>
          <h3 class="font-semibold mb-2">Description</h3>
          <p class="text-muted-foreground">{{ selectedProduct.description }}</p>
        </div>
        
        <div>
          <h3 class="font-semibold mb-2">Ingredients</h3>
          <ul class="space-y-1">
            <li v-for="ingredient in selectedProduct.ingredients" :key="ingredient" class="flex items-start">
              <span class="text-primary mr-2">•</span>
              {{ ingredient }}
            </li>
          </ul>
        </div>
        
        <div>
          <h3 class="font-semibold mb-2">Preparation</h3>
          <p class="text-muted-foreground">{{ selectedProduct.preparation }}</p>
        </div>

        <div v-if="selectedProduct.dietaryTags && selectedProduct.dietaryTags.length">
          <h3 class="font-semibold mb-2">Dietary Information</h3>
          <div class="flex flex-wrap gap-2">
            <span 
              v-for="tag in selectedProduct.dietaryTags" 
              :key="tag" 
              class="nom-badge"
            >
              {{ tag }}
            </span>
          </div>
        </div>
      </div>
      
      <div class="flex justify-between">
        <button 
          @click="addToCart(selectedProduct)" 
          class="nom-btn-primary"
        >
          Add to Cart
        </button>
        <button 
          @click="closeModal" 
          class="nom-btn-outline"
        >
          Close
        </button>
      </div>
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
      selectedTags: [],
      priceFilter: '',
      mealTypes: [], // New filter for meal types
      products: [],
      loading: true,
      showModal: false,
      selectedProduct: {},
    }
  },
  computed: {
    uniqueDietaryTags() {
      const allTags = this.products.flatMap((product) => product.dietaryTags || [])
      return [...new Set(allTags)]
    },
    priceDisplay() {
      switch(this.priceFilter) {
        case 'lessThan5': return 'Under $5';
        case '5to10': return '$5 - $10';
        case '10to15': return '$10 - $15';
        case '15to20': return '$15 - $20';
        case 'above25': return 'Above $20';
        default: return '';
      }
    },
    filteredProducts() {
      let result = this.products

      // Search Filter
      if (this.searchTerm.trim() !== '')
        result = result.filter((product) =>
          product.name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
          (product.description && product.description.toLowerCase().includes(this.searchTerm.toLowerCase()))
        )

      // Price Filter
      if (this.priceFilter) {
        if (this.priceFilter === 'lessThan5') result = result.filter((product) => product.price < 5)
        else if (this.priceFilter === '5to10')
          result = result.filter((product) => product.price >= 5 && product.price <= 10)
        else if (this.priceFilter === '10to15')
          result = result.filter((product) => product.price >= 10 && product.price <= 15)
        else if (this.priceFilter === '15to20')
          result = result.filter((product) => product.price >= 15 && product.price <= 20)
        else if (this.priceFilter === 'above25')
          result = result.filter((product) => product.price > 20)
      }

      // Dietary Tags Filter
      if (this.selectedTags.length > 0) {
        result = result.filter((product) =>
          product.dietaryTags && product.dietaryTags.some((tag) => this.selectedTags.includes(tag))
        )
      }
      
      // Meal Type Filter (New)
      if (this.mealTypes.length > 0) {
        result = result.filter((product) => 
          product.mealType && this.mealTypes.includes(product.mealType)
        )
      }

      // Sorting
      if (this.sortOption === 'priceLowToHigh')
        result = result.slice().sort((a, b) => a.price - b.price)
      else if (this.sortOption === 'priceHighToLow')
        result = result.slice().sort((a, b) => b.price - a.price)
      else if (this.sortOption === 'nameAZ')
        result = result.slice().sort((a, b) => a.name.localeCompare(b.name))

      return result
    },
  },
  created() {
    this.fetchProducts()
  },
  methods: {
    async fetchProducts() {
      try {
        const response = await fetch('http://localhost:5006/inventory')
        const data = await response.json()
        if (data.code === 200) {
          // Add some sample meal types if they don't exist
          this.products = data.data
            .filter((product) => product.numAvailable > 0)
            .map(product => {
              // Just for demo purposes - assign meal types if they don't exist
              if (!product.mealType) {
                const types = ['Breakfast', 'Lunch', 'Dinner'];
                product.mealType = types[Math.floor(Math.random() * types.length)];
              }
              // Mark some products as new for demo
              product.isNew = Math.random() > 0.8;
              // Add servings if not present
              if (!product.servings) {
                product.servings = Math.floor(Math.random() * 3) + 2;
              }
              return product;
            });
        } else {
          console.error('No products available')
        }
      } catch (error) {
        console.error('Error fetching inventory:', error)
      } finally {
        this.loading = false
      }
    },
    addToCart(product) {
      const user = sessionStorage.getItem('customerId')
      if (!user) {
        this.$router.push('/login')
        return
      }

      let cart = JSON.parse(sessionStorage.getItem('shoppingCart')) || []
      let existingItem = cart.find((item) => item.id === product.id)

      if (existingItem) {
        existingItem.quantity++
      } else {
        cart.push({ ...product, quantity: 1 })
      }

      sessionStorage.setItem('shoppingCart', JSON.stringify(cart))
      
      // Use a more elegant notification instead of alert
      this.showNotification(`${product.name} added to cart!`)
    },
    clearFilters() {
      this.selectedTags = []
      this.priceFilter = ''
      this.mealTypes = []
      this.searchTerm = ''
      this.sortOption = 'default'
    },
    removeTag(tag) {
      this.selectedTags = this.selectedTags.filter(t => t !== tag)
    },
    viewProductDetail(product) {
      this.selectedProduct = product
      this.showModal = true
      
      // Prevent scrolling when modal is open
      document.body.style.overflow = 'hidden'
    },
    closeModal() {
      this.showModal = false
      this.selectedProduct = {}
      
      // Re-enable scrolling
      document.body.style.overflow = 'auto'
    },
  },
}
</script>