<template>
  <div class="auth-container">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit">Login</button>
    </form>

    <!-- <button @click="googleSignIn">Sign in with Google</button> -->

    <p>
      Don't have an account?
      <router-link to="/signup">Sign Up</router-link>
    </p>
  </div>
</template>

<script>
import customerApi from "../api/customerApi"; // Ensure customerApi.js is correct
import { login as setAuth } from "@/stores/auth"; // Import auth store
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

        if (response.status === 200) {
          setAuth(response.data.token); // Updates global authentication state
          this.router.push("/profile"); // Redirect on success
        } else {
          alert(response.data.message);
        }
      } catch (error) {
        console.error("Login failed:", error.response?.data || error); // 🔹 Log error
        alert("Login failed. Please check your credentials.");
      }
    },

    // async googleSignIn() {
    //   try {
    //     // 🔹 Open Google Sign-In in a new window and get the token from Flask
    //     const response = await customerApi.googleLogin();
    //     if (response.status === 200) {
    //       setAuth(response.data.token);
    //       this.router.push("/profile");
    //     } else {
    //       alert(response.data.message);
    //     }
    //   } catch (error) {
    //     console.error("Google Sign-In failed:", error);
    //     alert("Google Sign-In failed.");
    //   }
    // },
  },
};
</script>

<style scoped>
.auth-container {
  max-width: 400px;
  margin: auto;
  text-align: center;
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
