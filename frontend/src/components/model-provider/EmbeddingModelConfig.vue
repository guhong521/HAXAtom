<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { t } from "../../locales";
import {
  getModelConfigs,
  createModelConfig,
  deleteModelConfig,
} from "../../api/modelConfig";
import type { ModelConfigListItem } from "../../api/modelConfig";

const $t = t;

// 提供商数据
const providers = ref<
  {
    id: string;
    name: string;
    modelNames: string[];
    url: string;
    apiBase?: string;
    apiKey?: string;
    status: "active" | "inactive";
  }[]
>([]);
const loading = ref(false);

// 选中的提供商
const selectedProvider = ref<{
  id: string;
  name: string;
  modelNames: string[];
  url: string;
  apiBase?: string;
  apiKey?: string;
  status: "active" | "inactive";
} | null>(null);

// 是否显示二级菜单
const showSubMenu = ref(false);
const subMenuRef = ref<HTMLElement | null>(null);
const addBtnRef = ref<HTMLElement | null>(null);

// 是否显示配置表单
const showConfigForm = ref(false);

// 当前正在配置的提供商
const configuringProvider = ref<{
  id: string;
  name: string;
  icon: string;
} | null>(null);

// 表单数据
const formData = ref({
  id: "",
  apiKey: "",
  apiBase: "",
});

// 加载模型配置列表
const loadModelConfigs = async () => {
  loading.value = true;
  try {
    const response = await getModelConfigs("embedding");
    if (response.data) {
      providers.value = response.data.map((item: ModelConfigListItem) => ({
        id: item.model_id,
        name: Array.isArray(item.model_name)
          ? item.model_name[0]
          : item.model_name,
        modelNames: item.model_name as string[],
        url: item.provider,
        apiBase: item.api_base,
        apiKey: item.api_key,
        status: item.is_active ? "active" : "inactive",
      }));
    }
  } catch (error) {
    console.error("加载嵌入模型配置失败:", error);
  } finally {
    loading.value = false;
  }
};

// 点击外部关闭二级菜单
const handleClickOutside = (event: MouseEvent) => {
  if (
    showSubMenu.value &&
    subMenuRef.value &&
    !subMenuRef.value.contains(event.target as Node) &&
    addBtnRef.value &&
    !addBtnRef.value.contains(event.target as Node)
  ) {
    showSubMenu.value = false;
  }
};

// 组件挂载时加载数据
onMounted(() => {
  loadModelConfigs();
  document.addEventListener("click", handleClickOutside);
});

// 组件卸载时移除事件监听
onUnmounted(() => {
  document.removeEventListener("click", handleClickOutside);
});

// 嵌入模型提供商列表
const availableProviders = ref([
  {
    id: "openai-embedding",
    name: "OpenAI Embedding",
    icon: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M22.282 9.821a5.985 5.985 0 0 0-.516-4.91 6.046 6.046 0 0 0-6.51-2.9A6.065 6.065 0 0 0 4.981 4.18a5.985 5.985 0 0 0-3.998 2.9 6.046 6.046 0 0 0 .743 7.097 5.98 5.98 0 0 0 .51 4.911 6.051 6.051 0 0 0 6.515 2.9A5.985 5.985 0 0 0 13.26 24a6.056 6.056 0 0 0 5.772-4.206 5.99 5.99 0 0 0 3.997-2.9 6.056 6.056 0 0 0-.747-7.073zM13.26 22.43a4.476 4.476 0 0 1-2.876-1.04l.141-.081 4.779-2.758a.795.795 0 0 0 .392-.681v-6.737l2.02 1.168a.071.071 0 0 1 .038.052v5.583a4.504 4.504 0 0 1-4.494 4.494zM3.6 18.304a4.47 4.47 0 0 1-.535-3.014l.142.085 4.783 2.759a.771.771 0 0 0 .78 0l5.843-3.369v2.332a.08.08 0 0 1-.033.062L9.74 19.95a4.5 4.5 0 0 1-6.14-1.646zM2.34 7.896a4.485 4.485 0 0 1 2.366-1.973V11.6a.766.766 0 0 0 .388.676l5.815 3.355-2.02 1.168a.076.076 0 0 1-.071 0l-4.83-2.786A4.504 4.504 0 0 1 2.34 7.896zm16.597 3.855l-5.833-3.387L15.119 7.2a.076.076 0 0 1 .071 0l4.83 2.791a4.494 4.494 0 0 1-.676 8.105v-5.678a.79.79 0 0 0-.407-.667zm2.01-3.023l-.141-.085-4.774-2.782a.776.776 0 0 0-.785 0L9.409 9.23V6.897a.066.066 0 0 1 .028-.061l4.83-2.787a4.5 4.5 0 0 1 6.68 4.66zm-12.64 4.135l-2.02-1.164a.08.08 0 0 1-.038-.057V6.075a4.5 4.5 0 0 1 7.375-3.453l-.142.08L8.704 5.46a.795.795 0 0 0-.393.681zm1.097-2.365l2.602-1.5 2.607 1.5v2.999l-2.597 1.5-2.607-1.5z"/></svg>`,
  },
  {
    id: "zhipu-embedding",
    name: "智谱 Embedding",
    icon: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>`,
  },
  {
    id: "ollama-embedding",
    name: "Ollama Embedding",
    icon: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/></svg>`,
  },
]);

