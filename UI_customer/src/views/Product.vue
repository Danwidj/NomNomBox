<template>
  <div class="fixed-layout w-full">
    <div class="nom-container py-4">
      <div class="flex flex-col lg:flex-row gap-6 min-h-[calc(100vh-120px)]">
        <!-- Left Sidebar: Enhanced Filters -->
        <aside class="w-full lg:w-1/4 lg:min-w-64 shrink-0 h-full">
          <div class="nom-card sticky top-24 flex flex-col h-full animate-in slide-in-from-left-4 duration-300">
            <!-- Header with animated underline -->
            <div class="relative mb-6">
              <h2 class="text-xl font-semibold relative inline-block">Filters</h2>
              <div class="absolute bottom-0 left-0 w-0 h-0.5 bg-primary group-hover:w-full transition-all duration-300 hover:w-full"></div>
              <button 
                @click="clearFilters" 
                class="absolute right-0 top-0 text-sm text-primary hover:text-primary/80 font-medium transition-colors duration-200 flex items-center gap-1"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M3 3h18v18H3z"></path>
                  <path d="M12 8v8"></path>
                  <path d="M8 12h8"></path>
                </svg>
                Reset
              </button>
            </div>

            <!-- Collapsible Sections -->

            <!-- Dietary Tags Dropdown -->
            <div class="mb-4">
              <div @click="toggleDietaryTags" class="flex justify-between items-center cursor-pointer hover:text-primary transition-colors duration-200 p-2 -mx-2 rounded-md hover:bg-accent/50">
                <label class="nom-label mb-0 font-medium text-base">Dietary Tags</label>
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  width="18" 
                  height="18" 
                  viewBox="0 0 24 24" 
                  fill="none" 
                  stroke="currentColor" 
                  stroke-width="2" 
                  stroke-linecap="round" 
                  stroke-linejoin="round"
                  :class="{'transform rotate-180 transition-transform duration-300': dietaryTagsOpen, 'transition-transform duration-300': !dietaryTagsOpen}"
                >
                  <polyline points="6 9 12 15 18 9"></polyline>
                </svg>
              </div>

              <div 
                v-if="dietaryTagsOpen" 
                class="mt-2 bg-muted/40 p-4 rounded-md border border-border/50 max-h-60 overflow-y-auto animate-in fade-in zoom-in-95 duration-200 origin-top"
              >
                <div class="space-y-3">
                  <label 
                    v-for="tag in uniqueDietaryTags" 
                    :key="tag" 
                    class="flex items-center space-x-3 cursor-pointer p-2 hover:bg-accent/40 rounded transition-colors duration-200"
                  >
                    <div class="relative h-6 w-6">
                      <input 
                        type="checkbox" 
                        :value="tag" 
                        v-model="selectedTags"
                        class="peer sr-only"
                      >
                      <div class="h-6 w-6 rounded border border-primary/30 peer-checked:bg-primary peer-checked:border-primary transition-colors duration-200"></div>
                      <svg 
                        v-show="selectedTags.includes(tag)"
                        class="absolute top-0.5 left-0.5 h-5 w-5 text-white pointer-events-none"
                        fill="none" 
                        stroke="currentColor" 
                        viewBox="0 0 24 24" 
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path>
                      </svg>
                    </div>
                    <span class="text-base font-medium">{{ tag }}</span>
                  </label>
                </div>
              </div>
            </div>

          <!-- Price Range with Enhanced Slider -->
          <div class="mb-6">
            <div @click="togglePriceRange" class="flex justify-between items-center cursor-pointer hover:text-primary transition-colors duration-200 p-2 -mx-2 rounded-md hover:bg-accent/50">
              <label class="nom-label mb-0 font-medium">Price Range</label>
              <div class="flex items-center">
                <span class="text-sm font-medium mr-2">
                  ${{ priceRange[0] }} - ${{ priceRange[1] }}
                </span>
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  width="18" 
                  height="18" 
                  viewBox="0 0 24 24" 
                  fill="none" 
                  stroke="currentColor" 
                  stroke-width="2" 
                  stroke-linecap="round" 
                  stroke-linejoin="round"
                  :class="{'transform rotate-180 transition-transform duration-300': priceRangeOpen, 'transition-transform duration-300': !priceRangeOpen}"
                >
                  <polyline points="6 9 12 15 18 9"></polyline>
                </svg>
              </div>
            </div>

            <div 
              v-if="priceRangeOpen"
              class="mt-2 bg-muted/40 p-3 rounded-md border border-border/50 animate-in fade-in zoom-in-95 duration-200 origin-top"
            >
              <!-- Price range labels -->
              <div class="flex justify-between mt-2 mb-6">
                <span class="text-sm font-medium">Min: ${{ priceRange[0] }}</span>
                <span class="text-sm font-medium">Max: ${{ priceRange[1] }}</span>
              </div>
            
              <div class="px-4 py-2">
                <!-- Slider Track with Animated Handles -->
                <div class="relative h-2 bg-border/70 rounded-full" ref="sliderTrack">
                  <!-- Filled Track -->
                  <div 
                    class="absolute h-2 bg-primary/80 rounded-full transition-all duration-300 ease-out"
                    :style="{
                      left: `${((priceRange[0] - minPrice) / (maxPrice - minPrice)) * 100}%`,
                      width: `${((priceRange[1] - priceRange[0]) / (maxPrice - minPrice)) * 100}%`
                    }"
                  ></div>
                  
                  <!-- Min Handle -->
                  <div
                    class="absolute w-6 h-6 bg-primary rounded-full -mt-2 cursor-pointer shadow-md ring-4 ring-primary/20 hover:ring-primary/30 transition-all duration-200"
                    :style="{
                      left: `${((priceRange[0] - minPrice) / (maxPrice - minPrice)) * 100}%`,
                      marginLeft: '-12px'
                    }"
                    @mousedown="startDrag($event, 'min')"
                    @touchstart="startDrag($event, 'min')"
                  ></div>
                  
                  <!-- Max Handle -->
                  <div
                    class="absolute w-6 h-6 bg-primary rounded-full -mt-2 cursor-pointer shadow-md ring-4 ring-primary/20 hover:ring-primary/30 transition-all duration-200"
                    :style="{
                      left: `${((priceRange[1] - minPrice) / (maxPrice - minPrice)) * 100}%`,
                      marginLeft: '-12px'
                    }"
                    @mousedown="startDrag($event, 'max')"
                    @touchstart="startDrag($event, 'max')"
                  ></div>
                </div>
              
                <!-- Price inputs with better spacing -->
                <div class="flex justify-between mt-8 gap-4">
                  <div class="relative w-1/2">
                    <span class="text-sm font-medium text-muted-foreground">Min Price</span>
                    <div class="flex items-center mt-2">
                      <span class="text-sm mr-1">$</span>
                      <input
                        type="number"
                        :min="minPrice"
                        :max="priceRange[1] - 1"
                        v-model.number="priceRange[0]"
                        class="w-full p-2 border border-input rounded-md text-center"
                      />
                    </div>
                  </div>
                  <div class="relative w-1/2">
                    <span class="text-sm font-medium text-muted-foreground">Max Price</span>
                    <div class="flex items-center mt-2">
                      <span class="text-sm mr-1">$</span>
                      <input
                        type="number"
                        :min="priceRange[0] + 1"
                        :max="maxPrice"
                        v-model.number="priceRange[1]"
                        class="w-full p-2 border border-input rounded-md text-center"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

            <!-- Meal Type Filter with Icons -->
            <div class="mb-6">
              <div @click="toggleMealType" class="flex justify-between items-center cursor-pointer hover:text-primary transition-colors duration-200 p-2 -mx-2 rounded-md hover:bg-accent/50">
                <label class="nom-label mb-0 font-medium text-base">Meal Type</label>
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  width="18" 
                  height="18" 
                  viewBox="0 0 24 24" 
                  fill="none" 
                  stroke="currentColor" 
                  stroke-width="2" 
                  stroke-linecap="round" 
                  stroke-linejoin="round"
                  :class="{'transform rotate-180 transition-transform duration-300': mealTypeOpen, 'transition-transform duration-300': !mealTypeOpen}"
                >
                  <polyline points="6 9 12 15 18 9"></polyline>
                </svg>
              </div>
              
              <div 
                v-if="mealTypeOpen"
                class="mt-2 bg-muted/40 p-4 rounded-md border border-border/50 animate-in fade-in zoom-in-95 duration-200 origin-top"
              >
                <div class="grid grid-cols-3 gap-3">
                  <label 
                    class="cursor-pointer flex flex-col items-center justify-center p-3 rounded-md border-2 transition-all duration-200"
                    :class="mealTypes.includes('Breakfast') ? 'border-primary bg-primary/10' : 'border-transparent hover:border-primary/30 hover:bg-accent/50'"
                  >
                    <input type="checkbox" class="sr-only" value="Breakfast" v-model="mealTypes">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mb-2">
                      <path d="M18 8h1a4 4 0 0 1 0 8h-1"></path>
                      <path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"></path>
                      <line x1="6" y1="1" x2="6" y2="4"></line>
                      <line x1="10" y1="1" x2="10" y2="4"></line>
                      <line x1="14" y1="1" x2="14" y2="4"></line>
                    </svg>
                    <span class="text-base font-medium">Breakfast</span>
                  </label>
                  
                  <label 
                    class="cursor-pointer flex flex-col items-center justify-center p-3 rounded-md border-2 transition-all duration-200"
                    :class="mealTypes.includes('Lunch') ? 'border-primary bg-primary/10' : 'border-transparent hover:border-primary/30 hover:bg-accent/50'"
                  >
                    <input type="checkbox" class="sr-only" value="Lunch" v-model="mealTypes">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mb-2">
                      <path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"></path>
                      <path d="M7 2v20"></path>
                      <path d="M21 15V2v0a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"></path>
                    </svg>
                    <span class="text-base font-medium">Lunch</span>
                  </label>
                  
                  <label 
                    class="cursor-pointer flex flex-col items-center justify-center p-3 rounded-md border-2 transition-all duration-200"
                    :class="mealTypes.includes('Dinner') ? 'border-primary bg-primary/10' : 'border-transparent hover:border-primary/30 hover:bg-accent/50'"
                  >
                    <input type="checkbox" class="sr-only" value="Dinner" v-model="mealTypes">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mb-2">
                      <path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"></path>
                      <path d="M3 10v10a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2V10"></path>
                      <path d="M15 8V2"></path>
                      <path d="M15 12V2a5 5 0 0 1 5 5c0 3.03-2 5-5 5Z"></path>
                      <path d="M15 12v10"></path>
                    </svg>
                    <span class="text-base font-medium">Dinner</span>
                  </label>
                </div>
              </div>
            </div>

            <!-- Applied Filters Summary -->
            <div v-if="hasActiveFilters" class="mb-6 animate-in fade-in duration-200">
              <h3 class="text-sm font-medium mb-2">Applied Filters:</h3>
              <div class="flex flex-wrap gap-1.5">
                <div 
                  v-for="tag in selectedTags" 
                  :key="`tag-${tag}`" 
                  class="group flex items-center bg-accent/70 text-accent-foreground px-2 py-1 rounded-full text-xs"
                >
                  {{ tag }}
                  <button 
                    @click="removeTag(tag)" 
                    class="ml-1 h-4 w-4 rounded-full flex items-center justify-center bg-accent-foreground/10 group-hover:bg-accent-foreground/20 transition-colors"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <line x1="18" y1="6" x2="6" y2="18"></line>
                      <line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>
                  </button>
                </div>
                
                <div 
                  v-for="type in mealTypes" 
                  :key="`meal-${type}`" 
                  class="group flex items-center bg-primary/10 text-primary px-2 py-1 rounded-full text-xs"
                >
                  {{ type }}
                  <button 
                    @click="removeMealType(type)" 
                    class="ml-1 h-4 w-4 rounded-full flex items-center justify-center bg-primary/10 group-hover:bg-primary/20 transition-colors"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <line x1="18" y1="6" x2="6" y2="18"></line>
                      <line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>
                  </button>
                </div>
                
                <div 
                  v-if="isPriceRangeModified"
                  class="group flex items-center bg-secondary/10 text-secondary px-2 py-1 rounded-full text-xs"
                >
                  ${{ priceRange[0] }}-${{ priceRange[1] }}
                  <button 
                    @click="resetPriceRange" 
                    class="ml-1 h-4 w-4 rounded-full flex items-center justify-center bg-secondary/10 group-hover:bg-secondary/20 transition-colors"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <line x1="18" y1="6" x2="6" y2="18"></line>
                      <line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            <!-- Clear Filters Button - with animation -->
            <button 
              v-if="hasActiveFilters"
              @click="clearFilters" 
              class="w-full py-2 px-4 mt-auto bg-muted text-muted-foreground rounded-md hover:bg-accent hover:text-accent-foreground transition-all duration-300 font-medium flex items-center justify-center gap-2 animate-in fade-in duration-300"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 3h18v18H3z"></path>
                <path d="M12 8v8"></path>
                <path d="M8 12h8"></path>
              </svg>
              Clear All Filters
            </button>
          </div>
        </aside>

        <!-- Right Content: Search/Sort and Products Grid -->
        <main class="flex-1">
          <div class="mb-4">
            <h1 class="text-2xl font-bold mb-4">Browse Meal Kits</h1>
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
          <div v-if="loading" class="py-8 text-center">
            <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            <p class="mt-4 text-lg text-muted-foreground">Loading delicious meals...</p>
          </div>
          
          <!-- Empty State -->
          <div v-else-if="filteredProducts.length === 0" class="py-8 text-center">
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
          
          <!-- Product Grid - with reduced top margin -->
          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-4">
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
                    @click="addToCart(product, $event.target)" 
                    class="nom-btn-primary py-2 relative overflow-hidden"
                  >
                    Add to Cart
                    <span 
                      v-if="product.cartAnimation" 
                      class="absolute inset-0 bg-white/30 add-to-cart-ripple"
                    ></span>
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
  </div>

  <!-- Product Detail Modal -->
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

  <!-- Add to Cart Toast Notification -->
  <div 
    v-if="showToast" 
    class="fixed bottom-4 right-4 bg-primary text-primary-foreground px-4 py-3 rounded-md shadow-lg nom-fade-in flex items-center gap-2 z-50"
  >
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
      <line x1="3" y1="6" x2="21" y2="6"></line>
      <path d="M16 10a4 4 0 0 1-8 0"></path>
    </svg>
    {{ toastMessage }}
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
      mealTypes: [],
      products: [],
      loading: true,
      showModal: false,
      selectedProduct: {},
      
      // Price range slider
      minPrice: 0,
      maxPrice: 30,
      priceRange: [0, 30],
      isDragging: false,
      activeDragHandle: null,
      
      // Toast notification
      showToast: false,
      toastMessage: '',
      toastTimeout: null,
      
      // Collapsible sections state
      dietaryTagsOpen: true,
      priceRangeOpen: true,
      mealTypeOpen: true
    }
  },
  computed: {
    uniqueDietaryTags() {
      const allTags = this.products.flatMap((product) => product.dietaryTags || [])
      return [...new Set(allTags)]
    },
    filteredProducts() {
      let result = this.products

      // Search Filter
      if (this.searchTerm.trim() !== '')
        result = result.filter((product) =>
          product.name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
          (product.description && product.description.toLowerCase().includes(this.searchTerm.toLowerCase()))
        )

      // Price Range Filter
      result = result.filter((product) => 
        product.price >= this.priceRange[0] && product.price <= this.priceRange[1]
      )

      // Dietary Tags Filter
      if (this.selectedTags.length > 0) {
        result = result.filter((product) =>
          product.dietaryTags && product.dietaryTags.some((tag) => this.selectedTags.includes(tag))
        )
      }
      
      // Meal Type Filter
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
    // Check if any filters are active
    hasActiveFilters() {
      return this.selectedTags.length > 0 || 
             this.mealTypes.length > 0 || 
             this.isPriceRangeModified;
    },
    // Check if price range has been modified from default
    isPriceRangeModified() {
      return this.priceRange[0] !== this.minPrice || this.priceRange[1] !== this.maxPrice;
    }
  },
  created() {
    this.fetchProducts()
  },
  mounted() {
    // Add global event listeners for drag functionality
    window.addEventListener('mousemove', this.onDrag)
    window.addEventListener('mouseup', this.stopDrag)
    window.addEventListener('touchmove', this.onDrag)
    window.addEventListener('touchend', this.stopDrag)
    window.addEventListener('touchcancel', this.stopDrag)
    
    // Force scrollbar to be visible to prevent layout shifting
    const style = document.createElement('style')
    style.innerHTML = `html { overflow-y: scroll !important; }`
    document.head.appendChild(style)
    this.injectedStyle = style
  },
  beforeUnmount() {
    // Clean up event listeners
    window.removeEventListener('mousemove', this.onDrag)
    window.removeEventListener('mouseup', this.stopDrag)
    window.removeEventListener('touchmove', this.onDrag)
    window.removeEventListener('touchend', this.stopDrag)
    window.removeEventListener('touchcancel', this.stopDrag)
    
    // Clear any pending timeouts
    if (this.toastTimeout) clearTimeout(this.toastTimeout)
    
    // Remove injected style
    if (this.injectedStyle) {
      document.head.removeChild(this.injectedStyle)
    }
  },
  methods: {
    // Toggle section visibility
    toggleDietaryTags() {
      this.dietaryTagsOpen = !this.dietaryTagsOpen;
    },
    togglePriceRange() {
      this.priceRangeOpen = !this.priceRangeOpen;
    },
    toggleMealType() {
      this.mealTypeOpen = !this.mealTypeOpen;
    },
    
    // Remove individual filters
    removeTag(tag) {
      this.selectedTags = this.selectedTags.filter(t => t !== tag);
    },
    removeMealType(type) {
      this.mealTypes = this.mealTypes.filter(t => t !== type);
    },
    resetPriceRange() {
      this.priceRange = [this.minPrice, this.maxPrice];
    },
    
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
              // Add cartAnimation property
              product.cartAnimation = false;
              return product;
            });
            
          // Update price range based on actual products
          if (this.products.length > 0) {
            this.minPrice = Math.floor(Math.min(...this.products.map(p => p.price)))
            this.maxPrice = Math.ceil(Math.max(...this.products.map(p => p.price)))
            this.priceRange = [this.minPrice, this.maxPrice]
          }
        } else {
          console.error('No products available')
        }
      } catch (error) {
        console.error('Error fetching inventory:', error)
      } finally {
        this.loading = false
      }
    },
    addToCart(product, buttonEl) {
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
      
      // Play the add-to-cart animation on the button
      const productToAnimate = this.products.find(p => p.id === product.id)
      if (productToAnimate) {
        productToAnimate.cartAnimation = true
        setTimeout(() => {
          productToAnimate.cartAnimation = false
        }, 700)
      }
      
      // Show toast notification
      this.showToastNotification(`${product.name} added to cart!`)
      
      // Emit event for navbar to update cart count
      this.$emit('cartUpdated')
    },
    showToastNotification(message) {
      // Clear any existing timeout
      if (this.toastTimeout) clearTimeout(this.toastTimeout)
      
      this.toastMessage = message
      this.showToast = true
      
      // Hide the toast after 3 seconds
      this.toastTimeout = setTimeout(() => {
        this.showToast = false
      }, 3000)
    },
    clearFilters() {
      this.selectedTags = []
      this.priceRange = [this.minPrice, this.maxPrice]
      this.mealTypes = []
      this.searchTerm = ''
      this.sortOption = 'default'
    },

    viewProductDetail(product) {
      this.selectedProduct = product
      this.showModal = true
      
      // Prevent scrolling when modal is open
      document.body.classList.add('modal-open')
      
      // Calculate scrollbar width and add as padding-right to prevent shifting
      const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth
      document.body.style.paddingRight = `${scrollbarWidth}px`
    },
    closeModal() {
      this.showModal = false
      this.selectedProduct = {}
      
      // Re-enable scrolling and remove padding
      document.body.classList.remove('modal-open')
      document.body.style.paddingRight = ''
    },
    
    // Price Range Slider Methods
    startDrag(event, handle) {
      event.preventDefault()
      this.isDragging = true
      this.activeDragHandle = handle

      // Directly call onDrag to update immediately on click
      this.onDrag(event)
    },
    onDrag(event) {
      if (!this.isDragging) return

      const sliderTrack = this.$refs.sliderTrack
      if (!sliderTrack) return

      const bounds = sliderTrack.getBoundingClientRect()
      const trackWidth = bounds.width

      // Get clientX from either mouse or touch event
      const clientX = event.touches ? event.touches[0].clientX : event.clientX

      // Calculate percentage along track
      let percentage = (clientX - bounds.left) / trackWidth
      percentage = Math.max(0, Math.min(1, percentage))

      // Map percentage to price value
      const priceValue = this.minPrice + percentage * (this.maxPrice - this.minPrice)
      const roundedPrice = Math.round(priceValue)

      // Update the appropriate price range value
      if (this.activeDragHandle === 'min') {
        this.priceRange = [
          Math.min(roundedPrice, this.priceRange[1] - 1), 
          this.priceRange[1]
        ]
      } else if (this.activeDragHandle === 'max') {
        this.priceRange = [
          this.priceRange[0], 
          Math.max(roundedPrice, this.priceRange[0] + 1)
        ]
      }
    },
    stopDrag() {
      this.isDragging = false
      this.activeDragHandle = null
    }
  }
}
</script>

