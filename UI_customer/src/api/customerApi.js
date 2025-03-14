import axios from "axios";

const API_URL = "http://127.0.0.1:5002";  // Customer Microservice URL

//Register Customer
export const registerCustomer = async (userData) => {
  return axios.post(`${API_URL}/register`, userData);
};

//Get Customer Data (Requires Auth Token)
export const getCustomer = async (customerId, token) => {
  return axios.get(`${API_URL}/customer/${customerId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
};
