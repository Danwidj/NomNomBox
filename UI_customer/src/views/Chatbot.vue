<script setup>
import { ref, onMounted } from 'vue'
import { fetchConvo, sendPrompt } from '@/lib/chatService'

const messages = ref([
  {
    text: "Hello! How can I help you today?", // Initial bot message
    sender: 'bot',
    timestamp: new Date().toLocaleTimeString()
  }
])
const newMessage = ref('')
const isLoading = ref(false)
const uid = 'D2lgMOKmVFvRLFBUiNa1'; // Replace with actual user ID

// Fetch messages on component mount
onMounted(async () => {
  await loadMessages(); // Load messages when component mounts
});

// Function to load messages
const loadMessages = async () => {
  try {
    const data = await fetchConvo(uid);

    for (let i = 0; i < data.length; i++) {
      const msg = data[i];
      messages.value.push({
        text: msg.prompt,
        sender: 'user',
        timestamp: new Date().toLocaleTimeString()
      });
      messages.value.push({
        text: msg.response,
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString()
      });
    }
  } catch (error) {
    console.error('Failed to load messages:', error);
  }
};

const sendMessage = async () => {
  if (newMessage.value.trim()) {
    // Add user message
    const userMessage = {
      text: newMessage.value,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString()
    };
    messages.value.push(userMessage);

    newMessage.value = '';
    isLoading.value = true;

    try {
      // Use sendPrompt to send the user's message
      const data = await sendPrompt(uid, userMessage.text);
      console.log(data)

      const botMessage = {
      text: data.response, // Assuming the response contains the bot's reply
      sender: 'bot',
      timestamp: new Date().toLocaleTimeString()
      }
      messages.value.push(botMessage);
    } catch (error) {
      console.error('Error:', error);
      messages.value.push({
        text: "I apologize, but I'm having trouble connecting right now. Please try again later.",
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString()
      });
    } finally {
      isLoading.value = false;
    }
  }
}
</script>

<template>
  <div class="chat-container">
    <div class="chat-header">
      <h1>Reccomendation</h1>
    </div>

    <div class="chat-messages" ref="messageContainer">
      <div v-for="(message, index) in messages" :key="index" :class="['message', message.sender]">
        <div class="message-content">
          {{ message.text }}
        </div>
        <div class="message-timestamp">
          {{ message.timestamp }}
        </div>
      </div>
      <div v-if="isLoading" class="message bot loading">
        <div class="typing-indicator">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </div>

    <div class="chat-input">
      <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="Type your message here..." type="text"
        :disabled="isLoading" />
      <button @click="sendMessage" :disabled="isLoading">
        Send
      </button>
    </div>
  </div>
</template>

<style scoped>
.chat-container {
  width: 60vw;
  /* 60% of viewport width */
  max-width: 1200px;
  /* Cap the width on large screens */
  height: 80vh;
  /* 80% of viewport height */
  margin: 0 auto;
  /* Not strictly needed if parent is flex + center */
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-header {
  background-color: #1a73e8;
  color: white;
  padding: 20px;
  text-align: center;
}

.chat-header h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 500;
}

.chat-header p {
  margin: 5px 0 0;
  font-size: 14px;
  opacity: 0.9;
}

.chat-messages {
  flex-grow: 1;
  overflow-y: auto;
  padding: 20px;
  background-color: #f1f3f4;
}

.message {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 12px;
  position: relative;
  margin-bottom: 15px;
}

.message.user {
  background-color: #1a73e8;
  color: white;
  align-self: flex-end;
  border-bottom-right-radius: 4px;
  margin-left: auto;
}

.message.bot {
  background-color: #fff;
  color: #202124;
  align-self: flex-start;
  border-bottom-left-radius: 4px;
  margin-right: auto;
}

.message-content {
  margin-bottom: 4px;
  line-height: 1.4;
}

.message-timestamp {
  font-size: 11px;
  opacity: 0.7;
}

.chat-input {
  padding: 20px;
  background-color: white;
  border-top: 1px solid #e0e0e0;
  display: flex;
  gap: 10px;
}

input {
  flex-grow: 1;
  padding: 12px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  outline: none;
  font-size: 14px;
  transition: border-color 0.2s;
}

input:focus {
  border-color: #1a73e8;
}

button {
  padding: 12px 24px;
  background-color: #1a73e8;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #1557b0;
}

button:active {
  background-color: #174ea6;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 12px 16px;
  background: white;
  border-radius: 12px;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: #1a73e8;
  border-radius: 50%;
  animation: bounce 1.5s infinite;
  opacity: 0.6;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {

  0%,
  60%,
  100% {
    transform: translateY(0);
  }

  30% {
    transform: translateY(-4px);
  }
}

input:disabled,
button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.loading {
  opacity: 0.7;
}
</style>