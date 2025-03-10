<template>
  <div class="container">
    <section class="hero">
      <div class="hero-content">
        <h1>Fresh Ingredients, Delicious Meals, Delivered to Your Door</h1>
        <p>Choose your meal plan and enjoy cooking with high-quality, pre-portioned ingredients.</p>
        <a href="#plans" class="btn">Get Started</a>
      </div>
    </section>

    <section id="how-it-works" class="section">
      <h2>How It Works</h2>
      <div class="steps">
        <div class="step">1. Choose Your Plan</div>
        <div class="step">2. Pick Your Meals</div>
        <div class="step">3. Receive Fresh Ingredients</div>
        <div class="step">4. Cook & Enjoy</div>
      </div>
    </section>

    <section id="meals" class="section">
      <h2>Featured Meals</h2>
      <div class="meal-container">
        <div class="meal">🍲 Grilled Chicken & Veggies</div>
        <div class="meal">🥗 Vegan Buddha Bowl</div>
        <div class="meal">🍝 Classic Spaghetti Bolognese</div>
      </div>
      <a href="#full-menu" class="btn">See Full Menu</a>
    </section>

    <section id="reviews" class="section">
      <h2>What Our Customers Say</h2>
      <blockquote>"Best meal kit service! Fresh ingredients and easy-to-follow recipes." - Sarah L.</blockquote>
      <blockquote>"So convenient and tasty! I love trying new meals every week." - James K.</blockquote>
    </section>

    <section id="pricing" class="section">
      <h2>Choose Your Plan</h2>
      <div class="plans">
        <div class="plan">🥡 2 Meals per Week - $29.99</div>
        <div class="plan">🥡 3 Meals per Week - $39.99</div>
        <div class="plan">🥡 Family Plan - $59.99</div>
      </div>
      <a href="#sign-up" class="btn">Select a Plan</a>
    </section>

    <footer class="footer">
      <p>&copy; 2025 MealKit. All rights reserved.</p>
      <p><a href="#contact">Contact Us</a> | <a href="#faq">FAQ</a></p>
    </footer>
  </div>
</template>

<script>
export default {
  name: "HomePage",
};
</script>

<style scoped>
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f8f8f8;
  color: #333;
  text-align: center;
}

.container {
  width: 100%;
  max-width: 1400px;
  margin: auto;
}

.hero {
  text-align: center;
  padding: 100px 5%;
  background: url('https://source.unsplash.com/1600x900/?food') no-repeat center center/cover;
  color: white;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 500px;
  flex-direction: column;
}

.hero-content {
  max-width: 800px;
  font-size: 1.7rem;
  text-align: center;
}

.section {
  text-align: center;
  padding: 60px 5%;
  background: white;
  margin: 20px auto;
  border-radius: 12px;
  box-shadow: 0px 6px 10px rgba(0, 0, 0, 0.1);
  width: 95%;
  max-width: 1200px;
  font-size: 1.3rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.steps, .meal-container, .plans {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 30px;
  flex-wrap: wrap;
  font-size: 1.2rem;
  width: 100%;
}

.btn {
  background-color: #ff6600;
  color: white;
  padding: 18px 30px;
  border-radius: 8px;
  text-decoration: none;
  display: inline-block;
  margin-top: 20px;
  font-size: 1.3rem;
}

.footer {
  text-align: center;
  padding: 30px;
  background-color: #222;
  color: white;
  width: 100%;
  font-size: 1.2rem;
}
</style>