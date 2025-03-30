<template>
  <div class="nom-container py-8">
    <section class="max-w-6xl mx-auto nom-fade-in">
      <h2 class="nom-heading text-center mb-8">Shopping Cart</h2>

      <!-- Empty Cart Message -->
      <div v-if="cart.length === 0" class="nom-card py-12 text-center">
        <div class="flex flex-col items-center justify-center space-y-4">
          <svg class="w-16 h-16 text-muted-foreground/50" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M16 6V5C16 3.34315 14.6569 2 13 2H11C9.34315 2 8 3.34315 8 5V6H4C3.44772 6 3 6.44772 3 7V19C3 20.6569 4.34315 22 6 22H18C19.6569 22 21 20.6569 21 19V7C21 6.44772 20.5523 6 20 6H16ZM10 5C10 4.44772 10.4477 4 11 4H13C13.5523 4 14 4.44772 14 5V6H10V5ZM18 20H6C5.44772 20 5 19.5523 5 19V8H19V19C19 19.5523 18.5523 20 18 20Z" fill="currentColor"/>
          </svg>
          <p class="text-xl text-muted-foreground">Your shopping cart is empty.</p>
          <router-link to="/Product" class="nom-btn-primary mt-4">Browse Products</router-link>
        </div>
      </div>

      <!-- Cart Content -->
      <div v-else class="flex flex-col lg:flex-row gap-8">
        <!-- Cart Items List -->
        <div class="flex-1 space-y-6">
          <div 
            v-for="item in cart" 
            :key="item.id" 
            class="nom-card nom-card-hover flex flex-col md:flex-row gap-6"
          >
            <div class="w-full md:w-36 h-36 bg-muted/20 rounded-md overflow-hidden shrink-0">
              <img 
                :src="item.image" 
                :alt="item.name" 
                class="w-full h-full object-cover"
              />
            </div>

            <div class="flex-1">
              <div class="flex flex-col md:flex-row md:justify-between md:items-start gap-4">
                <div>
                  <h3 class="text-xl font-semibold">{{ item.name }}</h3>
                  <p class="text-muted-foreground mt-1 line-clamp-2">{{ item.description }}</p>
                  <p class="text-primary font-bold mt-2">${{ item.price.toFixed(2) }}</p>
                </div>
                
                <button 
                  class="text-destructive hover:text-destructive/80 font-medium self-start md:self-center flex items-center gap-1"
                  @click="removeItem(item.id)"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M3 6h18"></path>
                    <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
                    <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
                  </svg>
                  Remove
                </button>
              </div>

              <div class="mt-4 flex justify-between items-end">
                <div>
                  <div class="flex items-center">
                    <button 
                      class="w-8 h-8 bg-muted text-foreground rounded-md flex items-center justify-center hover:bg-muted/80 transition-colors border border-border"
                      @click="decreaseQuantity(item)"
                    >
                      −
                    </button>
                    <span class="w-12 text-center font-medium">{{ item.quantity }}</span>
                    <button 
                      class="w-8 h-8 bg-primary text-primary-foreground rounded-md flex items-center justify-center hover:bg-primary/80 transition-colors"
                      @click="increaseQuantity(item)"
                      :disabled="item.quantity >= (stockData[item.id] || item.stock)"
                    >
                      +
                    </button>
                  </div>
                  <p class="text-sm mt-2" :class="{'text-destructive font-medium': (stockData[item.id] || item.stock) < 5}">
                    Available: {{ stockData[item.id] || item.stock }} in stock
                  </p>
                </div>
                
                <p class="font-bold">
                  Subtotal: ${{ (item.price * item.quantity).toFixed(2) }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Order Summary -->
        <div class="w-full lg:w-80 shrink-0">
          <div class="space-y-4 mb-6">
            <div class="flex justify-between">
              <span class="text-muted-foreground">Total Items:</span>
              <span>{{ totalItems }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-muted-foreground">Subtotal:</span>
              <span>${{ totalPrice.toFixed(2) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-muted-foreground">Delivery Fee:</span>
              <span>${{ deliveryFee.toFixed(2) }}</span>
            </div>
            <div class="h-px bg-border my-2"></div>
            <div class="flex justify-between font-bold">
              <span>Total:</span>
              <span class="text-primary">${{ (totalPrice + deliveryFee).toFixed(2) }}</span>
            </div>
          

            <button 
              class="nom-btn-primary w-full py-3"
              @click="proceedToCheckout"
              :disabled="cart.length === 0"
            >
              Proceed to Checkout
            </button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { loadStripe } from '@stripe/stripe-js'

export default {
  name: 'CartPage',
  data() {
    return {
      cart: [],
      stockData: {}, // To store stock levels from Firestore
      stripe: null,
      customerId: '1', // or null if you prefer
      selectedTimeSlot: null, // track user-selected delivery slot
      promoCode: '', // for promo code functionality
      deliveryFee: 5.99, // default delivery fee
    }
  },
  computed: {
    totalItems() {
      return this.cart.reduce((total, item) => total + item.quantity, 0)
    },
    totalPrice() {
      return this.cart.reduce((total, item) => total + item.price * item.quantity, 0)
    },
    // Generate 30-minute increment time slots from 08:00 to 22:00
    timeSlots() {
      const slots = []
      let start = 8 * 60 // 08:00 in minutes
      const end = 22 * 60 // 22:00 in minutes

      while (start < end) {
        let endSlot = start + 30
        const startHour = String(Math.floor(start / 60)).padStart(2, '0')
        const startMin = String(start % 60).padStart(2, '0')
        const endHour = String(Math.floor(endSlot / 60)).padStart(2, '0')
        const endMin = String(endSlot % 60).padStart(2, '0')

        slots.push(`${startHour}:${startMin} - ${endHour}:${endMin}`)
        start += 30
      }
      return slots
    },
  },
  created() {
    this.loadCart()
    this.loadCustomerId()
    this.initStripe()
  },
  methods: {
    async initStripe() {
      try {
        const response = await fetch('http://localhost:5004/api/payment/public-key')
        const data = await response.json()

        if (!data.publicKey) {
          throw new Error('Stripe public key is missing from the backend.')
        }
        console.log('Using Stripe Public Key:', data.publicKey)

        this.stripe = await loadStripe(data.publicKey)
        console.log('Stripe initialized successfully')
      } catch (error) {
        console.error('Stripe initialization error:', error)
      }
    },
    async loadCart() {
      this.cart = JSON.parse(sessionStorage.getItem('shoppingCart')) || []

      try {
        const response = await fetch('http://localhost:5006/inventory') // Inventory API
        const data = await response.json()

        if (data.code === 200) {
          this.stockData = data.data.reduce((acc, item) => {
            acc[item.id] = item.numAvailable
            return acc
          }, {})
        } else {
          console.error('No stock data available')
        }
      } catch (error) {
        console.error('Error fetching stock data:', error)
      }
    },
    saveCart() {
      sessionStorage.setItem('shoppingCart', JSON.stringify(this.cart))
    },
    loadCustomerId() {
      this.customerId = sessionStorage.getItem('customerId') || '1' // or null if desired
    },
    saveCustomerId(id) {
      sessionStorage.setItem('customerId', id)
      this.customerId = id
    },
    removeItem(itemId) {
      this.cart = this.cart.filter((item) => item.id !== itemId)
      this.saveCart()
    },
    increaseQuantity(item) {
      const availableStock = this.stockData[item.id] ?? item.numAvailable ?? 0
      if (availableStock === 0) {
        console.error(`Stock not found for item ID: ${item.id}`)
        alert('Stock information is unavailable. Please try again later.')
        return
      }
      if (item.quantity < availableStock) {
        item.quantity++
        this.saveCart()
      } else {
        alert(`Only ${availableStock} left in stock!`)
      }
    },
    decreaseQuantity(item) {
      if (item.quantity > 1) {
        item.quantity--
      } else {
        this.removeItem(item.id)
      }
      this.saveCart()
    },
    async proceedToCheckout() {
      try {
        // Prepare the checkout data with customerId, items, totalPrice, & time slot
        const checkoutData = {
          customerId: this.customerId,
          items: this.cart.map((item) => ({
            id: item.id,
            name: item.name,
            price: item.price,
            quantity: item.quantity,
          })),
          totalPrice: this.totalPrice + this.deliveryFee,
          timeSlot: this.selectedTimeSlot, // pass the selected time slot
        }
        console.log('Checkout Request:', checkoutData)
        // **Store in sessionStorage** so we can retrieve it after payment success
        sessionStorage.setItem('deliveryTimeSlot', this.selectedTimeSlot)
        // Call the composite service endpoint
        const compositeResponse = await fetch('http://localhost:5005/order/checkout', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(checkoutData),
        })
        const compositeData = await compositeResponse.json()

        if (!compositeResponse.ok) {
          throw new Error(compositeData.message)
        }

        // Retrieve the Stripe session ID from the composite response.
        const stripeSessionId = compositeData.sessionId

        // Redirect to Stripe Checkout using the session ID.
        const result = await this.stripe.redirectToCheckout({ sessionId: stripeSessionId })
        if (result.error) {
          alert(result.error.message)
        }
      } catch (error) {
        alert('Error processing checkout: ' + error.message)
      }
    },
  },
}
</script>