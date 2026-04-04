<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { t } from "../../locales";
import {
  getPresets,
  getPreset,
  createPreset,
  updatePreset,
  deletePreset,
  clonePreset,
  type PresetDetail,
  type PresetListItem,
  type PresetCreate,
  type ModelInfo,
  type PromptInfo,
  type MemoryInfo,
  type KnowledgeBaseInfo,
  type PluginInfo,
} from "../../api/preset";
import {
  getModelConfigs,
  type ModelConfigListItem,
} from "../../api/modelConfig";

const $t = computed(() => t);

// 预设列表
const presets = ref<PresetListItem[]>([]);
const loading = ref(false);
const selectedPreset = ref<PresetDetail | null>(null);

// 模型列表
const models = ref<ModelConfigListItem[]>([]);

// 表单数据
const formData = ref<Partial<PresetCreate>>({
  preset_id: "",
  preset_name: "",
  description: "",
  selected_model: "",
  selected_prompt: "",
  selected_memory: "",
  selected_plugins: [],
  selected_knowledge_bases: [],
  is_default: false,
  is_active: true,
});

// 编辑模式
const isEditing = ref(false);
const showForm = ref(false);

// 选择器显示状态
const showModelSelector = ref(false);
const showPromptSelector = ref(false);
const showMemorySelector = ref(false);
const showKBSelector = ref(false);
const showPluginSelector = ref(false);

// 其他资源列表（用于下拉选择）
const prompts = ref<{ prompt_id: string; prompt_name: string }[]>([]);
const memories = ref<{ memory_id: string; memory_name: string }[]>([]);

// 确认对话框
const showConfirmDialog = ref(false);
const confirmText = ref("");
const confirmAction = ref<() => void>(() => {});

// Toast 提示
const toastMessage = ref("");
const showToastFlag = ref(false);
let toastTimer: number | null = null;

// 显示提示
const showToast = (message: string, type: "success" | "error" = "success") => {
  toastMessage.value = message;
  showToastFlag.value = true;
  if (toastTimer) clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => {
    showToastFlag.value = false;
  }, 3000);
};

// 加载预设列表
const loadPresets = async () => {
  loading.value = true;
  try {
    const res = await getPresets();
    // 后端返回 ResponseBase 结构，数据在 res.data 中
    presets.value = (res as any).data || [];
  } catch (error) {
    console.error("加载预设列表失败:", error);
    showToast($t.value("config.loadFailed") || "加载失败", "error");
  } finally {
    loading.value = false;
  }
};

// 加载模型列表
const loadModels = async () => {
  try {
    const res = await getModelConfigs("chat");
    // 后端返回 ResponseBase 结构，数据在 res.data 中
    models.value = (res as any).data || [];
  } catch (error) {
    console.error("加载模型列表失败:", error);
  }
};

// 选择预设
const selectPreset = async (preset: PresetListItem) => {
  try {
    const res = await getPreset(preset.preset_id);
    selectedPreset.value = (res as any).data;
    isEditing.value = true;
    showForm.value = true;
    // 填充表单
    formData.value = {
      preset_id: selectedPreset.value.preset_id,
      preset_name: selectedPreset.value.preset_name,
      description: selectedPreset.value.description || "",
      selected_model: selectedPreset.value.selected_model,
      selected_prompt: selectedPreset.value.selected_prompt || "",
      selected_memory: selectedPreset.value.selected_memory || "",
      selected_plugins: selectedPreset.value.selected_plugins || [],
      selected_knowledge_bases:
        selectedPreset.value.selected_knowledge_bases || [],
      is_default: selectedPreset.value.is_default,
      is_active: selectedPreset.value.is_active,
    };
  } catch (error) {
    console.error("加载预设详情失败:", error);
    showToast($t.value("config.loadDetailFailed") || "加载详情失败", "error");
  }
};

