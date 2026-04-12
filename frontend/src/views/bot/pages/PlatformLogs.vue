<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from "vue";
import { getLogs, getLogStats, downloadLogs } from "../../../api/logs";
import { t } from "../../../locales";

const $t = computed(() => t);

// 日志数据
const logs = ref<string[]>([]);
const stats = ref<any>(null);
const loading = ref(false);
const autoScroll = ref(true);
const autoRefresh = ref(5000);

// 过滤条件
const filters = ref({
  info: true,
  warning: true,
  error: true,
  debug: false,
});
const search = ref("");
let refreshTimer: any = null;

// 日志容器引用
const logContainer = ref<HTMLElement | null>(null);

// 过滤后的日志
const filteredLogs = computed(() => {
  let result = [...logs.value];

  // 按级别过滤
  const levels = [];
  if (filters.value.info) levels.push("INFO");
  if (filters.value.warning) levels.push("WARNING");
  if (filters.value.error) levels.push("ERROR");
  if (filters.value.debug) levels.push("DEBUG");

  if (levels.length > 0) {
    result = result.filter((log) =>
      levels.some((level) => log.includes(level)),
    );
  }

  // 关键词搜索
  if (search.value.trim()) {
    const keyword = search.value.toLowerCase();
    result = result.filter((log) => log.toLowerCase().includes(keyword));
  }

  return result;
});

// 日志级别颜色
const getLevelClass = (log: string) => {
  if (log.includes("ERROR")) return "level-error";
  if (log.includes("WARNING")) return "level-warning";
  if (log.includes("INFO")) return "level-info";
  if (log.includes("DEBUG")) return "level-debug";
  return "";
};

// 刷新日志
const refreshLogs = async () => {
  loading.value = true;
  try {
    const [logsData, statsData] = await Promise.all([
      getLogs(500),
      getLogStats(),
    ]);
    logs.value = logsData;
    stats.value = statsData;

    // 等待 DOM 更新后滚动到底部
    nextTick(() => {
      if (autoScroll.value && logContainer.value) {
        logContainer.value.scrollTop = logContainer.value.scrollHeight;
      }
    });
  } catch (error: any) {
    console.error("获取日志失败:", error);
  } finally {
    loading.value = false;
  }
};

// 清空日志显示
const clearLogs = () => {
  logs.value = [];
};

// 下载日志
const downloadLog = () => {
  downloadLogs();
};

// 切换自动滚动
const toggleAutoScroll = () => {
  autoScroll.value = !autoScroll.value;
};

// 设置自动刷新
const setupAutoRefresh = () => {
  if (refreshTimer) {
    clearInterval(refreshTimer);
  }

  if (autoRefresh.value > 0) {
    refreshTimer = setInterval(refreshLogs, autoRefresh.value);
  }
};

// 监听自动刷新设置
watch(autoRefresh, setupAutoRefresh);

// 生命周期
onMounted(() => {
  refreshLogs();
  setupAutoRefresh();
});

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer);
  }
});
</script>

