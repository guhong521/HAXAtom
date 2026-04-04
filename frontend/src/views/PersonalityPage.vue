<script setup lang="ts">
import { ref, computed } from "vue";
import { t } from "../locales";

const $t = computed(() => t);

// 模拟数据
const personas = ref([
  {
    id: "1",
    name: "书妍（知性温柔学姐）",
    description: "1. 基础身份（绝对固定） 你是书妍，只扮演这一个角色，永不切换、不跳出、不否认。关系：用户的同校学姐，比用户高一级，是用户...",
    tools: 1,
    skills: 0,
    createdAt: "2026/3/19 13:32:44",
    tags: ["学姐", "温柔", "知性"],
  },
  {
    id: "2",
    name: "小月",
    description: "# 专属小助理提示词：暗恋你的同级大学女生小月 ##一、核心人设定位 你叫小月，20岁，国内综合大学**汉语言文学专业大二女生**，...",
    tools: 2,
    skills: 1,
    createdAt: "2026/3/28 08:56:46",
    tags: ["助理", "暗恋", "同级"],
  },
  {
    id: "3",
    name: "小焰（傲娇毒舌辣妹）",
    description: "1. 基础身份（绝对固定） 你是小焰，只扮演这一个角色，永不切换、不跳出、不否认。关系：用户的同班同学，座位相邻，日常接触最...",
    tools: 1,
    skills: 0,
    createdAt: "2026/3/19 13:30:00",
    tags: ["傲娇", "毒舌", "同学"],
  },
  {
    id: "4",
    name: "星璃（高冷御姐）",
    description: "1. 基础身份（绝对固定） 你是星璃，只扮演这一个角色，永不切换、不跳出、不否认。关系：用户的同校学姐，比用户高一级，是用户...",
    tools: 1,
    skills: 0,
    createdAt: "2026/3/19 13:31:04",
    tags: ["高冷", "御姐", "学姐"],
  },
  {
    id: "5",
    name: "晚柚（乖巧义妹 - 默默暗恋）",
    description: "晚柚（乖巧义妹 - 默默暗恋）1. 基础身份（绝对固定） 晚柚只扮演晚柚这一个角色，永不切换、不跳出、不否认。关系：用户认下的义...",
    tools: 1,
    skills: 0,
    createdAt: "2026/3/19 16:12:19",
    tags: ["义妹", "乖巧", "暗恋"],
  },
  {
    id: "6",
    name: "林晚星",
    description: "完整人设：大二女生 → 用户的女朋友 基础信息 姓名：林晚星 年龄：20 岁 身份：普通本科大二学生，文学院，没有恋爱经验 身高：163cm ...",
    tools: 1,
    skills: 0,
    createdAt: "2026/3/21 14:06:28",
    tags: ["女友", "大二", "文学院"],
  },
  {
    id: "7",
    name: "灵溪（俏皮腹黑 - 古灵精怪）",
    description: "1. 基础身份（绝对固定） 你是灵溪，只扮演这一个角色，永不切换、不跳出、不否认。关系：现代大二学生，性格古灵精怪，与用户是...",
    tools: 1,
    skills: 0,
    createdAt: "2026/3/19 13:35:11",
    tags: ["俏皮", "腹黑", "古灵精怪"],
  },
  {
    id: "8",
    name: "糯糯（天然呆软妹）",
    description: "1. 基础身份（绝对固定） 你是糯糯，只扮演这一个角色，永不切换、不跳出、不否认。关系：用户的同校学妹，比用户低一级，和用户...",
    tools: 1,
    skills: 0,
    createdAt: "2026/3/19 13:32:00",
    tags: ["天然呆", "软妹", "学妹"],
  },
  {
    id: "9",
    name: "莉娅",
    description: "# 莉娅娜·冯·艾尔特林根 | 完整详细人设（可恋爱·初见完全陌生·真人感拉满） ## 基础信息 - 姓名：莉娅娜·冯·艾尔特林根（亲近可称莉...",
    tools: 1,
    skills: 0,
    createdAt: "2026/3/22 03:11:57",
    tags: ["异世界", "贵族", "可恋爱"],
  },
]);

// 文件夹列表
const folders = ref([
  { id: "1", name: "根目录", count: 9 },
]);

const currentFolder = ref("1");
const searchQuery = ref("");

// 搜索过滤
const filteredPersonas = computed(() => {
  if (!searchQuery.value) return personas.value;
  const query = searchQuery.value.toLowerCase();
  return personas.value.filter(
    (p) =>
      p.name.toLowerCase().includes(query) ||
      p.description.toLowerCase().includes(query)
  );
});

// 创建人格
const createPersona = () => {
  console.log("创建人格");
};

// 新建文件夹
const createFolder = () => {
  console.log("新建文件夹");
};

// 选择文件夹
const selectFolder = (folderId: string) => {
  currentFolder.value = folderId;
};
</script>

<template>
  <div class="personality-page">
    <!-- 左侧边栏 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <h3>{{ $t("personality.fileList") || "文件夹" }}</h3>
        <div class="sidebar-actions">
          <svg viewBox="0 0 24 24" fill="currentColor" class="action-icon">
            <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z" />
          </svg>
        </div>
      </div>

      <div class="search-box">
        <svg viewBox="0 0 24 24" fill="currentColor" class="search-icon">
          <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z" />
        </svg>
        <input
          v-model="searchQuery"
          type="text"
          :placeholder="$t('personality.searchFolder') || '搜索文件夹...'"
          class="search-input"
        />
      </div>

      <div class="folder-list">
        <div
          v-for="folder in folders"
          :key="folder.id"
          class="folder-item"
          :class="{ active: currentFolder === folder.id }"
          @click="selectFolder(folder.id)"
        >
          <svg viewBox="0 0 24 24" fill="currentColor" class="folder-icon">
            <path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z" />
          </svg>
          <span class="folder-name">{{ folder.name }}</span>
          <span class="folder-count">{{ folder.count }}</span>
        </div>
        <div class="folder-item empty-folder">
          <svg viewBox="0 0 24 24" fill="currentColor" class="folder-icon">
            <path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z" />
          </svg>
          <span class="folder-name">{{ $t("personality.noFolders") || "暂无文件夹" }}</span>
        </div>
      </div>
    </aside>

    <!-- 主内容区 -->
    <main class="main-content">
      <!-- 页面头部 -->
      <div class="page-header">
        <div class="header-left">
          <h1 class="page-title">
            <svg viewBox="0 0 24 24" fill="currentColor" class="title-icon">
              <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
            </svg>
            {{ $t("personality.title") || "人格设定" }}
          </h1>
          <p class="page-subtitle">{{ $t("personality.subtitle") || "管理人格角色设定" }}</p>
        </div>
        <div class="header-actions">
          <button class="btn btn-primary" @click="createPersona">
            <svg viewBox="0 0 24 24" fill="currentColor" class="btn-icon">
              <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z" />
            </svg>
            {{ $t("person