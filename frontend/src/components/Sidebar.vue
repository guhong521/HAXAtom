<script setup>
import { computed, ref } from "vue";
import { t } from "../locales";

const props = defineProps({
  collapsed: Boolean,
  activePage: {
    type: String,
    default: "welcome",
  },
});

const emit = defineEmits(["change-page"]);

const $t = computed(() => t);

// 跟踪菜单展开状态
const expandedMenus = ref({
  config: true,
  plugin: true,
  more: false,
});

// 切换菜单展开状态
const toggleMenu = (menuKey) => {
  if (expandedMenus.value.hasOwnProperty(menuKey)) {
    expandedMenus.value[menuKey] = !expandedMenus.value[menuKey];
  }
};

const menuItems = [
  {
    icon: "welcome",
    label: computed(() => $t.value("bot.sidebar.welcome") || "欢迎"),
    page: "welcome",
  },
  {
    icon: "bot",
    label: computed(() => $t.value("bot.sidebar.bot") || "机器人"),
    page: "bot",
  },
  {
    icon: "model",
    label: computed(() => $t.value("bot.sidebar.models") || "模型提供商"),
    page: "model",
  },
  {
    icon: "config",
    label: computed(() => $t.value("bot.sidebar.config") || "配置文件"),
    expandable: true,
    menuKey: "config",
    children: [
      {
        icon: "config",
        label: computed(
          () => $t.value("bot.sidebar.generalConfig") || "普通配置",
        ),
        page: "generalConfig",
      },
      {
        icon: "system",
        label: computed(
          () => $t.value("bot.sidebar.systemConfig") || "系统配置",
        ),
        page: "systemConfig",
      },
    ],
  },
  {
    icon: "plugin",
    label: computed(() => $t.value("bot.sidebar.plugins") || "插件"),
    expandable: true,
    menuKey: "plugin",
    children: [
      {
        icon: "plugin",
        label: computed(
          () => $t.value("bot.sidebar.haxatomPlugin") || "HAXAtom 插件",
        ),
        page: "haxatom-plugin",
      },
      {
        icon: "market",
        label: computed(
          () => $t.value("bot.sidebar.pluginMarket") || "插件市场",
        ),
        page: "plugin-market",
      },
      {
        icon: "mcp",
        label: "MCP",
        page: "mcp",
      },
      {
        icon: "skills",
        label: "Skills",
        page: "skills",
      },
      {
        icon: "manage",
        label: computed(() => $t.value("bot.sidebar.manage") || "管理行为"),
        page: "manage",
      },
    ],
  },
  {
    icon: "knowledge",
    label: computed(() => $t.value("bot.sidebar.knowledge") || "知识库"),
    page: "knowledge",
  },
  {
    icon: "personality",
    label: computed(() => $t.value("bot.sidebar.personality") || "人格设定"),
    page: "personality",
  },
  {
    icon: "more",
    label: computed(() => $t.value("bot.sidebar.more") || "更多功能"),
    expandable: true,
    menuKey: "more",
    children: [],
  },
];

const bottomItems = [
  {
    icon: "settings",
    label: computed(() => $t.value("settings.settings") || "设置"),
  },
  {
    icon: "changelog",
    label: computed(() => $t.value("sidebar.changelog") || "更新日志"),
  },
  {
    icon: "docs",
    label: computed(() => $t.value("sidebar.docs") || "官方文档"),
  },
  { icon: "faq", label: "FAQ" },
  { icon: "github", label: "GitHub" },
];
</script>

