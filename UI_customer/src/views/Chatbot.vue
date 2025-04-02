<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { fetchConvo, sendPrompt } from '@/lib/chatService'
import { fetchMealKitDetails } from '@/lib/inventoryService'
import { useRouter } from 'vue-router'

// ===== State Management =====
const messages = ref([])
const newMessage = ref('')
const isLoading = ref(false)
const isInitialLoading = ref(true)
const messageContainer = ref(null)
const streamingMessage = ref('')
const isStreaming = ref(false)
const mealKits = ref([])
const router = useRouter()

// ===== Auto-scrolling Functionality =====
// Watch for new messages and scroll to bottom
watch(() => messages.value.length, () => {
  scrollToBottom();
});

// Watch streaming message for auto-scroll
watch(() => streamingMessage.value, () => {
  scrollToBottom();
});

// Helper function to scroll to bottom of message container
const scrollToBottom = () => {
  nextTick(() => {
    if (messageContainer.value) {
      messageContainer.value.scrollTop = messageContainer.value.scrollHeight;
    }
  });
};

// ===== Message Streaming =====
// Function to simulate streaming text
const streamText = async (text, delay = 30) => {
  isStreaming.value = true;
  streamingMessage.value = '';

  for (let i = 0; i < text.length; i++) {
    streamingMessage.value += text[i];
    await new Promise(resolve => setTimeout(resolve, delay));
  }

  isStreaming.value = false;
  return streamingMessage.value;
};

// ===== Meal Kit Processing =====
// Function to fetch and process meal kit details
const fetchMealKitDetailsById = async (mealId) => {
  try {
    console.log('Fetching details for meal kit:', mealId);
    const response = await fetchMealKitDetails(mealId);

    if (response) {
      return {
        id: mealId,
        name: response.name || 'Unknown Meal',
        price: response.price || 0,
        description: response.description || '',
        preparationTime: response.preparationTime || 0,
        servings: response.servings || 1,
        imageURL: response.imageURL || ''
      };
    }
    return null;
  } catch (error) {
    console.error(`Error fetching details for meal kit ${mealId}:`, error);
    return null;
  }
};

// Function to process recommended meal kits
const processRecommendedMealKits = async (recommendedMealKits) => {
  if (!Array.isArray(recommendedMealKits) || recommendedMealKits.length === 0) {
    return [];
  }

  console.log('Processing meal kits:', recommendedMealKits);
  const mealKits = await Promise.all(
    recommendedMealKits.map(fetchMealKitDetailsById)
  );

  // Filter out any null values from failed requests
  return mealKits.filter(meal => meal !== null);
};

// ===== Chat History Management =====
// Function to load messages from chat history
const loadMessages = async () => {
  try {
    console.log('Fetching chat history...');
    const data = await fetchConvo();

    if (!Array.isArray(data)) {
      console.warn('Chat history is not an array:', data);
      return;
    }

    // Sort messages by created_at if available
    const sortedMessages = [...data].sort((a, b) => {
      const timeA = a.created_at ? new Date(a.created_at).getTime() : 0;
      const timeB = b.created_at ? new Date(b.created_at).getTime() : 0;
      return timeA - timeB;
    });

    // Add welcome message first
    messages.value = [{
      text: "Hello! How can I help you today?",
      sender: 'bot',
      timestamp: new Date().toISOString()
    }];

    // Process each message from the chat history
    for (const msg of sortedMessages) {
      const msgTime = msg.created_at || new Date().toISOString();

      // Add user message first (from prompt)
      messages.value.push({
        text: msg.prompt,
        sender: 'user',
        timestamp: msgTime
      });

      // Process bot response if it exists
      if (msg.response) {
        // Get meal kit details if there are any recommendations
        const recommendedMealKits = msg.recommended_meal_kits || msg['recommended meal-kit'] || [];
        const mealKits = await processRecommendedMealKits(recommendedMealKits);

        messages.value.push({
          text: msg.response,
          sender: 'bot',
          timestamp: msgTime,
          recommended_meal_kits: mealKits
        });
      }
    }
  } catch (error) {
    console.error('Failed to load messages:', error);
  } finally {
    isInitialLoading.value = false;
  }
};

