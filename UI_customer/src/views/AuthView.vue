<template>
  <div class="nom-container my-16">
    <div class="max-w-md mx-auto nom-card nom-fade-in">
      <div class="mb-8 text-center">
        <h2 class="nom-heading mb-2">Welcome Back</h2>
        <p class="text-muted-foreground">Sign in to your NomNomBox account</p>
      </div>
      
      <form @submit.prevent="login" class="space-y-6">
        <div class="space-y-2">
          <label for="email" class="nom-label">Email</label>
          <input 
            v-model="email" 
            type="email" 
            id="email" 
            placeholder="Enter your email" 
            required
            class="nom-input"
          />
        </div>

        <div class="space-y-2">
          <div class="flex justify-between items-center">
            <label for="password" class="nom-label">Password</label>
            <a href="#" class="text-sm text-primary hover:underline">Forgot password?</a>
          </div>
          <input 
            v-model="password" 
            type="password" 
            id="password" 
            placeholder="Enter your password" 
            required
            class="nom-input"
          />
        </div>

        <button type="submit" class="w-full nom-btn-primary py-3">Login</button>
      </form>

      <div class="mt-8 pt-6 text-center border-t border-border">
        <p class="text-muted-foreground">
          Don't have an account?
          <router-link to="/signup" class="text-primary font-medium hover:underline">
            Create an account
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import customerApi from "../api/customerApi";
import { login as setAuth } from "@/stores/auth"; 
import { useRouter } from "vue-router";

export default {
  data() {
    return {
      email: "",
      password: "",
    };
  },
  setup() {
    const router = useRouter();
    return { router };
  },
  methods: {
    async login() {
      try {
        const response = await customerApi.login({
          email: this.email,
          password: this.password,
        });

        console.log("Login response:", response);

        if (response.status === 200) {
          const token = response.data.token; 
          const customerId = response.data.id; 

          // Update authentication state with the token
          setAuth(customerId, token);
          // Store token and customer ID in sessionStorage
          sessionStorage.setItem("token", token);
          sessionStorage.setItem("customerId", customerId);

          // Redirect to the profile page
          this.router.push("/profile");
        } else {
          alert(response.data.message);
        }
      } catch (error) {
        console.error("Login failed:", error);
        alert("Login failed. Please check your credentials.");
      }
    }
  },
};
</script>