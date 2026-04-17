<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { http } from "../../../api/request";

const router = useRouter();

const stats = ref({
  models: 0,
  prompts: 0,
  plugins: 0,
  knowledgeBases: 0,
  memories: 0,
  presets: 0,
});

const loading = ref(false);

const fetchStats = async () => {
  loading.value = true;
  try {
    const [modelsRes, promptsRes, pluginsRes, kbRes, memoriesRes, presetsRes] =
      await Promise.allSettled([
        http.get<any>("/models?limit=1"),
        http.get<any>("/prompts?limit=1"),
        http.get<any>("/plugins"),
        http.get<any>("/knowledge-bases?limit=1"),
        http.get<any>("/memories"),
        http.get<any>("/presets?limit=1"),
      ]);

    if (modelsRes.status === "fulfilled") {
      const total = modelsRes.value.total ?? modelsRes.value.data?.length ?? 0;
      stats.value.models = typeof total === "number" ? total : 0;
    }
    if (promptsRes.status === "fulfilled") {
      const total =
        promptsRes.value.total ?? promptsRes.value.data?.length ?? 0;
      stats.value.prompts = typeof total === "number" ? total : 0;
    }
    if (pluginsRes.status === "fulfilled") {
      const data = pluginsRes.value.data ?? pluginsRes.value;
      stats.value.plugins = Array.isArray(data) ? data.length : 0;
    }
    if (kbRes.status === "fulfilled") {
      const total = kbRes.value.total ?? kbRes.value.data?.length ?? 0;
      stats.value.knowledgeBases = typeof total === "number" ? total : 0;
    }
    if (memoriesRes.status === "fulfilled") {
      const data = memoriesRes.value.data ?? memoriesRes.value;
      stats.value.memories = Array.isArray(data) ? data.length : 0;
    }
    if (presetsRes.status === "fulfilled") {
      const total =
        presetsRes.value.total ?? presetsRes.value.data?.length ?? 0;
      stats.value.presets = typeof total === "number" ? total : 0;
    }
  } catch (error) {
    console.error("获取资源池统计失败:", error);
  } finally {
    loading.value = false;
  }
};

const resourceCards = [
  {
    label: "模型池",
    value: computed(() => stats.value.models),
    unit: "个配置",
    path: "/bot/model",
  },
  {
    label: "提示词池",
    value: computed(() => stats.value.prompts),
    unit: "个人设",
    path: "/bot/personality",
  },
  {
    label: "插件池",
    value: computed(() => stats.value.plugins),
    unit: "个工具",
    path: "/bot/plugins",
  },
  {
    label: "知识库",
    value: computed(() => stats.value.knowledgeBases),
    unit: "个文档集",
    path: "/bot/knowledge",
  },
  {
    label: "记忆池",
    value: computed(() => stats.value.memories),
    unit: "个策略",
    path: "/bot/memory",
  },
  {
    label: "预设方案",
    value: computed(() => stats.value.presets),
    unit: "个智能体",
    path: "/bot/preset",
  },
];

const navigateTo = (path: string) => {
  router.push(path);
};

onMounted(() => {
  fetchStats();
});
</script>

<template>
  <div class="welcome-page">
    <div class="bg-gradient"></div>
    <div class="floating-orb orb-1"></div>
    <div class="floating-orb orb-2"></div>
    <div class="floating-orb orb-3"></div>

    <div class="page-content">
      <div class="page-header fade-in-up">
        <h1 class="page-title">
          欢迎使用 <span class="gradient-text">HAXAtom</span>
        </h1>
        <p class="page-desc">
          原子化 AI 智能体管理平台 · 五大资源池独立解耦，乐高式组合装配
        </p>
      </div>

      <div class="stats-section fade-in-up delay-1">
        <div class="section-header">
          <h2 class="section-title">资源池概览</h2>
          <button class="refresh-btn" @click="fetchStats" :class="{ loading }">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
              />
            </svg>
          </button>
        </div>

        <div class="stats-grid">
          <div
            v-for="card in resourceCards"
            :key="card.label"
            class="glass-card stat-card"
            @click="navigateTo(card.path)"
          >
            <div class="stat-value gradient-text">{{ card.value }}</div>
            <div class="stat-label">{{ card.label }}</div>
            <div class="stat-unit">{{ card.unit }}</div>
          </div>
        </div>
      </div>

      <div class="features-section fade-in-up delay-2">
        <h2 class="section-title">核心特性</h2>
        <div class="features-grid">
          <div class="glass-card feature-card">
            <h3 class="feature-title">五大原子化资源池</h3>
            <p class="feature-desc">
              模型、提示词、插件、知识库、记忆完全解耦，一次配置，全项目无限复用
            </p>
          </div>
          <div class="glass-card feature-card">
            <h3 class="feature-title">乐高式拼装</h3>
            <p class="feature-desc">
              从资源池挑选零件，快速组装 AI 智能体，支持温度、top_p 等参数覆盖
            </p>
          </div>
          <div class="glass-card feature-card">
            <h3 class="feature-title">LangGraph 工作流</h3>
            <p class="feature-desc">
              基于 LangChain + LangGraph 构建，支持 RAG 检索、工具调用、多轮对话
            </p>
          </div>
          <div class="glass-card feature-card">
            <h3 class="feature-title">全渠道触达</h3>
            <p class="feature-desc">
              一套配置同时支持 Web、飞书、钉钉、QQ、Telegram 等多平台
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap");