// 新增预设
const addPreset = () => {
  isEditing.value = false;
  showForm.value = true;
  selectedPreset.value = null;
  formData.value = {
    preset_id: "",
    preset_name: "",
    description: "",
    selected_model: "",
    selected_prompt: "",
    selected_memory: "",
    selected_plugins: [],
    selected_knowledge_bases: [],
    is_default: false,
    is_active: true,
  };
};

// 保存预设
const savePreset = async () => {
  if (!formData.value.preset_id || !formData.value.preset_name) {
    showToast($t.value("config.requiredFields") || "请填写必填项", "error");
    return;
  }

  try {
    if (isEditing.value && selectedPreset.value) {
      await updatePreset(selectedPreset.value.preset_id, formData.value);
      showToast($t.value("config.updateSuccess") || "更新成功");
    } else {
      await createPreset(formData.value as PresetCreate);
      showToast($t.value("config.createSuccess") || "创建成功");
    }
    await loadPresets();
    showForm.value = false;
  } catch (error) {
    console.error("保存预设失败:", error);
    showToast($t.value("config.saveFailed") || "保存失败", "error");
  }
};

// 删除预设
const deletePresetItem = (presetId: string) => {
  confirmText.value =
    $t.value("config.confirmDelete") || "确定要删除这个预设吗？";
  confirmAction.value = async () => {
    try {
      await deletePreset(presetId);
      showToast($t.value("config.deleteSuccess") || "删除成功");
      await loadPresets();
      if (selectedPreset.value?.preset_id === presetId) {
        selectedPreset.value = null;
        showForm.value = false;
      }
    } catch (error) {
      console.error("删除预设失败:", error);
      showToast($t.value("config.deleteFailed") || "删除失败", "error");
    }
    showConfirmDialog.value = false;
  };
  showConfirmDialog.value = true;
};

// 克隆预设
const clonePresetItem = async (preset: PresetListItem) => {
  const newId = `${preset.preset_id}_copy_${Date.now()}`;
  try {
    await clonePreset(preset.preset_id, {
      new_preset_id: newId,
      new_preset_name: `${preset.preset_name} (Copy)`,
    });
    showToast($t.value("config.cloneSuccess") || "克隆成功");
    await loadPresets();
  } catch (error) {
    console.error("克隆预设失败:", error);
    showToast($t.value("config.cloneFailed") || "克隆失败", "error");
  }
};

// 设置默认预设
const setDefault = async (presetId: string) => {
  try {
    await updatePreset(presetId, { is_default: true });
    showToast($t.value("config.setDefaultSuccess") || "已设为默认");
    await loadPresets();
  } catch (error) {
    console.error("设置默认预设失败:", error);
    showToast($t.value("config.setDefaultFailed") || "设置默认失败", "error");
  }
};

// 取消编辑
const cancelEdit = () => {
  showForm.value = false;
  selectedPreset.value = null;
};

// 确认对话框操作
const handleConfirm = () => {
  confirmAction.value();
};

const handleCancel = () => {
  showConfirmDialog.value = false;
};

// 初始化
onMounted(() => {
  loadPresets();
  loadModels();
});
</script>

