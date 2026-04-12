<script setup lang="ts">
import { computed } from "vue";
import { useRouter } from "vue-router";
import { t } from "../../../locales";

const $t = computed(() => t);
const router = useRouter();

// 快捷操作卡片
const quickActions = [
  {
    title: "创建预设方案",
    description: "从资源池挑选零件，快速组装 AI 智能体",
    icon: "plus-circle",
    action: () => router.push("/bot/presets"),
    color: "from-violet-500 to-purple-600",
  },
  {
    title: "配置模型",
    description: "管理所有大模型配置（OpenAI、智谱、DeepSeek 等）",
    icon: "cpu",
    action: () => router.push("/bot/models"),
    color: "from-blue-500 to-cyan-600",
  },
  {
    title: "知识库管理",
    description: "上传文档，构建企业级 RAG 知识库",
    icon: "database",
    action: () => router.push("/bot/knowledge"),
    color: "from-emerald-500 to-green-600",
  },
  {
    title: "插件中心",
    description: "管理工具插件（搜索、天气、计算器等）",
    icon: "puzzle",
    action: () => router.push("/bot/plugins"),
    color: "from-orange-500 to-amber-600",
  },
];

// 资源池统计
const resourceStats = [
  {
    label: "模型池",
    value: "0",
    unit: "个配置",
    icon: "cpu",
    color: "text-violet-600",
    bg: "bg-violet-50",
  },
  {
    label: "提示词池",
    value: "0",
    unit: "个人设",
    icon: "message-square",
    color: "text-blue-600",
    bg: "bg-blue-50",
  },
  {
    label: "插件池",
    value: "0",
    unit: "个工具",
    icon: "puzzle",
    color: "text-emerald-600",
    bg: "bg-emerald-50",
  },
  {
    label: "知识库",
    value: "0",
    unit: "个文档集",
    icon: "database",
    color: "text-orange-600",
    bg: "bg-orange-50",
  },
  {
    label: "记忆池",
    value: "0",
    unit: "个策略",
    icon: "brain",
    color: "text-pink-600",
    bg: "bg-pink-50",
  },
];

// 导航到指定页面
const navigateTo = (path: string) => {
  router.push(path);
};
</script>