<template>
  <aside class="sidebar" :class="{ collapsed }">
    <!-- 菜单列表 -->
    <nav class="menu-list">
      <div
        v-for="(item, index) in menuItems"
        :key="index"
        class="menu-item-wrapper"
      >
        <div
          class="menu-item"
          :class="{
            active: activePage === item.page,
            expandable: item.expandable,
            expanded: item.menuKey && expandedMenus[item.menuKey],
          }"
          @click="
            item.expandable
              ? toggleMenu(item.menuKey)
              : item.page && emit('change-page', item.page)
          "
        >
          <div class="menu-content">
            <svg class="menu-icon" viewBox="0 0 24 24" fill="currentColor">
              <!-- 欢迎/首页 -->
              <g v-if="item.icon === 'welcome'">
                <path
                  d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"
                />
              </g>
              <!-- 机器人 -->
              <g v-else-if="item.icon === 'bot'">
                <path
                  d="M12 2a2 2 0 0 1 2 2c0 .74-.4 1.38-1 1.72v.78h3c1.1 0 2 .9 2 2v10c0 1.1-.9 2-2 2H6c-1.1 0-2-.9-2-2V8.5c0-1.1.9-2 2-2h3v-.78c-.6-.34-1-.98-1-1.72a2 2 0 0 1 2-2M9 7.5h6v-1H9v1zm-3 3h12v-1H6v1zm0 3h12v-1H6v1zm0 3h12v-1H6v1z"
                />
                <circle cx="9" cy="12" r="1" />
                <circle cx="15" cy="12" r="1" />
              </g>
              <!-- 模型提供商 -->
              <g v-else-if="item.icon === 'model'">
                <path
                  d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"
                />
              </g>
              <!-- 配置 -->
              <g v-else-if="item.icon === 'config'">
                <path
                  d="M12 15.5A3.5 3.5 0 0 1 8.5 12 3.5 3.5 0 0 1 12 8.5a3.5 3.5 0 0 1 3.5 3.5 3.5 3.5 0 0 1-3.5 3.5m7.43-2.53c.04-.32.07-.64.07-.97 0-.33-.03-.66-.07-1l2.11-1.63c.19-.15.24-.42.12-.64l-2-3.46c-.12-.22-.39-.3-.61-.22l-2.49 1c-.52-.4-1.08-.73-1.69-.98l-.38-2.65A.488.488 0 0 0 14 2h-4c-.25 0-.46.18-.5.42l-.38 2.65c-.61.25-1.17.59-1.69.98l-2.49-1c-.23-.09-.49 0-.61.22l-2 3.46c-.13.22-.07.49.12.64l2.11 1.63c-.04.34-.07.67-.07 1 0 .33.03.66.07.97l-2.11 1.63c-.19.15-.24.42-.12.64l2 3.46c.12.22.39.3.61.22l2.49-1.01c.52.4 1.08.73 1.69.98l.38 2.65c.04.24.25.42.5.42h4c.25 0 .46-.18.5-.42l.38-2.65c.61-.25 1.17-.59 1.69-.98l2.49 1.01c.22.08.49 0 .61-.22l2-3.46c.12-.22.07-.49-.12-.64l-2.11-1.63z"
                />
              </g>
              <!-- 插件 -->
              <g v-else-if="item.icon === 'plugin'">
                <path
                  d="M20.5 11H19V7c0-1.1-.9-2-2-2h-4V3.5C13 2.12 11.88 1 10.5 1S8 2.12 8 3.5V5H4c-1.1 0-1.99.9-1.99 2v3.8H3.5c1.49 0 2.7 1.21 2.7 2.7s-1.21 2.7-2.7 2.7H2V20c0 1.1.9 2 2 2h3.8v-1.5c0-1.49 1.21-2.7 2.7-2.7s2.7 1.21 2.7 2.7V22H17c1.1 0 2-.9 2-2v-4h1.5c1.38 0 2.5-1.12 2.5-2.5S21.88 11 20.5 11z"
                />
              </g>
              <!-- MCP -->
              <g v-else-if="item.icon === 'mcp'">
                <path
                  d="M4 6h4v2H4zm0 5h4v2H4zm0 5h4v2H4zm6-10h10v2H10zm0 5h10v2H10zm0 5h10v2H10z"
                />
              </g>
              <!-- Skills -->
              <g v-else-if="item.icon === 'skills'">
                <path d="M7 2v11h3v9l7-12h-4l4-8z" />
              </g>
              <!-- 管理 -->
              <g v-else-if="item.icon === 'manage'">
                <path
                  d="M22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.7C.4 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4z"
                />
              </g>
              <!-- 知识库 -->
              <g v-else-if="item.icon === 'knowledge'">
                <path
                  d="M12 3L1 9l4 2.18v6L12 21l7-3.82v-6l2-1.09V17h2V9L12 3zm6.82 6L12 12.72 5.18 9 12 5.28 18.82 9zM17 15.99l-5 2.73-5-2.73v-3.72L12 15l5-2.73v3.72z"
                />
              </g>
              <!-- 人格设定 -->
              <g v-else-if="item.icon === 'personality'">
                <path
                  d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"
                />
              </g>
              <!-- 更多 -->
              <g v-else-if="item.icon === 'more'">
                <circle cx="6" cy="12" r="2" />
                <circle cx="12" cy="12" r="2" />
                <circle cx="18" cy="12" r="2" />
              </g>
            </svg>
            <span class="menu-label" v-if="!collapsed">{{ item.label }}</span>
            <svg
              v-if="item.expandable && !collapsed"
              class="expand-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path d="M6 9l6 6 6-6" />
            </svg>
          </div>
          <!-- 二级菜单 -->
          <div
            v-show="item.children && expandedMenus[item.menuKey] && !collapsed"
            class="submenu"
            :class="{ 'submenu-collapsed': !expandedMenus[item.menuKey] }"
          >
            <div class="submenu-content">
              <div
                v-for="(child, childIndex) in item.children"
                :key="childIndex"
                class="submenu-item"
                :class="{ active: activePage === child.page }"
                @click.stop="child.page && emit('change-page', child.page)"
              >
                <svg
                  class="submenu-icon"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                >
                  <!-- 配置图标 -->
                  <g v-if="child.icon === 'config'">
                    <path
                      d="M12 15.5A3.5 3.5 0 0 1 8.5 12 3.5 3.5 0 0 1 12 8.5a3.5 3.5 0 0 1 3.5 3.5 3.5 3.5 0 0 1-3.5 3.5m7.43-2.53c.04-.32.07-.64.07-.97 0-.33-.03-.66-.07-1l2.11-1.63c.19-.15.24-.42.12-.64l-2-3.46c-.12-.22-.39-.3-.61-.22l-2.49 1c-.52-.4-1.08-.73-1.69-.98l-.38-2.65A.488.488 0 0 0 14 2h-4c-.25 0-.46.18-.5.42l-.38 2.65c-.61.25-1.17.59-1.69.98l-2.49-1c-.23-.09-.49 0-.61.22l-2 3.46c-.13.22-.07.49.12.64l2.11 1.63c-.04.34-.07.67-.07 1 0 .33.03.66.07.97l-2.11 1.63c-.19.15-.24.42-.12.64l2 3.46c.12.22.39.3.61.22l2.49-1.01c.52.4 1.08.73 1.69.98l.38 2.65c.04.24.25.42.5.42h4c.25 0 .46-.18.5-.42l.38-2.65c.61-.25 1.17-.59 1.69-.98l2.49 1.01c.22.08.49 0 .61-.22l2-3.46c.12-.22.07-.49-.12-.64l-2.11-1.63z"
                    />
                  </g>
                  <!-- 系统图标 -->
                  <g v-else-if="child.icon === 'system'">
                    <path
                      d="M19.14 12.94c.04-.32.06-.64.06-.97 0-.33-.02-.66-.06-.97l2.03-1.58a.49.49 0 0 0 .12-.61l-1.92-3.32a.488.488 0 0 0-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54a.484.484 0 0 0-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96a.488.488 0 0 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.04.32-.06.65-.06.97s.02.66.06.97l-2.03 1.58a.49.49 0 0 0-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z"
                    />
                  </g>
                  <!-- 插件图标 -->
                  <g v-else-if="child.icon === 'plugin'">
                    <path
                      d="M20.5 11H19V7c0-1.1-.9-2-2-2h-4V3.5C13 2.12 11.88 1 10.5 1S8 2.12 8 3.5V5H4c-1.1 0-1.99.9-1.99 2v3.8H3.5c1.49 0 2.7 1.21 2.7 2.7s-1.21 2.7-2.7 2.7H2V20c0 1.1.9 2 2 2h3.8v-1.5c0-1.49 1.21-2.7 2.7-2.7s2.7 1.21 2.7 2.7V22H17c1.1 0 2-.9 2-2v-4h1.5c1.38 0 2.5-1.12 2.5-2.5S21.88 11 20.5 11z"
                    />
                  </g>
                  <!-- 市场图标 -->
                  <g v-else-if="child.icon === 'market'">
                    <path
                      d="M19 6h-2c0-2.76-2.24-5-5-5S7 3.24 7 6H5c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm-7-3c1.66 0 3 1.34 3 3H9c0-1.66 1.34-3 3-3zm7 17H5V8h14v12zm-7-8c-1.66 0-3-1.34-3-3H7c0 2.76 2.24 5 5 5s5-2.24 5-5h-2c0 1.66-1.34 3-3 3z"
                    />
                  </g>
                  <!-- MCP -->
                  <g v-else-if="child.icon === 'mcp'">
                    <path
                      d="M4 6h4v2H4zm0 5h4v2H4zm0 5h4v2H4zm6-10h10v2H10zm0 5h10v2H10zm0 5h10v2H10z"
                    />
                  </g>
                  <!-- Skills -->
                  <g v-else-if="child.icon === 'skills'">
                    <path d="M7 2v11h3v9l7-12h-4l4-8z" />
                  </g>
                  <!-- 管理 -->
                  <g v-else-if="child.icon === 'manage'">
                    <path
                      d="M22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.7C.4 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4z"
                    />
                  </g>
                </svg>
                <span class="submenu-label">{{ child.label }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- 底部菜单 -->
    <div class="bottom-menu">
      <div v-for="(item, index) in bottomItems" :key="index" class="menu-item">
        <div class="menu-content">
          <svg class="menu-icon" viewBox="0 0 24 24" fill="currentColor">
            <!-- 设置 -->
            <g v-if="item.icon === 'settings'">
              <path
                d="M19.14 12.94c.04-.32.06-.64.06-.97 0-.33-.02-.66-.06-.97l2.03-1.58a.49.49 0 0 0 .12-.61l-1.92-3.32a.488.488 0 0 0-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54a.484.484 0 0 0-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96a.488.488 0 0 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.04.32-.06.65-.06.97s.02.66.06.97l-2.03 1.58a.49.49 0 0 0-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z"
              />
            </g>
            <!-- 更新日志 -->
            <g v-else-if="item.icon === 'changelog'">
              <path
                d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"
              />
            </g>
            <!-- 文档 -->
            <g v-else-if="item.icon === 'docs'">
              <path
                d="M12 3L1 9l4 2.18v6L12 21l7-3.82v-6l2-1.09V17h2V9L12 3zm6.82 6L12 12.72 5.18 9 12 5.28 18.82 9zM17 15.99l-5 2.73-5-2.73v-3.72L12 15l5-2.73v3.72z"
              />
            </g>
            <!-- FAQ -->
            <g v-else-if="item.icon === 'faq'">
              <path
                d="M21 6h-2v9H6v2c0 .55.45 1 1 1h11l4 4V7c0-.55-.45-1-1-1zm-4 6V3c0-.55-.45-1-1-1H3c-.55 0-1 .45-1 1v14l4-4h10c.55 0 1-.45 1-1z"
              />
            </g>
            <!-- GitHub -->
            <g v-else-if="item.icon === 'github'">
              <path
                d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2z"
              />
            </g>
          </svg>
          <span class="menu-label" v-if="!collapsed">{{ item.label }}</span>
        </div>
      </div>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 240px;
  height: 100%;
  background: transparent;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
}