// ===== Message Sending =====
const sendMessage = async () => {
  if (!newMessage.value.trim()) return;

  const currentTime = new Date().toISOString();

  // Add user message
  const userMessage = {
    text: newMessage.value,
    sender: 'user',
    timestamp: currentTime
  };
  messages.value.push(userMessage);

  newMessage.value = '';
  isLoading.value = true;
  mealKits.value = []; // Reset meal kits

  try {
    // Use sendPrompt to send the user's message
    const data = await sendPrompt(userMessage.text);

    isLoading.value = false;

    // Get meal kit details for each recommended meal kit
    const recommendedMealKits = data.recommended_meal_kits || data['recommended meal-kit'] || [];

    // Stream the bot's response first
    await streamText(data.response);

    // Then fetch and show meal kits with animation
    if (Array.isArray(recommendedMealKits) && recommendedMealKits.length > 0) {
      mealKits.value = await processRecommendedMealKits(recommendedMealKits);
    }

    // After streaming and showing meal kits, add the complete message
    const botMessage = {
      text: data.response,
      sender: 'bot',
      timestamp: currentTime,
      recommended_meal_kits: mealKits.value
    };

    // Small delay before adding the final message to ensure animations complete
    await new Promise(resolve => setTimeout(resolve, 500));
    messages.value.push(botMessage);
    streamingMessage.value = ''; // Clear streaming message
    mealKits.value = []; // Clear streaming meal kits
  } catch (error) {
    console.error('Error:', error);
    isLoading.value = false;
    messages.value.push({
      text: "I apologize, but I'm having trouble connecting right now. Please try again later.",
      sender: 'bot',
      timestamp: currentTime
    });
  }
};

// ===== Cart Management =====
const addToCart = async (mealKit) => {
  try {
    // Get existing cart from sessionStorage or initialize empty array
    const cart = JSON.parse(sessionStorage.getItem('shoppingCart') || '[]');

    // Create a clean meal kit object with only the necessary data
    const cartItem = {
      id: mealKit.id,
      name: mealKit.name,
      price: mealKit.price,
      imageURL: mealKit.imageURL,
      description: mealKit.description,
      preparationTime: mealKit.preparationTime,
      servings: mealKit.servings,
      quantity: 1,
      stock: 10, // Adding default stock value
      addedAt: new Date().toISOString()
    };

    // Check if item already exists in cart
    const existingItemIndex = cart.findIndex(item => item.id === mealKit.id);

    if (existingItemIndex >= 0) {
      // If item exists, increment quantity
      cart[existingItemIndex].quantity += 1;
    } else {
      // If item doesn't exist, add new item
      cart.push(cartItem);
    }

    // Save back to sessionStorage
    sessionStorage.setItem('shoppingCart', JSON.stringify(cart));
    console.log('Cart updated:', cart);

    // Navigate to shopping cart page
    router.push('/cart');
  } catch (error) {
    console.error('Error adding to cart:', error);
    console.error('Meal kit data:', mealKit);
  }
};

// ===== Lifecycle Hooks =====
// Fetch messages on component mount
onMounted(async () => {
  await loadMessages();
});
</script>