.welcome-page {
  position: relative;
  min-height: 100vh;
  padding: clamp(2rem, 5vw, 4rem);
  font-family:
    "Inter",
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    Roboto,
    sans-serif;
  overflow: hidden;
}

.bg-gradient {
  position: fixed;
  inset: 0;
  background: linear-gradient(
    135deg,
    #667eea 0%,
    #764ba2 25%,
    #f093fb 50%,
    #4facfe 75%,
    #43e97b 100%
  );
  background-size: 400% 400%;
  animation: gradientShift 15s ease infinite;
  opacity: 0.15;
  z-index: -2;
}

@keyframes gradientShift {
  0%,
  100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

.floating-orb {
  position: fixed;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
  z-index: -1;
  animation: float 20s ease-in-out infinite;
}

.orb-1 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  top: -100px;
  right: -100px;
  animation-delay: 0s;
}

.orb-2 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #f093fb, #f5576c);
  bottom: -50px;
  left: -50px;
  animation-delay: -5s;
}

.orb-3 {
  width: 250px;
  height: 250px;
  background: linear-gradient(135deg, #4facfe, #00f2fe);
  top: 50%;
  left: 50%;
  animation-delay: -10s;
}

@keyframes float {
  0%,
  100% {
    transform: translate(0, 0) scale(1);
  }
  25% {
    transform: translate(30px, -30px) scale(1.05);
  }
  50% {
    transform: translate(-20px, 20px) scale(0.95);
  }
  75% {
    transform: translate(20px, 10px) scale(1.02);
  }
}

.page-content {
  position: relative;
  z-index: 1;
  max-width: 1280px;
  margin: 0 auto;
}

.fade-in-up {
  opacity: 0;
  transform: translateY(30px);
  animation: fadeInUp 0.8s ease forwards;
}

.delay-1 {
  animation-delay: 0.2s;
}

.delay-2 {
  animation-delay: 0.4s;
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.page-header {
  margin-bottom: clamp(2rem, 4vw, 3rem);
}

.page-title {
  font-size: clamp(2rem, 5vw, 3rem);
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 0.75rem 0;
  letter-spacing: -0.02em;
}

.gradient-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #4facfe 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-desc {
  font-size: clamp(0.9rem, 2vw, 1.1rem);
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.6;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: clamp(1.1rem, 2vw, 1.3rem);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 1rem 0;
}

.refresh-btn {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  background: #ffffff;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

html.dark .refresh-btn {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.12);
}

.refresh-btn:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
  transform: scale(1.05);
}

.refresh-btn.loading svg {
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

.refresh-btn svg {
  width: 18px;
  height: 18px;
}

.stats-section {
  margin-bottom: clamp(2rem, 4vw, 3rem);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 1rem;
}

.glass-card {
  background: #ffffff;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 16px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

html.dark .glass-card {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.12);
}

.glass-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
  border-color: rgba(0, 0, 0, 0.12);
}

html.dark .glass-card:hover {
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  border-color: rgba(255, 255, 255, 0.2);
}

.stat-card {
  padding: 1.5rem;
  text-align: center;
  cursor: pointer;
}

.stat-value {
  font-size: clamp(1.8rem, 3vw, 2.2rem);
  font-weight: 700;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: clamp(0.85rem, 1.5vw, 0.95rem);
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: 0.25rem;
}

.stat-unit {
  font-size: clamp(0.75rem, 1.2vw, 0.85rem);
  color: var(--text-tertiary);
}

.features-section {
  margin-bottom: clamp(2rem, 4vw, 3rem);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.feature-card {
  padding: 1.5rem;
}

.feature-title {
  font-size: clamp(0.95rem, 1.5vw, 1.05rem);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 0.5rem 0;
}

.feature-desc {
  font-size: clamp(0.8rem, 1.2vw, 0.9rem);
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
}

::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .features-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
