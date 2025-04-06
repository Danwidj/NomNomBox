<template>
    <div class="nom-container py-12 nom-fade-in">
      <div class="max-w-3xl mx-auto nom-card">
        <!-- Delivery Scheduling Section -->
        <div class="mt-8 p-6">
          <h2 class="text-2xl font-semibold mb-4">Schedule Your Delivery</h2>
          <p class="text-muted-foreground mb-6">
            Order #{{ orderId }}: Choose a convenient date and time for your delivery.
          </p>
  
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
              Cancel
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
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  
  export default {
    name: 'DeliverySchedulePage',
    setup() {
      const route = useRoute()
      const router = useRouter()
  
      const orderId = ref(null)
      const selectedDate = ref('')
      const minDate = ref('')
      const timeSlots = ref([])
      const selectedSlot = ref(null)
      const errorMessage = ref('')
      const availableSlots = ref([])
      const isLoadingSlots = ref(false)
  
      // Set minimum date to tomorrow
      onMounted(() => {
        const tomorrow = new Date()
        tomorrow.setDate(tomorrow.getDate() + 1)
        minDate.value = tomorrow.toISOString().split('T')[0]
  
        // Get orderId from route query
        orderId.value = route.query.orderId
        if (!orderId.value) {
          router.push('/profile')
        }
      })
  
      const generateTimeSlots = async () => {
        if (!selectedDate.value) return
  
        timeSlots.value = []
        selectedSlot.value = null
        isLoadingSlots.value = true
        
        // Pass the selected date explicitly to fetchAvailableSlots
        availableSlots.value = await fetchAvailableSlots(selectedDate.value)
  
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
            const isAvailable = availableSlots.value.includes(unixTime)
  
            timeSlots.value.push({
              display,
              startTime: startTime,
              endTime: endTime,
              unixStart: unixTime,
              unixEnd: Math.floor((slotDate.getTime() + 30 * 60 * 1000) / 1000), // Add 30 minutes and convert to seconds
              available: isAvailable
            })
          })
        }
        
        isLoadingSlots.value = false
      }
  
      const fetchAvailableSlots = async (selectedDateValue) => {
        // Validate the selectedDateValue was passed
        if (!selectedDateValue) {
          console.error('No date selected')
          return []
        }

        // Get start and end timestamps for the selected day
        const selectedDate = new Date(selectedDateValue)
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
      }
  
      const getSlotClasses = (slot) => {
        if (selectedSlot.value === slot) {
          return 'bg-primary text-primary-foreground border-primary'
        }
        
        if (!slot.available) {
          return 'bg-muted/30 text-muted-foreground/50 border-border cursor-not-allowed'
        }
        
        return 'bg-card hover:bg-muted/50 border-border'
      }
  
      const selectTimeSlot = (slot) => {
        if (!slot.available) return
        
        selectedSlot.value = slot
        errorMessage.value = ''
      }
  
      const scheduleDelivery = async () => {
        if (!selectedSlot.value) {
          errorMessage.value = 'Please select a delivery slot'
          return
        }
      
        if (!orderId.value) {
          errorMessage.value = 'Order ID is not available'
          return
        }
      
        // Get user ID from localStorage
        const userId = localStorage.getItem('customerId') || sessionStorage.getItem('customerId')
        
        if (!userId) {
          errorMessage.value = 'User ID is not available'
          return
        }
      
        // Get token from storage
        const token = localStorage.getItem('token') || sessionStorage.getItem('token')
        if (!token) {
          errorMessage.value = 'Authentication token is not available'
          return
        }
      
        const deliveryData = {
          user_id: userId,
          order_id: orderId.value,
          delivery_time: selectedSlot.value.unixStart,
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
            errorMessage.value =
              result.message || 'Failed to schedule delivery. Please try another slot.'
            console.error('Delivery scheduling failed:', result)
            return
          }
        
          // Update order status to "Assigned to Driver"
          await updateOrderStatus(orderId.value, token)
          // Add a more detailed success handling
          const deliveryConfirmation = {
            orderId: orderId.value,
            deliveryDate: new Date(selectedSlot.value.unixStart * 1000).toLocaleString('en-US', {
              timeZone: 'Asia/Singapore',
              weekday: 'long',
              year: 'numeric',
              month: 'long',
              day: 'numeric',
              hour: '2-digit',
              minute: '2-digit',
              hour12: true
            }),
            deliveryTimeSlot: selectedSlot.value.display
          }
      
          // Store delivery confirmation details in localStorage
          localStorage.setItem('deliveryConfirmation', JSON.stringify(deliveryConfirmation))
          
          // Redirect to profile with success message
          router.push({
              path: '/profile',
              query: { 
                deliveryScheduled: 'true',
                orderId: orderId.value,
                deliveryTime: selectedSlot.value.unixStart
              }
            })
            
        } catch (error) {
          console.error('Error scheduling delivery:', error)
          errorMessage.value = 'An error occurred. Please try again.'
        }
      }
  
      const updateOrderStatus = async (orderId, token) => {
        try {
          const response = await fetch(`http://localhost:5001/api/orders/${orderId}/status`, {
            method: 'PATCH',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
              status: 'Assigned To Driver',
              deliveryTime: selectedSlot.value.unixStart // Include the selected delivery time
            })
          })

          const result = await response.json()

          if (result.code !== 200) {
            console.error('Failed to update order status:', result.message)
          }
        } catch (error) {
          console.error('Error updating order status:', error)
        }
      }
  
      return {
        orderId,
        selectedDate,
        minDate,
        timeSlots,
        selectedSlot,
        errorMessage,
        isLoadingSlots,
        generateTimeSlots,
        getSlotClasses,
        selectTimeSlot,
        scheduleDelivery
      }
    }
  }
  </script>