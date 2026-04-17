<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { t } from "../../../locales";
import ImportExportDialog from "../../../components/ImportExportDialog.vue";

const $t = computed(() => t);

const loading = ref(false);
const memoryConfig = ref({
  enabled: true,
  max_history: 10,
  summary_enabled: false,
});

// 导入导出弹窗状态
const showImportExportDialog = ref(false);
const importExportMode = ref<"import" | "export">("import");
const selectedMemoryForExport = ref<string | undefined>(undefined);

const loadMemoryConfig = async () => {
  loading.value = true;
  try {
    // TODO: 调用 API 获取记忆配置
    console.log("加载记忆配置");
  } catch (error) {
    console.error("加载记忆配置失败:", error);
  } finally {
    loading.value = false;
  }
};

const saveMemoryConfig = async () => {
  try {
    // TODO: 调用 API 保存记忆配置
    console.log("保存记忆配置", memoryConfig.value);
    alert("保存成功");
  } catch (error) {
    console.error("保存记忆配置失败:", error);
  }
};

// 打开导入弹窗
const handleImport = () => {
  selectedMemoryForExport.value = undefined;
  importExportMode.value = "import";
  showImportExportDialog.value = true;
};

// 导入导出成功后刷新
const handleImportExportSuccess = () => {
  loadMemoryConfig();
};

onMounted(() => {
  loadMemoryConfig();
});
</script>

<template>
  <div class="memory-config-page">
    <div class="page-header">
      <h1>{{ $t("bot.memory.title") || "记忆配置" }}</h1>
      <p>{{ $t("bot.memory.subtitle") || "配置 AI 对话记忆功能" }}</p>
    </div>

    <div class="page-content">
      <div v-if="loading" class="loading-state">
        <span>加载中...</span>
      </div>

      <div v-else class="config-form">
        <div class="form-group">
          <label class="form-label">
            <input
              type="checkbox"
              v-model="memoryConfig.enabled"
              class="form-checkbox"
            />
            启用对话记忆
          </label>
          <p class="form-hint">开启后，AI 会记住之前的对话内容</p>
        </div>

        <div class="form-group">
          <label class="form-label">最大历史轮数</label>
          <input
            type="number"
            v-model.number="memoryConfig.max_history"
            class="form-input"
            min="1"
            max="50"
          />
          <p class="form-hint">AI 最多记住多少轮对话历史</p>
        </div>

        <div class="form-group">
          <label class="form-label">
            <input
              type="checkbox"
              v-model="memoryConfig.summary_enabled"
              class="form-checkbox"
            />
            启用对话摘要
          </label>
          <p class="form-hint">开启后，AI 会对长对话进行摘要总结</p>
        </div>

        <div class="form-actions">
          <button class="btn btn-secondary" @click="handleImport">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M9 16h6v-6h4l-7-7-7 7h4v6zm-4 2h14v2H5v-2z" />
            </svg>
            导入配置
          </button>
          <button class="btn btn-primary" @click="saveMemoryConfig">
            保存配置
          </button>
        </div>
      </div>
    </div>

    <!-- 导入导出弹窗 -->
    <ImportExportDialog
      v-model:visible="showImportExportDialog"
      :mode="importExportMode"
      resource-type="memory"
      :resource-id="selectedMemoryForExport"
      @success="handleImportExportSuccess"
    />
  </div>
</template>

<style scoped>
.memory-config-page {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 24px 32px;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 8px 0;
}

.page-header p {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
}

.page-content {
  flex: 1;
}

.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: var(--text-tertiary);
}

.config-form {
  max-width: 480px;
}

.form-group {
  margin-bottom: 24px;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.form-checkbox {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

.form-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  font-size: 14px;
  background: var(--bg-primary);
  color: var(--text-primary);
  outline: none;
  transition: all 0.2s;
}

.form-input:focus {
  border-color: var(--primary-color);
}

.form-hint {
  font-size: 12px;
  color: var(--text-tertiary);
  margin: 4px 0 0 0;
}

.form-actions {
  margin-top: 32px;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
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
  background: var(--bg-tertiary);
}
</style>
