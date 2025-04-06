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
        <p class="text-muted-foreground text-lg mb-8">Thank you for your order. Your payment has been processed successfully.</p>
        
        <div class="bg-primary/10 p-6 rounded-lg border border-primary/20 max-w-xl mx-auto">
          <p class="text-lg font-medium mb-4">Next Step: Schedule Your Delivery</p>
          <p class="text-muted-foreground mb-6">
            Please go to your profile page to schedule a convenient delivery time for your order.
          </p>
          <router-link to="/profile" class="nom-btn-primary mx-auto inline-flex">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2">
              <path d="M19 12H5M12 19l-7-7 7-7"></path>
            </svg>
            Go to My Profile
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  async mounted() {
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

      const orderId = data.orderId
      if (!orderId) {
        console.error('No orderId found in payment status response.')
        return
      }

      console.log('Payment confirmed for order:', orderId)

      // Store the orderId in localStorage so we can reference it on the profile page
      localStorage.setItem('pendingDeliveryOrderId', orderId)
      
      // Get current user ID
      const userId = localStorage.getItem('customerId') || sessionStorage.getItem('customerId')
      const token = localStorage.getItem('token') || sessionStorage.getItem('token') || ''
      
      // Finalize the payment on the backend
      const finalizePayload = {
        session_id: sessionId,
        orderId: orderId,
        user_id: userId,
        token: token
      }

      console.log('Calling /order/payment-success with:', finalizePayload)

      const finalizeResponse = await fetch('http://localhost:5005/order/payment-success', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
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
  }
}
</script>