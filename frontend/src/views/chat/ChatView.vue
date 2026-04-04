<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { t } from "../../locales";
import {
  sendChatMessage,
  sendChatMessageStream,
  listPresets,
} from "../../api/chat";

// ChatView 使用自己独立的侧边栏状态，不使用全局的
const localSidebarCollapsed = ref(false);

const messageInput = ref("");
const messages = ref([]);
const isLoading = ref(false);
const currentSessionId = ref("");
const currentPreset = ref(null);
const presets = ref([]);
const showConfigMenu = ref(false);
const streamEnabled = ref(true);

// 切换侧边栏
const toggleSidebar = () => {
  localSidebarCollapsed.value = !localSidebarCollapsed.value;
};

// 翻译函数
const $t = computed(() => t);

// 加载预设列表
const loadPresets = async () => {
  try {
    const response = await listPresets();
    if (response.code === 200) {
      presets.value = response.data;
      // 设置默认预设
      const defaultPreset =
        response.data.find((p) => p.is_default) || response.data[0];
      if (defaultPreset) {
        currentPreset.value = defaultPreset;
      }
    }
  } catch (error) {
    console.error("加载预设失败:", error);
  }
};

// 选择预设
const selectPreset = (preset) => {
  currentPreset.value = preset;
  showConfigMenu.value = false;
  // 切换预设时创建新会话
  currentSessionId.value = "";
  messages.value = [];
};

// 切换配置菜单
const toggleConfigMenu = () => {
  showConfigMenu.value = !showConfigMenu.value;
};

// 切换流式响应
const toggleStream = () => {
  streamEnabled.value = !streamEnabled.value;
  showConfigMenu.value = false;
};

// 发送消息
const sendMessage = async () => {
  if (!messageInput.value.trim() || isLoading.value) return;
  if (!currentPreset.value) {
    alert("请先选择预设方案");
    return;
  }

  const userMessage = messageInput.value.trim();
  messageInput.value = "";

  // 添加用户消息到列表
  messages.value.push({
    role: "user",
    content: userMessage,
    timestamp: new Date(),
  });

  isLoading.value = true;

  // 添加AI占位消息
  const aiMessageIndex = messages.value.length;
  messages.value.push({
    role: "assistant",
    content: "",
    timestamp: new Date(),
  });

  try {
    if (streamEnabled.value) {
      // 流式响应
      await sendChatMessageStream(
        {
          preset_id: currentPreset.value.preset_id,
          message: userMessage,
          session_id: currentSessionId.value || undefined,
          stream: true,
          enable_memory: true,
          enable_tools: true,
          enable_rag: true,
          channel_type: "web",
        },
        // onChunk - 收到流式数据
        (chunk) => {
          messages.value[aiMessageIndex].content += chunk;
        },
        // onComplete - 完成
        (fullResponse, sessionId) => {
          currentSessionId.value = sessionId;
          isLoading.value = false;
        },
        // onError - 错误
        (error) => {
          console.error("流式响应错误:", error);
          messages.value[aiMessageIndex].content =
            "[错误] " + (error.message || "请求失败");
          isLoading.value = false;
        },
      );
    } else {
      // 非流式响应
      const response = await sendChatMessage({
        preset_id: currentPreset.value.preset_id,
        message: userMessage,
        session_id: currentSessionId.value || undefined,
        stream: false,
        enable_memory: true,
        enable_tools: true,
        enable_rag: true,
        channel_type: "web",
      });

      if (response.code === 200) {
        messages.value[aiMessageIndex].content = response.data.content;
        currentSessionId.value = response.data.session_id;
      } else {
        messages.value[aiMessageIndex].content =
          "[错误] " + (response.message || "请求失败");
      }
      isLoading.value = false;
    }
  } catch (error) {
    console.error("发送消息失败:", error);
    messages.value[aiMessageIndex].content =
      "[错误] " + (error.message || "网络错误");
    isLoading.value = false;
  }
};