<template>
  <div class="general-config">
    <!-- 左侧预设列表 -->
    <div class="preset-list-section">
      <div class="section-header">
        <h3 class="section-title">
          {{ $t("config.presetList") || "预设方案" }}
        </h3>
        <button class="add-btn" @click="addPreset">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z" />
          </svg>
          {{ $t("config.add") || "新增" }}
        </button>
      </div>

      <div v-if="loading" class="loading">{{ $t("common.loading") }}</div>

      <div v-else-if="presets.length === 0" class="empty-state">
        {{ $t("config.noPresets") || "暂无预设方案" }}
      </div>

      <div v-else class="preset-list">
        <div
          v-for="preset in presets"
          :key="preset.preset_id"
          class="preset-item"
          :class="{ active: selectedPreset?.preset_id === preset.preset_id }"
          @click="selectPreset(preset)"
        >
          <div class="preset-info">
            <div class="preset-name">
              {{ preset.preset_name }}
              <span v-if="preset.is_default" class="default-badge">
                {{ $t("config.default") || "默认" }}
              </span>
            </div>
            <div class="preset-id">{{ preset.preset_id }}</div>
            <!-- 资源摘要信息 -->
            <div class="preset-resources">
              <span v-if="preset.model_name" class="resource-tag model-tag">
                {{ preset.model_name }}
              </span>
              <span v-if="preset.prompt_name" class="resource-tag prompt-tag">
                {{ preset.prompt_name }}
              </span>
              <span v-if="preset.knowledge_base_names?.length" class="resource-tag kb-tag">
                {{ preset.knowledge_base_names.length }} 知识库
              </span>
              <span v-if="preset.plugin_names?.length" class="resource-tag plugin-tag">
                {{ preset.plugin_names.length }} 插件
              </span>
            </div>
          </div>
          <div class="preset-actions">
            <div v-if="preset.is_active" class="status-dot active"></div>
            <button
              class="action-btn"
              @click.stop="clonePresetItem(preset)"
              :title="$t('config.clone') || '克隆'"
            >
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path
                  d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"
                />
              </svg>
            </button>
            <button
              v-if="!preset.is_default"
              class="action-btn"
              @click.stop="setDefault(preset.preset_id)"
              :title="$t('config.setDefault') || '设为默认'"
            >
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path
                  d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"
                />
              </svg>
            </button>
            <button
              class="action-btn delete"
              @click.stop="deletePresetItem(preset.preset_id)"
              :title="$t('common.delete') || '删除'"
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

    <!-- 右侧表单区域 -->
    <div class="preset-form-section">
      <div v-if="!showForm" class="empty-state">
        <svg class="empty-icon" viewBox="0 0 24 24" fill="currentColor">
          <path
            d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"
          />
        </svg>
        <p>{{ $t("config.selectPreset") || "请选择一个预设方案" }}</p>
      </div>

      <div v-else class="form-container">
        <!-- 基本信息卡片 -->
        <div class="config-card">
          <div class="config-card-header">
            <h3 class="config-card-title">{{ $t("config.basicInfo") || "基本信息" }}</h3>
          </div>
          <div class="config-card-body">
            <div class="form-row">
              <div class="form-group flex-1">
                <label class="form-label">
                  {{ $t("config.presetId") || "预设ID" }}
                  <span class="required">*</span>
                </label>
                <input
                  v-model="formData.preset_id"
                  type="text"
                  class="form-input"
                  :placeholder="$t('config.presetIdHint') || '唯一标识'"
                  :disabled="isEditing"
                />
              </div>
              <div class="form-group flex-1">
                <label class="form-label">
                  {{ $t("config.presetName") || "预设名称" }}
                  <span class="required">*</span>
                </label>
                <input
                  v-model="formData.preset_name"
                  type="text"
                  class="form-input"
                  :placeholder="$t('config.presetNameHint') || '显示名称'"
                />
              </div>
            </div>
            <div class="form-group">
              <label class="form-label">{{ $t("config.description") || "描述" }}</label>
              <textarea
                v-model="formData.description"
                class="form-textarea"
                :placeholder="$t('config.descriptionHint') || '预设方案描述'"
                rows="2"
              ></textarea>
            </div>
            <div class="form-row">
              <div class="form-group checkbox-group">
                <label class="checkbox-label">
                  <input v-model="formData.is_default" type="checkbox" />
                  <span>{{ $t("config.setAsDefault") || "设为默认" }}</span>
                </label>
              </div>
              <div class="form-group checkbox-group">
                <label class="checkbox-label">
                  <input v-model="formData.is_active" type="checkbox" />
                  <span>{{ $t("config.enable") || "启用" }}</span>
                </label>
              </div>
            </div>
          </div>
        </div>

        <!-- 模型配置卡片 -->
        <div class="config-card">
          <div class="config-card-header">
            <h3 class="config-card-title">{{ $t("config.modelConfig") || "模型配置" }}</h3>
            <p class="config-card-desc">{{ $t("config.modelConfigDesc") || "选择用于对话的大语言模型" }}</p>
          </div>
          <div class="config-card-body">
            <div class="config-item">
              <div class="config-item-label">
                <span>{{ $t("config.selectedModel") || "选择模型" }}</span>
                <span class="required">*</span>
              </div>
              <div class="config-item-control">
                <select v-model="formData.selected_model" class="form-select">
                  <option value="">{{ $t("config.pleaseSelect") || "请选择" }}</option>
                  <option v-for="model in models" :key="model.model_id" :value="model.model_id">
                    {{ model.model_id }}
                  </option>
                </select>
                <button class="select-btn" @click="showModelSelector = true">
                  {{ $t("config.selectProvider") || "选择提供商..." }}
                </button>
              </div>
            </div>
            <!-- 模型信息展示 -->
            <div v-if="selectedPreset?.model_info" class="selected-resource-info">
              <div class="selected-resource-header">
                <span class="selected-resource-name">{{ selectedPreset.model_info.model_name?.[0] || selectedPreset.model_info.model_id }}</span>
                <span class="selected-resource-badge provider">{{ selectedPreset.model_info.provider }}</span>
              </div>
              <div class="selected-resource-meta">{{ selectedPreset.model_info.model_type }} · {{ selectedPreset.model_info.model_id }}</div>
            </div>
            <div v-else-if="formData.selected_model" class="selected-resource-placeholder">
              {{ formData.selected_model }}
            </div>
            <div v-else class="selected-resource-empty">
              {{ $t("config.noModelSelected") || "未选择模型" }}
            </div>
          </div>
        </div>

        <!-- 人格/提示词卡片 -->
        <div class="config-card">
          <div class="config-card-header">
            <h3 class="config-card-title">{{ $t("config.personaConfig") || "人格配置" }}</h3>
            <p class="config-card-desc">{{ $t("config.personaConfigDesc") || "设置AI的人格和系统提示词" }}</p>
          </div>
          <div class="config-card-body">
            <div class="config-item">
              <div class="config-item-label">{{ $t("config.selectedPrompt") || "选择人格" }}</div>
              <div class="config-item-control">
                <select v-model="formData.selected_prompt" class="form-select">
                  <option value="">{{ $t("config.pleaseSelect") || "请选择" }}</option>
                  <option v-for="prompt in prompts" :key="prompt.prompt_id" :value="prompt.prompt_id">
                    {{ prompt.prompt_name }}
                  </option>
                </select>
                <button class="select-btn" @click="showPromptSelector = true">
                  {{ $t("config.selectPersona") || "选择人格..." }}
                </button>
              </div>
            </div>
            <!-- 人格信息展示 -->
            <div v-if="selectedPreset?.prompt_info" class="persona-preview-card">
              <div class="persona-preview-header">
                <span class="persona-name">{{ selectedPreset.prompt_info.prompt_name }}</span>
                <span v-if="selectedPreset.prompt_info.temperature_override" class="persona-temp">
                  temperature: {{ selectedPreset.prompt_info.temperature_override }}
                </span>
              </div>
              <div class="persona-preview-content">{{ selectedPreset.prompt_info.system_prompt }}</div>
            </div>
            <div v-else-if="formData.selected_prompt" class="selected-resource-placeholder">
              {{ formData.selected_prompt }}
            </div>
            <div v-else class="selected-resource-empty">
              {{ $t("config.noPersonaSelected") || "未选择人格，使用默认提示词" }}
            </div>
          </div>
        </div>

        <!-- 记忆配置卡片 -->
        <div class="config-card">
          <div class="config-card-header">
            <h3 class="config-card-title">{{ $t("config.memoryConfig") || "记忆配置" }}</h3>
            <p class="config-card-desc">{{ $t("config.memoryConfigDesc") || "设置对话记忆策略" }}</p>
          </div>
          <div class="config-card-body">
            <div class="config-item">
              <div class="config-item-label">{{ $t("config.selectedMemory") || "选择记忆策略" }}</div>
              <div class="config-item-control">
                <select v-model="formData.selected_memory" class="form-select">
                  <option value="">{{ $t("config.pleaseSelect") || "请选择" }}</option>
                  <option v-for="memory in memories" :key="memory.memory_id" :value="memory.memory_id">
                    {{ memory.memory_name }}
                  </option>
                </select>
                <button class="select-btn" @click="showMemorySelector = true">
                  {{ $t("config.selectMemory") || "选择记忆策略..." }}
                </button>
              </div>
            </div>
            <!-- 记忆信息展示 -->
            <div v-if="selectedPreset?.memory_info" class="selected-resource-info memory-info">
              <div class="selected-resource-header">
                <span class="selected-resource-name">{{ selectedPreset.memory_info.memory_name }}</span>
                <span class="selected-resource-badge type">{{ selectedPreset.memory_info.memory_type }}</span>
              </div>
              <div v-if="selectedPreset.memory_info.memory_params" class="memory-params">
                <code>{{ JSON.stringify(selectedPreset.memory_info.memory_params, null, 2) }}</code>
              </div>
            </div>
            <div v-else-if="formData.selected_memory" class="selected-resource-placeholder">
              {{ formData.selected_memory }}
            </div>
            <div v-else class="selected-resource-empty">
              {{ $t("config.noMemorySelected") || "未选择记忆策略，使用默认配置" }}
            </div>
          </div>
        </div>

        <!-- 知识库卡片 -->
        <div class="config-card">
          <div class="config-card-header">
            <h3 class="config-card-title">{{ $t("config.knowledgeBaseConfig") || "知识库配置" }}</h3>
            <p class="config-card-desc">{{ $t("config.knowledgeBaseConfigDesc") || "选择用于RAG检索的知识库" }}</p>
          </div>
          <div class="config-card-body">
            <div class="config-item">
              <div class="config-item-label">{{ $t("config.selectedKnowledgeBases") || "选择知识库" }}</div>
              <button class="select-btn" @click="showKBSelector = true">
                {{ $t("config.selectKnowledgeBases") || "选择知识库..." }}
              </button>
            </div>
            <!-- 已选知识库列表 -->
            <div v-if="selectedPreset?.knowledge_bases_info?.length || formData.selected_knowledge_bases?.length" class="selected-kb-list">
              <div v-for="kb in selectedPreset?.knowledge_bases_info || []" :key="kb.kb_id" class="kb-item">
                <div class="kb-info">
                  <span class="kb-name">{{ kb.kb_name }}</span>
                  <span class="kb-meta">{{ kb.document_count }} 文档 · {{ kb.total_chunks }} 块</span>
                </div>
                <span class="kb-badge">{{ kb.embedding_model }}</span>
              </div>
              <!-- 显示已选但还未加载详情的知识库ID -->
              <div v-for="kbId in formData.selected_knowledge_bases?.filter(id => !selectedPreset?.knowledge_bases_info?.some(k => k.kb_id === id)) || []" :key="kbId" class="kb-item placeholder">
                <span class="kb-name">{{ kbId }}</span>
              </div>
            </div>
            <div v-else class="selected-resource-empty">
              {{ $t("config.noKnowledgeBaseSelected") || "未选择知识库" }}
            </div>
          </div>
        </div>

        <!-- 插件配置卡片 -->
        <div class="config-card">
          <div class="config-card-header">
            <h3 class="config-card-title">{{ $t("config.pluginConfig") || "插件配置" }}</h3>
            <p class="config-card-desc">{{ $t("config.pluginConfigDesc") || "选择启用的插件工具" }}</p>
          </div>
          <div class="config-card-body">
            <div class="config-item">
              <div class="config-item-label">{{ $t("config.selectedPlugins") || "选择插件" }}</div>
              <button class="select-btn" @click="showPluginSelector = true">
                {{ $t("config.selectPlugins") || "选择插件..." }}
              </button>
            </div>
            <!-- 已选插件列表 -->
            <div v-if="selectedPreset?.plugins_info?.length || formData.selected_plugins?.length" class="selected-plugin-list">
              <div v-for="plugin in selectedPreset?.plugins_info || []" :key="plugin.plugin_id" class="plugin-item">
                <div class="plugin-info">
                  <span class="plugin-name">{{ plugin.plugin_name }}</span>
                  <span class="plugin-class">{{ plugin.class_name }}</span>
                </div>
              </div>
              <!-- 显示已选但还未加载详情的插件ID -->
              <div v-for="pluginId in formData.selected_plugins?.filter(id => !selectedPreset?.plugins_info?.some(p => p.plugin_id === id)) || []" :key="pluginId" class="plugin-item placeholder">
                <span class="plugin-name">{{ pluginId }}</span>
              </div>
            </div>
            <div v-else class="selected-resource-empty">
              {{ $t("config.noPluginSelected") || "未选择插件" }}
            </div>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="form-actions">
          <button class="cancel-btn" @click="cancelEdit">
            {{ $t("common.cancel") || "取消" }}
          </button>
          <button class="save-btn" @click="savePreset">
            {{ $t("common.save") || "保存" }}
          </button>
        </div>
      </div>
    </div>

    <!-- 确认对话框 -->
    <div v-if="showConfirmDialog" class="confirm-overlay">
      <div class="confirm-dialog">
        <div class="confirm-header">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path
              d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"
            />
          </svg>
          <span>{{ $t("provider.confirmTitle") || "确认操作" }}</span>
        </div>
        <div class="confirm-content">{{ confirmText }}</div>
        <div class="confirm-actions">
          <button class="confirm-cancel" @click="handleCancel">
            {{ $t("provider.confirmCancel") || "取消" }}
          </button>
          <button class="confirm-ok" @click="handleConfirm">
            {{ $t("provider.confirmOk") || "确定" }}
          </button>
        </div>
      </div>
    </div>

    <!-- Toast 提示 -->
    <div
      v-if="showToastFlag"
      class="toast"
      :class="{ error: toastMessage.includes('失败') }"
    >
      {{ toastMessage }}
    </div>
  </div>
