<template>
  <div class="nom-container py-12 nom-fade-in">
    <div class="max-w-3xl mx-auto">
      <!-- Signup Header -->
      <div class="text-center mb-8">
        <h2 class="nom-heading mb-2">Create an Account</h2>
        <p class="text-muted-foreground">Join NomNomBox and start enjoying delicious meals</p>
      </div>
      
      <form @submit.prevent="signUp" class="nom-card nom-fade-in">
        <!-- Progress Steps -->
        <div class="mb-8">
          <div class="flex items-center justify-between">
            <div class="flex flex-col items-center">
              <div class="w-8 h-8 bg-muted text-muted-foreground rounded-full flex items-center justify-center font-medium">1</div>
              <span class="text-xs mt-2 font-medium">Account</span>
            </div>
            <div class="h-px bg-border flex-1 mx-2"></div>
            <div class="flex flex-col items-center">
              <div class="w-8 h-8 bg-muted text-muted-foreground rounded-full flex items-center justify-center font-medium">2</div>
              <span class="text-xs mt-2">Details</span>
            </div>
            <div class="h-px bg-border flex-1 mx-2"></div>
            <div class="flex flex-col items-center">
              <div class="w-8 h-8 bg-muted text-muted-foreground rounded-full flex items-center justify-center font-medium">3</div>
              <span class="text-xs mt-2">Preferences</span>
            </div>
          </div>
        </div>

        <div class="space-y-8">
          <!-- Account Information Section -->
          <div>
            <h3 class="text-lg font-semibold mb-4">Account Information</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-2">
                <label for="name" class="nom-label">Full Name</label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-3 flex items-center pointer-events-none text-muted-foreground">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                      <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                  </div>
                  <input 
                    v-model="name" 
                    type="text" 
                    id="name"
                    placeholder="Enter your full name" 
                    required
                    class="nom-input pl-10"
                  />
                </div>
              </div>
              
              <div class="space-y-2">
                <label for="email" class="nom-label">Email Address</label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-3 flex items-center pointer-events-none text-muted-foreground">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M22 6c0-1.1-.9-2-2-2H4c-1.1 0-2 .9-2 2"></path>
                      <path d="M22 6l-10 7L2 6"></path>
                      <path d="M2 6v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6"></path>
                    </svg>
                  </div>
                  <input 
                    v-model="email" 
                    type="email" 
                    id="email"
                    placeholder="Enter your email" 
                    required
                    class="nom-input pl-10"
                  />
                </div>
              </div>
              
              <div class="space-y-2">
                <label for="password" class="nom-label">Password</label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-3 flex items-center pointer-events-none text-muted-foreground">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                      <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                    </svg>
                  </div>
                  <input 
                    v-model="password" 
                    :type="showPassword ? 'text' : 'password'" 
                    id="password"
                    placeholder="Create a secure password" 
                    required
                    class="nom-input pl-10 pr-10"
                  />
                  <button 
                    type="button" 
                    @click="showPassword = !showPassword"
                    class="absolute inset-y-0 right-3 flex items-center text-muted-foreground hover:text-foreground transition-colors"
                  >
                    <svg v-if="showPassword" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"></path>
                      <path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"></path>
                      <path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"></path>
                      <line x1="2" y1="2" x2="22" y2="22"></line>
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path>
                      <circle cx="12" cy="12" r="3"></circle>
                    </svg>
                  </button>
                </div>
                <div v-if="password" class="mt-2">
                  <div class="text-xs text-muted-foreground mb-1">Password strength:</div>
                  <div class="h-1 w-full bg-muted rounded-full overflow-hidden">
                    <div 
                      class="h-full rounded-full transition-all duration-300" 
                      :style="{ width: passwordStrength + '%' }"
                      :class="{
                        'bg-destructive': passwordStrength < 40,
                        'bg-secondary': passwordStrength >= 40 && passwordStrength < 70,
                        'bg-primary': passwordStrength >= 70
                      }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Delivery Information Section -->
          <div>
            <h3 class="text-lg font-semibold mb-4">Delivery Information</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-2">
                <label for="phone" class="nom-label">Phone Number</label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-3 flex items-center pointer-events-none text-muted-foreground">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
                    </svg>
                  </div>
                  <input 
                    v-model="phone" 
                    type="tel" 
                    id="phone"
                    placeholder="Enter your phone number"
                    class="nom-input pl-10"
                  />
                </div>
              </div>
            
              <div class="md:col-span-2 space-y-2">
                <label for="address" class="nom-label">Delivery Address</label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-3 flex items-center pointer-events-none text-muted-foreground">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                      <circle cx="12" cy="10" r="3"></circle>
                    </svg>
                  </div>
                  <input 
                    v-model="address" 
                    type="text" 
                    id="address"
                    placeholder="Enter your full address"
                    class="nom-input pl-10"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Dietary Preferences Section -->
          <div>
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-lg font-semibold">Dietary Preferences</h3>
              <span class="text-xs text-muted-foreground">Optional</span>
            </div>
            
            <!-- Tags Display -->
            <div class="bg-muted/20 rounded-lg p-4 mb-4">
              <div v-if="selectedDietaryPreferences.length > 0" class="flex flex-wrap gap-2">
                <div
                  v-for="tag in selectedDietaryPreferences"
                  :key="tag"
                  class="nom-badge-primary flex items-center"
                >
                  {{ tag }}
                  <button 
                    @click="removeTag(tag)" 
                    class="ml-1 hover:text-primary/70"
                    type="button"
                  >×</button>
                </div>
              </div>
              <div v-else class="text-muted-foreground text-sm">
                No preferences selected. Select dietary preferences to get personalized recommendations.
              </div>
            </div>
            
            <!-- Tag Selection -->
            <div class="relative">
              <div 
                @click="toggleDropdown" 
                class="w-full p-3 border border-input rounded-md flex justify-between items-center cursor-pointer bg-background hover:bg-muted/30 transition-colors"
              >
                <span class="text-muted-foreground">
                  Select preferences...
                </span>
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  width="16" 
                  height="16" 
                  viewBox="0 0 24 24" 
                  fill="none" 
                  stroke="currentColor" 
                  stroke-width="2" 
                  stroke-linecap="round" 
                  stroke-linejoin="round"
                  class="transition-transform duration-200"
                  :class="{ 'transform rotate-180': isDropdownOpen }"
                >
                  <polyline points="6 9 12 15 18 9"></polyline>
                </svg>
              </div>

              <div 
                v-if="isDropdownOpen" 
                class="absolute z-10 mt-1 w-full max-h-60 overflow-auto bg-card border border-input rounded-md shadow-lg nom-fade-in"
              >
                <div
                  v-for="tag in availableDietaryTags"
                  :key="tag"
                  @click.stop="toggleTag(tag)"
                  class="p-3 cursor-pointer hover:bg-muted/40 flex items-center gap-2 transition-colors"
                  :class="{ 'bg-muted/30': selectedDietaryPreferences.includes(tag) }"
                >
                  <div 
                    class="w-4 h-4 border border-input rounded flex items-center justify-center transition-colors"
                    :class="{ 'bg-primary border-primary': selectedDietaryPreferences.includes(tag) }"
                  >
                    <svg v-if="selectedDietaryPreferences.includes(tag)" xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" class="text-primary-foreground">
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                  </div>
                  <span>{{ tag }}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="pt-4">
            <button 
              type="submit" 
              class="w-full nom-btn-primary py-3"
            >
              Create Account
            </button>
          </div>
        </div>
      </form>

      <p class="text-center mt-8">
        Already have an account?
        <router-link to="/login" class="text-primary font-medium hover:underline">
          Sign in
        </router-link>
      </p>
    </div>
  </div>
