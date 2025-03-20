<template>
  <div class="page-container">
    <section class="profile-section">
      <h2>My Profile</h2>
      <div class="profile-card">
        <div class="profile-pic-container">
          <!-- <div class="profile-pic">Profile Picture</div> -->
        </div>
        <div class="profile-info">
          <!-- <p><strong>ID:</strong> {{ customer.customerId }}</p> -->
          <p><strong>Name:</strong> {{ customer.name }}</p>
          <p><strong>Email:</strong> {{ customer.email }}</p>
          <p><strong>Address:</strong> {{ customer.address }}</p>
          <p><strong>Phone:</strong> {{ customer.phone }}</p>
          <p><strong>Dietary Preferences: </strong> 
              <span v-if="customer.dietary_preferences && customer.dietary_preferences.length">
                {{ customer.dietary_preferences.join(', ') }}
              </span>
              <span v-else>No preferences specified</span>
            </p>          
          <router-link to="/edit-profile" class="btn">Edit Profile</router-link>
        </div>
      </div>
    </section>

    <section class="order-history section">
      <h2>Order History</h2>
      <div class="order-container">
        <div v-if="orders.length === 0" class="no-orders">
          <p>No order history available.</p>
        </div>
        <div class="order-item" v-for="order in orders" :key="order.id">
          <p><strong>Order #{{ order.id }}</strong></p>
          <p>Date: {{ order.date }}</p>
          <p>Status: {{ order.status }}</p>
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
      dietary_preferences: "",
    });
    const orders = ref([]);
    
    onMounted(async () => {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('userId');
      
      if (!token || !userId) {
        console.error("User is not authenticated");
        router.push('/login');
        return;
      }
      
      try {
        await fetchUserData(userId, token);
      } catch (error) {
        console.error("Failed to load profile:", error);
      }
    });
    
    const fetchUserData = async (customerId, token) => {
      try {
        const response = await customerApi.getCustomerDetails(customerId, token);
        console.log("Customer data response:", response);
        
        if (response && response.data && response.data.data) {
          customer.value = response.data.data;
          // You could fetch order history here as well
        } else {
          console.error("Failed to fetch customer data");
        }
      } catch (error) {
        console.error("Error fetching customer data:", error);
        if (error.response && error.response.status === 401) {
          // Token expired or invalid
          localStorage.removeItem('token');
          localStorage.removeItem('isAuthenticated');
          localStorage.removeItem('userId');
          router.push('/login');
        }
      }
    };
    
    return {
      customer,
      orders
    };
  }
};
</script>

<style scoped>
/* Ensures page fills screen & pushes footer down */
.page-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* Full screen height */
  flex-grow: 1;
  padding-top: 60px; /* Add space for the fixed navbar */
}

/* Profile Section */
.profile-section {
  text-align: center;
  padding: 60px 5%;
  background: white;
  margin: 20px auto;
  border-radius: 12px;
  box-shadow: 0px 6px 10px rgba(0, 0, 0, 0.1);
  width: 95%;
  max-width: 800px;
}

/* Profile Card */
.profile-card {
  display: flex;
  align-items: center;
  gap: 20px;
  justify-content: center;
}

.profile-pic-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.profile-pic {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  border: 3px solid #ff6600;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
  color: #666;
  font-size: 14px;
}

.profile-info {
  text-align: left;
  font-size: 1.2rem;
}

/* Order History */
.order-history {
  text-align: center;
  padding: 60px 5%;
  background: white;
  margin: 20px auto;
  border-radius: 12px;
  box-shadow: 0px 6px 10px rgba(0, 0, 0, 0.1);
  width: 95%;
  max-width: 800px;
}

.order-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
  align-items: center;
}

.order-item {
  background: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
  width: 80%;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.no-orders {
  color: #666;
  font-style: italic;
  margin: 20px 0;
}

/* Button */
.btn {
  background-color: #ff6600;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  text-decoration: none;
  display: inline-block;
  margin-top: 10px;
  font-size: 1rem;
  border: none;
  cursor: pointer;
  transition: background 0.3s;
}

.btn:hover {
  background-color: #e65c00;
}
</style>