// 处理键盘事件
const handleKeyPress = (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    sendMessage();
  }
};

// 点击外部关闭菜单
const handleClickOutside = (event) => {
  const menu = document.querySelector(".config-menu");
  const button = document.querySelector(".action-btn");
  if (
    menu &&
    button &&
    !menu.contains(event.target) &&
    !button.contains(event.target)
  ) {
    showConfigMenu.value = false;
  }
};

// 初始化
onMounted(() => {
  loadPresets();
  document.addEventListener("click", handleClickOutside);
});
</script>

<template>
  <div class="chat-container">
    <!-- 侧边栏 -->
    <aside class="sidebar" :class="{ collapsed: localSidebarCollapsed }">
      <div class="sidebar-header">
        <button
          class="collapse-btn"
          @click="toggleSidebar"
          title="收起/展开侧边栏"
        >
          <svg
            class="icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M3 12h18M3 6h18M3 18h18" v-if="localSidebarCollapsed" />
            <path d="M3 6h18M3 12h18M3 18h18" v-else />
          </svg>
        </button>
      </div>

      <div class="sidebar-content">
        <div
          class="new-chat-btn"
          @click="
            messages = [];
            currentSessionId = '';
          "
        >
          <svg
            class="icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M12 5v14M5 12h14" />
          </svg>
          <span>{{ $t("chat.newChat") }}</span>
        </div>

        <div class="chat-history">
          <div class="chat-history-title">{{ $t("chat.history") }}</div>
          <div class="chat-list">
            <div class="chat-item">
              <svg
                class="chat-icon"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"
                />
              </svg>
              <span class="chat-title">Previous Chat 1</span>
            </div>
          </div>
        </div>
      </div>
    </aside>

    <!-- 主聊天区域 -->
    <main class="chat-main">
      <div class="chat-content">
        <!-- 空状态 -->
        <div v-if="messages.length === 0" class="empty-state">
          <div class="welcome-text">
            <h1>
              {{ $t("chat.welcome") }} HAXAtom
              <svg class="welcome-icon" viewBox="0 0 24 24" fill="currentColor">
                <path
                  d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"
                />
              </svg>
            </h1>
          </div>
          <div class="input-wrapper">
            <div class="chat-input-container">
              <div class="chat-input-wrapper">
                <textarea
                  v-model="messageInput"
                  :placeholder="
                    currentPreset ? $t('chat.placeholder') : '请先选择预设方案'
                  "
                  @keydown="handleKeyPress"
                  rows="1"
                  class="chat-input"
                  :disabled="!currentPreset || isLoading"
                ></textarea>
              </div>
              <div class="input-actions">
                <!-- 配置菜单按钮 -->
                <div class="config-menu-wrapper">
                  <button
                    class="action-btn"
                    @click.stop="toggleConfigMenu"
                    :class="{ active: showConfigMenu }"
                    title="更多选项"
                  >
                    <svg
                      class="icon"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <path d="M12 5v14M5 12h14" />
                    </svg>
                  </button>

                  <!-- 配置菜单 -->
                  <div v-if="showConfigMenu" class="config-menu">
                    <!-- 上传文件 -->
                    <div class="menu-item">
                      <svg
                        class="menu-icon"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                      >
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                        <polyline points="17 8 12 3 7 8" />
                        <line x1="12" y1="3" x2="12" y2="15" />
                      </svg>
                      <span class="menu-text">上传文件</span>
                    </div>

                    <!-- 配置文件 -->
                    <div class="menu-item has-submenu">
                      <svg
                        class="menu-icon"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                      >
                        <circle cx="12" cy="12" r="3" />
                        <path
                          d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"
                        />
                      </svg>
                      <div class="menu-text-wrapper">
                        <span class="menu-text">配置文件</span>
                        <span v-if="currentPreset" class="menu-subtext">
                          {{ currentPreset.preset_name }}
                        </span>
                        <span v-else class="menu-subtext">未选择</span>
                      </div>
                      <svg
                        class="menu-arrow"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                      >
                        <polyline points="9 18 15 12 9 6" />
                      </svg>

                      <!-- 预设子菜单 -->
                      <div class="submenu">
                        <div
                          v-for="preset in presets"
                          :key="preset.preset_id"
                          class="submenu-item"
                          :class="{
                            active:
                              currentPreset?.preset_id === preset.preset_id,
                          }"
                          @click.stop="selectPreset(preset)"
                        >
                          <span class="submenu-name">{{
                            preset.preset_name
                          }}</span>
                          <span class="submenu-desc">{{
                            preset.description
                          }}</span>
                        </div>
                      </div>
                    </div>

                    <!-- 流式响应开关 -->
                    <div class="menu-item" @click.stop="toggleStream">
                      <svg
                        class="menu-icon"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                      >
                        <polygon
                          points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"
                        />
                      </svg>
                      <span class="menu-text">
                        {{
                          streamEnabled ? "流式响应已开启" : "流式响应已关闭"
                        }}
                      </span>
                    </div>
                  </div>
                </div>

                <button
                  class="send-btn"
                  @click="sendMessage"
                  :disabled="
                    !messageInput.trim() || isLoading || !currentPreset
                  "
                >
                  <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 消息列表 -->
        <div v-else class="message-list">
          <div
            v-for="(message, index) in messages"
            :key="index"
            class="message"
            :class="message.role"
          >
            <div class="message-avatar">
              <svg
                v-if="message.role === 'user'"
                class="avatar-icon"
                viewBox="0 0 24 24"
                fill="currentColor"
              >
                <path
                  d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"
                />
              </svg>
              <svg
                v-else
                class="avatar-icon bot"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="#409EFF" />
              </svg>
            </div>
            <div class="message-content">
              <div class="message-text">{{ message.content }}</div>
              <div class="message-time">
                {{ new Date(message.timestamp).toLocaleTimeString() }}
              </div>
            </div>
          </div>

          <!-- 输入框（有消息时显示在底部） -->
          <div class="input-wrapper-bottom">
            <div class="chat-input-container">
              <div class="chat-input-wrapper">
                <textarea
                  v-model="messageInput"
                  :placeholder="
                    currentPreset ? $t('chat.placeholder') : '请先选择预设方案'
                  "
                  @keydown="handleKeyPress"
                  rows="1"
                  class="chat-input"
                  :disabled="!currentPreset || isLoading"
                ></textarea>
              </div>
              <div class="input-actions">
                <!-- 配置菜单按钮 -->
                <div class="config-menu-wrapper">
                  <button
                    class="action-btn"
                    @click.stop="toggleConfigMenu"
                    :class="{ active: showConfigMenu }"
                    title="更多选项"
                  >
                    <svg
                      class="icon"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <path d="M12 5v14M5 12h14" />
                    </svg>
                  </button>

                  <!-- 配置菜单 -->
                  <div v-if="showConfigMenu" class="config-menu">
                    <div class="menu-item">
                      <svg
                        class="menu-icon"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                      >
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                        <polyline points="17 8 12 3 7 8" />
                        <line x1="12" y1="3" x2="12" y2="15" />
                      </svg>
                      <span class="menu-text">上传文件</span>
                    </div>

                    <div class="menu-item has-submenu">
                      <svg
                        class="menu-icon"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                      >
                        <circle cx="12" cy="12" r="3" />
                        <path
                          d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"
                        />
                      </svg>
                      <div class="menu-text-wrapper">
                        <span class="menu-text">配置文件</span>
                        <span v-if="currentPreset" class="menu-subtext">
                          {{ currentPreset.preset_name }}
                        </span>
                        <span v-else class="menu-subtext">未选择</span>
                      </div>
                      <svg
                        class="menu-arrow"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                      >
                        <polyline points="9 18 15 12 9 6" />
                      </svg>

                      <div class="submenu">
                        <div
                          v-for="preset in presets"
                          :key="preset.preset_id"
                          class="submenu-item"
                          :class="{
                            active:
                              currentPreset?.preset_id === preset.preset_id,
                          }"
                          @click.stop="selectPreset(preset)"
                        >
                          <span class="submenu-name">{{
                            preset.preset_name
                          }}</span>
                          <span class="submenu-desc">{{
                            preset.description
                          }}</span>
                        </div>
                      </div>
                    </div>

                    <div class="menu-item" @click.stop="toggleStream">
                      <svg
                        class="menu-icon"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                      >
                        <polygon
                          points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"
                        />
                      </svg>
                      <span class="menu-text">
                        {{
                          streamEnabled ? "流式响应已开启" : "流式响应已关闭"
                        }}
                      </span>
                    </div>
                  </div>
                </div>

                <button
                  class="send-btn"
                  @click="sendMessage"
                  :disabled="
                    !messageInput.trim() || isLoading || !currentPreset
                  "
                >
                  <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.chat-container {
  display: flex;
  height: calc(100vh - 56px);
  background: rgba(255, 255, 255, var(--bg-opacity));
  overflow: hidden;
  position: relative;
}

