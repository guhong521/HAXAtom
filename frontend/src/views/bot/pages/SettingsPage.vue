<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from "vue";
import * as echarts from "echarts";
import { t } from "../../../locales";

const $t = computed(() => t);

// 系统信息
const systemInfo = ref({
  platform: "Unknown",
  platform_version: "Unknown",
  python_version: "Unknown",
  cpu_model: "Unknown",
  cpu_count: 0,
  memory_total: 0,
  memory_available: 0,
  memory_used: 0,
  memory_percent: 0,
  disk_total: 0,
  disk_used: 0,
  disk_percent: 0,
  haxatom_version: "1.0.0",
  uptime: 0,
});

// CPU 使用率历史（用于图表）
const cpuHistory = ref<number[]>([]);
const memoryHistory = ref<number[]>([]);

// 加载状态
const loading = ref(false);
const autoRefresh = ref(5000);
let refreshTimer: any = null;
let uptimeTimer: any = null;

// ECharts 实例
let cpuChart: echarts.ECharts | null = null;
let memoryChart: echarts.ECharts | null = null;

// 运行时长格式化
const formatUptime = (seconds: number) => {
  const days = Math.floor(seconds / 86400);
  const hours = Math.floor((seconds % 86400) / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = Math.floor(seconds % 60);

  if (days > 0) {
    return `${days}天 ${hours}小时 ${minutes}分钟 ${secs}秒`;
  } else if (hours > 0) {
    return `${hours}小时 ${minutes}分钟 ${secs}秒`;
  } else if (minutes > 0) {
    return `${minutes}分钟 ${secs}秒`;
  } else {
    return `${secs}秒`;
  }
};

// 格式化字节
const formatBytes = (bytes: number) => {
  if (bytes === 0) return "0 B";
  const k = 1024;
  const sizes = ["B", "KB", "MB", "GB", "TB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
};

// 初始化 ECharts
const initCharts = () => {
  const cpuChartEl = document.getElementById("cpu-chart");
  const memoryChartEl = document.getElementById("memory-chart");

  if (cpuChartEl) {
    cpuChart = echarts.init(cpuChartEl);
    // 初始化配置
    cpuChart.setOption({
      grid: {
        top: 5,
        left: 0,
        right: 0,
        bottom: 0,
        containLabel: false,
      },
      xAxis: {
        type: "category",
        boundaryGap: false,
        show: false,
      },
      yAxis: {
        type: "value",
        min: 0,
        max: 100,
        show: false,
      },
      series: [
        {
          type: "line",
          smooth: 0.4,
          symbol: "none",
          lineStyle: {
            color: "#667eea",
            width: 2.5,
            cap: "round",
          },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              {
                offset: 0,
                color: "rgba(102, 126, 234, 0.6)",
              },
              {
                offset: 1,
                color: "rgba(102, 126, 234, 0.1)",
              },
            ]),
          },
        },
      ],
    });
  }

  if (memoryChartEl) {
    memoryChart = echarts.init(memoryChartEl);
    // 初始化配置
    memoryChart.setOption({
      grid: {
        top: 5,
        left: 0,
        right: 0,
        bottom: 0,
        containLabel: false,
      },
      xAxis: {
        type: "category",
        boundaryGap: false,
        show: false,
      },
      yAxis: {
        type: "value",
        min: 0,
        max: 100,
        show: false,
      },
      series: [
        {
          type: "line",
          smooth: 0.4,
          symbol: "none",
          lineStyle: {
            color: "#f5576c",
            width: 2.5,
            cap: "round",
          },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              {
                offset: 0,
                color: "rgba(245, 87, 108, 0.6)",
              },
              {
                offset: 1,
                color: "rgba(245, 87, 108, 0.1)",
              },
            ]),
          },
        },
      ],
    });
  }
};

// 更新图表
const updateCharts = () => {
  if (cpuChart && cpuHistory.value.length > 0) {
    cpuChart.setOption({
      xAxis: {
        data: cpuHistory.value,
      },
      series: [
        {
          data: cpuHistory.value,
        },
      ],
    });
  }

  if (memoryChart && memoryHistory.value.length > 0) {
    memoryChart.setOption({
      xAxis: {
        data: memoryHistory.value,
      },
      series: [
        {
          data: memoryHistory.value,
        },
      ],
    });
  }
};

// 获取系统信息
const fetchSystemInfo = async () => {
  loading.value = true;
  try {
    const response = await fetch("/api/v1/system/info");
    if (response.ok) {
      const data = await response.json();
      systemInfo.value = data;

      // 更新历史记录
      cpuHistory.value.push(data.cpu_percent || 0);
      memoryHistory.value.push(data.memory_percent || 0);

      // 保持最近 20 条记录
      if (cpuHistory.value.length > 20) {
        cpuHistory.value.shift();
        memoryHistory.value.shift();
      }

      // 更新图表
      updateCharts();
    }
  } catch (error) {
    console.error("获取系统信息失败:", error);
  } finally {
    loading.value = false;
  }
};

