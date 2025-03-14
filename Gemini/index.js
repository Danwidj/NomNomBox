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

//Helper function
function time_generator() {
    // Get the current timestamp in milliseconds
    const timestamp = Date.now();

    // Create a new Date object using the timestamp
    const date = new Date(timestamp);

    // Extract the components of the date
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are 0-based
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');

    // Construct the formatted date string
    return `${year}/${month}/${day},${hours}:${minutes}:${seconds}`;
}

// Endpoint to get messages
app.get('/messages/:uid', async (req, res) => {
    const { uid } = req.params;
    const messagesCollection = db.collection(`users/${uid}/messages`);

    try {
        const snapshot = await messagesCollection.orderBy('createTime', 'asc').get();
        const messages = snapshot.docs.map(doc => ({
            id: doc.id,
            ...doc.data(),
        }));
        res.status(200).json(messages);
    } catch (error) {
        console.error("Error fetching messages: ", error);
        res.status(500).send("Error fetching messages");
    }
});

// Endpoint to send a message
app.post('/messages', async (req, res) => {
    const { uid } = req.body;
    const { prompt } = req.body;

    if (!prompt) {
        return res.status(400).send("Prompt is required");
    }

    const messagesCollection = db.collection(`users/${uid}/messages`);

    try {
        /* const newMessageRef = await messagesCollection.add({
            prompt,
            createTime: admin.firestore.FieldValue.serverTimestamp(),
        }); */
        const ID = time_generator() + "{" + uid + "}"


        await messagesCollection.doc(ID).set({
            prompt,
            createTime: admin.firestore.FieldValue.serverTimestamp(),
        });

        res.status(200).json({'id':ID, prompt});
    } catch (error) {
        console.error("Error adding message: ", error);
        res.status(500).send("Error adding message");
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});