html.dark .chat-container {
  background: rgba(26, 26, 26, var(--bg-opacity));
}

/* 侧边栏 */
.sidebar {
  width: 260px;
  background: rgba(249, 250, 252, var(--bg-opacity));
  display: flex;
  flex-direction: column;
  overflow: hidden;
  flex-shrink: 0;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

html.dark .sidebar {
  background: rgba(26, 26, 26, var(--bg-opacity));
}

.sidebar.collapsed {
  width: 60px;
  background: rgba(255, 255, 255, var(--bg-opacity));
}

html.dark .sidebar.collapsed {
  background: rgba(26, 26, 26, var(--bg-opacity));
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 12px;
  flex-shrink: 0;
  min-height: 56px;
}

.collapse-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  color: var(--text-secondary);
  flex-shrink: 0;
}

.collapse-btn:hover {
  background: var(--bg-hover);
  color: var(--primary-color);
}

.collapse-btn .icon {
  width: 18px;
  height: 18px;
}

.sidebar-content {
  flex: 1;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow: hidden;
  opacity: 1;
  visibility: visible;
  transition:
    opacity 0.2s ease,
    visibility 0.2s ease;
  transition-delay: 0.15s;
}

.sidebar.collapsed .sidebar-content {
  opacity: 0;
  visibility: hidden;
  transition-delay: 0s;
}

