<template>
  <div class="nom-container py-8 nom-fade-in">
    <div class="max-w-3xl mx-auto">
      <!-- Back Button -->
      <div class="mb-6">
        <router-link
          to="/profile"
          class="inline-flex items-center text-muted-foreground hover:text-foreground transition-colors"
        >
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
            class="mr-2"
          >
            <path d="M19 12H5M12 19l-7-7 7-7"></path>
          </svg>
          Back to Profile
        </router-link>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="nom-card py-16 text-center">
        <div class="flex flex-col items-center justify-center">
          <svg
            class="animate-spin w-10 h-10 text-primary mb-4"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              class="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
            ></circle>
            <path
              class="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
          <p class="text-lg text-muted-foreground">Loading order details...</p>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="errorMessage" class="nom-card py-12 text-center">
        <div class="flex flex-col items-center justify-center space-y-4">
          <svg
            class="w-16 h-16 text-destructive/60"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"></circle>
            <line x1="12" y1="8" x2="12" y2="12" stroke="currentColor" stroke-width="2"></line>
            <line x1="12" y1="16" x2="12.01" y2="16" stroke="currentColor" stroke-width="2"></line>
          </svg>
          <p class="text-xl text-muted-foreground">{{ errorMessage }}</p>
          <router-link to="/profile" class="nom-btn-primary mt-4">Return to Profile</router-link>
        </div>
      </div>

      <!-- Delivery Scheduling Content -->
      <div v-else class="space-y-6 nom-fade-in">
        <div class="nom-card">
          <h2 class="text-2xl font-semibold mb-6">Schedule Delivery</h2>

          <!-- Order Summary -->
          <div class="bg-muted/20 p-4 rounded-md mb-6">
            <div class="flex flex-col md:flex-row justify-between mb-2">
              <div>
                <p class="text-sm text-muted-foreground">Order #</p>
                <p class="font-medium">{{ order.orderId }}</p>
              </div>
              <div>
                <p class="text-sm text-muted-foreground">Date Placed</p>
                <p class="font-medium">{{ formatDate(order.createdAt) }}</p>
              </div>
              <div>
                <p class="text-sm text-muted-foreground">Total Amount</p>
                <p class="font-semibold text-primary">${{ order.totalPrice?.toFixed(2) }}</p>
              </div>
            </div>
            <div class="mt-2">
              <p class="text-sm text-muted-foreground">Status</p>
              <p class="mt-1">
                <span
                  class="px-3 py-1 rounded-full text-sm font-medium bg-secondary/10 text-secondary"
                >
                  {{ order.status }}
                </span>
              </p>
            </div>
          </div>

          <!-- Delivery Scheduling Section -->
          <h3 class="text-lg font-medium mb-4">Select Delivery Date and Time</h3>

          <!-- Date Picker -->
          <div class="mb-6">
            <label for="delivery-date" class="nom-label">Select Delivery Date:</label>
            <input
              type="date"
              id="delivery-date"
              v-model="selectedDate"
              :min="minDate"
              @change="generateTimeSlots"
              class="nom-input"
            />
            <div v-if="isLoadingSlots" class="mt-2 text-muted-foreground text-sm flex items-center">
              <svg
                class="animate-spin mr-2 h-4 w-4 text-primary"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  class="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  stroke-width="4"
                ></circle>
                <path
                  class="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
              Loading available slots...
            </div>
          </div>

          <!-- Time Slots -->
          <div v-if="selectedDate && timeSlots.length > 0" class="mb-6 nom-fade-in">
            <label class="nom-label mb-3">Available Time Slots:</label>
            <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
              <button
                v-for="(slot, index) in timeSlots"
                :key="index"
                @click="slot.available ? selectTimeSlot(slot) : null"
                class="p-3 rounded-md border transition-all duration-200 text-sm"
                :class="getSlotClasses(slot)"
                :disabled="!slot.available"
              >
                {{ slot.display }}
              </button>
            </div>
            <p class="mt-2 text-muted-foreground text-sm flex items-center">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="mr-1"
              >
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="16" x2="12" y2="12"></line>
                <line x1="12" y1="8" x2="12.01" y2="8"></line>
              </svg>
              Greyed out slots have no available drivers
            </p>
          </div>

          <!-- No Slots Selected Message -->
          <div
            v-else-if="selectedDate && timeSlots.length === 0 && !isLoadingSlots"
            class="mb-6 p-4 bg-destructive/10 text-destructive rounded-md"
          >
            No delivery slots available for the selected date. Please choose another date.
          </div>

          <!-- Schedule Button -->
          <div class="flex justify-end gap-3 mt-8">
            <router-link to="/profile" class="nom-btn-outline"> Cancel </router-link>
            <button
              @click="scheduleDelivery"
              :disabled="!selectedSlot"
              class="nom-btn-primary"
              :class="{ 'opacity-50 cursor-not-allowed': !selectedSlot }"
            >
              Confirm Delivery Time
            </button>
          </div>

          <!-- Error Message -->
          <div
            v-if="scheduleError"
            class="mt-4 p-3 bg-destructive/10 text-destructive rounded-md text-sm"
          >
            {{ scheduleError }}
          </div>
        </div>

        <!-- Order Details Card -->
        <div class="nom-card">
          <h3 class="text-lg font-medium mb-4">Order Details</h3>

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

    <!-- Success Modal -->
    <div
      v-if="showSuccessModal"
      class="fixed inset-0 bg-foreground/20 backdrop-blur-sm z-50 flex items-center justify-center p-4"
    >
      <div class="bg-card border border-border rounded-lg shadow-lg w-full max-w-md nom-slide-up">
        <div class="p-6">
          <div class="flex justify-end">
            <button
              @click="closeSuccessModal"
              class="p-1 rounded-full hover:bg-muted transition-colors"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>

          <div class="text-center mb-6">
            <div
              class="w-16 h-16 bg-primary/20 text-primary rounded-full flex items-center justify-center mx-auto mb-4"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="32"
                height="32"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                <polyline points="22 4 12 14.01 9 11.01"></polyline>
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">Delivery Scheduled!</h3>
            <p class="text-muted-foreground">
              Your order delivery has been scheduled successfully.
            </p>
          </div>

          <div class="space-y-4 mb-6">
            <div class="p-4 bg-muted/30 rounded-md">
              <p class="text-muted-foreground text-sm mb-1">Delivery Date</p>
              <p class="font-medium">{{ formattedDeliveryDate }}</p>
            </div>
            <div class="p-4 bg-muted/30 rounded-md">
              <p class="text-muted-foreground text-sm mb-1">Delivery Time</p>
              <p class="font-medium">{{ formattedDeliveryTime }}</p>
            </div>
          </div>

          <div class="flex justify-center">
            <router-link to="/profile" class="nom-btn-primary"> Go to My Orders </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default {
  name: 'ScheduleDeliveryPage',
  setup() {
    const route = useRoute()
    const router = useRouter()

    // State variables
    const orderId = ref('')
    const order = ref({})
    const isLoading = ref(true)
    const errorMessage = ref('')
    const selectedDate = ref('')
    const timeSlots = ref([])
    const selectedSlot = ref(null)
    const isLoadingSlots = ref(false)
    const scheduleError = ref('')
    const showSuccessModal = ref(false)
    const formattedDeliveryDate = ref('')
    const formattedDeliveryTime = ref('')

    // Set minimum date to tomorrow
    const today = new Date()
    const tomorrow = new Date(today)
    tomorrow.setDate(tomorrow.getDate() + 1)
    const minDate = ref(tomorrow.toISOString().split('T')[0])

    onMounted(async () => {
      // Get order ID from route params
      orderId.value = route.params.orderId

      if (!orderId.value) {
        errorMessage.value = 'No order ID provided.'
        isLoading.value = false
        return
      }

      // Check if user is authenticated
      const token = localStorage.getItem('token')
      const userId = localStorage.getItem('userId')

      if (!token || !userId) {
        errorMessage.value = 'You need to be logged in to schedule a delivery.'
        isLoading.value = false
        router.push('/login')
        return
      }

      try {
        // Fetch order details
        const response = await fetch(`http://localhost:5001/api/orders/${orderId.value}`)
        const data = await response.json()

        if (data.code !== 200) {
          errorMessage.value = 'Failed to load order details. Please try again.'
          isLoading.value = false
          return
        }

        order.value = data.data

        // Verify this order belongs to the current user
        if (order.value.customerId !== userId) {
          errorMessage.value = 'You do not have permission to schedule delivery for this order.'
          isLoading.value = false
          return
        }

        // Verify order is in a valid state for scheduling
        if (order.value.status.toLowerCase() !== 'paid') {
          errorMessage.value = 'This order is not eligible for delivery scheduling.'
          isLoading.value = false
          return
        }

        isLoading.value = false
      } catch (error) {
        console.error('Error fetching order details:', error)
        errorMessage.value = 'An error occurred while loading order details.'
        isLoading.value = false
      }
    })

    // Generate time slots for selected date
    const generateTimeSlots = async () => {
      if (!selectedDate.value) return

      timeSlots.value = []
      selectedSlot.value = null
      isLoadingSlots.value = true
      const availableSlots = await fetchAvailableSlots()

      // Generate time slots from 08:00 to 22:00 in 30-minute increments
      const startHour = 8
      const endHour = 23

      for (let hour = startHour; hour < endHour; hour++) {
        // Create slots for :00 and :30 of each hour
        const times = [
          { hour, minute: 0 },
          { hour, minute: 30 },
        ]

        times.forEach((time) => {
          if (hour === endHour - 1 && time.minute === 30) return // Skip 22:30

          const startTime = `${time.hour.toString().padStart(2, '0')}:${time.minute.toString().padStart(2, '0')}`
          const endTime =
            time.minute === 30
              ? `${(time.hour + 1).toString().padStart(2, '0')}:00`
              : `${time.hour.toString().padStart(2, '0')}:30`

          const display = `${startTime} - ${endTime}`

          // Create Date object for the selected date and time
          const slotDate = new Date(selectedDate.value)
          slotDate.setHours(time.hour, time.minute, 0, 0)

          const unixTime = Math.floor(slotDate.getTime() / 1000)

          // Check if this slot is available by comparing with available slots from server
          const isAvailable = availableSlots.includes(unixTime)

          timeSlots.value.push({
            display,
            startTime,
            endTime,
            unixStart: unixTime,
            unixEnd: Math.floor((slotDate.getTime() + 30 * 60 * 1000) / 1000), // Add 30 minutes and convert to seconds
            available: isAvailable,
          })
        })
      }

      isLoadingSlots.value = false
    }

    // Fetch available slots from the backend
    const fetchAvailableSlots = async () => {
      // Get start and end timestamps for the selected day
      const selectedDateObj = new Date(selectedDate.value)
      const startOfDay = new Date(selectedDateObj)
      startOfDay.setHours(0, 0, 0, 0)

      const endOfDay = new Date(selectedDateObj)
      endOfDay.setHours(23, 59, 59, 999)

      const startTimestamp = Math.floor(startOfDay.getTime() / 1000)
      const endTimestamp = Math.floor(endOfDay.getTime() / 1000)

      try {
        const response = await fetch(
          `http://localhost:5007/available_slots?start=${startTimestamp}&end=${endTimestamp}`,
        )

        if (!response.ok) {
          console.error('Failed to fetch available slots:', response.statusText)
          return []
        }

        const data = await response.json()

        if (data.code === 200 && Array.isArray(data.data)) {
          return data.data
        }

        return []
      } catch (error) {
        console.error('Error fetching available slots:', error)
        return []
      }
    }

    // Get CSS classes for time slots based on selection and availability
    const getSlotClasses = (slot) => {
      if (selectedSlot.value === slot) {
        return 'bg-primary text-primary-foreground border-primary'
      }

      if (!slot.available) {
        return 'bg-muted/30 text-muted-foreground/50 border-border cursor-not-allowed'
      }

      return 'bg-card hover:bg-muted/50 border-border'
    }

    // Select a time slot
    const selectTimeSlot = (slot) => {
      if (!slot.available) return

      selectedSlot.value = slot
      scheduleError.value = ''
    }

    // Format date for display
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

    // Schedule delivery
    const scheduleDelivery = async () => {
      if (!selectedSlot.value) {
        scheduleError.value = 'Please select a delivery slot'
        return
      }

      const userId = localStorage.getItem('userId')
      if (!userId) {
        scheduleError.value = 'User ID is not available'
        return
      }

      // Get token from storage
      const token = localStorage.getItem('token')
      if (!token) {
        scheduleError.value = 'Authentication token is not available'
        return
      }

      const deliveryData = {
        user_id: userId,
        order_id: orderId.value,
        delivery_time: selectedSlot.value.unixStart,
      }

      try {
        console.log('Sending delivery request:', deliveryData)

        // Make the actual API call to schedule the delivery
        // Place delivery request
        const response = await fetch('http://localhost:5014', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(deliveryData),
        })

        const result = await response.json()

        if (response.status !== 200 || result.code !== 200) {
          scheduleError.value =
            result.message || 'Failed to schedule delivery. Please try another slot.'
          console.error('Delivery scheduling failed:', result)
          return
        }

        // If we get here, the delivery was scheduled successfully
        console.log('Delivery scheduled successfully:', result)

        // Store the delivery ID if it's in the response
        if (result.data && result.data.id) {
          localStorage.setItem(`order_${orderId.value}_deliveryId`, result.data.id)
        }

        // Also store the delivery time and status in localStorage as a fallback
        localStorage.setItem(
          `order_${orderId.value}_deliveryTime`,
          selectedSlot.value.unixStart.toString(),
        )
        localStorage.setItem(`order_${orderId.value}_status`, 'Assigned To Driver')

        // Create delivery date for display
        const deliveryDate = new Date(selectedSlot.value.unixStart * 1000)
        formattedDeliveryDate.value = deliveryDate.toLocaleDateString('en-US', {
          weekday: 'long',
          year: 'numeric',
          month: 'long',
          day: 'numeric',
        })
        formattedDeliveryTime.value = `${selectedSlot.value.startTime} - ${selectedSlot.value.endTime}`

        // Show success modal
        showSuccessModal.value = true

        // Redirect after 5 seconds
        setTimeout(() => {
          showSuccessModal.value = false
          router.push('/profile')
        }, 5000)
      } catch (error) {
        console.error('Error scheduling delivery:', error)
        scheduleError.value = 'An error occurred during scheduling. Please try again later.'
      }
    }

    // Close success modal
    const closeSuccessModal = () => {
      showSuccessModal.value = false
      router.push('/profile')
    }

    return {
      orderId,
      order,
      isLoading,
      errorMessage,
      selectedDate,
      minDate,
      timeSlots,
      selectedSlot,
      isLoadingSlots,
      scheduleError,
      showSuccessModal,
      formattedDeliveryDate,
      formattedDeliveryTime,
      formatDate,
      generateTimeSlots,
      getSlotClasses,
      selectTimeSlot,
      scheduleDelivery,
      closeSuccessModal,
    }
  },
}
</script>
