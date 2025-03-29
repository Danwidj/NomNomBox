<template>
  <div class="success-container">
    <h2>Payment Successful!</h2>
    <p>Thank you for your order. Your payment was successful.</p>

    <div v-if="!deliveryScheduled" class="delivery-scheduler">
      <h3>Schedule Your Delivery</h3>

      <div class="date-picker">
        <label for="delivery-date">Select Delivery Date:</label>
        <input
          type="date"
          id="delivery-date"
          v-model="selectedDate"
          :min="minDate"
          @change="generateTimeSlots"
        />
      </div>

      <div v-if="timeSlots.length > 0" class="time-slots">
        <h4>Available Time Slots:</h4>
        <div class="slot-grid">
          <button
            v-for="(slot, index) in timeSlots"
            :key="index"
            @click="selectTimeSlot(slot)"
            :class="{ selected: selectedSlot === slot }"
          >
            {{ slot.display }}
          </button>
        </div>
      </div>

      <button class="confirm-btn" @click="scheduleDelivery" :disabled="!selectedSlot">
        Confirm Delivery Slot
      </button>

      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
    </div>

    <div v-else class="confirmation-message">
      <h3>Delivery Scheduled Successfully!</h3>
      <p>
        Your order will be delivered on {{ formattedDeliveryDate }} between
        {{ formattedDeliveryTime }}.
      </p>
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
    } catch (error) {
      console.error('Error verifying payment:', error)
    }
  },
  methods: {
    generateTimeSlots() {
      if (!this.selectedDate) return

      this.timeSlots = []
      this.selectedSlot = null

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

          this.timeSlots.push({
            display,
            startTime: startTime,
            endTime: endTime,
            unixStart: Math.floor(slotDate.getTime() / 1000), // Ensure it's a whole number
            unixEnd: Math.floor((slotDate.getTime() + 30 * 60 * 1000) / 1000), // Add 30 minutes and convert to seconds
          })
        })
      }
    },
    selectTimeSlot(slot) {
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
    },
  },
}
</script>

<style scoped>
.success-container {
  text-align: center;
  margin-top: 50px;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.delivery-scheduler {
  margin-top: 30px;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.date-picker {
  margin: 20px 0;
}

.date-picker input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-left: 10px;
}

.time-slots {
  margin: 20px 0;
}

.slot-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 10px;
  margin-top: 15px;
}

.slot-grid button {
  padding: 10px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.slot-grid button:hover {
  background-color: #f0f0f0;
}

.slot-grid button.selected {
  background-color: #42b983;
  color: white;
  border-color: #42b983;
}

.confirm-btn {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.confirm-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error-message {
  color: #ff4444;
  margin-top: 15px;
}

.confirmation-message {
  margin-top: 30px;
  padding: 20px;
  background-color: #e8f5e9;
  border-radius: 8px;
}
</style>