// 选择提供商
const selectProvider = (provider: (typeof providers.value)[0]) => {
  selectedProvider.value = provider;
  showConfigForm.value = false;
  configuringProvider.value = null;
  showSubMenu.value = false;
};

// 打开二级菜单
const addProvider = () => {
  showSubMenu.value = !showSubMenu.value;
};

// 选择模型提供商
const selectModelProvider = (
  provider: (typeof availableProviders.value)[0],
) => {
  configuringProvider.value = provider;
  formData.value = {
    id: provider.id,
    apiKey: "",
    apiBase: getDefaultApiBase(provider.id),
  };
  showSubMenu.value = false;
  showConfigForm.value = true;
  selectedProvider.value = null;
};

// 获取默认 API Base
const getDefaultApiBase = (providerId: string) => {
  const defaults: Record<string, string> = {
    "openai-embedding": "https://api.openai.com/v1",
    "zhipu-embedding": "https://open.bigmodel.cn/api/paas/v4",
    "ollama-embedding": "http://localhost:11434",
  };
  return defaults[providerId] || "";
};

// 保存配置
const saveConfig = async () => {
  try {
    const configData = {
      model_id: formData.value.id,
      model_name: [configuringProvider.value?.name.toLowerCase() || ""],
      model_type: "embedding" as const,
      provider: configuringProvider.value?.id || "",
      api_base: formData.value.apiBase,
      api_key: formData.value.apiKey,
      is_active: true,
    };

    await createModelConfig(configData);
    await loadModelConfigs();

    showConfigForm.value = false;
    configuringProvider.value = null;
  } catch (error) {
    console.error("保存配置失败:", error);
  }
};

// 取消配置
const cancelConfig = () => {
  showConfigForm.value = false;
  configuringProvider.value = null;
};

// 删除提供商
const deleteProvider = async (providerId: string) => {
  try {
    await deleteModelConfig(providerId);
    await loadModelConfigs();
    if (selectedProvider.value?.id === providerId) {
      selectedProvider.value = null;
    }
  } catch (error) {
    console.error("删除配置失败:", error);
  }
};
</script>