<template>
  <div class="log-console-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2z"
          />
        </svg>
        系统日志控制台
      </h1>
      <p class="page-description">实时查看系统运行日志，支持过滤、搜索和导出</p>
    </div>

    <!-- 统计卡片 -->
    <div v-if="stats" class="stats-section">
      <div class="stat-card">
        <div class="stat-value">{{ stats.total }}</div>
        <div class="stat-label">总日志数</div>
      </div>
      <div class="stat-card level-info">
        <div class="stat-value">{{ stats.info }}</div>
        <div class="stat-label">INFO</div>
      </div>
      <div class="stat-card level-warning">
        <div class="stat-value">{{ stats.warning }}</div>
        <div class="stat-label">WARNING</div>
      </div>
      <div class="stat-card level-error">
        <div class="stat-value">{{ stats.error }}</div>
        <div class="stat-label">ERROR</div>
      </div>
      <div class="stat-card level-debug">
        <div class="stat-value">{{ stats.debug }}</div>
        <div class="stat-label">DEBUG</div>
      </div>
    </div>

    <!-- 工具栏 -->
    <div class="toolbar">
      <div class="toolbar-left">
        <button
          class="btn btn-primary"
          @click="refreshLogs"
          :disabled="loading"
        >
          <svg
            class="icon"
            :class="{ spinning: loading }"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
            />
          </svg>
          刷新
        </button>
        <button class="btn btn-secondary" @click="toggleAutoScroll">
          <svg
            class="icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
          >
            <path
              v-if="autoScroll"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 13l-7 7-7-7m14-8l-7 7-7-7"
            />
            <path
              v-else
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"
            />
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          {{ autoScroll ? "暂停滚动" : "自动滚动" }}
        </button>
        <button class="btn btn-secondary" @click="clearLogs">
          <svg
            class="icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
            />
          </svg>
          清空
        </button>
        <button class="btn btn-success" @click="downloadLog">
          <svg
            class="icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
            />
          </svg>
          下载日志
        </button>
      </div>

      <div class="toolbar-right">
        <select v-model="autoRefresh" class="select">
          <option :value="0">暂停刷新</option>
          <option :value="3000">3 秒刷新</option>
          <option :value="5000">5 秒刷新</option>
          <option :value="10000">10 秒刷新</option>
        </select>
      </div>
    </div>

    <!-- 过滤栏 -->
    <div class="filter-bar">
      <div class="filter-group">
        <span class="filter-label">级别过滤：</span>
        <label class="filter-checkbox">
          <input type="checkbox" v-model="filters.info" />
          <span class="level-badge level-info">INFO</span>
        </label>
        <label class="filter-checkbox">
          <input type="checkbox" v-model="filters.warning" />
          <span class="level-badge level-warning">WARNING</span>
        </label>
        <label class="filter-checkbox">
          <input type="checkbox" v-model="filters.error" />
          <span class="level-badge level-error">ERROR</span>
        </label>
        <label class="filter-checkbox">
          <input type="checkbox" v-model="filters.debug" />
          <span class="level-badge level-debug">DEBUG</span>
        </label>
      </div>

      <div class="filter-search">
        <svg
          class="icon search-icon"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>
        <input
          v-model="search"
          type="text"
          placeholder="搜索日志..."
          class="search-input"
        />
      </div>
    </div>

    <!-- 日志内容区域 -->
    <div class="log-container" ref="logContainer">
      <div v-if="loading" class="loading-state">
        <svg
          class="icon spinning"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
          />
        </svg>
        <span>加载中...</span>
      </div>

      <div v-else-if="filteredLogs.length === 0" class="empty-state">
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
          />
        </svg>
        <span>暂无日志</span>
      </div>

      <div
        v-for="(log, index) in filteredLogs"
        :key="index"
        :class="['log-entry', getLevelClass(log)]"
      >
        <pre>{{ log }}</pre>
      </div>
    </div>
  </div>
</template>

<style scoped>
.log-console-page {
  padding: 2rem;
  max-width: 1600px;
  margin: 0 auto;
  background: transparent;
  min-height: calc(100vh - 80px);
}

/* Page Header */
.page-header {
  margin-bottom: 2rem;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1f2937;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

html.dark .page-title {
  color: #f3f4f6;
}

.page-title .icon {
  width: 32px;
  height: 32px;
  color: #6366f1;
}

.page-description {
  font-size: 0.875rem;
  color: #6b7280;
}

html.dark .page-description {
  color: #9ca3af;
}

/* Stats Section */
.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  padding: 1.25rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  text-align: center;
  transition: all 0.2s ease;
}

html.dark .stat-card {
  background: #1e293b;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

html.dark .stat-value {
  color: #f3f4f6;
}

.stat-label {
  font-size: 0.875rem;
  color: #6b7280;
  text-transform: uppercase;
  font-weight: 600;
}

html.dark .stat-label {
  color: #9ca3af;
}

.stat-card.level-info .stat-value {
  color: #3b82f6;
}

.stat-card.level-warning .stat-value {
  color: #f59e0b;
}

.stat-card.level-error .stat-value {
  color: #ef4444;
}

.stat-card.level-debug .stat-value {
  color: #8b5cf6;
}

/* Toolbar */
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  gap: 1rem;
  flex-wrap: wrap;
}

