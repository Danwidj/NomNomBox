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
      console.error("No session_id found in URL.");
      return;
    }

    console.log("Checking payment status for session:", sessionId);

    try {
      // Fetch payment status from backend to get the correct orderId
      const response = await fetch(`http://localhost:5004/api/payment/status?session_id=${sessionId}`);
      const data = await response.json();

      if (data.status !== "complete") {
        console.error("Payment not completed.");
        return;
      }

      const orderId = data.orderId; //  Get orderId from backend response

      if (!orderId) {
        console.error("No orderId found in payment status response.");
        return;
      }

      console.log("Payment confirmed for order:", orderId);

      // Notify backend that payment was successful
      const updateResponse = await fetch("http://localhost:5005/order/payment-success", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ orderId, session_id: sessionId }) // Send correct orderId
      });

      const result = await updateResponse.json();

      if (updateResponse.status !== 200) {
        console.error("Payment processing failed:", result.message);
        return;
      }

      console.log("Payment confirmed, order updated, and stock adjusted!");

      // Clear cart after successful order and stock update
      sessionStorage.removeItem("shoppingCart");
      localStorage.removeItem("currentOrderId");

      console.log("Cart cleared after successful payment!");

    } catch (error) {
      console.error("Error verifying payment:", error);
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