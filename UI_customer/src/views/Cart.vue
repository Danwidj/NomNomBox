<template>
  <div class="page-container">
    <section class="cart-section">
      <h2>Shopping Cart</h2>

      <!-- Empty Cart Message -->
      <div v-if="cart.length === 0" class="empty-cart">
        <p>Your shopping cart is empty.</p>
      </div>

      <!-- Cart Content -->
      <div v-else class="cart-content">
        <!-- Cart Items List -->
        <div class="cart-items">
          <div v-for="item in cart" :key="item.id" class="cart-item">
            <img :src="item.image" :alt="item.name" class="cart-item-image" />
            
            <div class="cart-item-details">
              <h3 class="cart-item-title">{{ item.name }}</h3>
              <p class="cart-item-description">{{ item.description }}</p>
              <p class="cart-item-price">$ {{ item.price.toFixed(2) }}</p>

              <div class="quantity-controls">
                <button class="btn quantity-btn" @click="decreaseQuantity(item)">−</button>
                <span class="quantity">{{ item.quantity }}</span>
                <button 
                  class="btn quantity-btn" 
                  @click="increaseQuantity(item)" 
                  :disabled="item.quantity >= (stockData[item.id] || item.stock)"
                >
                  +
                </button>             
                 </div>
              <p class="stock-info">
  Available: {{ stockData[item.id] || item.stock }} in stock
</p><br>
              <p class="cart-item-total">
                Subtotal: <strong>$ {{ (item.price * item.quantity).toFixed(2) }}</strong>
              </p>
            </div>

            <button class="btn remove-btn" @click="removeItem(item.id)">Remove</button>
          </div>
        </div>

        <!-- Order Summary -->
        <div class="cart-summary">
          <h3>Order Summary</h3>
          <div class="summary-item">
            <span>Total Items:</span> <span>{{ totalItems }}</span>
          </div>
          <div class="summary-item">
            <span>Total Price:</span> <span class="total-price">$ {{ totalPrice.toFixed(2) }}</span>
          </div>
        <button class="checkout-btn" @click="proceedToCheckout">Proceed to Checkout</button>
        </div>
      </div>
    </section>
  </div>
  <div class="customer-id">
  <p>Customer ID: <strong>{{ customerId }}</strong></p>
</div>
</template>
<script>
import { loadStripe } from "@stripe/stripe-js";

export default {
  name: "CartPage",
  data() {
    return {
      cart: [],
      stockData: {}, // To store stock levels from Firestore
  stripe: null  ,
      customerId: "1"//change to null

    };
  },
  computed: {
    totalItems() {
      return this.cart.reduce((total, item) => total + item.quantity, 0);
    },
    totalPrice() {
      return this.cart.reduce((total, item) => total + item.price * item.quantity, 0);
    }
  },
  created() {
    this.loadCart();
    this.loadCustomerId();
    this.initStripe(); 
  },
  methods: {
    async initStripe() {
    try {
        const response = await fetch("http://localhost:5004/api/payment/public-key");
        const data = await response.json();

        if (!data.publicKey) {
            throw new Error(" Stripe public key is missing from the backend.");
        }

        console.log(" Using Stripe Public Key:", data.publicKey);

        this.stripe = await loadStripe(data.publicKey);
        console.log(" Stripe initialized successfully");
    } catch (error) {
        console.error("Stripe initialization error:", error);
    }
},
   async loadCart() {
  this.cart = JSON.parse(sessionStorage.getItem("shoppingCart")) || [];
  

  try {
    const response = await fetch("http://127.0.0.1:5006/inventory"); // Inventory API
    const data = await response.json();

    if (data.code === 200) {
      this.stockData = data.data.reduce((acc, item) => {
        acc[item.id] = item.numAvailable; // Use correct field name
        return acc;
      }, {});
    } else {
      console.error("No stock data available");
    }
  } catch (error) {
    console.error("Error fetching stock data:", error);
  }
},
    saveCart() {
      sessionStorage.setItem("shoppingCart", JSON.stringify(this.cart));
    },
    loadCustomerId() {
    this.customerId = sessionStorage.getItem("customerId") || "1"; //change to null
  },
    saveCustomerId(id) {
      sessionStorage.setItem("customerId", id);
      this.customerId = id;
    },
    removeItem(itemId) {
      this.cart = this.cart.filter(item => item.id !== itemId);
      this.saveCart();
    },
increaseQuantity(item) {
  console.log("Stock Data:", this.stockData); // Debugging
  console.log("Checking stock for item:", item.id); // Debugging

  const availableStock = this.stockData[item.id] ?? item.numAvailable ?? 0; // Use numAvailable

  if (availableStock === 0) {
    console.error(`Stock not found for item ID: ${item.id}`);
    alert("Stock information is unavailable. Please try again later.");
    return;
  }

  if (item.quantity < availableStock) {
    item.quantity++;
    this.saveCart();
  } else {
    alert(`Only ${availableStock} left in stock!`); // Notify user with correct stock
  }
},
    decreaseQuantity(item) {
      if (item.quantity > 1) {
        item.quantity--;
      } else {
        this.removeItem(item.id);
      }
      this.saveCart();
    },
async proceedToCheckout() {
  try {
    // Prepare the checkout data with customerId, items, and totalPrice.
    const checkoutData = {
      customerId: this.customerId,
      items: this.cart.map(item => ({
        id: item.id,
        name: item.name,
        price: item.price,
        quantity: item.quantity
      })),
      totalPrice: this.totalPrice
    };
    console.log("Checkout Request:", checkoutData); // Debugging

    // Call the composite service endpoint
    const compositeResponse = await fetch("http://localhost:5005/order/checkout", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(checkoutData)
    });

    const compositeData = await compositeResponse.json();
    if (!compositeResponse.ok) {
      throw new Error(compositeData.message);
    }

    // Retrieve the Stripe session ID from the composite response.
    const stripeSessionId = compositeData.sessionId;

    // Redirect to Stripe Checkout using the session ID.
    const result = await this.stripe.redirectToCheckout({ sessionId: stripeSessionId });
    if (result.error) {
      alert(result.error.message);
    }
  } catch (error) {
    alert("Error processing checkout: " + error.message);
  }
}

  }
};
</script>

