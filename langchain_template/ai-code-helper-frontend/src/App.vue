<template>
  <div class="app">
    <div class="app-header">
      <h1 class="app-title">AI Coding Assistant</h1>
      <div class="app-subtitle">
        Helping with programming questions and interview preparation
      </div>
    </div>

    <div class="chat-container">
      <div class="messages-container" ref="messagesContainer">
        <div v-if="messages.length === 0" class="welcome-message">
          <div class="welcome-content">
            <div class="welcome-icon">🤖</div>
            <h2>Welcome to AI Coding Assistant</h2>
            <p>I can help you with:</p>
            <ul>
              <li>Answering technical questions</li>
              <li>Providing code examples</li>
              <li>Interview preparation</li>
              <li>Programming learning advice</li>
            </ul>
            <p>Feel free to ask me anything!</p>
          </div>
        </div>

        <ChatMessage
          v-for="message in messages"
          :key="message.id"
          :message="message.content"
          :is-user="message.isUser"
          :timestamp="message.timestamp"
        />

        <div v-if="isAiTyping" class="chat-message ai-message">
          <div class="message-avatar">
            <div class="avatar ai-avatar">AI</div>
          </div>
          <div class="message-content">
            <div class="message-bubble">
              <div class="ai-typing-content">
                <div
                  class="ai-response-text message-markdown"
                  v-html="currentAiResponseRendered"
                ></div>
                <LoadingDots v-if="isStreaming" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <ChatInput
        :disabled="isAiTyping"
        @send-message="sendMessage"
        placeholder="Type your programming question..."
      />
    </div>

    <div v-if="connectionError" class="connection-error">
      <div class="error-content">
        <span class="error-icon">⚠️</span>
        <span>Connection failed. Please check backend service.</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import ChatMessage from "./components/ChatMessage.vue";
import ChatInput from "./components/ChatInput.vue";
import LoadingDots from "./components/LoadingDots.vue";
import { chatWithSSE } from "./api/chatApi.ts";
import { generateMemoryId } from "./utils/index.ts";
import { marked } from "marked";

export default {
  name: "App",
  components: {
    ChatMessage,
    ChatInput,
    LoadingDots,
  },
  data() {
    return {
      messages: [],
      memoryId: null,
      isAiTyping: false,
      isStreaming: false,
      currentAiResponse: "",
      currentEventSource: null,
      connectionError: false,
    };
  },
  computed: {
    currentAiResponseRendered() {
      if (!this.currentAiResponse) return "";
      marked.setOptions({
        breaks: true,
        gfm: true,
        sanitize: false,
        highlight: function (code, lang) {
          return code;
        },
      });
      return marked(this.currentAiResponse);
    },
  },
  methods: {
    sendMessage(message) {
      this.addMessage(message, true);
      this.startAiResponse(message);
    },

    addMessage(content, isUser = false) {
      const message = {
        id: Date.now() + Math.random(),
        content,
        isUser,
        timestamp: new Date(),
      };
      this.messages.push(message);
      this.scrollToBottom();
    },

    startAiResponse(userMessage) {
      this.isAiTyping = true;
      this.isStreaming = true;
      this.currentAiResponse = "";
      this.connectionError = false;

      if (this.currentEventSource) {
        this.currentEventSource.close();
      }

      this.currentEventSource = chatWithSSE(
        this.memoryId,
        userMessage,
        this.handleAiMessage,
        this.handleAiError,
        this.handleAiClose,
      );
    },

    handleAiMessage(data) {
      this.currentAiResponse += data;
      this.scrollToBottom();
    },

    handleAiError(error) {
      console.error("AI response error:", error);
      this.connectionError = true;
      this.finishAiResponse();

      setTimeout(() => {
        this.connectionError = false;
      }, 5000);
    },

    handleAiClose() {
      this.finishAiResponse();
    },

    finishAiResponse() {
      this.isStreaming = false;

      if (this.currentAiResponse.trim()) {
        this.addMessage(this.currentAiResponse.trim(), false);
      }

      this.isAiTyping = false;
      this.currentAiResponse = "";

      this.connectionError = false;

      if (this.currentEventSource) {
        this.currentEventSource.close();
        this.currentEventSource = null;
      }
    },

    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messagesContainer;
        if (container) {
          container.scrollTop = container.scrollHeight;
        }
      });
    },

    initializeChat() {
      this.memoryId = generateMemoryId();
      console.log("chatroom ID:", this.memoryId);
    },
  },

  mounted() {
    this.initializeChat();
  },

  beforeUnmount() {
    if (this.currentEventSource) {
      this.currentEventSource.close();
    }
  },
};
</script>

<style scoped>
.app {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f0f0f0;
}

.app-header {
  background-color: #fff;
  padding: 20px;
  border-bottom: 1px solid #e1e5e9;
  text-align: center;
}

.app-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.app-subtitle {
  font-size: 14px;
  color: #666;
  margin-top: 5px;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px 0;
}