</template>

<style scoped>
.general-config {
  display: flex;
  height: 100%;
  gap: 24px;
}

/* 左侧列表 */
.preset-list-section {
  width: 360px;
  display: flex;
  flex-direction: column;
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 20px;
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

.add-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.add-btn:hover {
  opacity: 0.9;
}

.add-btn svg {
  width: 16px;
  height: 16px;
}

.loading,
.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: var(--text-secondary);
}

.preset-list {
  flex: 1;
  overflow-y: auto;
}

.preset-item {
  display: flex;
  align-items: center;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: 8px;
  background: var(--bg-primary);
}

.preset-item:hover {
  background: var(--bg-hover);
}

.preset-item.active {
  background: var(--primary-light);
  border: 1px solid var(--primary-color);
}

.preset-info {
  flex: 1;
  min-width: 0;
}

.preset-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 8px;
}

.default-badge {
  font-size: 11px;
  padding: 2px 6px;
  background: var(--primary-color);
  color: white;
  border-radius: 4px;
}

.preset-id {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.preset-resources {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: 6px;
}

.resource-tag {
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 4px;
  white-space: nowrap;
}

.resource-tag.model-tag {
  background: #e6f7ff;
  color: #1890ff;
}

.resource-tag.prompt-tag {
  background: #f6ffed;
  color: #52c41a;
}

.resource-tag.kb-tag {
  background: #fff7e6;
  color: #fa8c16;
}

.resource-tag.plugin-tag {
  background: #f9f0ff;
  color: #722ed1;
}

.preset-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ccc;
}

