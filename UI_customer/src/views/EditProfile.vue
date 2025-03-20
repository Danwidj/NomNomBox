<template>
  <div class="container">
    <section class="profile-section">
      <h2>Edit Profile</h2>
      <form @submit.prevent="updateProfile" class="edit-form">
        <label for="name">Name:</label>
        <input type="text" id="name" v-model="customer.name" required />

        <label for="email">Email:</label>
        <input type="email" id="email" v-model="customer.email" required disabled />

        <label for="address">Address:</label>
        <input type="text" id="address" v-model="customer.address" required />

        <label for="phone">Phone:</label>
        <input type="text" id="phone" v-model="customer.phone" required />

        <label>Dietary Preferences:</label>
        <div class="dietary-preferences">
          <div 
            v-for="(tag, index) in availableDietaryTags" 
            :key="index"
            :class="['tag', { 'selected': isTagSelected(tag) }]"
            @click="toggleDietaryTag(tag)"
          >
            {{ tag }}
          </div>
        </div>

        <button type="submit" class="btn">Save Changes</button>
        <button type="button" class="btn btn-secondary" @click="cancelEdit">Cancel</button>
      </form>
    </section>
  </div>
</template>

<script>
import customerApi from "@/api/customerApi";
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: "EditProfile",
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

    const availableDietaryTags = ref([
      "Vegetarian",
      "Vegan",
      "Gluten-Free",
      "Dairy-Free",
      "Nut-Free",
      "Low-Carb",
      "Keto",
      "Paleo",
      "Pescatarian",
      "Organic",
      "Plant-Based" // Including this since it appears in your current data
    ]);

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
        await fetchDietaryTags();
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
          
          // If dietary_preferences is a string, convert it to an array
          if (typeof customer.value.dietary_preferences === 'string') {
            customer.value.dietary_preferences = customer.value.dietary_preferences
              .split(',')
              .map(pref => pref.trim())
              .filter(pref => pref);
          }
          
          // Ensure dietary_preferences is an array
          if (!Array.isArray(customer.value.dietary_preferences)) {
            customer.value.dietary_preferences = [];
          }
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

    const fetchDietaryTags = async () => {
      try {
        // Attempt to fetch tags from API - same as in SignUpView
        const response = await fetch("http://127.0.0.1:5004/inventory");
        const data = await response.json();
        
        if (data.code === 200) {
          const allTags = data.data.flatMap(product => product.dietaryTags || []);
          availableDietaryTags.value = [...new Set(allTags)];
        }
      } catch (error) {
        console.error("Error fetching dietary tags:", error);
        // Keep using the default tags defined earlier
      }
    };

    const isTagSelected = (tag) => {
      return customer.value.dietary_preferences && 
             customer.value.dietary_preferences.includes(tag);
    };

    const toggleDietaryTag = (tag) => {
      if (!Array.isArray(customer.value.dietary_preferences)) {
        customer.value.dietary_preferences = [];
      }
      
      if (isTagSelected(tag)) {
        customer.value.dietary_preferences = customer.value.dietary_preferences.filter(t => t !== tag);
      } else {
        customer.value.dietary_preferences.push(tag);
      }
    };

    const updateProfile = async () => {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('userId');
      
      if (!token || !userId) {
        console.error("User is not authenticated");
        router.push('/login');
        return;
      }
      
      try {
        // Ensure dietary_preferences is an array
        if (!Array.isArray(customer.value.dietary_preferences)) {
          customer.value.dietary_preferences = [];
        }
        
        // Prepare data for API
        const updateData = {
          name: customer.value.name,
          address: customer.value.address,
          phone: customer.value.phone,
          dietary_preferences: customer.value.dietary_preferences
        };
        
        console.log("Sending update:", updateData);
        const token = localStorage.getItem('token');
        const response = await customerApi.updateCustomerDetails(userId, updateData, token);
        console.log("Update response:", response);
        
        alert("Profile Updated Successfully!");
        router.push("/profile");
      } catch (error) {
        console.error("Error updating profile:", error);
        
        if (error.response) {
          console.error("Response data:", error.response.data);
          console.error("Response status:", error.response.status);
          
          if (error.response.status === 401) {
            alert("Your session has expired. Please login again.");
            localStorage.removeItem('token');
            localStorage.removeItem('userId');
            router.push('/login');
            return;
          }
        }
        
        alert("Failed to update profile. Please try again.");
      }
    };

    const cancelEdit = () => {
      router.push("/profile");
    };

    return {
      customer,
      availableDietaryTags,
      isTagSelected,
      toggleDietaryTag,
      updateProfile,
      cancelEdit
    };
  }
};
</script>

<style scoped>
.profile-section {
  text-align: center;
  padding: 40px 5%;
  background: white;
  margin: 20px auto;
  border-radius: 12px;
  box-shadow: 0px 6px 10px rgba(0, 0, 0, 0.1);
  width: 95%;
  max-width: 600px;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  width: 100%;
  max-width: 500px;
  margin: auto;
}

.edit-form input {
  padding: 12px;
  border-radius: 5px;
  border: 1px solid #ddd;
  font-size: 1rem;
}

.edit-form label {
  text-align: left;
  font-weight: bold;
  margin-bottom: -10px;
}

.dietary-preferences {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: flex-start;
  margin: 10px 0;
}

.tag {
  background-color: #f0f0f0;
  padding: 8px 15px;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.tag:hover {
  background-color: #e0e0e0;
}

.tag.selected {
  background-color: #ff6600;
  color: white;
}

.btn {
  background-color: #ff6600;
  color: white;
  padding: 12px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.3s;
}

.btn:hover {
  background-color: #e65c00;
}

.btn-secondary {
  background-color: #6c757d;
  margin-top: 10px;
}

.btn-secondary:hover {
  background-color: #5a6268;
}
</style>