.new-chat-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px 8px 0;
  background: transparent;
  color: var(--text-secondary);
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s;
  font-size: 14px;
}

.new-chat-btn:hover {
  background: var(--bg-hover);
  color: var(--primary-color);
}

.new-chat-btn .icon {
  width: 18px;
  height: 18px;
}

.chat-history {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.chat-history-title {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: 8px;
  padding: 0 8px;
}

.chat-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.chat-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s;
  color: var(--text-secondary);
}

.chat-item:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.chat-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.chat-title {
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 主聊天区域 */
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

.chat-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 消息列表 */
.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message {
  display: flex;
  gap: 12px;
  padding: 16px;
  border-radius: 12px;
  background: var(--bg-secondary);
  max-width: 80%;
}

.message.user {
  align-self: flex-end;
  background: var(--primary-color);
  color: white;
}

.message.assistant {
  align-self: flex-start;
}

.message-content {
  flex: 1;
}

.message-text {
  font-size: 15px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
}

.message-time {
  font-size: 12px;
  opacity: 0.7;
  margin-top: 8px;
}

.message.user .message-time {
  color: rgba(255, 255, 255, 0.8);
}

.message-avatar {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-hover);
}

.message.user .message-avatar {
  background: rgba(255, 255, 255, 0.2);
}

.avatar-icon {
  width: 20px;
  height: 20px;
}

.avatar-icon.bot {
  width: 24px;
  height: 24px;
}