<template>
  <div class="embedding-model-config">
    <!-- 左侧提供商列表 -->
    <div class="provider-list-section">
      <div class="section-header">
        <h3 class="section-title">
          {{ $t("provider.providers") || "提供商源" }}
        </h3>
        <div class="add-btn-wrapper">
          <button ref="addBtnRef" class="add-btn" @click="addProvider">
            <svg class="add-icon" viewBox="0 0 24 24" fill="currentColor">
              <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z" />
            </svg>
            <span>{{ $t("provider.add") || "新增" }}</span>
          </button>
          <!-- 二级菜单 -->
          <div v-if="showSubMenu" ref="subMenuRef" class="sub-menu">
            <div
              v-for="provider in availableProviders"
              :key="provider.id"
              class="sub-menu-item"
              @click="selectModelProvider(provider)"
            >
              <div class="provider-icon-svg" v-html="provider.icon"></div>
              <span class="provider-name-text">{{ provider.name }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="loading-state">
        <svg class="loading-icon" viewBox="0 0 24 24" fill="currentColor">
          <path
            d="M12 4V1L8 5l4 4V6c3.31 0 6 2.69 6 6 0 1.01-.25 1.97-.7 2.8l1.46 1.46C19.54 15.03 20 13.57 20 12c0-4.42-3.58-8-8-8zm0 14c-3.31 0-6-2.69-6-6 0-1.01.25-1.97.7-2.8L5.24 7.74C4.46 8.97 4 10.43 4 12c0 4.42 3.58 8 8 8v3l4-4-4-4v3z"
          />
        </svg>
        <span>{{ $t("provider.loading") }}</span>
      </div>

      <!-- 空状态 -->
      <div v-else-if="providers.length === 0" class="empty-list-state">
        <svg viewBox="0 0 24 24" fill="currentColor">
          <path
            d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"
          />
        </svg>
        <span>{{ $t("provider.noProviders") }}</span>
      </div>

      <div v-else class="provider-list">
        <div
          v-for="provider in providers"
          :key="provider.id"
          class="provider-item"
          :class="{ active: selectedProvider?.id === provider.id }"
          @click="selectProvider(provider)"
        >
          <div class="provider-icon">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path
                d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"
              />
            </svg>
          </div>
          <div class="provider-info">
            <div class="provider-name">{{ provider.name }}</div>
            <div class="provider-url">{{ provider.url }}</div>
          </div>
          <div class="provider-actions">
            <div
              v-if="provider.status === 'active'"
              class="status-dot active"
            ></div>
            <button
              class="delete-btn"
              @click.stop="deleteProvider(provider.id)"
            >
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path
                  d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 右侧详情区域 -->
    <div class="provider-detail">
      <!-- 空状态 -->
      <div v-if="!selectedProvider && !showConfigForm" class="empty-state">
        <svg class="empty-icon" viewBox="0 0 24 24" fill="currentColor">
          <path
            d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"
          />
        </svg>
        <p class="empty-text">
          {{ $t("provider.selectProvider") || "请选择一个提供商源" }}
        </p>
      </div>

      <!-- 提供商详情 -->
      <div
        v-else-if="selectedProvider && !showConfigForm"
        class="detail-content"
      >
        <h2>{{ selectedProvider.name }}</h2>
        <p>Provider: {{ selectedProvider.url }}</p>
        <p>
          API Base: {{ selectedProvider.apiBase || $t("provider.apiBaseHint") }}
        </p>
        <p>Models: {{ selectedProvider.modelNames?.join(", ") }}</p>
        <p>
          Status:
          {{ selectedProvider.status === "active" ? "Active" : "Inactive" }}
        </p>
      </div>

      <!-- 配置表单 -->
      <div v-else-if="showConfigForm" class="config-form">
        <div class="form-header">
          <h2>{{ configuringProvider?.name }}</h2>
          <button class="save-btn" @click="saveConfig">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z" />
            </svg>
            <span>{{ $t("provider.saveConfig") }}</span>
          </button>
        </div>

        <div class="form-body">
          <div class="form-item">
            <label>{{ $t("provider.id") }}</label>
            <div class="form-input-wrapper">
              <input
                v-model="formData.id"
                type="text"
                class="form-input"
                :placeholder="$t('provider.id')"
              />
            </div>
            <span class="form-hint">{{ $t("provider.id") }}</span>
          </div>

          <div class="form-item">
            <label>{{ $t("provider.apiKey") }}</label>
            <div class="form-input-wrapper">
              <input
                v-model="formData.apiKey"
                type="password"
                class="form-input"
                placeholder="API 密钥"
              />
            </div>
            <span class="form-hint">API 密钥</span>
          </div>

          <div class="form-item">
            <label>{{ $t("provider.apiBase") }}</label>
            <div class="form-input-wrapper">
              <input
                v-model="formData.apiBase"
                type="text"
                class="form-input"
                :placeholder="$t('provider.apiBaseHint')"
              />
            </div>
            <span class="form-hint">{{ $t("provider.apiBaseHint") }}</span>
          </div>

          <div class="form-actions">
            <button class="cancel-btn" @click="cancelConfig">
              {{ $t("provider.cancel") }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.embedding-model-config {
  display: flex;
  gap: 24px;
  height: 100%;
}

/* 左侧提供商列表 */
.provider-list-section {
  width: 320px;
  display: flex;
  flex-direction: column;
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 16px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.add-btn-wrapper {
  position: relative;
}

.add-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-btn:hover {
  opacity: 0.9;
}

.add-icon {
  width: 16px;
  height: 16px;
}

/* 二级菜单 */
.sub-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  min-width: 200px;
  z-index: 100;
}

.sub-menu-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.sub-menu-item:hover {
  background: var(--bg-hover);
}

.sub-menu-item:first-child {
  border-radius: 8px 8px 0 0;
}

.sub-menu-item:last-child {
  border-radius: 0 0 8px 8px;
}

.provider-icon-svg {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.provider-icon-svg svg {
  width: 100%;
  height: 100%;
}

.provider-name-text {
  font-size: 14px;
  color: var(--text-primary);
}

/* 加载状态 */
.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 24px;
  color: var(--text-secondary);
  font-size: 14px;
}

.loading-icon {
  width: 20px;
  height: 20px;
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

/* 空状态 */
.empty-list-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 32px 24px;
  color: var(--text-tertiary);
  text-align: center;
}

.empty-list-state svg {
  width: 40px;
  height: 40px;
  opacity: 0.5;
}

.empty-list-state span {
  font-size: 13px;
}

.provider-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  overflow-y: auto;
}

.provider-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.provider-item:hover {
  background: var(--bg-hover);
}

.provider-item.active {
  background: var(--primary-light);
  border-color: var(--primary-color);
}

.provider-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: var(--bg-tertiary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
}

.provider-icon svg {
  width: 20px;
  height: 20px;
}

.provider-info {
  flex: 1;
  min-width: 0;
}

.provider-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 2px;
}

