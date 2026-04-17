<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from "vue";
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
const timeLabels = ref<string[]>([]);

// 加载状态
const loading = ref(false);
const autoRefresh = ref(5000);
let refreshTimer: any = null;
let uptimeTimer: any = null;

// ECharts 实例
let cpuChart: echarts.ECharts | null = null;
let memoryChart: echarts.ECharts | null = null;
let diskChart: echarts.ECharts | null = null;

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

// 获取当前时间标签
const getTimeLabel = () => {
  const now = new Date();
  return `${now.getHours().toString().padStart(2, "0")}:${now.getMinutes().toString().padStart(2, "0")}:${now.getSeconds().toString().padStart(2, "0")}`;
};

// 获取主题色
const getThemeColors = () => {
  const isDark = document.documentElement.classList.contains("dark");
  return {
    textColor: isDark ? "#e5e7eb" : "#374151",
    subtextColor: isDark ? "#9ca3af" : "#6b7280",
    borderColor: isDark ? "#374151" : "#e5e7eb",
    bgColor: isDark ? "#1f2937" : "#ffffff",
    cardBg: isDark ? "#111827" : "#f9fafb",
  };
};

// 初始化 ECharts
const initCharts = () => {
  const cpuChartEl = document.getElementById("cpu-trend-chart");
  const memoryChartEl = document.getElementById("memory-trend-chart");
  const diskChartEl = document.getElementById("disk-chart");

  const colors = getThemeColors();

  if (cpuChartEl) {
    cpuChart = echarts.init(cpuChartEl);
    cpuChart.setOption({
      tooltip: {
        trigger: "axis",
        backgroundColor: colors.cardBg,
        borderColor: colors.borderColor,
        textStyle: { color: colors.textColor },
        formatter: (params: any) => {
          const val = params[0]?.value;
          return `${params[0].axisValue}<br/>CPU: ${val.toFixed(1)}%`;
        },
      },
      grid: {
        top: 40,
        left: 50,
        right: 20,
        bottom: 30,
      },
      xAxis: {
        type: "category",
        boundaryGap: false,
        data: [],
        axisLine: { lineStyle: { color: colors.borderColor } },
        axisLabel: { color: colors.subtextColor, fontSize: 11 },
      },
      yAxis: {
        type: "value",
        min: 0,
        max: 100,
        axisLine: { lineStyle: { color: colors.borderColor } },
        axisLabel: { color: colors.subtextColor, formatter: "{value}%" },
        splitLine: { lineStyle: { color: colors.borderColor, type: "dashed" } },
      },
      series: [
        {
          name: "CPU",
          type: "line",
          smooth: true,
          symbol: "none",
          lineStyle: { color: "#6366f1", width: 3 },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: "rgba(99, 102, 241, 0.4)" },
              { offset: 1, color: "rgba(99, 102, 241, 0.05)" },
            ]),
          },
        },
      ],
    });
  }

  if (memoryChartEl) {
    memoryChart = echarts.init(memoryChartEl);
    memoryChart.setOption({
      tooltip: {
        trigger: "axis",
        backgroundColor: colors.cardBg,
        borderColor: colors.borderColor,
        textStyle: { color: colors.textColor },
        formatter: (params: any) => {
          const val = params[0]?.value;
          return `${params[0].axisValue}<br/>内存: ${val.toFixed(1)}%`;
        },
      },
      grid: {
        top: 40,
        left: 50,
        right: 20,
        bottom: 30,
      },
      xAxis: {
        type: "category",
        boundaryGap: false,
        data: [],
        axisLine: { lineStyle: { color: colors.borderColor } },
        axisLabel: { color: colors.subtextColor, fontSize: 11 },
      },
      yAxis: {
        type: "value",
        min: 0,
        max: 100,
        axisLine: { lineStyle: { color: colors.borderColor } },
        axisLabel: { color: colors.subtextColor, formatter: "{value}%" },
        splitLine: { lineStyle: { color: colors.borderColor, type: "dashed" } },
      },
      series: [
        {
          name: "内存",
          type: "line",
          smooth: true,
          symbol: "none",
          lineStyle: { color: "#ec4899", width: 3 },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: "rgba(236, 72, 153, 0.4)" },
              { offset: 1, color: "rgba(236, 72, 153, 0.05)" },
            ]),
          },
        },
      ],
    });
  }

  if (diskChartEl) {
    diskChart = echarts.init(diskChartEl);
    diskChart.setOption({
      tooltip: {
        trigger: "item",
        backgroundColor: colors.cardBg,
        borderColor: colors.borderColor,
        textStyle: { color: colors.textColor },
        formatter: "{b}: {c}GB ({d}%)",
      },
      series: [
        {
          name: "磁盘使用",
          type: "pie",
          radius: ["50%", "75%"],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 8,
            borderColor: colors.bgColor,
            borderWidth: 3,
          },
          label: {
            show: true,
            position: "outside",
            formatter: "{b}\n{d}%",
            color: colors.textColor,
            fontSize: 13,
          },
          labelLine: {
            lineStyle: { color: colors.borderColor },
          },
          data: [
            { value: 0, name: "已使用", itemStyle: { color: "#f59e0b" } },
            { value: 0, name: "可用", itemStyle: { color: "#10b981" } },
          ],
        },
      ],
    });
  }
};

