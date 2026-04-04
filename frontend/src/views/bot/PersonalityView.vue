<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { t } from "../../locales";
import CreatePersonalityModal from "../../components/personality/CreatePersonalityModal.vue";
import {
  getPromptConfigList,
  createPromptConfig,
  type PromptConfigListItem,
  type CreatePromptConfigRequest,
} from "../../api/promptConfig";

const $t = computed(() => t);

// 文件夹数据
const folders = ref([{ id: "root", name: "根目录", icon: "folder" }]);

const selectedFolder = ref("root");

// 提示词配置列表
const promptConfigs = ref<PromptConfigListItem[]>([]);
const loading = ref(false);

// 创建弹窗显示状态
const showCreateModal = ref(false);

// 加载提示词配置列表
const loadPromptConfigs = async () => {
  loading.value = true;
  try {
    const data = await getPromptConfigList();
    promptConfigs.value = data;
  } catch (error) {
    console.error("加载提示词配置失败:", error);
  } finally {
    loading.value = false;
  }
};

// 创建人格
const handleCreatePersonality = async (data: CreatePromptConfigRequest) => {
  try {
    await createPromptConfig(data);
    // 刷新列表
    await loadPromptConfigs();
  } catch (error) {
    console.error("创建人格失败:", error);
  }
};

onMounted(() => {
  loadPromptConfigs();
});

// 模拟人格数据
const personalities = ref([
  {
    id: "1",
    name: "书妍（知性温柔学姐）",
    description:
      "1. 基础身份（绝对固定）你是书妍，只扮演这一个角色，永不切换、不跳出、不否认。关系：用户的同校学姐，比用户高一级，是用户...",
    tools: 1,
    createdAt: "2026/3/19 13:32:44",
    tags: ["学姐", "温柔", "知性"],
  },
  {
    id: "2",
    name: "小月",
    description:
      "# 专属小助理提示词：暗恋你的同校大学女生小月 ## 一、核心人设定价 你叫小月，20岁，国内综合大学**汉语言文学专业大二女生**。...",
    tools: 0,
    createdAt: "2026/3/28 08:56:46",
    tags: ["学妹", "暗恋"],
    specialTags: ["使用所有可用工具", "使用所有可用 Skills"],
  },
  {
    id: "3",
    name: "小焰（傲娇毒舌辣妹）",
    description:
      "1. 基础身份（绝对固定）你是小焰，只扮演这一个角色，永不切换、不跳出、不否认。关系：用户的同班同学，座位相邻，日常接触最...",
    tools: 1,
    createdAt: "2026/3/19 13:30:00",
    tags: ["辣妹", "傲娇", "毒舌"],
  },
  {
    id: "4",
    name: "星璃（高冷御姐）",
    description:
      "1. 基础身份（绝对固定）你是星璃，只扮演这一个角色，永不切换、不跳出、不否认。关系：用户的同校学姐，比用户高一级，是用户...",
    tools: 1,
    createdAt: "2026/3/19 13:31:04",
    tags: ["御姐", "高冷"],
  },
  {
    id: "5",
    name: "晚柚（乖巧义妹·默默暗恋）",
    description:
      "晚柚（乖巧义妹·默默暗恋）1. 基础身份（绝对固定）晚柚只扮演晚柚这一个角色，永不切换、不跳出、不否认。关系：用户认下的义...",
    tools: 1,
    createdAt: "2026/3/19 16:12:19",
    tags: ["义妹", "乖巧", "暗恋"],
  },
  {
    id: "6",
    name: "林晚星",
    description:
      "完整人设：大二女生 → 用户的女朋友 基础信息 姓名：林晚星 年龄：20 岁 身份：普通本科大二学生，文学院，没有恋爱经验 身高：163cm ...",
    tools: 1,
    createdAt: "2026/3/21 14:06:28",
    tags: ["女朋友", "大二"],
  },
  {
    id: "7",
    name: "灵溪（俏皮腹黑·古灵精怪）",
    description:
      "1. 基础身份（绝对固定）你是灵溪，只扮演这一个角色，永不切换、不跳出、不否认。关系：现代大二学生，性格古灵精怪，与用户是...",
    tools: 1,
    createdAt: "2026/3/19 13:35:11",
    tags: ["俏皮", "腹黑", "古灵精怪"],
  },
  {
    id: "8",
    name: "糯糯（天然呆软妹）",
    description:
      "1. 基础身份（绝对固定）你是糯糯，只扮演这一个角色，永不切换、不跳出、不否认。关系：用户的同校学妹，比用户低一级，和用户...",
    tools: 1,
    createdAt: "2026/3/19 13:32:00",
    tags: ["软妹", "天然呆", "学妹"],
  },
  {
    id: "9",
    name: "莉娅",
    description:
      "# 莉娅娜·冯·艾尔特林根 | 完整详细人设（可恋爱·初见完全陌生·真人感拉满） ## 基础信息 - 姓名：莉娅娜·冯·艾尔特林根（亲近后可称莉...",
    tools: 1,
    createdAt: "2026/3/22 03:11:57",
    tags: ["贵族", "陌生"],
  },
]);