<template>
  <div class="nom-container py-8 flex justify-center">
    <div
      class="w-full max-w-4xl h-[80vh] bg-card shadow-lg rounded-xl flex flex-col overflow-hidden border border-border nom-fade-in">
      <div class="bg-primary text-primary-foreground px-6 py-4 flex items-center justify-between">
        <div>
          <h1 class="text-xl font-medium">Meal Recommendations</h1>
          <p class="text-sm text-primary-foreground/90">Ask for personalized meal suggestions</p>
        </div>
      </div>

      <div class="flex-1 p-4 overflow-y-auto bg-muted/30" ref="messageContainer">
        <!-- Initial Loading State -->
        <div v-if="isInitialLoading" class="flex flex-col items-center justify-center h-full">
          <div class="flex gap-2 items-center mb-4">
            <div class="w-3 h-3 bg-primary rounded-full animate-bounce" style="animation-delay: 0s"></div>
            <div class="w-3 h-3 bg-primary rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
            <div class="w-3 h-3 bg-primary rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
          </div>
          <p class="text-sm text-muted-foreground">Loading chat history...</p>
        </div>

        <!-- Chat Messages -->
        <div v-else>
          <div v-for="(message, index) in messages" :key="index" :class="[
            'mb-4 max-w-[80%]',
            message.sender === 'user' ? 'ml-auto' : 'mr-auto'
          ]">
            <div :class="[
              'p-4 rounded-lg shadow-sm relative',
              message.sender === 'user'
                ? 'bg-primary text-primary-foreground rounded-br-none'
                : 'bg-card border border-border rounded-bl-none'
            ]">
              <div class="whitespace-pre-line">{{ message.text }}</div>

              <!-- Recommended Meal Kits -->
              <div v-if="message.sender === 'bot' && message.recommended_meal_kits?.length > 0"
                class="mt-4 border-t border-border/50 pt-3 meal-kits-container">
                <div class="text-sm font-medium mb-2">Recommended Meal Kits:</div>
                <TransitionGroup name="meal-kit" tag="div" class="flex flex-col gap-2">
                  <div v-for="(meal, index) in message.recommended_meal_kits" :key="meal.id"
                    :style="{ transitionDelay: `${index * 150}ms` }"
                    class="flex items-center gap-3 p-2 bg-muted/30 rounded-lg">
                    <img v-if="meal.imageURL" :src="meal.imageURL" :alt="meal.name"
                      class="w-16 h-16 object-cover rounded-md" @error="$event.target.style.display = 'none'" />
                    <div class="flex-1">
                      <div class="font-medium">{{ meal.name }}</div>
                      <div class="text-sm text-muted-foreground">${{ meal.price }}</div>
                    </div>
                    <button @click="addToCart(meal)"
                      class="px-3 py-1 bg-primary text-primary-foreground text-sm rounded-md hover:bg-primary/90 transition-colors">
                      Add to Cart
                    </button>
                  </div>
                </TransitionGroup>
              </div>

              <div class="text-xs opacity-70 text-right mt-1 absolute bottom-1 right-2">
                {{ new Date(message.timestamp).toLocaleTimeString() }}
              </div>
            </div>
          </div>

          <!-- Streaming message -->
          <div v-if="streamingMessage" class="mb-4 max-w-[80%] mr-auto">
            <div class="p-4 rounded-lg shadow-sm bg-card border border-border rounded-bl-none relative">
              <div class="whitespace-pre-line">{{ streamingMessage }}<span class="animate-pulse">▋</span></div>

              <!-- Recommended Meal Kits for streaming message -->
              <Transition name="fade">
                <div v-if="mealKits?.length > 0" class="mt-4 border-t border-border/50 pt-3 meal-kits-container">
                  <div class="text-sm font-medium mb-2">Recommended Meal Kits:</div>
                  <TransitionGroup name="meal-kit" tag="div" class="flex flex-col gap-2">
                    <div v-for="(meal, index) in mealKits" :key="meal.id"
                      :style="{ transitionDelay: `${index * 150}ms` }"
                      class="flex items-center gap-3 p-2 bg-muted/30 rounded-lg">
                      <img v-if="meal.imageURL" :src="meal.imageURL" :alt="meal.name"
                        class="w-16 h-16 object-cover rounded-md" @error="$event.target.style.display = 'none'" />
                      <div class="flex-1">
                        <div class="font-medium">{{ meal.name }}</div>
                        <div class="text-sm text-muted-foreground">${{ meal.price }}</div>
                      </div>
                      <button @click="addToCart(meal)"
                        class="px-3 py-1 bg-primary text-primary-foreground text-sm rounded-md hover:bg-primary/90 transition-colors">
                        Add to Cart
                      </button>
                    </div>
                  </TransitionGroup>
                </div>
              </Transition>

              <div class="text-xs opacity-70 text-right mt-1 absolute bottom-1 right-2">
                {{ new Date().toLocaleTimeString() }}
              </div>
            </div>
          </div>

          <!-- Loading indicator -->
          <div v-if="isLoading"
            class="mr-auto max-w-[80%] bg-card p-4 rounded-lg shadow-sm rounded-bl-none border border-border">
            <div class="flex gap-1 items-center">
              <div class="w-2 h-2 bg-primary rounded-full animate-bounce" style="animation-delay: 0s"></div>
              <div class="w-2 h-2 bg-primary rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
              <div class="w-2 h-2 bg-primary rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
            </div>
          </div>
        </div>
      </div>

      <div class="p-4 bg-card border-t border-border">
        <div class="flex gap-2">
          <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="Type your message here..." type="text"
            :disabled="isLoading || isStreaming || isInitialLoading" class="nom-input" />
          <button @click="sendMessage" :disabled="isLoading || isStreaming || isInitialLoading"
            class="nom-btn-primary px-6">
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

<style scoped>
.fade-enter-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from {
  opacity: 0;
}

.fade-enter-to {
  opacity: 1;
}

.meal-kit-enter-active {
  transition: all 0.5s ease;
}

.meal-kit-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.meal-kit-enter-to {
  opacity: 1;
  transform: translateY(0);
}

.meal-kits-container {
  transition: max-height 0.5s ease-in-out;
}
</style>