.provider-url {
  font-size: 12px;
  color: var(--text-tertiary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.provider-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--text-tertiary);
}

.status-dot.active {
  background: #22c55e;
}

.delete-btn {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  color: var(--text-tertiary);
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.delete-btn:hover {
  background: var(--bg-hover);
  color: #ef4444;
}

.delete-btn svg {
  width: 16px;
  height: 16px;
}

/* 右侧详情区域 */
.provider-detail {
  flex: 1;
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 24px;
  overflow-y: auto;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--text-tertiary);
}

.empty-icon {
  width: 64px;
  height: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-text {
  font-size: 14px;
}

.detail-content h2 {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 16px 0;
}

.detail-content p {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 8px 0;
}

/* 配置表单 */
.config-form {
  height: 100%;
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.form-header h2 {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.save-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: #22c55e;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.save-btn:hover {
  opacity: 0.9;
}

.save-btn svg {
  width: 18px;
  height: 18px;
}

.form-body {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-item label {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.form-input-wrapper {
  display: flex;
  gap: 8px;
}

.form-input {
  flex: 1;
  padding: 10px 12px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 14px;
  outline: none;
  transition: all 0.2s ease;
}

.form-input:focus {
  border-color: var(--primary-color);
}

.form-input::placeholder {
  color: var(--text-tertiary);
}

.form-hint {
  font-size: 12px;
  color: var(--text-tertiary);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

.cancel-btn {
  padding: 8px 16px;
  background: transparent;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  color: var(--text-secondary);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cancel-btn:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}
</style>