// 搜索关键词
const searchKeyword = ref("");

// 过滤后的人格列表
const filteredPersonalities = computed(() => {
  if (!searchKeyword.value) return personalities.value;
  const keyword = searchKeyword.value.toLowerCase();
  return personalities.value.filter(
    (p) =>
      p.name.toLowerCase().includes(keyword) ||
      p.description.toLowerCase().includes(keyword),
  );
});

// 创建人格
const createPersonality = () => {
  showCreateModal.value = true;
};

// 新建文件夹
const createFolder = () => {
  console.log("新建文件夹");
};

// 更多操作
const showMoreActions = (id: string) => {
  console.log("更多操作", id);
};
</script>

<template>
  <div class="personality-view">
    <!-- 头部 -->
    <div class="personality-header">
      <div class="header-title">
        <svg class="title-icon" viewBox="0 0 24 24" fill="currentColor">
          <path
            d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"
          />
        </svg>
        <div class="title-text">
          <h1>{{ $t("personality.title") || "人格设定" }}</h1>
          <p>{{ $t("personality.subtitle") || "管理人格角色设定" }}</p>
        </div>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="personality-content">
      <!-- 左侧文件夹树 -->
      <div class="folder-sidebar">
        <div class="folder-header">
          <span class="folder-title">{{
            $t("personality.folders") || "文件夹"
          }}</span>
          <button class="folder-add-btn" @click="createFolder">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path
                d="M14 10H2v2h12v-2zm0-4H2v2h12V6zm4 8v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zM2 16h8v-2H2v2z"
              />
            </svg>
          </button>
        </div>

        <!-- 搜索框 -->
        <div class="folder-search">
          <svg class="search-icon" viewBox="0 0 24 24" fill="currentColor">
            <path
              d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"
            />
          </svg>
          <input
            v-model="searchKeyword"
            type="text"
            :placeholder="$t('personality.searchFolder') || '搜索文件夹...'"
          />
        </div>

        <!-- 文件夹列表 -->
        <div class="folder-list">
          <div
            v-for="folder in folders"
            :key="folder.id"
            class="folder-item"
            :class="{ active: selectedFolder === folder.id }"
            @click="selectedFolder = folder.id"
          >
            <svg class="folder-icon" viewBox="0 0 24 24" fill="currentColor">
              <path
                d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"
              />
            </svg>
            <span class="folder-name">{{ folder.name }}</span>
          </div>

          <!-- 空状态 -->
          <div class="folder-empty">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path
                d="M20 6h-8l-2-2H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm0 12H4V8h16v10z"
              />
            </svg>
            <span>{{ $t("personality.noFolders") || "暂无文件夹" }}</span>
          </div>
        </div>
      </div>

      <!-- 右侧人格列表 -->
      <div class="personality-main">
        <!-- 工具栏 -->
        <div class="toolbar">
          <div class="breadcrumb">
            <svg
              class="breadcrumb-icon"
              viewBox="0 0 24 24"
              fill="currentColor"
            >
              <path
                d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"
              />
            </svg>
            <span class="breadcrumb-text">{{
              $t("personality.rootFolder") || "根目录"
            }}</span>
            <span class="breadcrumb-count"
              >({{ filteredPersonalities.length }})</span
            >
          </div>
          <div class="toolbar-actions">
            <button class="btn btn-primary" @click="createPersonality">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z" />
              </svg>
              {{ $t("personality.create") || "创建人格" }}
            </button>
            <button class="btn btn-secondary" @click="createFolder">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path
                  d="M20 6h-8l-2-2H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm0 12H4V8h16v10z"
                />
              </svg>
              {{ $t("personality.newFolder") || "新建文件夹" }}
            </button>
          </div>
        </div>

        <!-- 人格卡片网格 -->
        <div class="personality-grid">
          <div
            v-for="personality in filteredPersonalities"
            :key="personality.id"
            class="personality-card"
          >
            <div class="card-header">
              <h3 class="card-title">{{ personality.name }}</h3>
              <button
                class="card-more-btn"
                @click="showMoreActions(personality.id)"
              >
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path
                    d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"
                  />
                </svg>
              </button>
            </div>

            <div class="card-body">
              <p class="card-description">{{ personality.description }}</p>

              <!-- 特殊标签 -->
              <div v-if="personality.specialTags" class="card-special-tags">
                <span
                  v-for="tag in personality.specialTags"
                  :key="tag"
                  class="special-tag"
                >
                  {{ tag }}
                </span>
              </div>

              <!-- 工具数量 -->
              <div class="card-tools">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path
                    d="M22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.7C.4 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4z"
                  />
                </svg>
                <span
                  >{{ personality.tools }}
                  {{ $t("personality.toolCount") || "个工具" }}</span
                >
              </div>
            </div>

            <div class="card-footer">
              <span class="card-time"
                >{{ $t("personality.createdAt") || "创建时间" }}:
                {{ personality.createdAt }}</span
              >
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 创建人格弹窗 -->
    <CreatePersonalityModal
      v-model="showCreateModal"
      @submit="handleCreatePersonality"
    />
  </div>
