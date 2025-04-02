import axios from 'axios';

const INVENTORY_API_URL = 'http://localhost:5006/inventory';

export const fetchMealKitDetails = async (kitId) => {
    try {
        console.log('Fetching meal kit details for:', kitId);
        const response = await axios.get(`${INVENTORY_API_URL}/${kitId}`);
        console.log('Raw inventory response:', response);

        if (response.data && response.data.code === 200 && response.data.data) {
            console.log('Processed meal kit details:', response.data.data);
            return response.data.data;
        }
        console.warn('Invalid response structure:', response.data);
        throw new Error(response.data.message || 'Failed to fetch meal kit details');
    } catch (error) {
        console.error('Error fetching meal kit:', error);
        throw error;
    }
};

export const fetchAllMealKits = async () => {
    try {
        const response = await axios.get(INVENTORY_API_URL);
        if (response.data.code === 200) {
            return response.data.data;
        }
        throw new Error(response.data.message || 'Failed to fetch meal kits');
    } catch (error) {
        console.error('Error fetching meal kits:', error);
        throw error;
    }
}; 