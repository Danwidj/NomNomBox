<template>
  <div>
    <!-- Enhanced Hero Section -->
    <section class="nom-hero">
      <div class="nom-container">
        <div class="max-w-2xl mx-auto text-center space-y-6">
          <h1 class="nom-hero-heading">
            Fresh Ingredients, <span class="text-primary">Delicious Meals</span>, Delivered to Your Door
          </h1>
          <p class="nom-hero-subheading">
            Choose your meal plan and enjoy cooking with high-quality, pre-portioned ingredients.
          </p>
          <a href="#plans" class="nom-btn-primary text-lg px-6 py-3">Get Started</a>
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

    <!-- Featured Meals Section -->
    <section id="meals" class="py-16 bg-muted/50">
      <div class="nom-container">
        <h2 class="nom-heading text-center mb-12">Featured Meals</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          <div class="nom-card hover:shadow-lg transition-shadow">
            <div class="text-4xl mb-4">🍲</div>
            <h3 class="text-xl font-medium mb-2">Grilled Chicken & Veggies</h3>
            <p class="text-muted-foreground">A delicious and healthy meal option for any day of the week.</p>
          </div>
          <div class="nom-card hover:shadow-lg transition-shadow">
            <div class="text-4xl mb-4">🥗</div>
            <h3 class="text-xl font-medium mb-2">Vegan Buddha Bowl</h3>
            <p class="text-muted-foreground">Fresh vegetables and grains in a colorful, nutritious bowl.</p>
          </div>
          <div class="nom-card hover:shadow-lg transition-shadow">
            <div class="text-4xl mb-4">🍝</div>
            <h3 class="text-xl font-medium mb-2">Classic Spaghetti Bolognese</h3>
            <p class="text-muted-foreground">A family favorite with our homemade sauce and fresh pasta.</p>
          </div>
        </div>
        <div class="text-center">
          <a href="#full-menu" class="nom-btn-secondary">See Full Menu</a>
        </div>
      </div>
    </section>

    <!-- Pricing Section -->
    <section id="pricing" class="py-16 bg-muted/50">
      <div class="nom-container">
        <h2 class="nom-heading text-center mb-12">Choose Your Plan</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          <div class="nom-card hover:shadow-lg transition-shadow text-center">
            <div class="text-4xl mb-4">🥡</div>
            <h3 class="text-xl font-medium mb-2">2 Meals per Week</h3>
            <p class="text-2xl font-bold text-primary my-4">$29.99</p>
            <p class="text-muted-foreground">Perfect for individuals or couples.</p>
          </div>
          <div class="nom-card hover:shadow-lg transition-shadow text-center">
            <div class="text-4xl mb-4">🥡</div>
            <h3 class="text-xl font-medium mb-2">3 Meals per Week</h3>
            <p class="text-2xl font-bold text-primary my-4">$39.99</p>
            <p class="text-muted-foreground">Our most popular plan.</p>
          </div>
          <div class="nom-card hover:shadow-lg transition-shadow text-center">
            <div class="text-4xl mb-4">🥡</div>
            <h3 class="text-xl font-medium mb-2">Family Plan</h3>
            <p class="text-2xl font-bold text-primary my-4">$59.99</p>
            <p class="text-muted-foreground">Feeds the whole family with ease.</p>
          </div>
        </div>
        <div class="text-center">
          <a href="#sign-up" class="nom-btn-primary">Select a Plan</a>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: "HomePage",
};
</script>