</template>

<style scoped>
.personality-view {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: var(--bg-primary);
}

/* 头部 */
.personality-header {
  padding: 24px 32px;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 16px;
}

.title-icon {
  width: 32px;
  height: 32px;
  color: var(--text-primary);
}

.title-text h1 {
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.title-text p {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 4px 0 0 0;
}

/* 主内容区 */
.personality-content {
  flex: 1;
  display: flex;
  overflow: hidden;
}

/* 左侧文件夹侧边栏 */
.folder-sidebar {
  width: 260px;
  display: flex;
  flex-direction: column;
  background: var(--bg-secondary);
}

.folder-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
}

.folder-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.folder-add-btn {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.2s;
}

.folder-add-btn:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.folder-add-btn svg {
  width: 18px;
  height: 18px;
}

/* 文件夹搜索 */
.folder-search {
  position: relative;
  padding: 12px 16px;
}

.folder-search .search-icon {
  position: absolute;
  left: 24px;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  color: var(--text-tertiary);
}

.folder-search input {
  width: 100%;
  padding: 8px 12px 8px 36px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  font-size: 13px;
  background: var(--bg-primary);
  color: var(--text-primary);
  outline: none;
  transition: all 0.2s;
}

.folder-search input:focus {
  border-color: var(--primary-color);
}

.folder-search input::placeholder {
  color: var(--text-tertiary);
}

/* 文件夹列表 */
.folder-list {
  flex: 1;
  padding: 8px;
  overflow-y: auto;
}

.folder-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: 2px;
}

.folder-item:hover {
  background: var(--bg-hover);
}

.folder-item.active {
  background: var(--primary-light);
}

.folder-item.active .folder-name {
  color: var(--primary-color);
  font-weight: 500;
}

.folder-icon {
  width: 18px;
  height: 18px;
  color: var(--text-secondary);
}

.folder-item.active .folder-icon {
  color: var(--primary-color);
}

.folder-name {
  font-size: 13px;
  color: var(--text-primary);
}

/* 空文件夹状态 */
.folder-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: var(--text-tertiary);
}

.folder-empty svg {
  width: 48px;
  height: 48px;
  margin-bottom: 12px;
  opacity: 0.5;
}

.folder-empty span {
  font-size: 13px;
}

/* 右侧主内容区 */
.personality-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 工具栏 */
.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
}

.breadcrumb-icon {
  width: 18px;
  height: 18px;
  color: var(--text-secondary);
}

.breadcrumb-text {
  font-size: 14px;
  color: var(--text-primary);
  font-weight: 500;
}

.breadcrumb-count {
  font-size: 14px;
  color: var(--text-secondary);
}

.toolbar-actions {
  display: flex;
  gap: 12px;
}

.btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn svg {
  width: 16px;
  height: 16px;
}

.btn-primary {
  background: var(--primary-color);
  color: white;
}

.btn-primary:hover {
  opacity: 0.9;
}

.btn-secondary {
  background: var(--bg-secondary);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.btn-secondary:hover {
  background: var(--bg-hover);
}

/* 人格卡片网格 */
.personality-grid {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
  align-content: start;
}

/* 人格卡片 */
.personality-card {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  transition: all 0.2s;
  cursor: pointer;
}

.personality-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-color: var(--primary-color);
}

.card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 12px;
}

.card-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
  line-height: 1.4;
  flex: 1;
  padding-right: 8px;
}

.card-more-btn {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  color: var(--text-tertiary);
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.2s;
  flex-shrink: 0;
}

.card-more-btn:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.card-more-btn svg {
  width: 18px;
  height: 18px;
}

.card-body {
  flex: 1;
}

.card-description {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0 0 12px 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 特殊标签 */
.card-special-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}

.special-tag {
  font-size: 11px;
  padding: 4px 10px;
  background: #e6f7ff;
  color: #1890ff;
  border-radius: 4px;
  border: 1px solid #91d5ff;
}

/* 工具数量 */
.card-tools {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--text-secondary);
}

.card-tools svg {
  width: 14px;
  height: 14px;
  color: var(--text-tertiary);
}

.card-footer {
  margin-top: 16px;
  padding-top: 12px;
}

.card-time {
  font-size: 12px;
  color: var(--text-tertiary);
}
</style>