<style scoped>
/* General Styling */
.page-container {
  display: flex;
  justify-content: center;
  padding: 20px;
  min-height: 100vh;
  background: #f7f7f7;
}

/* Shopping Cart Section */
.cart-section {
  width: 90%;
  max-width: 1000px;
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.1);
  text-align: center;
}

/* Empty Cart */
.empty-cart {
  font-size: 1.2rem;
  color: #777;
  padding: 20px;
}

/* Cart Content */
.cart-content {
  display: flex;
  justify-content: space-between;
  gap: 20px;
}

/* Cart Items */
.cart-items {
  flex: 2;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

/* Cart Item */
.cart-item {
  display: flex;
  align-items: center;
  background: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.08);
  transition: 0.3s;
}

.cart-item:hover {
  transform: scale(1.02);
  box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.12);
}

/* Product Image */
.cart-item-image {
  width: 100px;
  height: 100px;
  border-radius: 8px;
  object-fit: cover;
  margin-right: 15px;
}

/* Product Details */
.cart-item-details {
  flex: 1;
  text-align: left;
}

.cart-item-title {
  font-size: 1.1rem;
  font-weight: bold;
}

.cart-item-description {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 5px;
}

.cart-item-price {
  font-size: 1rem;
  font-weight: bold;
  color: #ff6600;
}

.cart-item-total {
  font-size: 1rem;
  font-weight: bold;
  margin-top: 8px;
}

/* Quantity Controls */
.quantity-controls {
  display: flex;
  align-items: center;
  margin-top: 10px;
}

.quantity {
  font-size: 1rem;
  font-weight: bold;
  margin: 0 10px;
}

.quantity-btn {
  background: #ff9900;
  border: none;
  color: white;
  padding: 6px 12px;
  font-size: 1rem;
  border-radius: 4px;
  cursor: pointer;
  margin: 0 5px;
  transition: 0.3s;
}

.quantity-btn:hover {
  background: #e68a00;
}

/* Remove Button (Always Red) */
.remove-btn {
  background: #ff4d4d;
  padding: 8px 14px;
  transition: 0.3s;
  border: none;
}

.remove-btn:hover {
  background: #e60000;
  transform: scale(1.1);
}

/* Order Summary */
.cart-summary {
  flex: 1;
  background: #fafafa;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.08);
  text-align: left;
}

.cart-summary h3 {
  font-size: 1.3rem;
  margin-bottom: 15px;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  font-size: 1rem;
  margin-bottom: 10px;
}

.total-price {
  font-weight: bold;
  color: #ff6600;
}

/* Checkout Button */
.checkout-btn {
  background: #009900;
  padding: 14px;
  font-size: 1rem;
  color: white;
  border-radius: 8px;
  cursor: pointer;
  margin-top: 10px;
  transition: 0.3s;
  border: none;
}

.checkout-btn:hover {
  background: #007700;
  transform: scale(1.05);
}
.stock-info {
  font-size: 0.9rem;
  color: #ff0000;
  font-weight: bold;
}
</style>
