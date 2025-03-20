<template>
  <div class="auth-container">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit">Login</button>
    </form>

    <p>
      Don't have an account?
      <router-link to="/signup">Sign Up</router-link>
    </p>
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

<style scoped>
.auth-container {
  max-width: 400px;
  margin: auto;
  text-align: center;
  padding-top: 100px; /* Push content below navbar */
}
input {
  display: block;
  width: 100%;
  margin: 10px 0;
  padding: 8px;
}
button {
  width: 100%;
  padding: 10px;
  background: blue;
  color: white;
  border: none;
}
</style>