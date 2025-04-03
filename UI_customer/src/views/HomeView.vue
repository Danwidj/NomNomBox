<template>
  <div class="home-container fixed-layout">
    <!-- Hero Section (Kept as is) -->
    <section class="nom-hero !p-0 relative bg-primary/95">
      <!-- Background Image with Overlay -->
      <div class="absolute inset-0 z-0">
        <img 
          src="https://img.freepik.com/free-photo/buddha-bowl-dish-with-vegetables-legumes-top-view_1150-42589.jpg" 
          alt="Fresh food background" 
          class="w-full h-full object-cover"
        />
        <div class="absolute inset-0 bg-gradient-to-r from-primary/80 to-secondary/80 mix-blend-multiply"></div>
      </div>
      
      <div class="nom-container relative z-10 py-24">
        <div class="max-w-2xl mx-auto text-center space-y-6">
          <h1 class="nom-hero-heading text-white">
            Fresh Ingredients, <span class="text-white" style="text-shadow: 1px 1px 3px rgba(0,0,0,0.5);">Delicious Meals</span>, Delivered to Your Door
          </h1>
          <p class="nom-hero-subheading text-white/90">
            Choose your meal plan and enjoy cooking with high-quality, pre-portioned ingredients.
          </p>
            <a href="signup" class="nom-btn-primary text-lg px-6 py-3">Get Started</a>
        </div>
      </div>
    </section>

    <!-- Featured Benefits Section (Kept as is) -->
    <section class="py-12 bg-background">
      <div class="nom-container">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="nom-card nom-fade-in flex items-start space-x-4">
            <div class="text-4xl text-primary">🥗</div>
            <div>
              <h3 class="text-lg font-medium mb-1">Fresh Ingredients</h3>
              <p class="text-muted-foreground">We source the freshest ingredients from local farms.</p>
            </div>
          </div>
          <div class="nom-card nom-fade-in flex items-start space-x-4">
            <div class="text-4xl text-primary">⏱️</div>
            <div>
              <h3 class="text-lg font-medium mb-1">Time-Saving</h3>
              <p class="text-muted-foreground">Skip the shopping and get meals ready in under 30 minutes.</p>
            </div>
          </div>
          <div class="nom-card nom-fade-in flex items-start space-x-4">
            <div class="text-4xl text-primary">♻️</div>
            <div>
              <h3 class="text-lg font-medium mb-1">Eco-Friendly</h3>
              <p class="text-muted-foreground">All our packaging is recyclable or compostable.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works Section (Kept as is) -->
    <section id="how-it-works" class="py-16 bg-background">
      <div class="nom-container">
        <h2 class="nom-heading text-center mb-12">How It Works</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div class="nom-card nom-card-hover nom-scale-hover flex flex-col items-center text-center">
            <div class="w-16 h-16 bg-primary/20 text-primary rounded-full flex items-center justify-center mb-4 text-xl font-bold">1</div>
            <h3 class="text-lg font-medium mb-2">Choose Your Plan</h3>
            <p class="text-muted-foreground">Select a plan that fits your lifestyle and dietary needs.</p>
          </div>
          <div class="nom-card nom-card-hover nom-scale-hover flex flex-col items-center text-center">
            <div class="w-16 h-16 bg-primary/20 text-primary rounded-full flex items-center justify-center mb-4 text-xl font-bold">2</div>
            <h3 class="text-lg font-medium mb-2">Pick Your Meals</h3>
            <p class="text-muted-foreground">Browse our menu and select the meals you'd like to cook.</p>
          </div>
          <div class="nom-card nom-card-hover nom-scale-hover flex flex-col items-center text-center">
            <div class="w-16 h-16 bg-primary/20 text-primary rounded-full flex items-center justify-center mb-4 text-xl font-bold">3</div>
            <h3 class="text-lg font-medium mb-2">Receive Fresh Ingredients</h3>
            <p class="text-muted-foreground">Get pre-portioned ingredients delivered right to your door.</p>
          </div>
          <div class="nom-card nom-card-hover nom-scale-hover flex flex-col items-center text-center">
            <div class="w-16 h-16 bg-primary/20 text-primary rounded-full flex items-center justify-center mb-4 text-xl font-bold">4</div>
            <h3 class="text-lg font-medium mb-2">Cook & Enjoy</h3>
            <p class="text-muted-foreground">Follow our simple recipes and enjoy your delicious home-cooked meal.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Featured Meals Section (Using actual products) -->
    <section id="meals" class="py-16 relative">
      <!-- Background with overlay -->
      <div class="absolute inset-0 z-0 opacity-10">
        <img 
          src="https://img.freepik.com/free-photo/buddha-bowl-dish-with-vegetables-legumes-top-view_1150-42589.jpg" 
          alt="Meals background" 
          class="w-full h-full object-cover"
        />
      </div>
      <div class="nom-container relative z-10">
        <h2 class="nom-heading text-center mb-12">Featured Meals</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          <div 
            v-for="product in featuredProducts" 
            :key="product.id" 
            class="nom-card hover:shadow-lg transition-shadow"
          >
            <!-- Image with hover overlay -->
            <div class="relative h-48 rounded-md mb-4 overflow-hidden">
              <img 
                :src="product.imageURL" 
                :alt="product.name" 
                class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
              />
              <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </div>
            
            <h3 class="text-xl font-medium mb-2">{{ product.name }}</h3>
            <p class="text-muted-foreground line-clamp-2">{{ product.description }}</p>
            
            <!-- Dietary Tags -->
            <div class="flex flex-wrap gap-1.5 mt-4">
              <span 
                v-for="tag in product.dietaryTags.slice(0, 2)" 
                :key="tag" 
                class="nom-badge"
              >
                {{ tag }}
              </span>
            </div>
            
            <div class="flex justify-between items-center mt-4">
              <p class="text-xl font-bold text-primary">${{ product.price.toFixed(2) }}</p>
              <router-link :to="'/products'" class="nom-btn-outline px-3 py-1 text-sm">View</router-link>
            </div>
          </div>
        </div>
        <div class="text-center">
          <router-link to="/product" class="nom-btn-secondary">See Full Menu</router-link>
        </div>
      </div>
    </section>

    <!-- Chatbot Section (Replacing Pricing Section) -->
    <section id="chatbot" class="py-16 bg-background">
      <div class="nom-container">
        <div class="max-w-3xl mx-auto text-center">
          <h2 class="nom-heading mb-6">Not Sure Which Meal Kit Suits You?</h2>
          <p class="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto">Our AI assistant can help you find the perfect meal plan based on your dietary needs, preferences, and lifestyle. Get personalized recommendations in minutes!</p>
          
          <div class="nom-card nom-scale-hover p-8 bg-gradient-to-br from-primary/10 to-secondary/10 border-none">
            <div class="flex flex-col md:flex-row items-center justify-between gap-8">
              <div class="flex-1">
                <div class="text-6xl mb-4">🤖</div>
                <h3 class="text-xl font-medium mb-2">MealBot Assistant</h3>
                <p class="text-muted-foreground mb-4">Chat with our AI to discover meal kits tailored to your preferences.</p>
                <ul class="text-left space-y-2 mb-6">
                  <li class="flex items-center"><span class="text-primary mr-2">✓</span> Dietary restriction analysis</li>
                  <li class="flex items-center"><span class="text-primary mr-2">✓</span> Personalized recommendations</li>
                  <li class="flex items-center"><span class="text-primary mr-2">✓</span> Quick and simple process</li>
                </ul>
              </div>
              
              <div class="flex-1 flex flex-col items-center">
                <div class="w-full max-w-sm p-4 bg-card rounded-lg shadow-lg mb-4">
                  <div class="flex items-start mb-3">
                    <div class="w-8 h-8 rounded-full bg-primary/20 text-primary flex items-center justify-center mr-2 flex-shrink-0">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"></circle>
                        <path d="M12 16v-4"></path>
                        <path d="M12 8h.01"></path>
                      </svg>
                    </div>
                    <div class="bg-muted/50 rounded-lg p-2 text-left text-sm">
                      Hello! I can help you find the perfect meal kit. Do you have any dietary preferences?
                    </div>
                  </div>
                </div>
                <a href="/chatbot" class="nom-btn-primary px-8 py-3 text-lg w-full max-w-sm">Chat Now</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Call to Action Section (Kept as is) -->
    <section class="py-16 bg-primary text-primary-foreground">
      <div class="nom-container text-center">
        <h2 class="text-3xl font-bold mb-4">Ready to Start Cooking?</h2>
        <p class="max-w-xl mx-auto mb-8">Join thousands of happy customers who enjoy fresh, delicious meals at home.</p>
        <a href="/signup" class="bg-white text-primary hover:bg-white/90 px-8 py-3 rounded-md font-medium text-lg transition-colors">Get Started Today</a>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: "HomePage",
  data() {
    return {
      featuredProducts: [],
      loading: true
    }
  },
  mounted() {
    this.fetchFeaturedProducts();
  },
  methods: {
    async fetchFeaturedProducts() {
      try {
        const response = await fetch('http://localhost:5006/inventory')
        const data = await response.json()
        if (data.code === 200) {
          // Filter available products and select 3 for featuring
          const availableProducts = data.data.filter(product => product.numAvailable > 0);
          
          // You can customize this logic to select specific products or random ones
          // Here we're selecting 3 random products
          const shuffled = availableProducts.sort(() => 0.5 - Math.random());
          this.featuredProducts = shuffled.slice(0, 3);
          
          // Alternatively, you could select specific products by ID or other criteria
          // For example: this.featuredProducts = availableProducts.filter(p => [1, 5, 9].includes(p.id));
        } else {
          console.error('No products available')
          // Fallback to default products if API fails
          this.setDefaultProducts();
        }
      } catch (error) {
        console.error('Error fetching inventory:', error)
        // Fallback to default products if API fails
        this.setDefaultProducts();
      } finally {
        this.loading = false;
      }
    },
    setDefaultProducts() {
      // Fallback products in case API fails
      this.featuredProducts = [
        {
          id: 1,
          name: "Classic Spaghetti Bolognese",
          description: "A family favorite with our homemade sauce and fresh pasta.",
          price: 14.99,
          imageURL: "https://img.freepik.com/free-photo/pasta-spaghetti-with-tomato-sauce-and-meatballs_1220-7319.jpg",
          dietaryTags: ["Family", "Comfort"]
        },
        {
          id: 2,
          name: "Vegan Buddha Bowl",
          description: "Fresh vegetables and grains in a colorful, nutritious bowl.",
          price: 12.99,
          imageURL: "https://img.freepik.com/free-photo/buddha-bowl-dish-with-vegetables-legumes-top-view_1150-42589.jpg",
          dietaryTags: ["Vegan", "High-Fiber"]
        },
        {
          id: 3,
          name: "Grilled Chicken & Veggies",
          description: "A delicious and healthy meal option for any day of the week.",
          price: 15.99,
          imageURL: "https://img.freepik.com/free-photo/grilled-chicken-breast-fresh-vegetable-salad-tomatoes-cucumbers_2829-14452.jpg",
          dietaryTags: ["Protein-Rich", "Low-Carb"]
        }
      ];
    }
  }
};
</script>

<style scoped>
/* Custom styles to ensure proper layout */
.home-container {
  margin-top: -64px; /* Offset the margin-top in main */
  width: 100%;
  overflow-x: hidden;
}

/* Override hero styles to ensure full-bleed */
.nom-hero {
  width: 100vw !important;
  margin-left: calc(50% - 50vw) !important;
  margin-right: calc(50% - 50vw) !important;
  margin-top: 0 !important;
  /* padding-top: 64px !important; Add padding to account for the navbar height */
}

/* Ensure any overflow is hidden */
:deep(body), :deep(html) {
  overflow-x: hidden;
}

/* Force proper width calculation */
:deep(#app), :deep(main) {
  max-width: 100vw;
  overflow-x: hidden;
}
</style>