.status-dot.active {
  background: #52c41a;
}

.action-btn {
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

.action-btn:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.action-btn.delete:hover {
  background: #ff4d4f;
  color: white;
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

/* 右侧表单 */
.preset-form-section {
  flex: 1;
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 24px;
  overflow-y: auto;
}

.preset-form-section .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--text-secondary);
}

.empty-icon {
  width: 64px;
  height: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.form-container {
  max-width: 800px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* 配置卡片 */
.config-card {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  overflow: hidden;
}

.config-card-header {
  padding: 16px 20px;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
}

.config-card-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 4px 0;
}

.config-card-desc {
  font-size: 13px;
  color: var(--text-secondary);
  margin: 0;
}

.config-card-body {
  padding: 20px;
}

/* 配置项 */
.config-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid var(--border-color);
}

.config-item:last-child {
  border-bottom: none;
}

.config-item-label {
  font-size: 14px;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 4px;
}

.config-item-control {
  display: flex;
  align-items: center;
  gap: 12px;
}

.select-btn {
  padding: 6px 12px;
  background: var(--primary-light);
  color: var(--primary-color);
  border: 1px solid var(--primary-color);
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.select-btn:hover {
  background: var(--primary-color);
  color: white;
}

/* 已选资源信息 */
.selected-resource-info {
  margin-top: 12px;
  padding: 12px 16px;
  background: #f6f8fa;
  border-radius: 8px;
  border-left: 3px solid var(--primary-color);
}

.selected-resource-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 4px;
}

