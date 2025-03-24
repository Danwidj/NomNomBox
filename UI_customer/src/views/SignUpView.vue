<template>
  <div class="signup-container">
    <h2>Sign Up</h2>
    <form @submit.prevent="signUp">
      <input v-model="name" type="text" placeholder="Full Name" required />
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <input v-model="address" type="text" placeholder="Address" />
      <input v-model="phone" type="text" placeholder="Phone Number" />
      
      <!-- Dietary Preferences Custom Multi-Select -->
      <div class="preferences-section">
        <label>Dietary Preferences (Optional)</label>
        <div class="dropdown-container">
          <div 
            class="dropdown-header" 
            @click="toggleDropdown"
          >
            <span v-if="selectedDietaryPreferences.length === 0">
              Select preferences (if any)
            </span>
            <span v-else>
              {{ selectedDietaryPreferences.length }} preference(s) selected
            </span>
            <span class="dropdown-arrow">▼</span>
          </div>
          
          <div class="dropdown-list" v-if="isDropdownOpen">
            <div 
              v-for="tag in availableDietaryTags" 
              :key="tag" 
              class="dropdown-item"
              :class="{ 'selected': selectedDietaryPreferences.includes(tag) }"
              @click.stop="toggleTag(tag)"
            >
              <div class="checkbox">
                <div v-if="selectedDietaryPreferences.includes(tag)" class="checkbox-inner"></div>
              </div>
              <span>{{ tag }}</span>
            </div>
          </div>
        </div>
        
        <!-- Display selected tags -->
        <div v-if="selectedDietaryPreferences.length > 0" class="selected-tags">
          <span>Selected: </span>
          <div class="tag-list">
            <span 
              v-for="tag in selectedDietaryPreferences" 
              :key="tag" 
              class="dietary-tag"
            >
              {{ tag }}
              <span @click="removeTag(tag)" class="remove-tag">×</span>
            </span>
          </div>
        </div>
      </div>
      
      <button type="submit">Sign Up</button>
    </form>

    <p>
      Already have an account?
      <router-link to="/login">Login</router-link>
    </p>
  </div>
</template>

<script>
import customerApi from "../api/customerApi";
import { useRouter } from "vue-router";

export default {
  setup() {
    const router = useRouter();
    return { router };
  },
  data() {
    return {
      name: "",
      email: "",
      password: "",
      address: "",
      phone: "",
      selectedDietaryPreferences: [],
      availableDietaryTags: [
        "Vegetarian",
        "Vegan",
        "Gluten-Free",
        "Dairy-Free",
        "Nut-Free",
        "Low-Carb",
        "Keto",
        "Paleo",
        "Pescatarian",
        "Organic"
      ],
      isDropdownOpen: false
    };
  },
  created() {
    this.fetchDietaryTags();
    
    // Add click event listener to close dropdown when clicking outside
    document.addEventListener('click', this.closeDropdown);
  },
  unmounted() {
    // Remove event listener when component is destroyed
    document.removeEventListener('click', this.closeDropdown);
  },
  methods: {
    toggleDropdown(event) {
      // Prevent event from bubbling up to document
      event.stopPropagation();
      this.isDropdownOpen = !this.isDropdownOpen;
    },
    closeDropdown() {
      this.isDropdownOpen = false;
    },
    toggleTag(tag) {
      if (this.selectedDietaryPreferences.includes(tag)) {
        this.removeTag(tag);
      } else {
        this.selectedDietaryPreferences.push(tag);
      }
    },
    removeTag(tag) {
      this.selectedDietaryPreferences = this.selectedDietaryPreferences.filter(t => t !== tag);
    },
    async fetchDietaryTags() {
      try {
        // Attempt to fetch tags from API
        const response = await fetch("http://127.0.0.1:5004/inventory");
        const data = await response.json();
        
        if (data.code === 200) {
          const allTags = data.data.flatMap(product => product.dietaryTags || []);
          this.availableDietaryTags = [...new Set(allTags)];
        }
      } catch (error) {
        console.error("Error fetching dietary tags:", error);
        // Keep using the default tags defined in data()
      }
    },
    async signUp() {
      try {
        // Log the data being sent to verify
        console.log("About to send registration data:");
        console.log("Email:", this.email);
        console.log("Name:", this.name);
        console.log("Dietary Preferences:", this.selectedDietaryPreferences);

        const userData = {
          email: this.email,
          password: this.password,
          name: this.name,
          address: this.address,
          phone: this.phone,
          dietary_preferences: this.selectedDietaryPreferences,
        };

        console.log("Full user data:", userData);

        const response = await customerApi.register(userData);

        if (response.status === 201) {
          alert("Registration successful!");
          this.router.push("/login");
        } else {
          alert(response.data.message);
        }
      } catch (error) {
        console.error("Sign-up failed:", error.response?.data || error);
        // Display the specific error message from the backend if available
        if (error.response?.data?.message) {
          alert(error.response.data.message);
        } else {
          alert("Sign-up failed. Please try again.");
        }
      }
    }
  },
};
</script>

<style scoped>
.signup-container {
  max-width: 400px;
  margin: auto;
  text-align: center;
  padding: 20px;
}

input {
  display: block;
  width: 100%;
  margin: 10px 0;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.preferences-section {
  margin: 15px 0;
  text-align: left;
}

.preferences-section label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

/* Custom Dropdown Styling */
.dropdown-container {
  position: relative;
  width: 100%;
}

.dropdown-header {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}

.dropdown-arrow {
  font-size: 12px;
  transition: transform 0.2s ease;
}

.dropdown-list {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  margin-top: 2px;
  max-height: 200px;
  overflow-y: auto;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  z-index: 100;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.dropdown-item {
  padding: 8px 10px;
  display: flex;
  align-items: center;
  cursor: pointer;
}

.dropdown-item:hover {
  background-color: #f5f5f5;
}

.dropdown-item.selected {
  background-color: #f0f8ff;
}

.checkbox {
  width: 16px;
  height: 16px;
  border: 1px solid #ccc;
  border-radius: 3px;
  margin-right: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.checkbox-inner {
  width: 10px;
  height: 10px;
  background-color: #4CAF50;
  border-radius: 2px;
}

/* Selected Tags Display */
.selected-tags {
  margin-top: 10px;
  display: flex;
  align-items: flex-start;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-left: 5px;
}

.dietary-tag {
  background: #ffcc80;
  color: #333;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.8rem;
  display: inline-flex;
  align-items: center;
}

.remove-tag {
  margin-left: 5px;
  cursor: pointer;
  font-weight: bold;
}

button {
  width: 100%;
  padding: 10px;
  background: green;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 15px;
}

button:hover {
  background: darkgreen;
}
</style>