<script setup lang="ts">
import { computed } from "vue";
import { t } from "../../../locales";

const $t = computed(() => t);

const changelogItems = [
  {
    version: "v1.0.0",
    date: "2026-04-16",
    status: "current",
    changes: [
      {
        type: "feature",
        title: "前后端集成与样式修复",
        description: "完成前后端静态资源集成，修复浅色模式文字显示问题",
      },
      {
        type: "feature",
        title: "系统设置页面重构",
        description: "全新设计系统监控大屏，支持 CPU/内存/磁盘实时趋势图表",
      },
      {
        type: "improve",
        title: "侧边栏底部菜单优化",
        description: "支持路由跳转和外部链接混合模式，添加选中状态样式",
      },
    ],
  },
  {
    version: "v0.9.0",
    date: "2026-04-15",
    status: "stable",
    changes: [
      {
        type: "feature",
        title: "完成机器人和插件管理页面",
        description: "新增完整的机器人配置管理和插件管理界面",
      },
      {
        type: "improve",
        title: "插件系统重构",
        description: "来源分类、整合内置工具、完善文档",
      },
      {
        type: "fix",
        title: "优化日志配置",
        description: "屏蔽心跳日志，只保留连接和消息日志",
      },
    ],
  },
  {
    version: "v0.8.0",
    date: "2026-04-14",
    status: "stable",
    changes: [
      {
        type: "feature",
        title: "添加 QQ 机器人功能",
        description: "支持 OneBot v11 协议，集成 NapCat 实现 QQ 机器人接入",
      },
    ],
  },
  {
    version: "v0.7.0",
    date: "2026-04-13",
    status: "stable",
    changes: [
      {
        type: "feature",
        title: "添加模型禁用功能",
        description: "支持禁用特定模型，统一数据库路径配置",
      },
      {
        type: "feature",
        title: "支持 Ollama 模型列表获取",
        description:
          "添加 Ollama 供应商支持，使用 GET /api/tags 端点获取本地模型，无需 API Key 认证",
      },
      {
        type: "feature",
        title: "实现获取模型列表和自定义模型功能",
        description: "支持动态获取可用模型列表，添加自定义模型配置",
      },
      {
        type: "improve",
        title: "优化系统设置页面显示",
        description: "改进系统信息展示布局和交互体验",
      },
    ],
  },
  {
    version: "v0.6.0",
    date: "2026-04-12",
    status: "stable",
    changes: [
      {
        type: "feature",
        title: "新增系统设置页面和平台日志页面",
        description: "实时监控系统负载、CPU/内存使用率、运行时长等信息",
      },
    ],
  },
  {
    version: "v0.5.0",
    date: "2026-04-11",
    status: "stable",
    changes: [
      {
        type: "feature",
        title: "完善预设方案提示词配置",
        description: "新增下拉框选择功能，支持快速切换提示词模板",
      },
      {
        type: "improve",
        title: "更新 GitHub 展示 README",
        description: "完善项目文档和展示页面",
      },
    ],
  },
  {
    version: "v0.4.0",
    date: "2026-04-06",
    status: "stable",
    changes: [
      {
        type: "feature",
        title: "完善人格设定页面和预设方案页面 UI",
        description: "优化界面布局和交互体验，提升视觉设计",
      },
    ],
  },
  {
    version: "v0.3.0",
    date: "2026-04-05",
    status: "stable",
    changes: [
      {
        type: "feature",
        title: "优化聊天界面和记忆功能",
        description: "改进对话体验，增强记忆管理能力",
      },
    ],
  },
  {
    version: "v0.1.0",
    date: "2026-04-04",
    status: "stable",
    changes: [
      {
        type: "feature",
        title: "Initial commit: HAXAtom",
        description:
          "原子化 AI 智能体管理平台，五大资源池独立解耦，乐高式组合装配",
      },
    ],
  },
];
</script>

