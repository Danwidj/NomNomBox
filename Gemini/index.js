// server.js
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const admin = require('firebase-admin');

// Initialize Firebase Admin SDK
const serviceAccount = require('./nomnombox-8bf47-firebase-adminsdk-fbsvc-6b42b7194a.json'); // Update the path to your service account key


admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
});

const db = admin.firestore();
const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(bodyParser.json());

// Helper function
function time_generator() {
    const timestamp = Date.now();
    const date = new Date(timestamp);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    return `${year}-${month}-${day},${hours}:${minutes}:${seconds}`;
}

// Endpoint to listen for real-time updates
app.get('/messages/:uid', (req, res) => {
    const { uid } = req.params;
    const messagesCollection = db.collection(`users/${uid}/messages`);

    // Set up a listener for real-time updates
    const unsubscribe = messagesCollection.orderBy('createTime', 'asc').onSnapshot(snapshot => {
        const messages = snapshot.docs.map(doc => ({
            id: doc.id,
            ...doc.data(),
        }));
        // Send the updated messages to the client
        res.json(messages);
    }, error => {
        console.error("Error fetching messages: ", error);
        res.status(500).send("Error fetching messages");
    });

    // Optionally, you can return a way to unsubscribe from the listener
    // For example, you could store the unsubscribe function and call it when needed
});

// Endpoint to send a message
app.post('/messages', async (req, res) => {
    const { uid, prompt } = req.body;

    if (!prompt) {
        return res.status(400).send("Prompt is required");
    }

    const messagesCollection = db.collection(`users/${uid}/messages`);

    try {
        const ID = time_generator() + "{" + uid + "}";
        await messagesCollection.doc(ID).set({
            prompt,
            createTime: admin.firestore.FieldValue.serverTimestamp(),
        });

        // Simulate getting a response
        const responseData = await getResponseData(prompt);
        res.status(200).json({ id: ID, prompt, response: responseData });
    } catch (error) {
        console.error("Error adding message: ", error);
        res.status(500).send("Error adding message");
    }
});

// Example function to simulate getting a response
const getResponseData = async (prompt) => {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(`Response for: ${prompt}`);
        }, 2000);
    });
};

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});