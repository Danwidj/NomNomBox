<template>
    <div class="container">
      <section class="cart-section">
        <h2>Shopping Cart</h2>
        <div v-if="cart.length === 0" class="empty-cart">
          <p>Your shopping cart is empty.</p>
        </div>
        <div v-else class="cart-items">
          <div v-for="item in cart" :key="item.id" class="cart-item">
            <p><strong>{{ item.name }}</strong></p>
            <p>Price: ${{ item.price.toFixed(2) }}</p>
            <p>Quantity: {{ item.quantity }}</p>
            <button class="btn" @click="removeItem(item.id)">Remove</button>
          </div>
        </div>
      </section>
  
      <footer class="footer">
        <p>&copy; 2025 MealKit. All rights reserved.</p>
        <p><a href="#contact">Contact Us</a> | <a href="#faq">FAQ</a></p>
      </footer>
    </div>
  </template>
  
  <script>
  export default {
    name: "CartPage",
    data() {
      return {
        cart: [
          { id: 1, name: "Grilled Chicken Meal", price: 12.99, quantity: 1 },
          { id: 2, name: "Vegan Buddha Bowl", price: 10.99, quantity: 2 }
        ],
      };
    },
    methods: {
      removeItem(itemId) {
        this.cart = this.cart.filter(item => item.id !== itemId);
      }
    }
  };
  </script>
  
  <style scoped>
  .container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }
  
  .cart-section {
    text-align: center;
    padding: 60px 5%;
    background: white;
    margin: 20px auto;
    border-radius: 12px;
    box-shadow: 0px 6px 10px rgba(0, 0, 0, 0.1);
    width: 95%;
    max-width: 800px;
    flex-grow: 1;
  }
  
  .empty-cart {
    font-size: 1.2rem;
    color: #777;
    padding: 20px;
  }
  
  .cart-items {
    display: flex;
    flex-direction: column;
    gap: 15px;
    align-items: center;
  }
  
  .cart-item {
    background: #f9f9f9;
    padding: 15px;
    border-radius: 8px;
    width: 80%;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .btn {
    background-color: #ff6600;
    color: white;
    padding: 10px 20px;
    border-radius: 5px;
    text-decoration: none;
    display: inline-block;
    margin-top: 10px;
    font-size: 1rem;
    border: none;
    cursor: pointer;
    transition: background 0.3s;
  }
  
  .btn:hover {
    background-color: #e65c00;
  }
  
  .footer {
    text-align: center;
    padding: 30px;
    background-color: #222;
    color: white;
    width: 100%;
    margin-top: auto;
    position: relative;
    bottom: 0;
  }
  </style>