/* 空状态 */
.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.welcome-text {
  text-align: center;
  margin-bottom: 40px;
}

.welcome-text h1 {
  font-size: 32px;
  font-weight: 500;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 12px;
}

.welcome-icon {
  width: 32px;
  height: 32px;
  color: #409eff;
}

/* 输入框 */
.input-wrapper,
.input-wrapper-bottom {
  width: 100%;
  max-width: 768px;
  margin: 0 auto;
  padding: 0 20px;
}

.input-wrapper-bottom {
  padding: 20px;
  border-top: 1px solid var(--border-color);
  background: rgba(255, 255, 255, var(--bg-opacity));
}

html.dark .input-wrapper-bottom {
  background: rgba(26, 26, 26, var(--bg-opacity));
}

.chat-input-container {
  display: flex;
  flex-direction: column;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 12px;
  transition: border-color 0.2s;
}

.chat-input-container:focus-within {
  border-color: var(--primary-color);
}

.chat-input-wrapper {
  flex: 1;
  margin-bottom: 8px;
}

.chat-input {
  width: 100%;
  min-height: 24px;
  max-height: 200px;
  border: none;
  outline: none;
  background: transparent;
  color: var(--text-primary);
  font-size: 15px;
  line-height: 1.5;
  resize: none;
  font-family: inherit;
}

.chat-input::placeholder {
  color: var(--text-secondary);
}

.chat-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.input-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.action-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  color: var(--text-secondary);
}

.action-btn:hover,
.action-btn.active {
  background: var(--bg-hover);
  color: var(--primary-color);
}

.action-btn .icon {
  width: 20px;
  height: 20px;
}

.send-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: var(--primary-color);
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  color: white;
}

.send-btn:hover:not(:disabled) {
  background: var(--primary-hover);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.send-btn .icon {
  width: 18px;
  height: 18px;
}

/* 配置菜单 */
.config-menu-wrapper {
  position: relative;
}

.config-menu {
  position: absolute;
  bottom: calc(100% + 8px);
  left: 0;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 8px;
  min-width: 220px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  z-index: 100;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
  color: var(--text-primary);
  position: relative;
}

.menu-item:hover {
  background: var(--bg-hover);
}

.menu-item.has-submenu:hover .submenu {
  display: block;
}

.menu-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  color: var(--text-secondary);
}

.menu-text-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.menu-text {
  font-size: 14px;
  font-weight: 500;
}

.menu-subtext {
  font-size: 12px;
  color: var(--text-secondary);
}

.menu-arrow {
  width: 16px;
  height: 16px;
  color: var(--text-secondary);
}

/* 子菜单 */
.submenu {
  display: none;
  position: absolute;
  left: calc(100% + 4px);
  top: 0;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 8px;
  min-width: 200px;
  max-height: 300px;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  z-index: 101;
}

.submenu-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.submenu-item:hover,
.submenu-item.active {
  background: var(--bg-hover);
}

.submenu-item.active .submenu-name {
  color: var(--primary-color);
}

.submenu-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.submenu-desc {
  font-size: 12px;
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 消息列表 */
.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.message {
  display: flex;
  gap: 12px;
  max-width: 80%;
}

.message.user {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.message.assistant {
  align-self: flex-start;
}

.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: var(--bg-secondary);
}

.message.user .message-avatar {
  background: var(--primary-color);
  color: white;
}

.avatar-icon {
  width: 20px;
  height: 20px;
}

.message-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.message-text {
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 15px;
  line-height: 1.6;
  word-wrap: break-word;
  white-space: pre-wrap;
}

.message.user .message-text {
  background: var(--primary-color);
  color: white;
  border-bottom-right-radius: 4px;
}

.message.assistant .message-text {
  background: var(--bg-secondary);
  color: var(--text-primary);
  border-bottom-left-radius: 4px;
}

.message-time {
  font-size: 12px;
  color: var(--text-secondary);
  padding: 0 4px;
}

.message.user .message-time {
  text-align: right;
}
</style>
