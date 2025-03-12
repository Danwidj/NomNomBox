import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
import { getAuth } from "firebase/auth";
// import { getAnalytics } from "firebase/analytics";

// Firebase Config (Move to .env for security)
// Import the functions you need from the SDKs you need

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
const db = getFirestore(app);
const auth = getAuth(app);

export { db, auth };
