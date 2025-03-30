<template>
  <div class="nom-container py-8">
    <section class="max-w-3xl mx-auto">
      <h2 class="nom-heading text-center mb-6">Edit Profile</h2>
      
      <form @submit.prevent="updateProfile" class="nom-card">
        <div class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="space-y-2">
              <label for="name" class="block text-sm font-medium">Name:</label>
              <input 
                type="text" 
                id="name" 
                v-model="customer.name" 
                required
                class="w-full p-2 border border-input rounded-md focus:outline-none focus:ring-2 focus:ring-ring"
              />
            </div>

            <div class="space-y-2">
              <label for="email" class="block text-sm font-medium">Email:</label>
              <input 
                type="email" 
                id="email" 
                v-model="customer.email" 
                required 
                disabled
                class="w-full p-2 border border-input rounded-md bg-muted/30 opacity-70"
              />
            </div>

            <div class="space-y-2">
              <label for="address" class="block text-sm font-medium">Address:</label>
              <input 
                type="text" 
                id="address" 
                v-model="customer.address" 
                required
                class="w-full p-2 border border-input rounded-md focus:outline-none focus:ring-2 focus:ring-ring"
              />
            </div>

            <div class="space-y-2">
              <label for="phone" class="block text-sm font-medium">Phone:</label>
              <input 
                type="text" 
                id="phone" 
                v-model="customer.phone" 
                required
                class="w-full p-2 border border-input rounded-md focus:outline-none focus:ring-2 focus:ring-ring"
              />
            </div>
          </div>

          <div class="space-y-3">
            <label class="block text-sm font-medium">Dietary Preferences:</label>
            <div class="flex flex-wrap gap-2">
              <button
                type="button"
                v-for="tag in availableDietaryTags"
                :key="tag"
                :class="[
                  'px-3 py-1.5 rounded-full text-base transition-colors',
                  isTagSelected(tag)
                    ? 'bg-secondary text-secondary-foreground' 
                    : 'bg-muted text-muted-foreground hover:bg-muted/80'
                ]"
                @click="toggleDietaryTag(tag)"
              >
                {{ tag }}
              </button>
            </div>
          </div>

          <div class="pt-4 flex gap-4">
            <button type="submit" class="nom-btn-primary flex-1">Save Changes</button>
            <button type="button" class="flex-1 bg-muted text-foreground hover:bg-muted/80 rounded-md px-4 py-2 transition-colors" @click="cancelEdit">
              Cancel
            </button>
          </div>
        </div>
      </form>
    </section>
  </div>
</template>

<script>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import customerApi from '@/api/customerApi'

export default {
  name: 'EditProfile',
  setup() {
    const router = useRouter()
    const customer = ref({
      customerId: '',
      name: '',
      email: '',
      address: '',
      phone: '',
      dietary_preferences: [],
    })

    const availableDietaryTags = ref([
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
      'Plant-Based',
    ])

    onMounted(async () => {
      const token = localStorage.getItem('token')
      const userId = localStorage.getItem('userId')

      if (!token || !userId) {
        console.error('User is not authenticated')
        router.push('/login')
        return
      }

      try {
        await fetchUserData(userId, token)
        await fetchDietaryTags()
      } catch (error) {
        console.error('Failed to load profile:', error)
      }
    })

    const fetchUserData = async (customerId, token) => {
      try {
        const response = await customerApi.getCustomerDetails(customerId, token)
        console.log('Customer data response:', response)

        if (response && response.data && response.data.data) {
          customer.value = response.data.data

          // If dietary_preferences is a string, convert it to an array
          if (typeof customer.value.dietary_preferences === 'string') {
            customer.value.dietary_preferences = customer.value.dietary_preferences
              .split(',')
              .map((pref) => pref.trim())
              .filter((pref) => pref)
          }

          // Ensure dietary_preferences is an array
          if (!Array.isArray(customer.value.dietary_preferences)) {
            customer.value.dietary_preferences = []
          }
        } else {
          console.error('Failed to fetch customer data')
        }
      } catch (error) {
        console.error('Error fetching customer data:', error)
        if (error.response && error.response.status === 401) {
          // Token expired or invalid
          localStorage.removeItem('token')
          localStorage.removeItem('isAuthenticated')
          localStorage.removeItem('userId')
          router.push('/login')
        }
      }
    }

    const fetchDietaryTags = async () => {
      try {
        // Attempt to fetch tags from API
        const response = await fetch('http://localhost:5004/inventory')
        const data = await response.json()

        if (data.code === 200) {
          const allTags = data.data.flatMap((product) => product.dietaryTags || [])
          availableDietaryTags.value = [...new Set(allTags)]
        }
      } catch (error) {
        console.error('Error fetching dietary tags:', error)
        // Keep using the default tags defined earlier
      }
    }

    const isTagSelected = (tag) => {
      return customer.value.dietary_preferences && customer.value.dietary_preferences.includes(tag)
    }

    const toggleDietaryTag = (tag) => {
      if (!Array.isArray(customer.value.dietary_preferences)) {
        customer.value.dietary_preferences = []
      }

      if (isTagSelected(tag)) {
        customer.value.dietary_preferences = customer.value.dietary_preferences.filter(
          (t) => t !== tag,
        )
      } else {
        customer.value.dietary_preferences.push(tag)
      }
    }

    const updateProfile = async () => {
      const token = localStorage.getItem('token')
      const userId = localStorage.getItem('userId')

      if (!token || !userId) {
        console.error('User is not authenticated')
        router.push('/login')
        return
      }

      try {
        // Ensure dietary_preferences is an array
        if (!Array.isArray(customer.value.dietary_preferences)) {
          customer.value.dietary_preferences = []
        }

        // Prepare data for API
        const updateData = {
          name: customer.value.name,
          address: customer.value.address,
          phone: customer.value.phone,
          dietary_preferences: customer.value.dietary_preferences,
        }

        console.log('Sending update:', updateData)
        const response = await customerApi.updateCustomerDetails(userId, updateData, token)
        console.log('Update response:', response)

        alert('Profile Updated Successfully!')
        router.push('/profile')
      } catch (error) {
        console.error('Error updating profile:', error)

        if (error.response) {
          console.error('Response data:', error.response.data)
          console.error('Response status:', error.response.status)

          if (error.response.status === 401) {
            alert('Your session has expired. Please login again.')
            localStorage.removeItem('token')
            localStorage.removeItem('userId')
            router.push('/login')
            return
          }
        }

        alert('Failed to update profile. Please try again.')
      }
    }

    const cancelEdit = () => {
      router.push('/profile')
    }

    return {
      customer,
      availableDietaryTags,
      isTagSelected,
      toggleDietaryTag,
      updateProfile,
      cancelEdit,
    }
  },
}
</script>