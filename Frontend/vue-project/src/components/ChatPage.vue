<template>
  <div class="chat-container">
    <h1>AI ChatBot</h1>
    <div class="chat-window">
      <div v-for="(message, index) in messages" :key="index" class="message">
        <div :class="['message-bubble', message.sender]">
          <span>{{ message.text }}</span>
        </div>
      </div>
    </div>
    <div class="input-area">
      <input v-model="userMessage" @keyup.enter="sendMessage" placeholder="Type your message..." />
      <button @click="sendMessage">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="send-icon">
          <line x1="22" y1="2" x2="11" y2="13"></line>
          <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
        </svg>
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ChatPage',
  data() {
    return {
      userMessage: '',
      messages: [],
    };
  },
  methods: {
    async sendMessage() {
      if (this.userMessage.trim() === '') return;

      // Add user's message to the chat
      this.messages.push({ text: this.userMessage, sender: 'user' });

      try {
        const response = await axios.post('http://127.0.0.1:5000/chat', {
          message: this.userMessage,
        }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('authToken')}`,
          },
        });

        // Add chatbot's reply to the chat
        this.messages.push({ text: response.data.reply, sender: 'bot' });
      } catch (error) {
        console.error(error);
        this.messages.push({ text: 'Error communicating with the server.', sender: 'bot' });
      }

      this.userMessage = '';
    },
  },
};
</script>

<style>
body {
  font-family: 'Roboto', sans-serif;
  background: linear-gradient(135deg, #cb9eff, #aabaff); /* Matches the blue of the chat container */
  height: 100vh; /* Ensures the gradient covers the full viewport height */
}
.chat-container {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  border-radius: 16px;
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
  font-family: 'Roboto', sans-serif;
  color: #fff;
  transition: transform 0.3s ease;
}

.chat-container:hover {
  transform: scale(1.02);
}

h1 {
  text-align: center;
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 20px;
}

.chat-window {
  height: 400px;
  overflow-y: auto;
  border-radius: 12px;
  padding: 15px;
  background: rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
  gap: 10px;
  box-shadow: inset 0 4px 6px rgba(0, 0, 0, 0.1);
  scrollbar-width: thin;
  scrollbar-color: #888 #333;
}

.chat-window::-webkit-scrollbar {
  width: 8px;
}

.chat-window::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.chat-window::-webkit-scrollbar-track {
  background: #333;
}

.message {
  display: flex;
  align-items: flex-start;
}

.message-bubble {
  max-width: 70%;
  padding: 12px 18px;
  border-radius: 18px;
  font-size: 16px;
  line-height: 1.5;
  position: relative;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.user {
  align-self: flex-end;
  background: linear-gradient(135deg, #ff9a9e, #fad0c4);
  color: #fff;
  border-top-right-radius: 0;
}

.bot {
  align-self: flex-start;
  background: linear-gradient(135deg, #a1c4fd, #c2e9fb);
  color: #333;
  border-top-left-radius: 0;
}

.input-area {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

input {
  flex-grow: 1;
  padding: 14px;
  border: none;
  border-radius: 16px;
  font-size: 16px;
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
  outline: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: background 0.3s ease;
}

input:focus {
  background: rgba(255, 255, 255, 0.3);
}

input::placeholder {
  color: #ddd;
}

button {
  padding: 12px 16px;
  border: none;
  border-radius: 16px;
  background: linear-gradient(135deg, #43e97b, #38f9d7);
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease, background 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

button:hover {
  background: linear-gradient(135deg, #3dd68b, #2fd8c8);
  transform: translateY(-2px);
}

button:active {
  transform: translateY(0);
}

.send-icon {
  width: 22px;
  height: 22px;
}
</style>
