<template>
  <div class="nom-container py-12 nom-fade-in">
    <div class="max-w-3xl mx-auto nom-card">
      <!-- Success Header -->
      <div class="text-center mb-8">
        <div class="w-16 h-16 bg-primary/20 text-primary rounded-full flex items-center justify-center mx-auto mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
          </svg>
        </div>
        <h2 class="nom-heading mb-2">Payment Successful!</h2>
        <p class="text-muted-foreground text-lg">Thank you for your order. Your payment has been processed successfully.</p>
      </div>

      <!-- Delivery Scheduling Section -->
      <div v-if="!deliveryScheduled" class="mt-8 bg-muted/30 p-6 rounded-lg border border-border">
        <h3 class="text-xl font-semibold mb-4">Schedule Your Delivery</h3>
        <p class="text-muted-foreground mb-6">Choose a convenient date and time for your delivery.</p>

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
            <svg class="animate-spin mr-2 h-4 w-4 text-primary" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
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
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-1">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="16" x2="12" y2="12"></line>
              <line x1="12" y1="8" x2="12.01" y2="8"></line>
            </svg>
            Greyed out slots have no available drivers
          </p>
        </div>

        <!-- No Slots Selected Message -->
        <div v-else-if="selectedDate && timeSlots.length === 0 && !isLoadingSlots" class="mb-6 p-4 bg-destructive/10 text-destructive rounded-md">
          No delivery slots available for the selected date. Please choose another date.
        </div>

        <!-- Confirm Button -->
        <div class="flex flex-col sm:flex-row justify-end gap-3 mt-6">
          <router-link to="/profile" class="nom-btn-outline">
            Skip for Now
          </router-link>
          <button 
            @click="scheduleDelivery" 
            :disabled="!selectedSlot"
            class="nom-btn-primary"
            :class="{'opacity-50 cursor-not-allowed': !selectedSlot}"
          >
            Confirm Delivery Slot
          </button>
        </div>

        <!-- Error Message -->
        <div v-if="errorMessage" class="mt-4 p-3 bg-destructive/10 text-destructive rounded-md text-sm">
          {{ errorMessage }}
        </div>
      </div>

      <!-- Confirmation Message -->
      <div v-else class="mt-8 bg-primary/10 p-6 rounded-lg border border-primary/20 nom-fade-in">
        <div class="flex items-center gap-4 mb-4">
          <div class="w-10 h-10 bg-primary/20 text-primary rounded-full flex items-center justify-center shrink-0">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
            </svg>
          </div>
          <h3 class="text-xl font-semibold">Delivery Scheduled Successfully!</h3>
        </div>
        
        <div class="flex flex-col sm:flex-row gap-6 mb-4">
          <div class="p-4 bg-background rounded-md flex-1">
            <p class="text-muted-foreground text-sm mb-1">Delivery Date</p>
            <p class="font-medium">{{ formattedDeliveryDate }}</p>
          </div>
          <div class="p-4 bg-background rounded-md flex-1">
            <p class="text-muted-foreground text-sm mb-1">Delivery Time</p>
            <p class="font-medium">{{ formattedDeliveryTime }}</p>
          </div>
        </div>
        
        <p class="text-muted-foreground">
          Your order will be delivered on the scheduled date and time. You can track your order status in your profile.
        </p>

        <div class="flex justify-center mt-6">
          <router-link to="/profile" class="nom-btn-primary">
            Go to My Orders
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedDate: '',
      minDate: '',
      timeSlots: [],
      selectedSlot: null,
      deliveryScheduled: false,
      errorMessage: '',
      orderId: null,
      userId: null,
      deliveryTime: null,
      formattedDeliveryDate: '',
      formattedDeliveryTime: '',
      availableSlots: [],
      isLoadingSlots: false,
    }
  },
  async mounted() {
    // Set minimum date to tomorrow
    const tomorrow = new Date()
    tomorrow.setDate(tomorrow.getDate() + 1)
    this.minDate = tomorrow.toISOString().split('T')[0]

    // Get user ID from localStorage
    this.userId = localStorage.getItem('customerId') || sessionStorage.getItem('customerId')

    const urlParams = new URLSearchParams(window.location.search)
    const sessionId = urlParams.get('session_id')

    if (!sessionId) {
      console.error('No session_id found in URL.')
      return
    }

    try {
      // Fetch payment status to get orderId
      const response = await fetch(
        `http://localhost:5004/api/payment/status?session_id=${sessionId}`,
      )
      const data = await response.json()

      if (data.status !== 'complete') {
        console.error('Payment not completed.')
        return
      }

      this.orderId = data.orderId
      if (!this.orderId) {
        console.error('No orderId found in payment status response.')
        return
      }

      console.log('Payment confirmed for order:', this.orderId)
      const token = localStorage.getItem('token') || sessionStorage.getItem('token') || ''
    const finalizePayload = {
      session_id: sessionId,
      orderId: this.orderId,
      user_id: this.userId,
      token: token // so the backend can fetch user’s email
    }

    console.log('Calling /order/payment-success with:', finalizePayload)

    const finalizeResponse = await fetch('http://localhost:5005/order/payment-success', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}` // if your composite needs auth
      },
      body: JSON.stringify(finalizePayload),
    })

    const finalizeData = await finalizeResponse.json()
    if (finalizeResponse.ok) {
      sessionStorage.removeItem('shoppingCart')
      console.log('Payment finalized on backend, email should be sent now:', finalizeData)
    } else {
      console.error('Error finalizing payment success:', finalizeData)
    }

    } catch (error) {
      console.error('Error verifying payment:', error)
    }
  },
  methods: {
    async generateTimeSlots() {
      if (!this.selectedDate) return

      this.timeSlots = []
      this.selectedSlot = null
      this.isLoadingSlots = true
      this.availableSlots = await this.fetchAvailableSlots()

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
          const slotDate = new Date(this.selectedDate)
          slotDate.setHours(time.hour, time.minute, 0, 0)
          
          const unixTime = Math.floor(slotDate.getTime() / 1000)
          
          // Check if this slot is available by comparing with available slots from server
          const isAvailable = this.availableSlots.includes(unixTime)

          this.timeSlots.push({
            display,
            startTime: startTime,
            endTime: endTime,
            unixStart: unixTime,
            unixEnd: Math.floor((slotDate.getTime() + 30 * 60 * 1000) / 1000), // Add 30 minutes and convert to seconds
            available: isAvailable
          })
        })
      }
      
      this.isLoadingSlots = false
    },
    
    async fetchAvailableSlots() {
      // Get start and end timestamps for the selected day
      const selectedDate = new Date(this.selectedDate)
      const startOfDay = new Date(selectedDate.setHours(0, 0, 0, 0))
      const endOfDay = new Date(selectedDate.setHours(23, 59, 59, 999))
      
      const startTimestamp = Math.floor(startOfDay.getTime() / 1000)
      const endTimestamp = Math.floor(endOfDay.getTime() / 1000)
      
      try {
        const response = await fetch(
          `http://localhost:5007/available_slots?start=${startTimestamp}&end=${endTimestamp}`
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
    },
    
    getSlotClasses(slot) {
      if (this.selectedSlot === slot) {
        return 'bg-primary text-primary-foreground border-primary'
      }
      
      if (!slot.available) {
        return 'bg-muted/30 text-muted-foreground/50 border-border cursor-not-allowed'
      }
      
      return 'bg-card hover:bg-muted/50 border-border'
    },
    
    selectTimeSlot(slot) {
      if (!slot.available) return
      
      this.selectedSlot = slot
      this.errorMessage = ''
    },
    
    async scheduleDelivery() {
      if (!this.selectedSlot) {
        this.errorMessage = 'Please select a delivery slot'
        return
      }
    
      if (!this.orderId) {
        this.errorMessage = 'Order ID is not available'
        return
      }
    
      if (!this.userId) {
        this.errorMessage = 'User ID is not available'
        return
      }
    
      // Get token from storage
      const token = localStorage.getItem('token') || sessionStorage.getItem('token')
      if (!token) {
        this.errorMessage = 'Authentication token is not available'
        return
      }
    
      const deliveryData = {
        user_id: this.userId,
        order_id: this.orderId,
        delivery_time: this.selectedSlot.unixStart,
      }
    
      try {
        console.log('Sending delivery request:', deliveryData)
        const response = await fetch('http://localhost:5000/place_delivery_request', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(deliveryData),
        })
      
        const result = await response.json()
      
        if (response.status !== 200) {
          this.errorMessage =
            result.message || 'Failed to schedule delivery. Please try another slot.'
          console.error('Delivery scheduling failed:', result)
          return
        }
      
        // Delivery scheduled successfully
        this.deliveryScheduled = true
        this.deliveryTime = this.selectedSlot.unixStart
      
        // Format for display
        const deliveryDate = new Date(this.selectedSlot.unixStart * 1000) // Convert from Unix timestamp
        this.formattedDeliveryDate = deliveryDate.toLocaleDateString('en-US', {
          weekday: 'long',
          year: 'numeric',
          month: 'long',
          day: 'numeric',
        })
        this.formattedDeliveryTime = `${this.selectedSlot.startTime} - ${this.selectedSlot.endTime}`
      
        // Clear cart and delivery slot from storage
        sessionStorage.removeItem('shoppingCart')
        localStorage.removeItem('currentOrderId')
        sessionStorage.removeItem('deliveryTimeSlot')
      } catch (error) {
        console.error('Error scheduling delivery:', error)
        this.errorMessage = 'An error occurred. Please try again.'
      }
    }
  },
}
</script>