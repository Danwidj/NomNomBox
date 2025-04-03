<template>
  <div class="home-container fixed-layout">
    <!-- Enhanced Hero Section with Background Image - Full viewport approach -->
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
            <a href="product" class="nom-btn-primary text-lg px-6 py-3">Get Started</a>
        </div>
      </div>
    </section>

    <!-- Featured Benefits Section (New) -->
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

    <!-- How It Works Section - Enhanced -->
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

    <!-- Featured Meals Section with image background -->
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
          <div class="nom-card hover:shadow-lg transition-shadow">
            <div class="text-4xl mb-4">🍲</div>
            <h3 class="text-xl font-medium mb-2">Grilled Chicken & Veggies</h3>
            <p class="text-muted-foreground">A delicious and healthy meal option for any day of the week.</p>
            <div class="flex items-center mt-4">
              <div class="nom-badge-primary mr-2">Protein-Rich</div>
              <div class="nom-badge-secondary">Low-Carb</div>
            </div>
          </div>
          <div class="nom-card hover:shadow-lg transition-shadow">
            <div class="text-4xl mb-4">🥗</div>
            <h3 class="text-xl font-medium mb-2">Vegan Buddha Bowl</h3>
            <p class="text-muted-foreground">Fresh vegetables and grains in a colorful, nutritious bowl.</p>
            <div class="flex items-center mt-4">
              <div class="nom-badge-primary mr-2">Vegan</div>
              <div class="nom-badge-secondary">High-Fiber</div>
            </div>
          </div>
          <div class="nom-card hover:shadow-lg transition-shadow">
            <div class="text-4xl mb-4">🍝</div>
            <h3 class="text-xl font-medium mb-2">Classic Spaghetti Bolognese</h3>
            <p class="text-muted-foreground">A family favorite with our homemade sauce and fresh pasta.</p>
            <div class="flex items-center mt-4">
              <div class="nom-badge-primary mr-2">Family</div>
              <div class="nom-badge-secondary">Comfort</div>
            </div>
          </div>
        </div>
        <div class="text-center">
          <a href="#full-menu" class="nom-btn-secondary">See Full Menu</a>
        </div>
      </div>
    </section>

    <!-- Pricing Section - Enhanced -->
    <section id="pricing" class="py-16 bg-background">
      <div class="nom-container">
        <h2 class="nom-heading text-center mb-4">Choose Your Plan</h2>
        <p class="text-center text-muted-foreground max-w-xl mx-auto mb-12">Select a meal plan that fits your lifestyle. All plans include free delivery and access to our recipe archive.</p>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          <div class="nom-card hover:shadow-lg transition-shadow text-center relative overflow-hidden">
            <div class="text-4xl mb-4">🥡</div>
            <h3 class="text-xl font-medium mb-2">2 Meals per Week</h3>
            <p class="text-2xl font-bold text-primary my-4">$29.99</p>
            <ul class="text-left space-y-2 mb-6">
              <li class="flex items-center"><span class="text-primary mr-2">✓</span> 2 recipes per week for 2 people</li>
              <li class="flex items-center"><span class="text-primary mr-2">✓</span> Fresh, pre-portioned ingredients</li>
              <li class="flex items-center"><span class="text-primary mr-2">✓</span> Free delivery</li>
            </ul>
            <a href="#sign-up" class="nom-btn-outline w-full">Select</a>
          </div>
          <div class="nom-card hover:shadow-lg transition-shadow text-center relative overflow-hidden">
            <div class="absolute top-0 right-0 bg-primary text-primary-foreground py-1 px-4 text-sm font-medium">Most Popular</div>
            <div class="text-4xl mb-4">🥡</div>
            <h3 class="text-xl font-medium mb-2">3 Meals per Week</h3>
            <p class="text-2xl font-bold text-primary my-4">$39.99</p>
            <ul class="text-left space-y-2 mb-6">
              <li class="flex items-center"><span class="text-primary mr-2">✓</span> 3 recipes per week for 2 people</li>
              <li class="flex items-center"><span class="text-primary mr-2">✓</span> Fresh, pre-portioned ingredients</li>
              <li class="flex items-center"><span class="text-primary mr-2">✓</span> Free delivery</li>
            </ul>
            <a href="#sign-up" class="nom-btn-primary w-full">Select</a>
          </div>
          <div class="nom-card hover:shadow-lg transition-shadow text-center relative overflow-hidden">
            <div class="text-4xl mb-4">🥡</div>
            <h3 class="text-xl font-medium mb-2">Family Plan</h3>
            <p class="text-2xl font-bold text-primary my-4">$59.99</p>
            <ul class="text-left space-y-2 mb-6">
              <li class="flex items-center"><span class="text-primary mr-2">✓</span> 3 recipes per week for 4 people</li>
              <li class="flex items-center"><span class="text-primary mr-2">✓</span> Fresh, pre-portioned ingredients</li>
              <li class="flex items-center"><span class="text-primary mr-2">✓</span> Free delivery</li>
            </ul>
            <a href="#sign-up" class="nom-btn-outline w-full">Select</a>
          </div>
        </div>
      </div>
    </section>

    <!-- Call to Action Section (New) -->
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