.selected-resource-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.selected-resource-badge {
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 4px;
}

.selected-resource-badge.provider {
  background: #e6f7ff;
  color: #1890ff;
}

.selected-resource-badge.type {
  background: #f6ffed;
  color: #52c41a;
}

.selected-resource-meta {
  font-size: 12px;
  color: var(--text-secondary);
}

.selected-resource-placeholder {
  margin-top: 12px;
  padding: 12px 16px;
  background: #f6f8fa;
  border-radius: 8px;
  font-size: 13px;
  color: var(--text-secondary);
}

.selected-resource-empty {
  margin-top: 12px;
  padding: 16px;
  background: var(--bg-secondary);
  border-radius: 8px;
  font-size: 13px;
  color: var(--text-secondary);
  text-align: center;
  font-style: italic;
}

/* 人格预览卡片 */
.persona-preview-card {
  margin-top: 12px;
  padding: 16px;
  background: #f6f8fa;
  border-radius: 8px;
  border-left: 3px solid #52c41a;
}

.persona-preview-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.persona-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.persona-temp {
  font-size: 11px;
  padding: 2px 8px;
  background: #fff7e6;
  color: #fa8c16;
  border-radius: 4px;
}

.persona-preview-content {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
  max-height: 120px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-break: break-word;
}