.sidebar.collapsed {
  width: 64px;
}

.menu-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.menu-item {
  margin-bottom: 4px;
}

.menu-content {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
  user-select: none;
  -webkit-user-select: none;
}

.menu-item:hover .menu-content {
  background: var(--bg-hover);
}

.menu-item:active .menu-content {
  transform: scale(0.96);
  transition: transform 0.1s ease;
}

/* 点击二级菜单时，一级菜单不触发active效果 */
.menu-item:has(.submenu-item:active) .menu-content {
  transform: none !important;
}

.menu-item.active .menu-content {
  background: var(--primary-light);
  color: var(--primary-color);
}

.menu-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  color: var(--text-secondary);
}

.menu-item.active .menu-icon {
  color: var(--primary-color);
}

.menu-label {
  flex: 1;
  font-size: 14px;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.menu-item.active .menu-label {
  color: var(--primary-color);
}

.expand-icon {
  width: 16px;
  height: 16px;
  color: var(--text-tertiary);
  transition: transform 0.2s;
}

.menu-item.expanded .expand-icon {
  transform: rotate(180deg);
}

/* 二级菜单样式 */
.submenu {
  display: grid;
  grid-template-rows: 1fr;
  transition: grid-template-rows 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  padding: 4px 8px;
}

.submenu-collapsed {
  grid-template-rows: 0fr;
}

.submenu-content {
  overflow: hidden;
}

.submenu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px 8px 40px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: 2px;
  user-select: none;
  -webkit-user-select: none;
}

.submenu-item:hover {
  background: var(--bg-hover);
}

.submenu-item:active {
  transform: scale(0.96);
  transition: transform 0.1s ease;
}

.submenu-item.active {
  background: var(--primary-light);
}

.submenu-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  color: var(--text-secondary);
}

.submenu-item.active .submenu-icon {
  color: var(--primary-color);
}

.submenu-label {
  flex: 1;
  font-size: 13px;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.submenu-item.active .submenu-label {
  color: var(--primary-color);
}

.bottom-menu {
  padding: 8px;
}

/* 折叠状态样式 */
.sidebar.collapsed .menu-content {
  justify-content: center;
  padding: 12px;
}

.sidebar.collapsed .menu-icon {
  width: 24px;
  height: 24px;
}
</style>
