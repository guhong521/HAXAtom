<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { ElMessage } from "element-plus";
import { useImport, useExport, type ResourceType } from "../composables/useImportExport";

const props = defineProps<{
  visible: boolean;
  mode: "import" | "export";
  resourceType: ResourceType;
  resourceId?: string;
}>();

const emit = defineEmits<{
  "update:visible": [value: boolean];
  success: [];
}>();

const { isImporting, importResource } = useImport();
const { isExporting, exportResource } = useExport();

const dialogVisible = computed({
  get: () => props.visible,
  set: (val) => emit("update:visible", val),
});

const importContent = ref("");
const importFormat = ref<"yaml" | "json">("yaml");
const conflictAction = ref<"skip" | "overwrite" | "rename">("rename");
const exportFormat = ref<"yaml" | "json">("yaml");
const includeResources = ref(true);

const isProcessing = computed(() => isImporting.value || isExporting.value);

const dialogTitle = computed(() => {
  const typeMap: Record<ResourceType, string> = {
    model: "模型配置",
    prompt: "提示词配置",
    plugin: "插件配置",
    knowledge_base: "知识库配置",
    memory: "记忆配置",
    preset: "预设方案",
  };
  const type = typeMap[props.resourceType] || "";
  return props.mode === "import" ? `导入${type}` : `导出${type}`;
});

watch(
  () => props.visible,
  (val) => {
    if (val) {
      importContent.value = "";
    }
  },
);

const handleFileUpload = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = (e) => {
    importContent.value = e.target?.result as string;
    if (file.name.endsWith(".json")) {
      importFormat.value = "json";
    } else {
      importFormat.value = "yaml";
    }
  };
  reader.readAsText(file);
};

const handleExport = async () => {
  if (!props.resourceId) {
    ElMessage.warning("缺少资源ID");
    return;
  }

  try {
    await exportResource(
      props.resourceType,
      props.resourceId,
      exportFormat.value,
      includeResources.value,
    );
    dialogVisible.value = false;
    emit("success");
  } catch {
    // 错误已在 composable 中处理
  }
};

const handleImport = async () => {
  if (!importContent.value.trim()) {
    ElMessage.warning("请粘贴或上传导入内容");
    return;
  }

  try {
    const result = await importResource(
      props.resourceType,
      importContent.value,
      importFormat.value,
      conflictAction.value,
    );

    if ("results" in result) {
      // 批量导入（预设方案）
      const { total, success, failed, skipped } = result;
      if (failed > 0) {
        ElMessage.warning(
          `导入完成：成功 ${success} 项，失败 ${failed} 项，跳过 ${skipped} 项，共 ${total} 项`,
        );
      } else {
        ElMessage.success(
          `导入成功：成功 ${success} 项，跳过 ${skipped} 项，共 ${total} 项`,
        );
      }
    } else {
      // 单条导入
      if (result.success) {
        const actionMap: Record<string, string> = {
          created: "创建成功",
          updated: "更新成功",
          skipped: "已存在，已跳过",
          renamed: `导入成功，新ID：${result.new_id}`,
        };
        ElMessage.success(actionMap[result.action] || "导入成功");
      } else {
        ElMessage.error(result.message || "导入失败");
      }
    }

    dialogVisible.value = false;
    emit("success");
  } catch {
    // 错误已在 composable 中处理
  }
};
</script>

<template>
  <el-dialog
    v-model="dialogVisible"
    :title="dialogTitle"
    width="600px"
    :close-on-click-modal="false"
  >
    <!-- 导出模式 -->
    <div v-if="mode === 'export'" class="export-form">
      <el-form label-width="100px">
        <el-form-item label="导出格式">
          <el-radio-group v-model="exportFormat">
            <el-radio value="yaml">YAML</el-radio>
            <el-radio value="json">JSON</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item
          v-if="resourceType === 'preset'"
          label="包含资源"
          tooltip="是否同时导出预设引用的模型、提示词、插件、知识库、记忆配置"
        >
          <el-switch v-model="includeResources" />
        </el-form-item>

        <el-alert
          type="info"
          :closable="false"
          show-icon
        >
          <template #default>
            导出文件将自动下载到浏览器默认下载目录。
            <template v-if="resourceType === 'preset' && includeResources">
              包含的资源配置中，API Key 等敏感信息会被自动移除，导入时需要重新填写。
            </template>
          </template>
        </el-alert>
      </el-form>
    </div>

    <!-- 导入模式 -->
    <div v-else class="import-form">
      <el-form label-width="100px">
        <el-form-item label="导入格式">
          <el-radio-group v-model="importFormat">
            <el-radio value="yaml">YAML</el-radio>
            <el-radio value="json">JSON</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="冲突处理">
          <el-select v-model="conflictAction" style="width: 100%">
            <el-option
              label="重命名（生成新ID）"
              value="rename"
            />
            <el-option
              label="覆盖（更新现有配置）"
              value="overwrite"
            />
            <el-option
              label="跳过（保留原配置）"
              value="skip"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="导入内容">
          <el-input
            v-model="importContent"
            type="textarea"
            :rows="10"
            placeholder="请粘贴 YAML/JSON 格式的配置内容..."
          />
        </el-form-item>

        <el-form-item label="或上传文件">
          <input
            type="file"
            accept=".yaml,.yml,.json"
            @change="handleFileUpload"
            style="width: 100%"
          />
        </el-form-item>

        <el-alert
          type="warning"
          :closable="false"
          show-icon
        >
          <template #default>
            请确保导入的文件来自可信来源。导入的配置将自动校验格式并处理ID冲突。
          </template>
        </el-alert>
      </el-form>
    </div>

    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button
        v-if="mode === 'export'"
        type="primary"
        :loading="isExporting"
        @click="handleExport"
      >
        导出
      </el-button>
      <el-button
        v-else
        type="primary"
        :loading="isImporting"
        @click="handleImport"
      >
        导入
      </el-button>
    </template>
  </el-dialog>
</template>