/* 记忆参数 */
.memory-params {
  margin-top: 8px;
  padding: 8px 12px;
  background: var(--bg-primary);
  border-radius: 4px;
  font-size: 12px;
}

.memory-params code {
  color: var(--text-secondary);
}

/* 知识库列表 */
.selected-kb-list {
  margin-top: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.kb-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  background: #f6f8fa;
  border-radius: 6px;
}

.kb-item.placeholder {
  background: var(--bg-secondary);
  color: var(--text-secondary);
}

.kb-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.kb-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.kb-meta {
  font-size: 12px;
  color: var(--text-secondary);
}

.kb-badge {
  font-size: 11px;
  padding: 2px 8px;
  background: #fff7e6;
  color: #fa8c16;
  border-radius: 4px;
}

/* 插件列表 */
.selected-plugin-list {
  margin-top: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.plugin-item {
  display: flex;
  align-items: center;
  padding: 10px 12px;
  background: #f6f8fa;
  border-radius: 6px;
}

.plugin-item.placeholder {
  background: var(--bg-secondary);
  color: var(--text-secondary);
}

.plugin-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.plugin-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.plugin-class {
  font-size: 12px;
  color: var(--text-secondary);
  font-family: monospace;
}

/* 表单基础样式 */
.form-group {
  margin-bottom: 16px;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-group.flex-1 {
  flex: 1;
}

.form-row {
  display: flex;
  gap: 16px;
}

.form-label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.required {
  color: #ff4d4f;
  margin-left: 4px;
}

.form-input,
.form-textarea,
.form-select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  font-size: 14px;
  background: var(--bg-primary);
  color: var(--text-primary);
  transition: all 0.2s;
}

.form-input:focus,
.form-textarea:focus,
.form-select:focus {
  outline: none;
  border-color: var(--primary-color);
}

.form-input:disabled {
  background: var(--bg-hover);
  cursor: not-allowed;
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.checkbox-group {
  display: flex;
  align-items: center;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 14px;
  color: var(--text-primary);
}

.checkbox-label input[type="checkbox"] {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid var(--border-color);
}

.cancel-btn,
.save-btn {
  padding: 10px 24px;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-btn {
  background: transparent;
  border: 1px solid var(--border-color);
  color: var(--text-primary);
}

.cancel-btn:hover {
  background: var(--bg-hover);
}

.save-btn {
  background: var(--primary-color);
  border: none;
  color: white;
}

.save-btn:hover {
  opacity: 0.9;
}

/* 资源信息卡片 */
.resource-info-card {
  margin-top: 8px;
  padding: 12px;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
}

.resource-info-card.prompt-card {
  background: #f6f8fa;
}

.resource-info-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 4px;
}

.resource-info-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.resource-info-badge {
  font-size: 11px;
  padding: 2px 8px;
  background: var(--primary-light);
  color: var(--primary-color);
  border-radius: 4px;
}

.resource-info-detail {
  font-size: 12px;
  color: var(--text-secondary);
}

.prompt-preview {
  font-size: 12px;
  color: var(--text-secondary);
  max-height: 120px;
  overflow-y: auto;
  line-height: 1.5;
  white-space: pre-wrap;
  word-break: break-word;
}

/* 资源列表 */
.resource-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.resource-list-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 6px;
}

.resource-list-main {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.resource-list-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.resource-list-meta {
  font-size: 12px;
  color: var(--text-secondary);
}

.resource-list-badge {
  font-size: 11px;
  padding: 2px 8px;
  background: var(--bg-hover);
  color: var(--text-secondary);
  border-radius: 4px;
}

/* 确认对话框 */
.confirm-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.confirm-dialog {
  background: var(--bg-primary);
  border-radius: 12px;
  padding: 24px;
  width: 400px;
  max-width: 90%;
}

.confirm-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.confirm-header svg {
  width: 24px;
  height: 24px;
  color: #faad14;
}

.confirm-header span {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.confirm-content {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 24px;
  line-height: 1.5;
}

.confirm-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.confirm-cancel,
.confirm-ok {
  padding: 8px 20px;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.confirm-cancel {
  background: transparent;
  border: 1px solid var(--border-color);
  color: var(--text-primary);
}

.confirm-ok {
  background: #ff4d4f;
  border: none;
  color: white;
}

.confirm-ok:hover {
  opacity: 0.9;
}

/* Toast */
.toast {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 12px 24px;
  background: #52c41a;
  color: white;
  border-radius: 6px;
  font-size: 14px;
  z-index: 1001;
  animation: slideIn 0.3s ease;
}

.toast.error {
  background: #ff4d4f;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
</style>
