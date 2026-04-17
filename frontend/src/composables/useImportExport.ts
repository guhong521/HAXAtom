import { ref } from "vue";
import { ElMessage } from "element-plus";
import {
  exportModelConfig,
  exportPromptConfig,
  exportPluginConfig,
  exportKnowledgeBase,
  exportMemoryConfig,
  exportPreset,
  importModelConfig,
  importPromptConfig,
  importPluginConfig,
  importKnowledgeBase,
  importMemoryConfig,
  importPreset,
  type ImportRequest,
  type ImportResult,
  type ImportReport,
} from "../api/export";

export type ResourceType =
  | "model"
  | "prompt"
  | "plugin"
  | "knowledge_base"
  | "memory"
  | "preset";

export function useExport() {
  const isExporting = ref(false);

  const exportResource = async (
    type: ResourceType,
    id: string,
    format: "yaml" | "json" = "yaml",
    includeResources: boolean = true,
  ) => {
    isExporting.value = true;
    try {
      let response;
      switch (type) {
        case "model":
          response = await exportModelConfig(id, format, false);
          break;
        case "prompt":
          response = await exportPromptConfig(id, format);
          break;
        case "plugin":
          response = await exportPluginConfig(id, format);
          break;
        case "knowledge_base":
          response = await exportKnowledgeBase(id, format);
          break;
        case "memory":
          response = await exportMemoryConfig(id, format);
          break;
        case "preset":
          response = await exportPreset(id, format, includeResources);
          break;
        default:
          throw new Error("未知的资源类型");
      }

      const { content, filename } = response.data;
      downloadFile(content, filename, format === "yaml" ? "text/yaml" : "application/json");
      ElMessage.success("导出成功");
    } catch (error: any) {
      ElMessage.error(error.response?.data?.detail || "导出失败");
      throw error;
    } finally {
      isExporting.value = false;
    }
  };

  const downloadFile = (content: string, filename: string, mimeType: string) => {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return { isExporting, exportResource };
}

export function useImport() {
  const isImporting = ref(false);

  const importResource = async (
    type: ResourceType,
    content: string,
    format: "yaml" | "json" = "yaml",
    conflictAction: "skip" | "overwrite" | "rename" = "rename",
  ): Promise<ImportResult | ImportReport> => {
    isImporting.value = true;
    try {
      const request: ImportRequest = {
        content,
        format,
        conflict_action: conflictAction,
      };

      let response;
      switch (type) {
        case "model":
          response = await importModelConfig(request);
          break;
        case "prompt":
          response = await importPromptConfig(request);
          break;
        case "plugin":
          response = await importPluginConfig(request);
          break;
        case "knowledge_base":
          response = await importKnowledgeBase(request);
          break;
        case "memory":
          response = await importMemoryConfig(request);
          break;
        case "preset":
          response = await importPreset(request);
          break;
        default:
          throw new Error("未知的资源类型");
      }

      const result = response.data;
      return result;
    } catch (error: any) {
      ElMessage.error(error.response?.data?.detail || "导入失败");
      throw error;
    } finally {
      isImporting.value = false;
    }
  };

  return { isImporting, importResource };
}
