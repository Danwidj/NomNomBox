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
        // 3. Now retrieve userId and delivery time slot from sessionStorage
      const userId = sessionStorage.getItem("customerId");

      // Notify backend that payment was successful
      const updateResponse = await fetch("http://localhost:5005/order/payment-success", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ orderId, session_id: sessionId, user_id: userId  }) // Send correct orderId
      });

      const result = await updateResponse.json();

      if (updateResponse.status !== 200) {
        console.error("Payment processing failed:", result.message);
        return;
      }

      console.log("Payment confirmed, order updated, and stock adjusted!");
    
      const deliveryTimeString = sessionStorage.getItem("deliveryTimeSlot"); 
      // e.g., "08:00 - 08:30"

      // If you just want to log the string:
      console.log("Selected Delivery Slot:", deliveryTimeString);

      // If you want to parse "08:00 - 08:30" into a Unix timestamp for the start time of 08:00:
      // You need to decide a date (e.g., today's date) or a specific date for that time. 
      const today = new Date();
      const [startTime, endTime] = deliveryTimeString.split(" - "); //  split both
      const [startHour, startMin] = startTime.split(":");
      const [endHour, endMin] = endTime.split(":");

      // Build a Date for 'today' at 8:00
      const deliveryStart = new Date(
      today.getFullYear(),
      today.getMonth(),
      today.getDate(),
      parseInt(startHour),
      parseInt(startMin),
      0,
      0
    );

    const deliveryEnd = new Date(
      today.getFullYear(),
      today.getMonth(),
      today.getDate(),
      parseInt(endHour),
      parseInt(endMin),
      0,
      0
    );

    const unixStart = deliveryStart.getTime();
    const unixEnd = deliveryEnd.getTime();
      console.log("Delivery Start (Unix):", unixStart);

      // 4. Log them in JSON format
      console.log(JSON.stringify({
        userId: userId, 
        orderId: orderId, 
        deliveryTimeString: deliveryTimeString
      }));

      // Clear cart after successful order and stock update
      sessionStorage.removeItem("shoppingCart");
      localStorage.removeItem("currentOrderId");
      sessionStorage.removeItem("deliveryTimeSlot");

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