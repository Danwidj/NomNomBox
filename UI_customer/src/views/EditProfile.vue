<template>
    <div class="container">
      <section class="profile-section">
        <h2>Edit Profile</h2>
        <form @submit.prevent="updateProfile" class="edit-form">
          <label for="name">Name:</label>
          <input type="text" id="name" v-model="customer.name" required />
  
          <label for="address">Address:</label>
          <input type="text" id="address" v-model="customer.address" required />
  
          <label for="phone">Phone:</label>
          <input type="text" id="phone" v-model="customer.phone" required />
  
          <label for="dietaryPreferences">Dietary Preferences:</label>
          <input type="text" id="dietaryPreferences" v-model="customer.dietaryPreferences" />
  
          <button type="submit" class="btn">Save Changes</button>
        </form>
      </section>
    </div>
  </template>
  
  <script>
  export default {
    name: "EditProfile",
    data() {
      return {
        customer: {
          name: "John Doe",
          address: "123 Main Street, City",
          phone: "+65 9876 5432",
          dietaryPreferences: "Vegetarian",
        },
      };
    },
    methods: {
      updateProfile() {
        alert("Profile Updated Successfully!");
        this.$router.push("/profile"); // Redirect to Profile Page
      },
    },
  };
  </script>
  
  <style scoped>
  .edit-form {
    display: flex;
    flex-direction: column;
    gap: 15px;
    width: 80%;
    max-width: 500px;
    margin: auto;
  }
  
  .edit-form input {
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ddd;
  }
  
  .edit-form button {
    background-color: #ff6600;
    color: white;
    padding: 12px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .edit-form button:hover {
    background-color: #e65c00;
  }
  </style>
  