.welcome-message {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  padding: 0 20px;
}

.welcome-content {
  text-align: center;
  max-width: 400px;
  color: #666;
}

.welcome-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.welcome-content h2 {
  font-size: 20px;
  margin-bottom: 15px;
  color: #333;
}

.welcome-content p {
  margin-bottom: 10px;
  line-height: 1.5;
}

.welcome-content ul {
  text-align: left;
  margin: 15px 0;
}

.welcome-content li {
  margin-bottom: 5px;
}

.chat-message {
  display: flex;
  margin-bottom: 20px;
  padding: 0 20px;
}

.ai-message {
  justify-content: flex-start;
  flex-direction: row;
}

.message-avatar {
  display: flex;
  align-items: flex-start;
  margin: 0 10px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: bold;
  color: white;
}

.ai-avatar {
  background-color: #6c757d;
}

.message-content {
  max-width: 70%;
  min-width: 100px;
}

.message-bubble {
  padding: 12px 16px;
  border-radius: 18px;
  position: relative;
  word-wrap: break-word;
  word-break: break-word;
  background-color: #f1f3f4;
  color: #333;
  border-bottom-left-radius: 4px;
}

.ai-typing-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.ai-response-text {
  font-size: 14px;
  line-height: 1.5;
}

/* AI实时回复的Markdown样式 */
.ai-response-text.message-markdown h1,
.ai-response-text.message-markdown h2,
.ai-response-text.message-markdown h3,
.ai-response-text.message-markdown h4,
.ai-response-text.message-markdown h5,
.ai-response-text.message-markdown h6 {
  margin: 0.5em 0;
  font-weight: bold;
}

.ai-response-text.message-markdown h1 {
  font-size: 1.5em;
}
.ai-response-text.message-markdown h2 {
  font-size: 1.3em;
}
.ai-response-text.message-markdown h3 {
  font-size: 1.2em;
}
.ai-response-text.message-markdown h4 {
  font-size: 1.1em;
}
.ai-response-text.message-markdown h5 {
  font-size: 1em;
}
.ai-response-text.message-markdown h6 {
  font-size: 0.9em;
}

.ai-response-text.message-markdown p {
  margin: 0.5em 0;
}

.ai-response-text.message-markdown ul,
.ai-response-text.message-markdown ol {
  margin: 0.5em 0;
  padding-left: 1.5em;
}

.ai-response-text.message-markdown li {
  margin: 0.2em 0;
}

.ai-response-text.message-markdown code {
  background-color: rgba(0, 0, 0, 0.1);
  padding: 0.2em 0.4em;
  border-radius: 3px;
  font-family: "Consolas", "Monaco", "Courier New", monospace;
  font-size: 0.9em;
}

.ai-response-text.message-markdown pre {
  background-color: rgba(0, 0, 0, 0.1);
  padding: 1em;
  border-radius: 5px;
  overflow-x: auto;
  margin: 0.5em 0;
}

.ai-response-text.message-markdown pre code {
  background-color: transparent;
  padding: 0;
  font-family: "Consolas", "Monaco", "Courier New", monospace;
  font-size: 0.9em;
}

.ai-response-text.message-markdown blockquote {
  border-left: 4px solid #ccc;
  padding-left: 1em;
  margin: 0.5em 0;
  font-style: italic;
  color: #666;
}

.ai-response-text.message-markdown a {
  color: #007bff;
  text-decoration: underline;
}

.ai-response-text.message-markdown table {
  border-collapse: collapse;
  width: 100%;
  margin: 0.5em 0;
}

.ai-response-text.message-markdown th,
.ai-response-text.message-markdown td {
  border: 1px solid #ddd;
  padding: 0.5em;
  text-align: left;
}

.ai-response-text.message-markdown th {
  background-color: #f2f2f2;
  font-weight: bold;
}

.ai-response-text.message-markdown hr {
  border: none;
  border-top: 1px solid #ddd;
  margin: 1em 0;
}

.connection-error {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #ff4444;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  z-index: 1000;
  animation: slideDown 0.3s ease-out;
}

.error-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.error-icon {
  font-size: 16px;
}

@keyframes slideDown {
  from {
    transform: translateX(-50%) translateY(-100%);
    opacity: 0;
  }
  to {
    transform: translateX(-50%) translateY(0);
    opacity: 1;
  }
}

/* 滚动条样式 */
.messages-container::-webkit-scrollbar {
  width: 6px;
}

.messages-container::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.messages-container::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.messages-container::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

@media (max-width: 768px) {
  .app-header {
    padding: 15px;
  }

  .app-title {
    font-size: 20px;
  }

  .messages-container {
    padding: 15px 0;
  }

  .welcome-content {
    padding: 0 10px;
  }

  .message-content {
    max-width: 85%;
  }

  .chat-message {
    padding: 0 10px;
  }
}
</style>
