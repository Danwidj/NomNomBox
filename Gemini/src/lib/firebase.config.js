// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";

const firebaseConfig = {
  apiKey: "AIzaSyAI-zk5Trivco0ZGTLHLEe3FhJGVtfQuQM",
  authDomain: "nomnombox-8bf47.firebaseapp.com",
  projectId: "nomnombox-8bf47",
  storageBucket: "nomnombox-8bf47.firebasestorage.app",
  messagingSenderId: "1059298931718",
  appId: "1:1059298931718:web:4aee9c812811194daaff87",
  measurementId: "G-JRKKFCWMHR"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);