</template>

<script>
import customerApi from '../api/customerApi'
import { useRouter } from 'vue-router'

export default {
  setup() {
    const router = useRouter()
    return { router }
  },
  data() {
    return {
      name: '',
      email: '',
      password: '',
      address: '',
      phone: '',
      selectedDietaryPreferences: [],
      availableDietaryTags: [
        'Vegetarian',
        'Vegan',
        'Gluten-Free',
        'Dairy-Free',
        'Nut-Free',
        'Low-Carb',
        'Keto',
        'Paleo',
        'Pescatarian',
        'Organic',
      ],
      isDropdownOpen: false,
      showPassword: false,
      isSubmitting: false,
    }
  },
  computed: {
    passwordStrength() {
      if (!this.password) return 0;
      
      let strength = 0;
      
      // Length contribution (up to 40%)
      strength += Math.min(this.password.length * 4, 40);
      
      // Complexity contribution (up to 60%)
      if (/[A-Z]/.test(this.password)) strength += 10; // uppercase
      if (/[a-z]/.test(this.password)) strength += 10; // lowercase
      if (/[0-9]/.test(this.password)) strength += 10; // numbers
      if (/[^A-Za-z0-9]/.test(this.password)) strength += 15; // special chars
      if (this.password.length > 10) strength += 15; // bonus for length
      
      return Math.min(strength, 100);
    }
  },
  created() {
    this.fetchDietaryTags()

    // Add click event listener to close dropdown when clicking outside
    document.addEventListener('click', this.closeDropdown)
  },
  unmounted() {
    // Remove event listener when component is destroyed
    document.removeEventListener('click', this.closeDropdown)
  },
  methods: {
    toggleDropdown(event) {
      // Prevent event from bubbling up to document
      event.stopPropagation()
      this.isDropdownOpen = !this.isDropdownOpen
    },
    closeDropdown() {
      this.isDropdownOpen = false
    },
    toggleTag(tag) {
      if (this.selectedDietaryPreferences.includes(tag)) {
        this.removeTag(tag)
      } else {
        this.selectedDietaryPreferences.push(tag)
      }
    },
    removeTag(tag) {
      this.selectedDietaryPreferences = this.selectedDietaryPreferences.filter((t) => t !== tag)
    },
    async fetchDietaryTags() {
      try {
        // Attempt to fetch tags from API
        const response = await fetch('http://localhost:5006/inventory')
        const data = await response.json()

        if (data.code === 200) {
          const allTags = data.data.flatMap((product) => product.dietaryTags || [])
          this.availableDietaryTags = [...new Set(allTags)]
        }
      } catch (error) {
        console.error('Error fetching dietary tags:', error)
        // Keep using the default tags defined in data()
      }
    },
    async signUp() {
      if (this.isSubmitting) return;
      
      try {
        this.isSubmitting = true;
        
        const userData = {
          email: this.email,
          password: this.password,
          name: this.name,
          address: this.address,
          phone: this.phone,
          dietary_preferences: this.selectedDietaryPreferences,
        }

        const response = await customerApi.register(userData);

        if (response.status === 201) {
          this.showToast('Registration successful!', 'success');
          
          // Small delay for better UX before redirect
          setTimeout(() => {
            this.router.push('/login');
          }, 1500);
        } else {
          this.showToast(response.data.message || 'Registration failed', 'error');
        }
      } catch (error) {
        console.error('Sign-up failed:', error.response?.data || error);
        
        // Display the specific error message from the backend if available
        if (error.response?.data?.message) {
          this.showToast(error.response.data.message, 'error');
        } else {
          this.showToast('Sign-up failed. Please try again.', 'error');
        }
      } finally {
        this.isSubmitting = false;
      }
    },
    showToast(message, type = 'info') {
      // For now, using alert, but you should replace this with a proper toast component
      if (type === 'error') {
        alert('Error: ' + message);
      } else {
        alert(message);
      }
    }
  },
}
</script>