// 更新图表
const updateCharts = () => {
  const colors = getThemeColors();

  if (cpuChart) {
    cpuChart.setOption({
      xAxis: { data: timeLabels.value },
      series: [{ data: cpuHistory.value }],
    });
  }

  if (memoryChart) {
    memoryChart.setOption({
      xAxis: { data: timeLabels.value },
      series: [{ data: memoryHistory.value }],
    });
  }

  if (diskChart) {
    const diskUsedGB = (
      (systemInfo.value.disk_used || 0) /
      (1024 * 1024 * 1024)
    ).toFixed(1);
    const diskTotalGB = (
      (systemInfo.value.disk_total || 0) /
      (1024 * 1024 * 1024)
    ).toFixed(1);
    const diskAvailGB = (
      parseFloat(diskTotalGB) - parseFloat(diskUsedGB)
    ).toFixed(1);
    diskChart.setOption({
      series: [
        {
          data: [
            { value: parseFloat(diskUsedGB), name: "已使用" },
            { value: parseFloat(diskAvailGB), name: "可用" },
          ],
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
      timeLabels.value.push(getTimeLabel());

      // 保持最近 30 条记录
      if (cpuHistory.value.length > 30) {
        cpuHistory.value.shift();
        memoryHistory.value.shift();
        timeLabels.value.shift();
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

// 监听主题变化
watch(
  () => document.documentElement.classList.contains("dark"),
  async () => {
    await nextTick();
    initCharts();
    updateCharts();
  },
);

// 生命周期
onMounted(async () => {
  await nextTick();
  initCharts();
  fetchSystemInfo();
  setupAutoRefresh();
  startUptimeTimer();

  // 窗口大小改变时重新渲染图表
  window.addEventListener("resize", () => {
    cpuChart?.resize();
    memoryChart?.resize();
    diskChart?.resize();
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
  diskChart?.dispose();
});
</script>

<template>
  <div class="settings-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">系统设置</h1>
        <p class="page-description">查看系统运行状态、资源使用情况和配置信息</p>
      </div>
      <div class="header-right">
        <div class="version-badge">v{{ systemInfo.haxatom_version }}</div>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-header">
          <div class="stat-icon cpu-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <rect
                x="4"
                y="4"
                width="16"
                height="16"
                rx="2"
                stroke-width="2"
              />
              <rect x="9" y="9" width="6" height="6" stroke-width="2" />
              <path
                d="M9 1v3M15 1v3M9 20v3M15 20v3M20 9h3M20 14h3M1 9h3M1 14h3"
                stroke-width="2"
              />
            </svg>
          </div>
          <span class="stat-label">CPU 使用率</span>
        </div>
        <div class="stat-value">
          {{ (systemInfo.cpu_percent || 0).toFixed(1) }}%
        </div>
        <div class="stat-detail">{{ systemInfo.cpu_model || "Unknown" }}</div>
        <div class="stat-progress">
          <div
            class="progress-bar"
            :style="{ width: `${systemInfo.cpu_percent || 0}%` }"
          ></div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-header">
          <div class="stat-icon memory-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path
                d="M6 4h12a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V6a2 2 0 012-2z"
                stroke-width="2"
              />
              <path d="M10 4v16M14 4v16M4 10h16M4 14h16" stroke-width="2" />
            </svg>
          </div>
          <span class="stat-label">内存使用率</span>
        </div>
        <div class="stat-value">
          {{ (systemInfo.memory_percent || 0).toFixed(1) }}%
        </div>
        <div class="stat-detail">
          {{ formatBytes(systemInfo.memory_used || 0) }} /
          {{ formatBytes(systemInfo.memory_total || 0) }}
        </div>
        <div class="stat-progress">
          <div
            class="progress-bar memory"
            :style="{ width: `${systemInfo.memory_percent || 0}%` }"
          ></div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-header">
          <div class="stat-icon uptime-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="12" cy="12" r="10" stroke-width="2" />
              <path d="M12 6v6l4 2" stroke-width="2" />
            </svg>
          </div>
          <span class="stat-label">运行时长</span>
        </div>
        <div class="stat-value uptime">
          {{ formatUptime(systemInfo.uptime || 0) }}
        </div>
        <div class="stat-detail">系统持续运行时间</div>
      </div>

      <div class="stat-card">
        <div class="stat-header">
          <div class="stat-icon disk-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M22 12H2l5-9h10l5 9z" stroke-width="2" />
              <path d="M22 12l-5 9H7l-5-9" stroke-width="2" />
              <path d="M12 2v20" stroke-width="2" />
            </svg>
          </div>
          <span class="stat-label">磁盘使用</span>
        </div>
        <div class="stat-value">
          {{ (systemInfo.disk_percent || 0).toFixed(1) }}%
        </div>
        <div class="stat-detail">
          {{ formatBytes(systemInfo.disk_used || 0) }} /
          {{ formatBytes(systemInfo.disk_total || 0) }}
        </div>
        <div class="stat-progress">
          <div
            class="progress-bar disk"
            :style="{ width: `${systemInfo.disk_percent || 0}%` }"
          ></div>
        </div>
      </div>
    </div>

    <!-- 资源使用趋势大屏 -->
    <div class="trend-section">
      <div class="section-header">
        <h2 class="section-title">资源使用趋势</h2>
        <div class="section-actions">
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
          <span class="update-hint"
            >每 {{ autoRefresh / 1000 }} 秒自动刷新</span
          >
        </div>
      </div>

      <div class="trend-grid">
        <div class="trend-card">
          <div class="trend-header">
            <div class="trend-label">
              <span class="trend-dot cpu"></span>
              <span>CPU 使用率</span>
            </div>
            <div class="trend-value">
              {{
                cpuHistory.length > 0
                  ? cpuHistory[cpuHistory.length - 1].toFixed(1)
                  : "0.0"
              }}%
            </div>
          </div>
          <div class="trend-chart" id="cpu-trend-chart"></div>
        </div>

        <div class="trend-card">
          <div class="trend-header">
            <div class="trend-label">
              <span class="trend-dot memory"></span>
              <span>内存使用率</span>
            </div>
            <div class="trend-value">
              {{
                memoryHistory.length > 0
                  ? memoryHistory[memoryHistory.length - 1].toFixed(1)
                  : "0.0"
              }}%
            </div>
          </div>
          <div class="trend-chart" id="memory-trend-chart"></div>
        </div>

        <div class="trend-card disk-card">
          <div class="trend-header">
            <div class="trend-label">
              <span class="trend-dot disk"></span>
              <span>磁盘使用</span>
            </div>
            <div class="trend-value">
              {{ (systemInfo.disk_percent || 0).toFixed(1) }}%
            </div>
          </div>
          <div class="disk-chart-wrapper">
            <div class="trend-chart" id="disk-chart"></div>
            <div class="disk-details">
              <div class="disk-item">
                <span class="disk-dot used"></span>
                <span class="disk-label">已使用</span>
                <span class="disk-size">{{
                  formatBytes(systemInfo.disk_used || 0)
                }}</span>
              </div>
              <div class="disk-item">
                <span class="disk-dot available"></span>
                <span class="disk-label">可用</span>
                <span class="disk-size">{{
                  formatBytes(systemInfo.disk_total - systemInfo.disk_used || 0)
                }}</span>
              </div>
              <div class="disk-item">
                <span class="disk-dot total"></span>
                <span class="disk-label">总计</span>
                <span class="disk-size">{{
                  formatBytes(systemInfo.disk_total || 0)
                }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 系统信息 -->
    <div class="info-section">
      <div class="section-header">
        <h2 class="section-title">系统信息</h2>
      </div>

      <div class="info-card">
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
  </div>
</template>

<style scoped>
.settings-page {
  padding: 32px;
  max-width: 1800px;
  margin: 0 auto;
  min-height: 100%;
}

/* Page Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
}

.header-left {
  flex: 1;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 8px 0;
}

.page-description {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
}

.version-badge {
  padding: 6px 14px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 32px;
}

.stat-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 20px;
  transition: all 0.2s ease;
}

.stat-card:hover {
  border-color: var(--primary-color);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.stat-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
}

.stat-icon svg {
  width: 20px;
  height: 20px;
}

.cpu-icon {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
}

.memory-icon {
  background: linear-gradient(135deg, #ec4899 0%, #f43f5e 100%);
}

.uptime-icon {
  background: linear-gradient(135deg, #10b981 0%, #14b8a6 100%);
}

.disk-icon {
  background: linear-gradient(135deg, #f59e0b 0%, #f97316 100%);
}

.stat-label {
  font-size: 14px;
  color: var(--text-secondary);
  font-weight: 500;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
  line-height: 1.2;
}

.stat-value.uptime {
  font-size: 20px;
}

.stat-detail {
  font-size: 12px;
  color: var(--text-tertiary);
  margin-bottom: 12px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.stat-progress {
  height: 4px;
  background: var(--bg-secondary);
  border-radius: 2px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
  border-radius: 2px;
  transition: width 0.3s ease;
}

.progress-bar.memory {
  background: linear-gradient(90deg, #ec4899 0%, #f43f5e 100%);
}

.progress-bar.disk {
  background: linear-gradient(90deg, #f59e0b 0%, #f97316 100%);
}

/* Trend Section */
.trend-section {
  margin-bottom: 32px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.section-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.refresh-indicator {
  width: 20px;
  height: 20px;
  color: var(--text-tertiary);
  cursor: pointer;
  transition: color 0.2s;
}

.refresh-indicator:hover {
  color: var(--primary-color);
}

.refresh-indicator.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.update-hint {
  font-size: 12px;
  color: var(--text-tertiary);
}

.trend-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.trend-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 20px;
  min-height: 320px;
  display: flex;
  flex-direction: column;
}

.trend-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.trend-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.trend-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.trend-dot.cpu {
  background: #6366f1;
}

.trend-dot.memory {
  background: #ec4899;
}

.trend-dot.disk {
  background: #f59e0b;
}

.trend-value {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
}

.trend-chart {
  flex: 1;
  min-height: 240px;
}

.disk-card {
  align-items: center;
}

.disk-chart-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

#disk-chart {
  width: 200px;
  height: 200px;
}

.disk-details {
  display: flex;
  gap: 24px;
}

.disk-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.disk-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.disk-dot.used {
  background: #f59e0b;
}

.disk-dot.available {
  background: #10b981;
}

.disk-dot.total {
  background: #6b7280;
}

.disk-label {
  font-size: 12px;
  color: var(--text-secondary);
}

.disk-size {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-primary);
}

/* Info Section */
.info-section {
  margin-bottom: 32px;
}

.info-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 24px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-label {
  font-size: 12px;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 500;
}

.info-value {
  font-size: 14px;
  color: var(--text-primary);
  font-weight: 500;
}

/* Responsive */
@media (max-width: 1400px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .trend-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 1024px) {
  .settings-page {
    padding: 24px;
  }
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .trend-grid {
    grid-template-columns: 1fr;
  }
  .info-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .settings-page {
    padding: 16px;
  }
  .page-header {
    flex-direction: column;
    gap: 16px;
  }
  .stats-grid {
    grid-template-columns: 1fr;
  }
  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>
