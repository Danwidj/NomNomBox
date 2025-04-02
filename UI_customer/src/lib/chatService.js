import axios from 'axios';

const CHAT_HISTORY_URL = 'http://localhost:5012';
const SEND_QUERY_URL = 'http://localhost:5100';

export const fetchConvo = async () => {
    try {
        const token = sessionStorage.getItem('token');
        const customerId = sessionStorage.getItem('customerId');

        console.log('Fetching conversation with:', {
            customerId,
            token: token ? 'Bearer ' + token : 'No token'
        });

        if (!token) {
            throw new Error('No authentication token found');
        }
        if (!customerId) {
            throw new Error('No customer ID found');
        }

        console.log('Making request to:', `${CHAT_HISTORY_URL}/chat/${customerId}`);

        const response = await axios.get(`${CHAT_HISTORY_URL}/chat/${customerId}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        console.log('Raw response from chat history:', response.data);

        // The backend returns { messages: [...] }
        const messages = response.data.messages || [];
        console.log('Extracted messages:', messages);

        return messages;
    } catch (error) {
        console.error('Error in fetchConvo:', error);
        if (error.response) {
            console.error('Response data:', error.response.data);
            console.error('Response status:', error.response.status);
        }
        throw error;
    }
};

export const sendPrompt = async (prompt) => {
    try {
        const token = sessionStorage.getItem('token');
        const customerId = sessionStorage.getItem('customerId');

        console.log('Sending prompt with:', {
            customerId,
            token: token ? 'Bearer ' + token : 'No token',
            prompt
        });

        if (!token) {
            throw new Error('No authentication token found');
        }
        if (!customerId) {
            throw new Error('No customer ID found');
        }

        console.log('Making request to:', `${SEND_QUERY_URL}/api/recommendations/${customerId}`);

        const response = await axios.post(
            `${SEND_QUERY_URL}/api/recommendations/${customerId}`,
            { prompt },
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            }
        );

        console.log('Response from send prompt:', response.data);
        return response.data;
    } catch (error) {
        console.error('Error in sendPrompt:', error);
        if (error.response) {
            console.error('Response data:', error.response.data);
            console.error('Response status:', error.response.status);
        }
        throw error;
    }
};