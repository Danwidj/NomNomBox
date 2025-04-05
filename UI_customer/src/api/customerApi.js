import axios from 'axios'

// Use the service name from docker-compose.yml instead of localhost
const API_URL = 'http://localhost:5003'

const customerApi = {
  // Register a new customer
  register(userData) {
    return axios.post(`${API_URL}/register`, userData)
  },

  // Login a customer
  login(credentials) {
    return axios.post(`${API_URL}/login`, credentials)
  },

  // Get customer details
  getCustomerDetails(customerId, token) {
    return axios.get(`${API_URL}/customer/${customerId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
  },

  // Update customer details
  updateCustomerDetails(customerId, updateData, token) {
    return axios.put(`${API_URL}/customer/${customerId}`, updateData, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
  },

  // Get all customers (admin only)
  getAllCustomers(token) {
    return axios.get(`${API_URL}/customer`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
  },

  // Delete a customer (admin or self)
  deleteCustomer(customerId, token) {
    return axios.delete(`${API_URL}/customer/${customerId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
  },
}

export default customerApi