// 启动运行时长计时器（每秒更新）
const startUptimeTimer = () => {
  if (uptimeTimer) {
    clearInterval(uptimeTimer);
  }
  uptimeTimer = setInterval(() => {
    if (systemInfo.value.uptime) {
      systemInfo.value.uptime += 1;
    }
  }, 1000);
};

// 自动刷新
const setupAutoRefresh = () => {
  if (refreshTimer) {
    clearInterval(refreshTimer);
  }

  if (autoRefresh.value > 0) {
    refreshTimer = setInterval(fetchSystemInfo, autoRefresh.value);
  }
};

// 生命周期
onMounted(() => {
  initCharts();
  fetchSystemInfo();
  setupAutoRefresh();
  startUptimeTimer();

  // 窗口大小改变时重新渲染图表
  window.addEventListener("resize", () => {
    cpuChart?.resize();
    memoryChart?.resize();
  });
});

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer);
  }
  if (uptimeTimer) {
    clearInterval(uptimeTimer);
  }
  cpuChart?.dispose();
  memoryChart?.dispose();
});
</script>

<template>
  <div class="settings-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
          />
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
          />
        </svg>
        系统设置
      </h1>
      <p class="page-description">查看系统运行状态、资源使用情况和配置信息</p>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon cpu-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <rect x="4" y="4" width="16" height="16" rx="2" stroke-width="2" />
            <rect x="9" y="9" width="6" height="6" stroke-width="2" />
            <path
              d="M9 1v3M15 1v3M9 20v3M15 20v3M20 9h3M20 14h3M1 9h3M1 14h3"
              stroke-width="2"
            />
          </svg>
        </div>
        <div class="stat-content">
          <div class="stat-label">CPU 使用率</div>
          <div class="stat-value">
            {{ (systemInfo.cpu_percent || 0).toFixed(1) }}%
          </div>
          <div class="stat-detail">{{ systemInfo.cpu_model || "Unknown" }}</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon memory-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path
              d="M6 4h12a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V6a2 2 0 012-2z"
              stroke-width="2"
            />
            <path d="M10 4v16M14 4v16M4 10h16M4 14h16" stroke-width="2" />
          </svg>
        </div>
        <div class="stat-content">
          <div class="stat-label">内存使用率</div>
          <div class="stat-value">
            {{ (systemInfo.memory_percent || 0).toFixed(1) }}%
          </div>
          <div class="stat-detail">
            {{ formatBytes(systemInfo.memory_used || 0) }} /
            {{ formatBytes(systemInfo.memory_total || 0) }}
          </div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon disk-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="12" cy="12" r="10" stroke-width="2" />
            <path d="M12 6v6l4 2" stroke-width="2" />
          </svg>
        </div>
        <div class="stat-content">
          <div class="stat-label">运行时长</div>
          <div class="stat-value">
            {{ formatUptime(systemInfo.uptime || 0) }}
          </div>
          <div class="stat-detail">系统持续运行时间</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon storage-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M22 12H2l5-9h10l5 9z" stroke-width="2" />
            <path d="M22 12l-5 9H7l-5-9" stroke-width="2" />
            <path d="M12 2v20" stroke-width="2" />
          </svg>
        </div>
        <div class="stat-content">
          <div class="stat-label">磁盘使用</div>
          <div class="stat-value">
            {{ (systemInfo.disk_percent || 0).toFixed(1) }}%
          </div>
          <div class="stat-detail">
            {{ formatBytes(systemInfo.disk_used || 0) }} /
            {{ formatBytes(systemInfo.disk_total || 0) }}
          </div>
        </div>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="content-grid">
      <!-- 系统信息 -->
      <div class="info-card">
        <div class="card-header">
          <h2 class="card-title">
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
                d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2z"
              />
            </svg>
            系统信息
          </h2>
        </div>
        <div class="card-content">
          <div class="info-grid">
            <div class="info-item">
              <div class="info-label">操作系统</div>
              <div class="info-value">
                {{ systemInfo.platform }} {{ systemInfo.platform_version }}
              </div>
            </div>
            <div class="info-item">
              <div class="info-label">Python 版本</div>
              <div class="info-value">{{ systemInfo.python_version }}</div>
            </div>
            <div class="info-item">
              <div class="info-label">CPU 型号</div>
              <div class="info-value">{{ systemInfo.cpu_model }}</div>
            </div>
            <div class="info-item">
              <div class="info-label">CPU 核心数</div>
              <div class="info-value">{{ systemInfo.cpu_count }} 核心</div>
            </div>
            <div class="info-item">
              <div class="info-label">总内存</div>
              <div class="info-value">
                {{ formatBytes(systemInfo.memory_total || 0) }}
              </div>
            </div>
            <div class="info-item">
              <div class="info-label">HAXAtom 版本</div>
              <div class="info-value">v{{ systemInfo.haxatom_version }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 资源使用趋势 -->
      <div class="info-card">
        <div class="card-header">
          <h2 class="card-title">
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
                d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
              />
            </svg>
            资源使用趋势
          </h2>
          <div class="card-actions">
            <span class="refresh-indicator" :class="{ loading }">
              <svg
                v-if="loading"
                class="spinning"
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
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                />
              </svg>
            </span>
          </div>
        </div>
        <div class="card-content">
          <div class="chart-container">
            <div class="chart-item">
              <div class="chart-label">
                <span class="chart-color cpu"></span>
                CPU 使用率
                <span class="chart-value"
                  >{{
                    cpuHistory.length > 0
                      ? cpuHistory[cpuHistory.length - 1].toFixed(1)
                      : "0.0"
                  }}%</span
                >
              </div>
              <div class="mini-chart" id="cpu-chart"></div>
            </div>
            <div class="chart-item">
              <div class="chart-label">
                <span class="chart-color memory"></span>
                内存使用率
                <span class="chart-value"
                  >{{
                    memoryHistory.length > 0
                      ? memoryHistory[memoryHistory.length - 1].toFixed(1)
                      : "0.0"
                  }}%</span
                >
              </div>
              <div class="mini-chart" id="memory-chart"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- 快速操作 -->
      <div class="info-card">
        <div class="card-header">
          <h2 class="card-title">
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
                d="M13 10V3L4 14h7v7l9-11h-7z"
              />
            </svg>
            快速操作
          </h2>
        </div>
        <div class="card-content">
          <div class="action-grid">
            <button class="action-btn">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                />
              </svg>
              刷新数据
            </button>
            <button class="action-btn">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                />
              </svg>
              导出日志
            </button>
            <button class="action-btn">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"
                />
              </svg>
              系统配置
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.settings-page {
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
  width: 28px;
  height: 28px;
  color: #4f46e5;
}

.page-description {
  font-size: 0.9375rem;
  color: #6b7280;
}

html.dark .page-description {
  color: #9ca3af;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
  cursor: pointer;
}

html.dark .stat-card {
  background: #1f2937;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

html.dark .stat-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon svg {
  width: 24px;
  height: 24px;
}

.cpu-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #ffffff;
}

.memory-icon {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: #ffffff;
}

.disk-icon {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: #ffffff;
}

.storage-icon {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  color: #ffffff;
}

.stat-content {
  flex: 1;
  min-width: 0;
}

.stat-label {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.5rem;
}

html.dark .stat-label {
  color: #9ca3af;
}

.stat-value {
  font-size: 1.875rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

html.dark .stat-value {
  color: #f3f4f6;
}

.stat-detail {
  font-size: 0.8125rem;
  color: #9ca3af;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Content Grid */
.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
}

.info-card {
  background: #ffffff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
}

html.dark .info-card {
  background: #1f2937;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

.info-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

html.dark .info-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
}

.card-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

html.dark .card-header {
  border-bottom-color: #374151;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

html.dark .card-title {
  color: #f3f4f6;
}

.card-title .icon {
  width: 20px;
  height: 20px;
  color: #4f46e5;
}

.card-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.refresh-indicator {
  width: 20px;
  height: 20px;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease;
}

html.dark .refresh-indicator {
  color: #9ca3af;
}

.refresh-indicator:hover {
  color: #4f46e5;
  transform: rotate(90deg);
}

.refresh-indicator svg {
  width: 100%;
  height: 100%;
}

.refresh-indicator.spinning .spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.card-content {
  padding: 1.5rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.25rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.info-label {
  font-size: 0.8125rem;
  color: #6b7280;
  font-weight: 500;
}

html.dark .info-label {
  color: #9ca3af;
}

.info-value {
  font-size: 0.9375rem;
  color: #1f2937;
  font-weight: 600;
}

html.dark .info-value {
  color: #f3f4f6;
}

/* Chart */
.chart-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.chart-item {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.chart-label {
  font-size: 0.875rem;
  color: #6b7280;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  flex: 1;
}

html.dark .chart-label {
  color: #9ca3af;
}

.chart-value {
  font-size: 0.9375rem;
  font-weight: 700;
  color: #1f2937;
}

html.dark .chart-value {
  color: #f3f4f6;
}

.chart-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.chart-color.cpu {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.chart-color.memory {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.mini-chart {
  height: 120px;
  width: 100%;
  background: #fafafa;
  border-radius: 8px;
  padding: 8px;
  box-sizing: border-box;
}

html.dark .mini-chart {
  background: #374151;
}

/* Action Buttons */
.action-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 1rem;
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.875rem 1rem;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  color: #374151;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

html.dark .action-btn {
  background: #374151;
  border-color: #4b5563;
  color: #f3f4f6;
}

.action-btn:hover {
  background: #f3f4f6;
  border-color: #d1d5db;
  transform: translateY(-1px);
}

html.dark .action-btn:hover {
  background: #4b5563;
  border-color: #6b7280;
}

.action-btn svg {
  width: 18px;
  height: 18px;
}

/* Responsive */
@media (max-width: 768px) {
  .settings-page {
    padding: 1rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .content-grid {
    grid-template-columns: 1fr;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .action-grid {
    grid-template-columns: 1fr;
  }
}
</style>