.toolbar-left,
.toolbar-right {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  flex-wrap: wrap;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.btn .icon {
  width: 18px;
  height: 18px;
}

.btn-primary {
  background: #6366f1;
  color: white;
}

.btn-primary:hover {
  background: #4f46e5;
}

.btn-secondary {
  background: #f1f5f9;
  color: #475569;
}

html.dark .btn-secondary {
  background: #334155;
  color: #e2e8f0;
}

.btn-secondary:hover {
  background: #e2e8f0;
}

html.dark .btn-secondary:hover {
  background: #475569;
}

.btn-success {
  background: #22c55e;
  color: white;
}

.btn-success:hover {
  background: #16a34a;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.select {
  padding: 0.625rem 1rem;
  border-radius: 8px;
  font-size: 0.875rem;
  border: 1px solid #e2e8f0;
  background: white;
  color: #475569;
  cursor: pointer;
}

html.dark .select {
  background: #1e293b;
  border-color: #334155;
  color: #e2e8f0;
}

/* Filter Bar */
.filter-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  gap: 1rem;
  flex-wrap: wrap;
  padding: 1rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

html.dark .filter-bar {
  background: #1e293b;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.filter-label {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
}

html.dark .filter-label {
  color: #9ca3af;
}

.filter-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.filter-checkbox input[type="checkbox"] {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

.level-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 700;
  color: white;
}

.level-badge.level-info {
  background: #3b82f6;
}

.level-badge.level-warning {
  background: #f59e0b;
}

.level-badge.level-error {
  background: #ef4444;
}

.level-badge.level-debug {
  background: #8b5cf6;
}

.filter-search {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  width: 18px;
  height: 18px;
  color: #9ca3af;
}

.search-input {
  padding: 0.625rem 1rem 0.625rem 2.5rem;
  border-radius: 8px;
  font-size: 0.875rem;
  border: 1px solid #e2e8f0;
  background: white;
  color: #475569;
  width: 250px;
}

html.dark .search-input {
  background: #334155;
  border-color: #475569;
  color: #e2e8f0;
}

.search-input:focus {
  outline: none;
  border-color: #6366f1;
}

/* Log Container */
.log-container {
  background: #1e1e1e;
  border-radius: 12px;
  padding: 1rem;
  height: calc(100vh - 500px);
  min-height: 400px;
  overflow-y: auto;
  font-family: "JetBrains Mono", "Fira Code", Consolas, monospace;
  font-size: 0.8125rem;
  line-height: 1.6;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.log-entry {
  padding: 0.5rem;
  margin: 0.25rem 0;
  border-radius: 4px;
  transition: background-color 0.15s ease;
}

.log-entry:hover {
  background: rgba(255, 255, 255, 0.05);
}

.log-entry pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  color: #e2e8f0;
}

.log-entry.level-info {
  border-left: 3px solid #3b82f6;
  padding-left: 0.75rem;
}

.log-entry.level-warning {
  border-left: 3px solid #f59e0b;
  padding-left: 0.75rem;
}

.log-entry.level-error {
  border-left: 3px solid #ef4444;
  padding-left: 0.75rem;
  background: rgba(239, 68, 68, 0.1);
}

.log-entry.level-debug {
  border-left: 3px solid #8b5cf6;
  padding-left: 0.75rem;
}

/* Loading & Empty States */
.loading-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #6b7280;
  gap: 1rem;
}

.loading-state .icon,
.empty-state .icon {
  width: 48px;
  height: 48px;
}

.loading-state {
  color: #6366f1;
}

/* Animations */
.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Scrollbar */
.log-container::-webkit-scrollbar {
  width: 10px;
}

.log-container::-webkit-scrollbar-track {
  background: #2d2d2d;
  border-radius: 5px;
}

.log-container::-webkit-scrollbar-thumb {
  background: #4a4a4a;
  border-radius: 5px;
}

.log-container::-webkit-scrollbar-thumb:hover {
  background: #5a5a5a;
}

/* Responsive */
@media (max-width: 768px) {
  .log-console-page {
    padding: 1rem;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .stats-section {
    grid-template-columns: repeat(2, 1fr);
  }

  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }

  .toolbar-left,
  .toolbar-right {
    justify-content: stretch;
  }

  .filter-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-group {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-input {
    width: 100%;
  }

  .log-container {
    height: calc(100vh - 600px);
    min-height: 300px;
  }
}
</style>
