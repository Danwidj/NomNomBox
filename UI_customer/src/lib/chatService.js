import axios from 'axios';


export const fetchConvo = async (uid) => {
    const API_URL = 'http://localhost:3000/messages';
    try {
        const response = await axios.get(`${API_URL}/${uid}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching messages:', error);
        throw error; // Rethrow the error for handling in the component
    }
};

// New function to send a prompt to the API
export const sendPrompt = async (uid, prompt) => {
    try {
        const API_URL = 'http://localhost:3000/messages';
        const response = await axios.post(`${API_URL}`, {
            uid: uid, // Include user ID if needed
            prompt: prompt // Send the user's prompt
        });
        return response.data; // Return the response from the server
    } catch (error) {
        console.error('Error sending prompt:', error);
        throw error; // Rethrow the error for handling in the component
    }
};