<template>
  <div class="changelog-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">更新日志</h1>
        <p class="page-description">了解 HAXAtom 的最新功能改进和修复</p>
      </div>
      <div class="header-right">
        <a
          href="https://github.com/guhong521/HAXAtom"
          target="_blank"
          class="github-link"
        >
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path
              d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"
            />
          </svg>
          GitHub
        </a>
      </div>
    </div>

    <!-- 时间线 -->
    <div class="timeline">
      <div
        v-for="(item, index) in changelogItems"
        :key="index"
        class="timeline-item"
      >
        <div class="timeline-marker">
          <div class="marker-dot" :class="item.status"></div>
          <div
            v-if="index < changelogItems.length - 1"
            class="marker-line"
          ></div>
        </div>

        <div class="timeline-content">
          <div class="version-card" :class="item.status">
            <div class="version-header">
              <div class="version-info">
                <h2 class="version-number">{{ item.version }}</h2>
                <span class="version-date">{{ item.date }}</span>
              </div>
              <span class="version-badge" :class="item.status">
                {{ item.status === "current" ? "最新版本" : "稳定版" }}
              </span>
            </div>

            <div class="version-content">
              <div
                v-for="(change, changeIndex) in item.changes"
                :key="changeIndex"
                class="change-item"
              >
                <div class="change-icon" :class="`change-${change.type}`">
                  <svg
                    v-if="change.type === 'feature'"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                    />
                  </svg>
                  <svg
                    v-else-if="change.type === 'fix'"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                  <svg
                    v-else-if="change.type === 'improve'"
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
                </div>
                <div class="change-content">
                  <h3 class="change-title">{{ change.title }}</h3>
                  <p class="change-description">{{ change.description }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.changelog-page {
  padding: 32px;
  max-width: 900px;
  margin: 0 auto;
  min-height: 100%;
}

/* Page Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 40px;
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

.github-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-primary);
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s ease;
}

.github-link:hover {
  border-color: var(--primary-color);
  background: var(--bg-secondary);
}

.github-link svg {
  width: 20px;
  height: 20px;
}

/* Timeline */
.timeline {
  position: relative;
}

.timeline-item {
  display: flex;
  gap: 20px;
}

.timeline-marker {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
}

.marker-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--border-color);
  border: 2px solid var(--bg-card);
  box-shadow: 0 0 0 2px var(--border-color);
  z-index: 1;
}

.marker-dot.current {
  background: var(--primary-color);
  box-shadow: 0 0 0 2px var(--primary-color);
}

.marker-line {
  width: 2px;
  flex: 1;
  min-height: 40px;
  background: var(--border-color);
  margin-top: 4px;
}

.timeline-content {
  flex: 1;
  padding-bottom: 32px;
}

/* Version Card */
.version-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.2s ease;
}

.version-card:hover {
  border-color: var(--primary-color);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.version-card.current {
  border-left: 3px solid var(--primary-color);
}

.version-header {
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.version-info {
  display: flex;
  align-items: baseline;
  gap: 12px;
}

.version-number {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.version-date {
  font-size: 13px;
  color: var(--text-tertiary);
}

.version-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.version-badge.current {
  background: var(--primary-light);
  color: var(--primary-color);
}

.version-badge.stable {
  background: var(--bg-secondary);
  color: var(--text-secondary);
}

.version-content {
  padding: 16px 20px;
}

.change-item {
  display: flex;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid var(--border-color);
}

.change-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.change-item:first-child {
  padding-top: 0;
}

.change-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.change-icon svg {
  width: 16px;
  height: 16px;
}

.change-icon.change-feature {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: #ffffff;
}

.change-icon.change-fix {
  background: linear-gradient(135deg, #f43f5e 0%, #e11d48 100%);
  color: #ffffff;
}

.change-icon.change-improve {
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  color: #ffffff;
}

.change-content {
  flex: 1;
  min-width: 0;
}

.change-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 4px 0;
}

.change-description {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
  margin: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .changelog-page {
    padding: 20px;
  }

  .page-header {
    flex-direction: column;
    gap: 16px;
  }

  .timeline-item {
    gap: 12px;
  }

  .version-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>
