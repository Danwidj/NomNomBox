<template>
  <div class="success-container">
    <h2>Payment Successful!</h2>
    <p>Thank you for your order. Your payment was successful.</p>
  </div>
</template>

<script>
export default {
  async mounted() {
    const urlParams = new URLSearchParams(window.location.search);
    const sessionId = urlParams.get("session_id");

    if (!sessionId) {
      console.error(" No session_id found in URL.");
      return;
    }

    console.log("Checking payment status for session:", sessionId);

    try {
      // Fetch payment status from backend
      const response = await fetch(`http://localhost:5004/api/payment/status?session_id=${sessionId}`);
      const data = await response.json();

      if (data.status !== "complete") {
        console.error(" Payment not completed.");
        return;
      }

      console.log(" Payment successful! Updating order...");

      //  Send request to update order status
      await fetch("http://localhost:5003/api/orders/update-payment", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          orderId: data.orderId,
          paymentIntentId: sessionId
        })
      });

      console.log(" Order successfully marked as paid!");

    } catch (error) {
      console.error(" Error verifying payment:", error);
    }
  }
};
</script>

<style scoped>
.success-container {
  text-align: center;
  margin-top: 50px;
}
</style>
