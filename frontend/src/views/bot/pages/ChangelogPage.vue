<script setup lang="ts">
import { computed } from "vue";
import { t } from "../../../locales";

const $t = computed(() => t);

const changelogItems = [
  {
    version: "v1.0.0",
    date: "2026-04-12",
    status: "current",
    changes: [
      {
        type: "feature",
        title: "新增系统设置页面",
        description: "实时监控系统负载、CPU/内存使用率、运行时长等信息",
      },
      {
        type: "feature",
        title: "资源使用趋势图表",
        description: "可视化展示最近 20 次采样的 CPU 和内存使用情况",
      },
      {
        type: "fix",
        title: "修复平台日志页面路由问题",
        description: "修复 API 导入错误，现在可以正常跳转和加载",
      },
      {
        type: "improve",
        title: "优化侧边栏底部菜单",
        description: "支持路由跳转和外部链接混合模式",
      },
    ],
  },
];
</script>

<template>
  <div class="changelog-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
          />
        </svg>
        更新日志
      </h1>
      <p class="page-description">了解 HAXAtom 的最新功能改进和修复</p>
    </div>

    <!-- 更新列表 -->
    <div class="changelog-list">
      <div
        v-for="(item, index) in changelogItems"
        :key="index"
        class="version-card"
        :class="item.status"
      >
        <div class="version-header">
          <div class="version-info">
            <h2 class="version-number">{{ item.version }}</h2>
            <span class="version-date">{{ item.date }}</span>
          </div>
          <span class="version-badge" :class="item.status">
            {{ item.status === "current" ? "当前版本" : "历史版本" }}
          </span>
        </div>

        <div class="version-content">
          <div
            v-for="(change, changeIndex) in item.changes"
            :key="changeIndex"
            class="change-item"
          >
            <div class="change-icon" :class="`change-${change.type}`">
              <svg v-if="change.type === 'feature'" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                />
              </svg>
              <svg v-else-if="change.type === 'fix'" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <svg v-else-if="change.type === 'improve'" viewBox="0 0 24 24" fill="none" stroke="currentColor">
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

    <!-- 更多更新 -->
    <div class="more-section">
      <div class="more-card">
        <div class="more-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
        </div>
        <div class="more-content">
          <h3>更多历史版本</h3>
          <p>查看完整的更新历史，了解 HAXAtom 的成长历程</p>
        </div>
        <a href="https://github.com/guhong521/HAXAtom/releases" target="_blank" class="more-link">
          查看 GitHub Releases
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
            />
          </svg>
        </a>
      </div>
    </div>
  </div>
</template>

<style scoped>
.changelog-page {
  padding: 2rem;
  max-width: 1000px;
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

/* Changelog List */
.changelog-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.version-card {
  background: #ffffff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
}

html.dark .version-card {
  background: #1f2937;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

.version-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

html.dark .version-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
}

.version-card.current {
  border-left: 4px solid #4f46e5;
}

.version-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

html.dark .version-header {
  border-bottom-color: #374151;
}

.version-info {
  display: flex;
  align-items: baseline;
  gap: 0.75rem;
}

.version-number {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1f2937;
}

html.dark .version-number {
  color: #f3f4f6;
}

.version-date {
  font-size: 0.875rem;
  color: #6b7280;
}

html.dark .version-date {
  color: #9ca3af;
}

.version-badge {
  padding: 0.375rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.version-badge.current {
  background: #e0e7ff;
  color: #4f46e5;
}

html.dark .version-badge.current {
  background: #312e81;
  color: #a5b4fc;
}

.version-content {
  padding: 1.5rem;
}

.change-item {
  display: flex;
  gap: 1rem;
  padding: 1rem 0;
  border-bottom: 1px solid #f3f4f6;
}

html.dark .change-item {
  border-bottom-color: #374151;
}

.change-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.change-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.change-icon svg {
  width: 20px;
  height: 20px;
}

.change-icon.change-feature {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  color: #ffffff;
}

.change-icon.change-fix {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: #ffffff;
}

.change-icon.change-improve {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #ffffff;
}

.change-content {
  flex: 1;
  min-width: 0;
}

.change-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

html.dark .change-title {
  color: #f3f4f6;
}

.change-description {
  font-size: 0.875rem;
  color: #6b7280;
  line-height: 1.5;
}

html.dark .change-description {
  color: #9ca3af;
}

/* More Section */
.more-section {
  margin-top: 2rem;
}

.more-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 2rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  color: #ffffff;
  transition: all 0.2s ease;
}

.more-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.more-icon {
  width: 56px;
  height: 56px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.more-icon svg {
  width: 28px;
  height: 28px;
}

.more-content {
  flex: 1;
}

.more-content h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.more-content p {
  font-size: 0.875rem;
  opacity: 0.9;
}

.more-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: #ffffff;
  font-size: 0.875rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.more-link:hover {
  background: rgba(255, 255, 255, 0.3);
}

.more-link svg {
  width: 18px;
  height: 18px;
}

/* Responsive */
@media (max-width: 768px) {
  .changelog-page {
    padding: 1rem;
  }

  .more-card {
    flex-direction: column;
    text-align: center;
  }

  .more-link {
    width: 100%;
    justify-content: center;
  }
}
</style>