<template>
  <div class="welcome-page">
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          <span class="gradient-text">HAXAtom</span>
          <span class="subtitle">AI 智能体管理与多端分发平台</span>
        </h1>
        <p class="hero-description">
          基于「原子化解耦 · 乐高式拼装」理念构建的全栈 AI 智能体管理平台
        </p>
        <div class="hero-actions">
          <button class="btn btn-primary" @click="navigateTo('/bot/presets')">
            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            创建第一个预设方案
          </button>
          <button class="btn btn-secondary" @click="navigateTo('/bot/models')">
            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2z"/>
            </svg>
            配置模型
          </button>
        </div>
      </div>
    </div>

    <!-- Resource Stats Section -->
    <div class="stats-section">
      <h2 class="section-title">资源池概览</h2>
      <div class="stats-grid">
        <div
          v-for="stat in resourceStats"
          :key="stat.label"
          class="stat-card"
        >
          <div :class="['stat-icon', stat.bg, stat.color]">
            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path v-if="stat.icon === 'cpu'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2z"/>
              <path v-else-if="stat.icon === 'message-square'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
              <path v-else-if="stat.icon === 'puzzle'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 4a2 2 0 114 0v1a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-1a2 2 0 100 4h1a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-1a2 2 0 10-4 0v1a1 1 0 01-1 1H7a1 1 0 01-1-1v-3a1 1 0 00-1-1H4a2 2 0 110-4h1a1 1 0 001-1V7a1 1 0 011-1h3a1 1 0 001-1V4z"/>
              <path v-else-if="stat.icon === 'database'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4"/>
              <path v-else-if="stat.icon === 'brain'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3M3.343 7.05l.707.707M6 12a6 6 0 0112 0v3a6 6 0 01-12 0v-3z"/>
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stat.value }}<span class="stat-unit">{{ stat.unit }}</span></div>
            <div class="stat-label">{{ stat.label }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions Section -->
    <div class="actions-section">
      <h2 class="section-title">快速开始</h2>
      <div class="actions-grid">
        <div
          v-for="action in quickActions"
          :key="action.title"
          :class="['action-card', 'cursor-pointer']"
          @click="action.action"
        >
          <div :class="['action-icon', 'gradient', action.color]">
            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path v-if="action.icon === 'plus-circle'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
              <path v-else-if="action.icon === 'cpu'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2z"/>
              <path v-else-if="action.icon === 'database'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4"/>
              <path v-else-if="action.icon === 'puzzle'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 4a2 2 0 114 0v1a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-1a2 2 0 100 4h1a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-1a2 2 0 10-4 0v1a1 1 0 01-1 1H7a1 1 0 01-1-1v-3a1 1 0 00-1-1H4a2 2 0 110-4h1a1 1 0 001-1V7a1 1 0 011-1h3a1 1 0 001-1V4z"/>
            </svg>
          </div>
          <div class="action-content">
            <h3 class="action-title">{{ action.title }}</h3>
            <p class="action-description">{{ action.description }}</p>
          </div>
          <svg class="action-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
          </svg>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div class="features-section">
      <h2 class="section-title">核心特性</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon gradient from-violet-500 to-purple-600">
            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
            </svg>
          </div>
          <h3 class="feature-title">五大原子化资源池</h3>
          <p class="feature-description">
            模型、提示词、插件、知识库、记忆完全解耦，一次配置，全项目无限复用
          </p>
        </div>
        <div class="feature-card">
          <div class="feature-icon gradient from-blue-500 to-cyan-600">
            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 4a2 2 0 114 0v1a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-1a2 2 0 100 4h1a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-1a2 2 0 10-4 0v1a1 1 0 01-1 1H7a1 1 0 01-1-1v-3a1 1 0 00-1-1H4a2 2 0 110-4h1a1 1 0 001-1V7a1 1 0 011-1h3a1 1 0 001-1V4z"/>
            </svg>
          </div>
          <h3 class="feature-title">乐高式拼装</h3>
          <p class="feature-description">
            从资源池挑选零件，快速组装 AI 智能体，支持温度、top_p 等参数覆盖
          </p>
        </div>
        <div class="feature-card">
          <div class="feature-icon gradient from-emerald-500 to-green-600">
            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
            </svg>
          </div>
          <h3 class="feature-title">LangGraph 工作流</h3>
          <p class="feature-description">
            基于 LangChain + LangGraph 构建，支持 RAG 检索、工具调用、多轮对话
          </p>
        </div>
        <div class="feature-card">
          <div class="feature-icon gradient from-orange-500 to-amber-600">
            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <h3 class="feature-title">全渠道触达</h3>
          <p class="feature-description">
            一套配置同时支持 Web、飞书、钉钉、QQ、Telegram 等多平台
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.welcome-page {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  background: transparent;
  min-height: calc(100vh - 80px);
}

html.dark .welcome-page {
  background: transparent;
}

/* Hero Section */
.hero-section {
  margin-bottom: 3rem;
  padding: 3rem 2rem;
  background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(124, 58, 237, 0.3);
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  color: white;
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.gradient-text {
  background: linear-gradient(135deg, #ffffff 0%, #f0e6ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-size: 1.25rem;
  font-weight: 400;
  opacity: 0.9;
  margin-top: 0.5rem;
}

.hero-description {
  font-size: 1.125rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 2rem;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.btn .icon {
  width: 20px;
  height: 20px;
}

.btn-primary {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.btn-primary:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.btn-secondary {
  background: #f97316;
  color: white;
}

.btn-secondary:hover {
  background: #ea580c;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.4);
}

/* Section Title */
.section-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #4c1d95;
  margin-bottom: 1.5rem;
  text-align: center;
}

html.dark .section-title {
  color: #a78bfa;
}

/* Stats Section */
.stats-section {
  margin-bottom: 3rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
  cursor: pointer;
}

html.dark .stat-card {
  background: #1a1a2e;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon .icon {
  width: 24px;
  height: 24px;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: #4c1d95;
  line-height: 1;
}

html.dark .stat-value {
  color: #a78bfa;
}

.stat-unit {
  font-size: 0.875rem;
  font-weight: 400;
  color: #6b7280;
  margin-left: 0.25rem;
}

html.dark .stat-unit {
  color: #9ca3af;
}

.stat-label {
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

html.dark .stat-label {
  color: #9ca3af;
}

/* Actions Section */
.actions-section {
  margin-bottom: 3rem;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.action-card {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
  position: relative;
}

html.dark .action-card {
  background: #1a1a2e;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.action-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: white;
}

.action-icon.gradient {
  background: linear-gradient(135deg, var(--tw-gradient-from), var(--tw-gradient-to));
}

.action-icon .icon {
  width: 24px;
  height: 24px;
}

.action-content {
  flex: 1;
}

.action-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

html.dark .action-title {
  color: #f3f4f6;
}

.action-description {
  font-size: 0.875rem;
  color: #6b7280;
  line-height: 1.5;
}

html.dark .action-description {
  color: #9ca3af;
}

.action-arrow {
  width: 20px;
  height: 20px;
  color: #9ca3af;
  flex-shrink: 0;
  transition: transform 0.2s ease;
}

.action-card:hover .action-arrow {
  transform: translateX(4px);
  color: #7c3aed;
}

/* Features Section */
.features-section {
  margin-bottom: 3rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.feature-card {
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
  text-align: center;
}

html.dark .feature-card {
  background: #1a1a2e;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 1.5rem;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.feature-icon.gradient {
  background: linear-gradient(135deg, var(--tw-gradient-from), var(--tw-gradient-to));
}

.feature-icon .icon {
  width: 32px;
  height: 32px;
}

.feature-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.75rem;
}

html.dark .feature-title {
  color: #f3f4f6;
}

.feature-description {
  font-size: 0.875rem;
  color: #6b7280;
  line-height: 1.6;
}

html.dark .feature-description {
  color: #9ca3af;
}

/* Responsive */
@media (max-width: 768px) {
  .welcome-page {
    padding: 1rem;
  }

  .hero-section {
    padding: 2rem 1rem;
  }

  .hero-title {
    font-size: 2rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .hero-actions {
    flex-direction: column;
  }

  .btn {
    width: 100%;
    justify-content: center;
  }

  .stats-grid,
  .actions-grid,
  .features-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
