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

      <!-- Empty State for Tab with No Orders -->
      <div v-else-if="(activeTab === 'active' && activeOrders.length === 0) || (activeTab === 'delivered' && deliveredOrders.length === 0)" class="nom-card py-8 text-center">
        <div class="flex flex-col items-center justify-center space-y-4">
          <svg class="w-12 h-12 text-muted-foreground/40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 5H7C5.89543 5 5 5.89543 5 7V19C5 20.1046 5.89543 21 7 21H17C18.1046 21 19 20.1046 19 19V7C19 5.89543 18.1046 5 17 5H15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M9 5C9 3.89543 9.89543 3 11 3H13C14.1046 3 15 3.89543 15 5V7H9V5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <p class="text-lg text-muted-foreground">
            {{ activeTab === 'active' ? 'No active orders at the moment.' : 'No delivered orders yet.' }}
          </p>
          <div v-if="activeTab === 'active'" class="mt-2">
            <router-link to="/" class="nom-btn-primary">Browse Products</router-link>
          </div>
          <div v-else class="mt-2">
            <button @click="activeTab = 'active'" class="nom-btn-outline">View Active Orders</button>
          </div>
        </div>
      </div>

      <!-- Active Orders Tab Content -->
      <div v-else-if="activeTab === 'active'" class="space-y-6 nom-fade-in">
        <div 
          class="nom-card nom-card-hover" 
          v-for="order in activeOrders" 
          :key="order.orderId"
        >
          <!-- Order Header -->
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6">
            <div>
              <h3 class="text-lg font-semibold">Order #{{ order.orderId }}</h3>
              <p class="text-muted-foreground">{{ formatDate(order.createdAt) }}</p>
              <p v-if="order.deliveryDate" class="text-muted-foreground text-sm">
                Expected Delivery: {{ formatDate(order.deliveryDate) }}
              </p>
            </div>
            
            <div class="mt-2 sm:mt-0 flex flex-col sm:items-end gap-2">
              <span 
                :class="[
                  'px-3 py-1 rounded-full text-sm font-medium',
                  {
                    'bg-destructive/10 text-destructive': order.status.toLowerCase() === 'canceled',
                    'bg-primary/10 text-primary': order.status.toLowerCase() === 'paid',
                    'bg-secondary/10 text-secondary': order.status.toLowerCase() === 'pending',
                    'bg-green-100 text-green-800': order.status === 'Received by Customer',
                    'bg-amber-100 text-amber-800': order.status === 'Delivered by Driver',
                    'bg-blue-100 text-blue-800': order.status === 'Picked up by Driver',
                    'bg-violet-100 text-violet-800': order.status === 'Assigned To Driver'
                  }
                ]"
              >
                {{ order.status }}
              </span>
              
              <!-- Delivery Confirmation Button -->
              <button 
                v-if="shouldShowDeliveryButton(order)"
                @click="confirmDelivery(order.orderId)"
                class="px-3 py-1.5 text-sm font-medium bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors flex items-center gap-1"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-1">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                  <polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
                Order Received
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
import { useRouter } from 'vue-router'

export default {
  name: 'ProfilePage',
  setup() {
    const router = useRouter()
    const customer = ref({
      customerId: '',
      name: '',
      email: '',
      address: '',
      phone: '',
      dietary_preferences: [],
    })
    const orders = ref([])
    const activeTab = ref('active') // Default to active orders tab

    // Compute sorted orders by date (newest first)
    const sortedOrders = computed(() => {
      return [...orders.value].sort((a, b) => {
        const dateA = getDateFromTimestamp(a.createdAt)
        const dateB = getDateFromTimestamp(b.createdAt)
        return dateB - dateA
      })
    })

    // Filter orders for active tab (not delivered or received)
    const activeOrders = computed(() => {
      return sortedOrders.value.filter(order => 
        order.status.toLowerCase() !== 'delivered' && 
        order.status.toLowerCase() !== 'canceled' &&
        order.status.toLowerCase() !== 'received by customer'
      )
    })

    // Filter orders for delivered tab (including both delivered and received)
    const deliveredOrders = computed(() => {
      return sortedOrders.value.filter(order => 
        order.status.toLowerCase() === 'delivered' ||
        order.status.toLowerCase() === 'delivered by driver' ||
        order.status.toLowerCase() === 'received by customer'
      )
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
      } catch (error) {
        console.error('Failed to load profile:', error)
      }
    })
    
    const fetchUserData = async (customerId, token) => {
      try {
        const response = await fetch(`http://localhost:5003/customer/${customerId}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
        })

        const data = await response.json()
        console.log('Customer API Response:', data)

        if (data.code === 200) {
          customer.value = data.data
          
          // Ensure dietary_preferences is an array
          if (!Array.isArray(customer.value.dietary_preferences)) {
            customer.value.dietary_preferences = []
          }
          
          console.log('Customer Data Loaded:', customer.value)
        } else {
          console.error('Failed to fetch customer data:', data.message)
        }
      } catch (error) {
        console.error('Error fetching customer data:', error)
      }
    }

    const fetchOrderHistory = async (customerId) => {
      try {
        const response = await fetch(
          `http://localhost:5001/api/orders/customer/${customerId}`,
        )
        const data = await response.json()

        if (data.code === 200) {
          // Add default deliveryDate for demo purposes if it doesn't exist
          orders.value = data.data.map(order => {
            if (!order.deliveryDate) {
              // Set delivery date to be 3 days after order creation
              const createdDate = getDateFromTimestamp(order.createdAt)
              const deliveryDate = new Date(createdDate)
              deliveryDate.setDate(deliveryDate.getDate() + 3)
              return {...order, deliveryDate: deliveryDate.toISOString()}
            }
            return order
          })
        } else {
          console.error('No orders found for this user.')
        }
      } catch (error) {
        console.error('Error fetching order history:', error)
      }
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

    const formatDate = (timestamp) => {
      if (!timestamp) return 'Unknown Date'

      // Handle Firestore Timestamp (if it exists)
      if (typeof timestamp === 'object' && 'seconds' in timestamp) {
        const date = new Date(timestamp.seconds * 1000)
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

      // Handle JavaScript Date (if stored as a string)
      const date = new Date(timestamp)
      if (isNaN(date)) return 'Unknown Date'

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

    return { 
      customer, 
      orders,
      sortedOrders,
      activeOrders,
      deliveredOrders, 
      activeTab,
      formatDate, 
      shouldShowDeliveryButton, 
      confirmDelivery 
    }
  },
}
</script>