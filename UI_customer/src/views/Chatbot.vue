<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { fetchConvo, sendPrompt } from '@/lib/chatService'

const messages = ref([
  {
    text: "Hello! How can I help you today?",
    sender: 'bot',
    timestamp: new Date().toLocaleTimeString()
  }
])
const newMessage = ref('')
const isLoading = ref(false)
const uid = 'D2lgMOKmVFvRLFBUiNa1'; // Replace with actual user ID
const messageContainer = ref(null)

// Fetch messages on component mount
onMounted(async () => {
  await loadMessages();
});

// Auto-scroll to the latest message
watch(() => messages.value.length, () => {
  nextTick(() => {
    if (messageContainer.value) {
      messageContainer.value.scrollTop = messageContainer.value.scrollHeight;
    }
  });
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
      text: data.response,
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
  <div class="nom-container py-8 flex justify-center">
    <div class="w-full max-w-4xl h-[80vh] bg-card shadow-lg rounded-xl flex flex-col overflow-hidden border border-border nom-fade-in">
      <div class="bg-primary text-primary-foreground px-6 py-4 flex items-center justify-between">
        <div>
          <h1 class="text-xl font-medium">Meal Recommendations</h1>
          <p class="text-sm text-primary-foreground/90">Ask for personalized meal suggestions</p>
        </div>
      </div>

      <div class="flex-1 p-4 overflow-y-auto bg-muted/30" ref="messageContainer">
        <div 
          v-for="(message, index) in messages" 
          :key="index" 
          :class="[
            'mb-4 max-w-[80%]',
            message.sender === 'user' ? 'ml-auto' : 'mr-auto'
          ]"
        >
          <div 
            :class="[
              'p-4 rounded-lg shadow-sm',
              message.sender === 'user' 
                ? 'bg-primary text-primary-foreground rounded-br-none' 
                : 'bg-card border border-border rounded-bl-none'
            ]"
          >
            <div class="mb-2 whitespace-pre-line">{{ message.text }}</div>
            <div class="text-xs opacity-70 text-right">{{ message.timestamp }}</div>
          </div>
        </div>
        
        <div 
          v-if="isLoading" 
          class="mr-auto max-w-[80%] bg-card p-4 rounded-lg shadow-sm rounded-bl-none border border-border"
        >
          <div class="flex gap-1 items-center">
            <div class="w-2 h-2 bg-primary rounded-full animate-bounce" style="animation-delay: 0s"></div>
            <div class="w-2 h-2 bg-primary rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
            <div class="w-2 h-2 bg-primary rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
          </div>
        </div>
      </div>

      <div class="p-4 bg-card border-t border-border">
        <div class="flex gap-2">
          <input 
            v-model="newMessage" 
            @keyup.enter="sendMessage" 
            placeholder="Type your message here..." 
            type="text"
            :disabled="isLoading"
            class="nom-input"
          />
          <button 
            @click="sendMessage" 
            :disabled="isLoading"
            class="nom-btn-primary px-6"
          >
            Send
          </button>
        </div>
        <div class="mt-2 text-xs text-muted-foreground">
          Try asking: "What meals are good for a vegetarian diet?" or "Recommend some quick dinners"
        </div>
      </div>
    </div>
  </div>
</template>