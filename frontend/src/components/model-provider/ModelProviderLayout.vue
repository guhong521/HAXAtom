<script setup lang="ts">
import { ref, computed } from "vue";
import { t } from "../../locales";

const $t = computed(() => t);

// 当前激活的标签页
const activeTab = ref("chat");

// 标签页配置
const tabs = [
  {
    key: "chat",
    label: computed(() => $t.value("provider.tabs.chat") || "对话"),
    icon: "chat",
  },
  {
    key: "agent",
    label: computed(() => $t.value("provider.tabs.agent") || "Agent 执行器"),
    icon: "agent",
  },
  {
    key: "stt",
    label: computed(() => $t.value("provider.tabs.stt") || "语音转文字"),
    icon: "stt",
  },
  {
    key: "tts",
    label: computed(() => $t.value("provider.tabs.tts") || "文字转语音"),
    icon: "tts",
  },
  {
    key: "embedding",
    label: computed(
      () => $t.value("provider.tabs.embedding") || "嵌入(Embedding)",
    ),
    icon: "embedding",
  },
  {
    key: "rerank",
    label: computed(() => $t.value("provider.tabs.rerank") || "重排序(Rerank)"),
    icon: "rerank",
  },
];

// 切换标签页
const switchTab = (key: string) => {
  activeTab.value = key;
};
</script>

<template>
  <div class="provider-layout">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="title-section">
        <svg class="title-icon" viewBox="0 0 24 24" fill="currentColor">
          <path
            d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"
          />
        </svg>
        <h1 class="page-title">{{ $t("provider.title") || "模型提供商" }}</h1>
      </div>
      <p class="page-desc">
        {{
          $t("provider.description") ||
          '可以在"对话"中配置对话模型。此外，"Agent 执行器"包含了 Dify、Coze、阿里云百炼应用等第三方服务的集成。'
        }}
      </p>
    </div>

    <!-- 标签页 -->
    <div class="tabs-container">
      <div
        v-for="tab in tabs"
        :key="tab.key"
        class="tab-item"
        :class="{ active: activeTab === tab.key }"
        @click="switchTab(tab.key)"
      >
        <svg class="tab-icon" viewBox="0 0 24 24" fill="currentColor">
          <!-- 对话图标 -->
          <g v-if="tab.icon === 'chat'">
            <path
              d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"
            />
          </g>
          <!-- Agent图标 -->
          <g v-else-if="tab.icon === 'agent'">
            <path
              d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-5.5-2.5l7.51-3.22-7.52-3.22 7.52 3.22z"
            />
            <circle cx="12" cy="12" r="3" />
          </g>
          <!-- 语音转文字图标 -->
          <g v-else-if="tab.icon === 'stt'">
            <path
              d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"
            />
            <path
              d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"
            />
          </g>
          <!-- 文字转语音图标 -->
          <g v-else-if="tab.icon === 'tts'">
            <path
              d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"
            />
          </g>
          <!-- Embedding图标 -->
          <g v-else-if="tab.icon === 'embedding'">
            <path
              d="M9 3L5 6.99h3V14h2V6.99h3L9 3zm7 14.01V10h-2v7.01h-3L15 21l4-3.99h-3z"
            />
          </g>
          <!-- Rerank图标 -->
          <g v-else-if="tab.icon === 'rerank'">
            <path
              d="M3 13h2v-2H3v2zm0 4h2v-2H3v2zm0-8h2V7H3v2zm4 4h14v-2H7v2zm0 4h14v-2H7v2zM7 7v2h14V7H7z"
            />
          </g>
        </svg>
        <span class="tab-label">{{ tab.label }}</span>
      </div>
    </div>

    <!-- 内容区域 - 使用插槽 -->
    <div class="content-area">
      <slot :activeTab="activeTab" />
    </div>
  </div>
</template>

<style scoped>
.provider-layout {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 24px;
  overflow-y: auto;
}

/* 页面标题 */
.page-header {
  margin-bottom: 24px;
}

.title-section {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.title-icon {
  width: 28px;
  height: 28px;
  color: var(--primary-color);
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.page-desc {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.5;
}

/* 标签页 */
.tabs-container {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 12px;
}

.tab-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: var(--text-secondary);
  font-size: 14px;
}

.tab-item:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.tab-item.active {
  background: var(--primary-light);
  color: var(--primary-color);
}

.tab-icon {
  width: 18px;
  height: 18px;
}

/* 内容区域 */
.content-area {
  flex: 1;
  min-height: 0;
}
</style>
