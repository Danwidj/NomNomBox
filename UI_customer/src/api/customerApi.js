import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:5002"; // Change if deployed

export default {
  async register(userData) {
    return axios.post(`${API_BASE_URL}/register`, userData);
  },

  async login(credentials) {
    return axios.post(`${API_BASE_URL}/login`, credentials);
  },

  async googleLogin(token) {
    return axios.post(`${API_BASE_URL}/register`, {}, {
      headers: { Authorization: `Bearer ${token}` },
      withCredentials: true,
    });
  },

  async getCustomerDetails(customerId, token) {
    return axios.get(`${API_BASE_URL}/customer/${customerId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
  },
};