<style scoped>
/* Add to cart animation */
.add-to-cart-ripple {
  animation: ripple 0.7s ease-out;
}

@keyframes ripple {
  from {
    opacity: 1;
    transform: scale(0);
  }
  to {
    opacity: 0;
    transform: scale(2);
  }
}

/* Force scrollbar to prevent layout shifts */
html {
  overflow-y: scroll !important;
}

/* Fix for modal opening */
body.modal-open {
  overflow: hidden;
}

/* Custom animations for filters */
.filter-slide-in {
  animation: filterSlideIn 0.3s ease-out forwards;
}

@keyframes filterSlideIn {
  from {
    opacity: 0;
    transform: translateX(-10px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Checkbox animations */
.checkbox-pop {
  animation: checkboxPop 0.3s ease-out;
}

@keyframes checkboxPop {
  0% {
    transform: scale(0.8);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

/* Improved scrollbar for filter lists */
.max-h-48::-webkit-scrollbar,
.max-h-60::-webkit-scrollbar {
  width: 6px;
}

.max-h-48::-webkit-scrollbar-track,
.max-h-60::-webkit-scrollbar-track {
  background: transparent;
}

.max-h-48::-webkit-scrollbar-thumb,
.max-h-60::-webkit-scrollbar-thumb {
  background: rgba(var(--primary), 0.3);
  border-radius: 6px;
}

.max-h-48::-webkit-scrollbar-thumb:hover,
.max-h-60::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--primary), 0.5);
}

/* Enhance slider interaction with standard properties */
input[type="number"] {
  appearance: textfield; /* Standard property */
  -moz-appearance: textfield; /* Firefox fallback */
}

input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Animated transition for collapsible sections */
[v-if].animate-in {
  transition: all 0.3s ease-in-out;
}

/* Improved focus states for accessibility */
input:focus, 
select:focus, 
button:focus {
  outline: 2px solid hsl(var(--ring));
  outline-offset: 2px;
}

/* Pulsing effect for "New" badge */
.nom-badge-secondary {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(var(--secondary), 0.4);
  }
  70% {
    box-shadow: 0 0 0 6px rgba(var(--secondary), 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(var(--secondary), 0);
  }
}

/* Improved slider styles */
[ref="sliderTrack"] {
  width: 100%;
  overflow: visible;
  position: relative;
  margin: 24px 0;
}

/* Better handle styles for price range slider */
.bg-primary.rounded-full {
  cursor: grab;
}

.bg-primary.rounded-full:active {
  cursor: grabbing;
}

/* Dietary tag and meal type styles */
.nom-label {
  font-size: 0.95rem;
}

label span.text-base {
  font-size: 0.95rem !important;
}

/* Price range label positioning */
.relative span.text-sm {
  position: absolute;
  top: -22px;
  font-size: 0.85rem;
  font-weight: 500;
  color: hsl(var(--muted-foreground));
}

/* Space between price slider and inputs */
.mt-8 {
  margin-top: 2rem !important;
}

/* Appropriate input sizing */
.p-2.border.border-input {
  height: 36px;
  font-size: 0.95rem;
}

/* Applied filters tag styling */
.group.flex.items-center.bg-accent\/70,
.group.flex.items-center.bg-primary\/10,
.group.flex.items-center.bg-secondary\/10 {
  transition: all 0.2s ease;
}

.group.flex.items-center.bg-accent\/70:hover,
.group.flex.items-center.bg-primary\/10:hover,
.group.flex.items-center.bg-secondary\/10:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

/* Enhance meal type selector */
.grid.grid-cols-3 label {
  transition: all 0.2s ease-in-out;
}

.grid.grid-cols-3 label:hover {
  transform: translateY(-2px);
}

.grid.grid-cols-3 label.border-primary {
  transform: translateY(-2px);
  box-shadow: 0 3px 6px rgba(var(--primary), 0.2);
}

/* Min/Max slider label spacing */
.flex.justify-between.mt-2.mb-6 {
  margin-bottom: 1rem;
  margin-top: 0.5rem;
  padding: 0 0.5rem;
}
</style>