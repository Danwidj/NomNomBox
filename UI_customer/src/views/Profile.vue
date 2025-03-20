<template>
  <div class="page-container">
    <section class="profile-section">
      <h2>My Profile</h2>
      <div class="profile-card">
        <div class="profile-pic-container">
<img src="https://via.placeholder.com/120" alt="Profile Picture" class="profile-pic" />
        </div>
        <div class="profile-info">
          <p><strong>Name:</strong> {{ customer.name }}</p>
          <p><strong>Email:</strong> {{ customer.email }}</p>
          <p><strong>Address:</strong> {{ customer.address }}</p>
          <p><strong>Phone:</strong> {{ customer.phone }}</p>
          <p><strong>Dietary Preferences: </strong> 
              <span v-if="customer.dietary_preferences.length">
                {{ customer.dietary_preferences.join(', ') }}
              </span>
              <span v-else>No preferences specified</span>
          </p>          
          <router-link to="/edit-profile" class="btn">Edit Profile</router-link>
        </div>
      </div>
    </section>

    <!-- Order History Section -->
    <section class="order-history">
      <h2>Order History</h2>
      <div v-if="orders.length === 0" class="no-orders">
        <p>No order history available.</p>
      </div>

      <!-- Order List -->
      <div class="order-list">
        <div class="order-card" v-for="order in orders" :key="order.orderId">
          <div class="order-header">
            <h3>Order #{{ order.orderId }}</h3>
            <span :class="['order-status', order.status.toLowerCase()]">{{ order.status }}</span>
          </div>
          <p class="order-date">📅 {{ formatDate(order.createdAt) }}</p>
          <p class="order-total">💰 Total: ${{ order.totalPrice.toFixed(2) }}</p>

          <!-- Order Items -->
          <div class="order-items">
            <div class="item" v-for="item in order.items" :key="item.id">
              <span class="item-name">{{ item.name }}</span>
              <span class="item-quantity">{{ item.quantity }}x</span>
              <span class="item-price">${{ item.price.toFixed(2) }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import customerApi from "@/api/customerApi";
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: "ProfilePage",
  setup() {
    const router = useRouter();
    const customer = ref({
      customerId: "",
      name: "",
      email: "",
      address: "",
      phone: "",
      dietary_preferences: [],
    });
    const orders = ref([]);

    onMounted(async () => {
  const token = localStorage.getItem('token');
  const customerId = localStorage.getItem('userId'); // Ensure it matches what backend expects

  if (!token || !customerId) {
    console.error("User is not authenticated");
    router.push('/login');
    return;
  }

  try {
    console.log("Fetching customer profile...");
    await fetchUserData(customerId, token); // Fetch customer details
    console.log("Fetching order history...");
    await fetchOrderHistory(customerId); // Fetch order history
  } catch (error) {
    console.error("Failed to load profile:", error);
  }
});
    const fetchUserData = async (customerId, token) => {
  try {
    const response = await fetch(`http://localhost:5002/customer/${customerId}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}` // Pass token for authentication
      }
    });

    const data = await response.json();
    console.log("Customer API Response:", data); // Debugging

    if (data.code === 200) {
      customer.value = data.data;
      console.log("Customer Data Loaded:", customer.value); // Debugging
    } else {
      console.error("Failed to fetch customer data:", data.message);
    }
  } catch (error) {
    console.error("Error fetching customer data:", error);
  }
};

    const fetchOrderHistory = async (customerId) => {
      try {
        const response = await fetch(`http://localhost:5003/api/orders/customer/${customerId}`);
        const data = await response.json();

        if (data.code === 200) {
          orders.value = data.data;
        } else {
          console.error("No orders found for this user.");
        }
      } catch (error) {
        console.error("Error fetching order history:", error);
      }
    };

    const formatDate = (timestamp) => {
  if (!timestamp) return "Unknown Date";

  // Handle Firestore Timestamp (if it exists)
  if (typeof timestamp === "object" && "seconds" in timestamp) {
    const date = new Date(timestamp.seconds * 1000);
    return date.toLocaleString("en-US", {
      timeZone: "Asia/Singapore",
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      hour12: true
    });
  }

  // Handle JavaScript Date (if stored as a string)
  const date = new Date(timestamp);
  if (isNaN(date)) return "Unknown Date"; // Fallback for invalid dates

  return date.toLocaleString("en-US", {
    timeZone: "Asia/Singapore",
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: true
  });
};


    return { customer, orders, formatDate };
  }
};
</script>

<style scoped>
/* Layout */
.page-container {
  display: flex;
  flex-direction: column;
  padding-top: 60px;
}

/* Profile Section */
.profile-section {
  text-align: center;
  padding: 40px 5%;
  background: white;
  margin: 20px auto;
  border-radius: 12px;
  box-shadow: 0px 6px 10px rgba(0, 0, 0, 0.1);
  width: 95%;
  max-width: 800px;
}

.profile-card {
  display: flex;
  align-items: center;
  gap: 20px;
  justify-content: center;
}

.profile-pic {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 3px solid #ff6600;
  object-fit: cover;
}

p{
  text-align: left;
}
.profile-info {
  text-align: left;
  font-size: 1.2rem;
}

/* Order History */
.order-history {
  text-align: center;
  padding: 40px 5%;
  background: white;
  margin: 20px auto;
  border-radius: 12px;
  box-shadow: 0px 6px 10px rgba(0, 0, 0, 0.1);
  width: 95%;
  max-width: 800px;
}

.order-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

/* Order Card */
.order-card {
  background: #f9f9f9;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  transition: 0.3s ease;
}

.order-card:hover {
  transform: scale(1.02);
}

/* Order Header */
.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1.2rem;
  font-weight: bold;
}

.order-status {
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: bold;
}

.order-status.paid {
  background-color: #28a745;
  color: white;
}

.order-status.pending {
  background-color: #ffc107;
  color: black;
}

.order-status.canceled {
  background-color: #dc3545;
  color: white;
}

/* Order Date & Total */
.order-date,
.order-total {
  font-size: 1rem;
  color: #555;
}

/* Order Items */
.order-items {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
}

.item {
  display: flex;
  justify-content: space-between;
  padding: 5px 0;
  font-size: 1rem;
}

.item-name {
  font-weight: bold;
}
</style>
