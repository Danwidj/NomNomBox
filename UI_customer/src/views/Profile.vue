<template>
  <div class="page-container">
    <section class="profile-section">
      <h2>My Profile</h2>
      <div class="profile-card">
        <img src="https://via.placeholder.com/150" alt="Profile Picture" class="profile-pic" />
        <div class="profile-info">
          <p><strong>ID:</strong> {{ customer.id }}</p>
          <p><strong>Name:</strong> {{ customer.name }}</p>
          <p><strong>Address:</strong> {{ customer.address }}</p>
          <p><strong>Phone:</strong> {{ customer.phone }}</p>
          <p><strong>Dietary Preferences:</strong> {{ customer.dietaryPreferences }}</p>
          <router-link to="/edit-profile" class="btn">Edit Profile</router-link>
        </div>
      </div>
    </section>

    <section class="order-history section">
      <h2>Order History</h2>
      <div class="order-container">
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
export default {
  name: "ProfilePage",
  data() {
    return {
      customer: {
        id: 1,
        name: "John Doe",
        address: "123 Main Street, City",
        phone: "+65 9876 5432",
        dietaryPreferences: "Vegetarian",
      },
      orders: [
        { id: 1023, date: "2025-03-01", status: "Delivered" },
        { id: 1024, date: "2025-03-10", status: "Processing" },
      ],
    };
  },
};
</script>

<style scoped>
/* Ensures page fills screen & pushes footer down */
.page-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* Full screen height */
  flex-grow: 1;
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

.profile-pic {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  border: 3px solid #ff6600;
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
