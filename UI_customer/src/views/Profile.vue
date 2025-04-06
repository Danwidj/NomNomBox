<template>
  <div class="nom-container py-8 nom-fade-in">
    <!-- Profile Section -->
    <section class="max-w-4xl mx-auto mb-12">
      <h2 class="nom-heading text-center mb-8">My Profile</h2>
      
      <div class="nom-card nom-card-hover">
        <!-- Profile Header - Removed profile picture -->
        <div class="flex flex-col sm:flex-row gap-6 items-center sm:items-start mb-8">
          <div class="flex-1 text-center sm:text-left">
            <h3 class="text-2xl font-semibold mb-2">{{ customer.name }}</h3>
            <p class="text-muted-foreground">{{ customer.email }}</p>
            
            <!-- Fixed Edit Profile Button -->
            <div class="mt-4">
              <router-link to="/edit-profile" class="nom-btn-outline inline-flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2">
                  <path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"></path>
                </svg>
                Edit Profile
              </router-link>
            </div>
          </div>
        </div>
        
        <!-- Profile Details -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Contact Information -->
          <div class="space-y-4">
            <h4 class="text-lg font-medium border-b border-border pb-2 mb-4">Contact Information</h4>
            
            <div>
              <p class="text-muted-foreground text-sm mb-1">Address</p>
              <p class="font-medium">{{ customer.address || 'Not specified' }}</p>
            </div>
            
            <div>
              <p class="text-muted-foreground text-sm mb-1">Phone</p>
              <p class="font-medium">{{ customer.phone || 'Not specified' }}</p>
            </div>
          </div>
          
          <!-- Preferences -->
          <div class="space-y-4">
            <h4 class="text-lg font-medium border-b border-border pb-2 mb-4">Dietary Preferences</h4>
            
            <div class="flex flex-wrap gap-2">
              <span 
                v-for="pref in customer.dietary_preferences" 
                :key="pref"
                class="px-3 py-1.5 bg-accent text-accent-foreground rounded-full text-sm font-medium"
              >
                {{ pref }}
              </span>
              <span v-if="!customer.dietary_preferences.length" class="text-muted-foreground text-base">
                No preferences specified
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Order History Section with Tabs -->
    <section class="max-w-4xl mx-auto">
      <div class="flex items-center justify-between mb-6">
        <h2 class="nom-heading">Order History</h2>
        <div class="flex items-center gap-2 text-muted-foreground" v-if="sortedOrders.length === 0">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-1">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <span class="text-sm">Recent orders will appear here</span>
        </div>
      </div>
      
      <!-- Tab Buttons -->
      <div class="mb-6 border-b border-border" v-if="sortedOrders.length > 0">
        <div class="flex space-x-2">
          <!-- Pending Orders Tab -->
          <button 
            @click="activeTab = 'pending'"
            :class="[
              'py-2 px-4 font-medium text-sm transition-colors duration-200 relative',
              activeTab === 'pending' 
                ? 'text-destructive border-b-2 border-destructive' 
                : 'text-muted-foreground hover:text-foreground'
            ]"
          >
            Pending Delivery
            <span v-if="pendingOrders.length > 0" 
              class="ml-2 px-2 py-0.5 text-xs font-medium rounded-full bg-destructive/10 text-destructive">
              {{ pendingOrders.length }}
            </span>
          </button>

          <!-- Active Orders Tab -->
          <button 
            @click="activeTab = 'active'"
            :class="[
              'py-2 px-4 font-medium text-sm transition-colors duration-200 relative',
              activeTab === 'active' 
                ? 'text-primary border-b-2 border-primary' 
                : 'text-muted-foreground hover:text-foreground'
            ]"
          >
            Active Orders
            <span v-if="activeOrders.length > 0" 
              class="ml-2 px-2 py-0.5 text-xs font-medium rounded-full bg-primary/10 text-primary">
              {{ activeOrders.length }}
            </span>
          </button>
          
          <!-- Delivered Orders Tab -->
          <button 
            @click="activeTab = 'delivered'"
            :class="[
              'py-2 px-4 font-medium text-sm transition-colors duration-200 relative',
              activeTab === 'delivered' 
                ? 'text-primary border-b-2 border-primary' 
                : 'text-muted-foreground hover:text-foreground'
            ]"
          >
            Delivered
            <span v-if="deliveredOrders.length > 0" 
              class="ml-2 px-2 py-0.5 text-xs font-medium rounded-full bg-primary/10 text-primary">
              {{ deliveredOrders.length }}
            </span>
          </button>
        </div>
      </div>

      <!-- No Orders State -->
      <div v-if="sortedOrders.length === 0" class="nom-card py-12 text-center">
        <div class="flex flex-col items-center justify-center space-y-4">
          <svg class="w-16 h-16 text-muted-foreground/50" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 5H7C5.89543 5 5 5.89543 5 7V19C5 20.1046 5.89543 21 7 21H17C18.1046 21 19 20.1046 19 19V7C19 5.89543 18.1046 5 17 5H15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M9 5C9 3.89543 9.89543 3 11 3H13C14.1046 3 15 3.89543 15 5V7H9V5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="9" y1="12" x2="15" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="9" y1="16" x2="15" y2="16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <p class="text-xl text-muted-foreground">No order history available.</p>
          <router-link to="/" class="nom-btn-primary mt-4">Start Shopping</router-link>
        </div>
      </div>

      <!-- Pending Orders Tab Content -->
      <div v-if="activeTab === 'pending'" class="space-y-6 nom-fade-in">
        <div 
          v-if="pendingOrders.length === 0" 
          class="nom-card py-8 text-center"
        >
          <div class="flex flex-col items-center justify-center space-y-4">
            <svg class="w-12 h-12 text-destructive/40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <p class="text-lg text-muted-foreground">
              No orders waiting for delivery scheduling.
            </p>
            <router-link to="product" class="nom-btn-primary">
              Continue Shopping
            </router-link>
          </div>
        </div>

        <div 
          v-else
          class="nom-card nom-card-hover" 
          v-for="order in pendingOrders" 
          :key="order.orderId"
        >
          <!-- Order Header -->
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6">
            <div>
              <h3 class="text-lg font-semibold">Order #{{ order.orderId }}</h3>
              <p class="text-muted-foreground">{{ formatDate(order.createdAt) }}</p>
            </div>
            
            <div class="mt-2 sm:mt-0 flex flex-col sm:items-end gap-2">
              <span 
                class="px-3 py-1 rounded-full text-sm font-medium bg-destructive/10 text-destructive"
              >
                Awaiting Delivery Scheduling
              </span>
              
              <!-- Schedule Delivery Button -->
              <button 
                @click="scheduleDelivery(order)"
                class="px-3 py-1.5 text-sm font-medium bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors flex items-center gap-1"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-1">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                  <line x1="16" y1="2" x2="16" y2="6"></line>
                  <line x1="8" y1="2" x2="8" y2="6"></line>
                  <line x1="3" y1="10" x2="21" y2="10"></line>
                </svg>
                Schedule Delivery
              </button>
            </div>
          </div>

          <!-- Order Details -->
          <div class="mb-6">
            <div class="flex justify-between items-center bg-muted/20 p-3 rounded-md">
              <div class="flex gap-4 items-center">
                <div class="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center text-primary">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
                    <line x1="3" y1="6" x2="21" y2="6"></line>
                    <path d="M16 10a4 4 0 0 1-8 0"></path>
                  </svg>
                </div>
                <div>
                  <p class="text-sm text-muted-foreground">Total Items</p>
                  <p class="font-medium">{{ order.items.reduce((sum, item) => sum + item.quantity, 0) }} items</p>
                </div>
              </div>
              
              <div>
                <p class="text-sm text-muted-foreground">Total Amount</p>
                <p class="font-semibold text-primary">${{ order.totalPrice.toFixed(2) }}</p>
              </div>
            </div>
          </div>

          <!-- Order Items -->
          <div class="border-t border-border pt-4">
            <p class="font-medium mb-4">Order Items:</p>
            <div class="space-y-2">
              <div 
                class="flex justify-between py-2 px-3 bg-muted/20 rounded" 
                v-for="item in order.items" 
                :key="item.id"
              >
                <div class="flex items-center gap-2">
                  <span class="font-medium">{{ item.name }}</span>
                  <span class="text-xs bg-muted px-2 py-0.5 rounded-full">× {{ item.quantity }}</span>
                </div>
                <span class="font-medium">${{ (item.price * item.quantity).toFixed(2) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Active Orders Tab Content -->
      <div v-else-if="activeTab === 'active'" class="space-y-6 nom-fade-in">
        <div 
          v-if="activeOrders.length === 0" 
          class="nom-card py-8 text-center"
        >
          <div class="flex flex-col items-center justify-center space-y-4">
            <svg class="w-12 h-12 text-muted-foreground/40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M9 5H7C5.89543 5 5 5.89543 5 7V19C5 20.1046 5.89543 21 7 21H17C18.1046 21 19 20.1046 19 19V7C19 5.89543 18.1046 5 17 5H15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M9 5C9 3.89543 9.89543 3 11 3H13C14.1046 3 15 3.89543 15 5V7H9V5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <p class="text-lg text-muted-foreground">
              No active orders at the moment.
            </p>
            <router-link to="product" class="nom-btn-primary">
              Continue Shopping
            </router-link>
          </div>
        </div>
      
        <div 
          v-else
          class="nom-card nom-card-hover" 
          v-for="order in activeOrders" 
          :key="order.orderId"
        >
          <!-- Order Header -->
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6">
            <div>
              <h3 class="text-lg font-semibold">Order #{{ order.orderId }}</h3>
              <p class="text-muted-foreground">{{ formatDate(order.createdAt) }}</p>
              <p v-if="order.deliveryTime" class="text-muted-foreground text-sm">
                Expected Delivery: {{ formatDate(order.deliveryTime * 1000) }}
              </p>
            </div>

            <div class="mt-2 sm:mt-0 flex flex-col sm:items-end gap-2">
              <span 
                :class="[
                  'px-3 py-1 rounded-full text-sm font-medium',
                  {
                    'bg-primary/10 text-primary': order.status.toLowerCase() === 'assigned to driver',
                    'bg-amber-100 text-amber-800': order.status.toLowerCase() === 'picked up by driver',
                    'bg-blue-100 text-blue-800': order.status.toLowerCase() === 'in transit'
                  }
                ]"
              >
                {{ order.status }}
              </span>
            </div>
          </div>
        
          <!-- Order Details (similar to other tabs) -->
          <div class="mb-6">
            <div class="flex justify-between items-center bg-muted/20 p-3 rounded-md">
              <div class="flex gap-4 items-center">
                <div class="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center text-primary">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
                    <line x1="3" y1="6" x2="21" y2="6"></line>
                    <path d="M16 10a4 4 0 0 1-8 0"></path>
                  </svg>
                </div>
                <div>
                  <p class="text-sm text-muted-foreground">Total Items</p>
                  <p class="font-medium">{{ order.items.reduce((sum, item) => sum + item.quantity, 0) }} items</p>
                </div>
              </div>

              <div>
                <p class="text-sm text-muted-foreground">Total Amount</p>
                <p class="font-semibold text-primary">${{ order.totalPrice.toFixed(2) }}</p>
              </div>
            </div>
          </div>
        
          <!-- Order Items -->
          <div class="border-t border-border pt-4">
            <p class="font-medium mb-4">Order Items:</p>
            <div class="space-y-2">
              <div 
                class="flex justify-between py-2 px-3 bg-muted/20 rounded" 
                v-for="item in order.items" 
                :key="item.id"
              >
                <div class="flex items-center gap-2">
                  <span class="font-medium">{{ item.name }}</span>
                  <span class="text-xs bg-muted px-2 py-0.5 rounded-full">× {{ item.quantity }}</span>
                </div>
                <span class="font-medium">${{ (item.price * item.quantity).toFixed(2) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Delivered Orders Tab Content -->
      <div v-else-if="activeTab === 'delivered'" class="space-y-6 nom-fade-in">
        <div 
          class="nom-card nom-card-hover" 
          v-for="order in deliveredOrders" 
          :key="order.orderId"
        >
          <!-- Order Header -->
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6">
            <div>
              <h3 class="text-lg font-semibold">Order #{{ order.orderId }}</h3>
              <p class="text-muted-foreground">{{ formatDate(order.createdAt) }}</p>
              <p class="text-muted-foreground text-sm">
                Delivered: {{ formatDate(order.deliveryDate) }}
              </p>
            </div>
            
            <div class="mt-2 sm:mt-0">
              <span 
                :class="[
                  'px-3 py-1 rounded-full text-sm font-medium',
                  {
                    'bg-green-100 text-green-800': order.status === 'Received by Customer',
                    'bg-amber-100 text-amber-800': order.status === 'Delivered by Driver' || order.status.toLowerCase() === 'delivered'
                  }
                ]"
              >
                {{ order.status }}
              </span>
            </div>
          </div>
          
          <!-- Order Details -->
          <div class="mb-6">
            <div class="flex justify-between items-center bg-muted/20 p-3 rounded-md">
              <div class="flex gap-4 items-center">
                <div class="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center text-primary">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
                    <line x1="3" y1="6" x2="21" y2="6"></line>
                    <path d="M16 10a4 4 0 0 1-8 0"></path>
                  </svg>
                </div>
                <div>
                  <p class="text-sm text-muted-foreground">Total Items</p>
                  <p class="font-medium">{{ order.items.reduce((sum, item) => sum + item.quantity, 0) }} items</p>
                </div>
              </div>
              
              <div>
                <p class="text-sm text-muted-foreground">Total Amount</p>
                <p class="font-semibold text-primary">${{ order.totalPrice.toFixed(2) }}</p>
              </div>
            </div>
          </div>

          <!-- Order Items -->
          <div class="border-t border-border pt-4">
            <p class="font-medium mb-4">Order Items:</p>
            <div class="space-y-2">
              <div 
                class="flex justify-between py-2 px-3 bg-muted/20 rounded" 
                v-for="item in order.items" 
                :key="item.id"
              >
                <div class="flex items-center gap-2">
                  <span class="font-medium">{{ item.name }}</span>
                  <span class="text-xs bg-muted px-2 py-0.5 rounded-full">× {{ item.quantity }}</span>
                </div>
                <span class="font-medium">${{ (item.price * item.quantity).toFixed(2) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { onMounted, ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

export default {
  name: 'ProfilePage',
  setup() {
    const router = useRouter()
    const route = useRoute()

    const customer = ref({
      customerId: '',
      name: '',
      email: '',
      address: '',
      phone: '',
      dietary_preferences: [],
    })

    const orders = ref([])
    const activeTab = ref('pending') // Default to pending orders tab
    const notification = ref(null)

    // Create a method to show delivery scheduled notification
    const showDeliveryScheduledNotification = (confirmationData) => {
      // Remove any existing notification
      const existingNotification = document.querySelector('.delivery-notification')
      if (existingNotification) {
        existingNotification.remove()
      }
    
      // Create notification element
      const notification = document.createElement('div')
      notification.className = 'delivery-notification fixed top-4 right-4 z-50 bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative nom-fade-in shadow-lg'
      notification.innerHTML = `
        <div class="flex items-center justify-between">
          <div>
            <strong class="font-bold block mb-1">Delivery Scheduled Successfully!</strong>
            <p class="text-sm">Order #${confirmationData.orderId} is scheduled for delivery</p>
            <p class="text-xs text-green-600">${confirmationData.deliveryDate}</p>
            <p class="text-xs text-green-600">Time Slot: ${confirmationData.deliveryTimeSlot}</p>
          </div>
          <button class="ml-4 text-green-700 hover:text-green-900 close-notification">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
      `
      
      // Add event listener to close button
      const closeButton = notification.querySelector('.close-notification')
      const closeNotification = () => {
        notification.remove()
      }
      closeButton.addEventListener('click', closeNotification)
    
      // Append to body and set timeout to remove
      document.body.appendChild(notification)

      // Set timeout to remove notification after 5 seconds
      const notificationTimeout = setTimeout(closeNotification, 5000)
    
      // Return cleanup function (though not used with onUnmounted)
      return () => {
        clearTimeout(notificationTimeout)
        notification.remove()
      }
    }


    // Compute sorted orders by date (newest first)
    const sortedOrders = computed(() => {
      return [...orders.value].sort((a, b) => {
        const dateA = getDateFromTimestamp(a.createdAt)
        const dateB = getDateFromTimestamp(b.createdAt)
        return dateB - dateA
      })
    })

    // Helper to get JavaScript Date object from various timestamp formats
    const getDateFromTimestamp = (timestamp) => {
      if (!timestamp) return new Date(0)
      
      // Handle Firestore Timestamp
      if (typeof timestamp === 'object' && 'seconds' in timestamp) {
        return new Date(timestamp.seconds * 1000)
      }
      
      // Handle regular date string
      return new Date(timestamp)
    }

    // Filter pending orders (including orders without delivery date)
    const pendingOrders = computed(() => {
      return sortedOrders.value.filter(order => 
        order.displayStatus === 'Pending Delivery Scheduling'
      )
    })

    // Filter orders for active tab (not delivered or canceled)
    const activeOrders = computed(() => {
      return sortedOrders.value.filter(order => 
        order.displayStatus === 'Active Order'
      )
    })

    // Filter orders for delivered tab
    const deliveredOrders = computed(() => {
      return sortedOrders.value.filter(order => 
        order.displayStatus === 'Delivered'
      )
    })

    // Method to handle delivery scheduling
    const scheduleDelivery = (order) => {
      // Redirect to a delivery scheduling page with the order ID
      router.push({
        path: '/schedule-delivery',
        query: { orderId: order.orderId }
      })
    }

    // Check if delivery confirmation button should be shown
    const shouldShowDeliveryButton = (order) => {
      // Only show button for orders with status "Delivered by Driver"
      return order.status === "Delivered by Driver";
    }

    // Handle delivery confirmation
    const confirmDelivery = async (orderId) => {
      try {
        const token = localStorage.getItem('token');
        
        if (!token) {
          console.error('User is not authenticated');
          router.push('/login');
          return;
        }

        // 1. First, get the delivery ID associated with this order
        const getOrderResponse = await fetch(`http://localhost:5001/api/orders/${orderId}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        });
        
        const orderData = await getOrderResponse.json();
        if (orderData.code !== 200) {
          console.error('Failed to get order details:', orderData.message);
          alert('Failed to confirm delivery. Please try again.');
          return;
        }
        
        const deliveryId = orderData.data.deliveryId;
        if (!deliveryId) {
          console.error('No delivery associated with this order');
          alert('No delivery found for this order.');
          return;
        }
        
        // 2. Call manage_deliveries API to update delivery status in MQ
        const deliveryResponse = await fetch(`http://localhost:5000/deliveries/${deliveryId}`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            order_id: orderId,
            status: 'Received by Customer'
          })
        });
        
        const deliveryResult = await deliveryResponse.json();
        if (deliveryResult.code !== 200) {
          console.error('Failed to update delivery status:', deliveryResult.message);
          alert('Failed to confirm delivery. Please try again.');
          return;
        }
        
        // Update order status locally
        const orderIndex = orders.value.findIndex(order => order.orderId === orderId);
        if (orderIndex !== -1) {
          orders.value[orderIndex].status = 'Received by Customer';
        }
        alert('Delivery confirmation successful! Thank you for your feedback.');
        
      } catch (error) {
        console.error('Error confirming delivery:', error);
        alert('Error confirming delivery. Please try again later.');
      }
    }

    // Format date for display
    const formatDate = (timestamp) => {
      if (!timestamp) return 'Unknown Date'

      // Handle Firestore Timestamp (if it exists)
      if (typeof timestamp === 'object' && 'seconds' in timestamp) {
        const date = new Date(timestamp.seconds * 1000)
        return formatDateHelper(date)
      }

      // Handle JavaScript Date (if stored as a string)
      const date = new Date(timestamp)
      if (isNaN(date)) return 'Unknown Date'

      return formatDateHelper(date)
    }

    // Helper function to format date consistently
    const formatDateHelper = (date) => {
      return date.toLocaleString('en-US', {
        timeZone: 'Asia/Singapore',
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true,
      })
    }

    // Fetch user data on component mount
    onMounted(async () => {
      const token = localStorage.getItem('token')
      const customerId = localStorage.getItem('userId')

      if (!token || !customerId) {
        console.error('User is not authenticated')
        router.push('/login')
        return
      }
    
      try {
        console.log('Fetching customer profile...')
        await fetchUserData(customerId, token)
        console.log('Fetching order history...')
        await fetchOrderHistory(customerId)
      
        // Check for delivery scheduling query param and show notification
        const deliveryConfirmation = localStorage.getItem('deliveryConfirmation')
        if (route.query.deliveryScheduled === 'true' && deliveryConfirmation) {
          const confirmationData = JSON.parse(deliveryConfirmation)

          // Show notification using a method that doesn't rely on onUnmounted
          showDeliveryScheduledNotification(confirmationData)
        
          // Switch to active orders tab
          activeTab.value = 'active'
        
          // Clear the localStorage item
          localStorage.removeItem('deliveryConfirmation')
        }
      } catch (error) {
        console.error('Failed to load profile:', error)
      }
    })
    
    // Fetch customer profile data
    const fetchUserData = async (customerId, token) => {
      try {
        // First, check if token exists
        if (!token) {
          console.error('No authentication token found');
          router.push('/login');
          return;
        }
      
        // Try to fetch user data
        const response = await fetch(`http://localhost:5003/customer/${customerId}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
        });
      
        const data = await response.json();
        console.log('Customer API Response:', data);
      
        // Handle 401 Unauthorized errors specifically
        if (data.code === 401) {
          console.error('Authentication error:', data.message);

          // If it's a token timing issue
          if (data.error && data.error.includes('Token used too early')) {
            // Wait a few seconds and try again
            console.log('Token timing issue detected. Retrying in 3 seconds...');
            setTimeout(async () => {
              await fetchUserData(customerId, token);
            }, 3000);
            return;
          }

          // For other auth errors, redirect to login
          alert('Your session has expired. Please log in again.');
          localStorage.removeItem('token');
          router.push('/login');
          return;
        }
      
        if (data.code === 200) {
          customer.value = data.data;

          // Ensure dietary_preferences is an array
          if (!Array.isArray(customer.value.dietary_preferences)) {
            customer.value.dietary_preferences = [];
          }

          console.log('Customer Data Loaded:', customer.value);
        } else {
          console.error('Failed to fetch customer data:', data.message);
        }
      } catch (error) {
        console.error('Error fetching customer data:', error);
      }
    }

    // Fetch order history
    const fetchOrderHistory = async (customerId) => {
      try {
        const response = await fetch(
          `http://localhost:5001/api/orders/customer/${customerId}`,
        )
        const data = await response.json()
      
        if (data.code === 200) {
          // Process orders with their actual delivery dates/times
          orders.value = data.data.map(order => {
            const processedOrder = { ...order }
            
            // Try multiple ways to get delivery time
            if (order.deliveryTime) {
              processedOrder.expectedDeliveryTime = order.deliveryTime
              processedOrder.expectedDeliveryDisplay = formatDate(order.deliveryTime * 1000)
            } else if (order.delivery_time) {
              processedOrder.expectedDeliveryTime = order.delivery_time
              processedOrder.expectedDeliveryDisplay = formatDate(order.delivery_time * 1000)
            } else if (order.deliveryDate) {
              processedOrder.expectedDeliveryTime = Math.floor(new Date(order.deliveryDate).getTime() / 1000)
              processedOrder.expectedDeliveryDisplay = formatDate(processedOrder.expectedDeliveryTime * 1000)
            }
            
            // Existing status determination logic
            const lowercaseStatus = order.status.toLowerCase();
            
            if (lowercaseStatus === 'pending payment' || 
                lowercaseStatus === 'pending' || 
                lowercaseStatus === 'pending delivery scheduling') {
              processedOrder.displayStatus = 'Pending Delivery Scheduling'
            } else if (lowercaseStatus === 'assigned to driver' || 
                       lowercaseStatus === 'picked up by driver' || 
                       lowercaseStatus === 'in transit') {
              processedOrder.displayStatus = 'Active Order'
            } else if (lowercaseStatus === 'delivered' || 
                       lowercaseStatus === 'delivered by driver' || 
                       lowercaseStatus === 'received by customer') {
              processedOrder.displayStatus = 'Delivered'
            } else {
              processedOrder.displayStatus = 'Pending Delivery Scheduling'
            }
          
            return processedOrder
          })
        
          console.log('Processed Orders:', JSON.stringify(orders.value, null, 2));
        } else {
          console.error('No orders found for this user.')
        }
      } catch (error) {
        console.error('Error fetching order history:', error)
      }
    }

    return { 
      customer, 
      orders,
      sortedOrders,
      activeOrders,
      pendingOrders,
      deliveredOrders, 
      activeTab,
      formatDate, 
      shouldShowDeliveryButton, 
      confirmDelivery,
      scheduleDelivery,
      notification
    }
  }
}
</script>