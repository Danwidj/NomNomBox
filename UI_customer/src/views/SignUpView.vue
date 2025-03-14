<template>
    <div class="signup-container">
      <h2>Sign Up</h2>
      <form @submit.prevent="signUp">
        <input v-model="name" type="text" placeholder="Full Name" required />
        <input v-model="email" type="email" placeholder="Email" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <input v-model="address" type="text" placeholder="Address" />
        <input v-model="phone" type="text" placeholder="Phone Number" />
        <button type="submit">Sign Up</button>
      </form>
  
      <!-- <button @click="googleSignUp">Sign up with Google</button> -->
  
      <p>
        Already have an account?
        <router-link to="/login">Login</router-link>
      </p>
    </div>
  </template>
  
  <script>
  import customerApi from "../api/customerApi";
  
  export default {
    data() {
      return {
        name: "",
        email: "",
        password: "",
        address: "",
        phone: "",
      };
    },
    methods: {
      async signUp() {
        try {
          const response = await customerApi.register({
            email: this.email,
            password: this.password,
            name: this.name,
            address: this.address,
            phone: this.phone,
          });
  
          if (response.status === 201) {
            alert("Registration successful!");
            this.$router.push("/login");
          } else {
            alert(response.data.message);
          }
        } catch (error) {
          alert("Sign-up failed.");
        }
      },
  
    //   async googleSignUp() {
    //     try {
    //       const provider = new window.firebase.auth.GoogleAuthProvider();
    //       const result = await window.firebase.auth().signInWithPopup(provider);
    //       const token = await result.user.getIdToken();
  
    //       const response = await customerApi.googleLogin(token);
  
    //       if (response.status === 201) {
    //         alert("Google sign-up successful!");
    //         this.$router.push("/profile");
    //       } else {
    //         alert(response.data.message);
    //       }
    //     } catch (error) {
    //       alert("Google Sign-Up failed.");
    //     }
    //   },
    },
  };
  </script>
  
  <style scoped>
  .signup-container {
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
    background: green;
    color: white;
    border: none;
  }
  </style>
  