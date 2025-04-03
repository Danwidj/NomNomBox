import { ref } from 'vue';
import customerApi from '@/api/customerApi';

// Reactive state for authentication
export const isAuthenticated = ref(false);
export const currentUser = ref({
  id: null,
  name: '',
  email: ''
});

// Initialize the auth state from localStorage
export const initAuth = () => {
  const token = localStorage.getItem('token');
  const userId = localStorage.getItem('userId');
  const authStatus = localStorage.getItem('isAuthenticated');
  
  if (token && userId && authStatus === 'true') {
    isAuthenticated.value = true;
    currentUser.value.id = userId;
    
    // Ensure sessionStorage is also set for components that rely on it
    sessionStorage.setItem('token', token);
    sessionStorage.setItem('customerId', userId);
    sessionStorage.setItem('isAuthenticated', 'true');
    
    // Optionally fetch additional user details
    if (userId) {
      fetchUserDetails(userId, token);
    }
  } else {
    // Clear any inconsistent state
    isAuthenticated.value = false;
    currentUser.value = { id: null, name: '', email: '' };
    
    // Also clear sessionStorage items to ensure consistency
    clearAuthStorage();
  }
};

// Helper function to clear all auth-related storage
const clearAuthStorage = () => {
  // Clear localStorage
  localStorage.removeItem('token');
  localStorage.removeItem('userId');
  localStorage.removeItem('isAuthenticated');
  
  // Clear sessionStorage as well
  sessionStorage.removeItem('token');
  sessionStorage.removeItem('customerId');
  sessionStorage.removeItem('userId');
  sessionStorage.removeItem('isAuthenticated');
};

// Fetch user details from the API
const fetchUserDetails = async (userId, token) => {
  try {
    const response = await customerApi.getCustomerDetails(userId, token);
    if (response.data && response.data.data) {
      currentUser.value.name = response.data.data.name || '';
      currentUser.value.email = response.data.data.email || '';
    }
  } catch (error) {
    console.error('Failed to fetch user details:', error);
    // If token is invalid, log out
    if (error.response && error.response.status === 401) {
      logout();
    }
  }
};

// Login function
export const login = (userId, token, userName = '') => {
  // Update localStorage
  localStorage.setItem('token', token);
  localStorage.setItem('userId', userId);
  localStorage.setItem('isAuthenticated', 'true');
  
  // Update sessionStorage for components that rely on it
  sessionStorage.setItem('token', token);
  sessionStorage.setItem('customerId', userId);
  sessionStorage.setItem('isAuthenticated', 'true');
  
  // Update reactive state
  isAuthenticated.value = true;
  currentUser.value.id = userId;
  currentUser.value.name = userName;
  
  // If userName wasn't provided, fetch user details
  if (!userName && token) {
    fetchUserDetails(userId, token);
  }
  
  // Notify components that user has logged in
  window.dispatchEvent(new Event('userLoggedIn'));
};

// Logout function
export const logout = () => {
  // Clear all auth storage
  clearAuthStorage();
  
  // Also clear shopping cart if needed
  sessionStorage.removeItem('shoppingCart');
  
  // Update reactive state
  isAuthenticated.value = false;
  currentUser.value = { id: null, name: '', email: '' };
  
  // Notify components that user has logged out
  window.dispatchEvent(new Event('userLoggedOut'));
  
  console.log('User logged out successfully');
};