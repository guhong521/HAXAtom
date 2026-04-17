import { http } from "./request";

// ==================== 导入导出类型定义 ====================

/** 导出响应 */
export interface ExportResponse {
  content: string;
  filename: string;
  export_type: string;
}

/** 导入请求 */
export interface ImportRequest {
  content: string;
  format: "yaml" | "json";
  conflict_action: "skip" | "overwrite" | "rename";
}

/** 单条导入结果 */
export interface ImportResult {
  success: boolean;
  action: "created" | "updated" | "skipped" | "renamed" | "failed";
  original_id?: string;
  new_id?: string;
  message: string;
}

/** 导入报告（批量导入） */
export interface ImportReport {
  total: number;
  success: number;
  failed: number;
  skipped: number;
  results: ImportResult[];
}

/** 后端统一响应结构 */
export interface ApiResponse<T> {
  code?: number;
  message?: string;
  data: T;
}

// ==================== 模型配置导入导出 ====================

/**
 * 导出模型配置
 * @param modelId 模型ID
 * @param format 导出格式（yaml/json）
 * @param includeResources 是否包含关联资源
 */
export const exportModelConfig = (
  modelId: string,
  format: "yaml" | "json" = "yaml",
  includeResources: boolean = false,
) => {
  return http.get<ApiResponse<ExportResponse>>(
    `/export/models/${modelId}/export`,
    { params: { format, include_resources: includeResources } },
  );
};

/**
 * 导入模型配置
 * @param data 导入请求数据
 */
export const importModelConfig = (data: ImportRequest) => {
  return http.post<ApiResponse<ImportResult>>("/export/models/import", data);
};

// ==================== 提示词配置导入导出 ====================

/**
 * 导出提示词配置
 * @param promptId 提示词ID
 * @param format 导出格式（yaml/json）
 */
export const exportPromptConfig = (
  promptId: string,
  format: "yaml" | "json" = "yaml",
) => {
  return http.get<ApiResponse<ExportResponse>>(
    `/export/prompts/${promptId}/export`,
    { params: { format } },
  );
};

/**
 * 导入提示词配置
 * @param data 导入请求数据
 */
export const importPromptConfig = (data: ImportRequest) => {
  return http.post<ApiResponse<ImportResult>>("/export/prompts/import", data);
};

// ==================== 插件配置导入导出 ====================

/**
 * 导出插件配置
 * @param pluginId 插件ID
 * @param format 导出格式（yaml/json）
 */
export const exportPluginConfig = (
  pluginId: string,
  format: "yaml" | "json" = "yaml",
) => {
  return http.get<ApiResponse<ExportResponse>>(
    `/export/plugins/${pluginId}/export`,
    { params: { format } },
  );
};

/**
 * 导入插件配置
 * @param data 导入请求数据
 */
export const importPluginConfig = (data: ImportRequest) => {
  return http.post<ApiResponse<ImportResult>>("/export/plugins/import", data);
};

// ==================== 知识库配置导入导出 ====================

/**
 * 导出知识库配置
 * @param kbId 知识库ID
 * @param format 导出格式（yaml/json）
 */
export const exportKnowledgeBase = (
  kbId: string,
  format: "yaml" | "json" = "yaml",
) => {
  return http.get<ApiResponse<ExportResponse>>(
    `/export/knowledge-bases/${kbId}/export`,
    { params: { format } },
  );
};

/**
 * 导入知识库配置
 * @param data 导入请求数据
 */
export const importKnowledgeBase = (data: ImportRequest) => {
  return http.post<ApiResponse<ImportResult>>(
    "/export/knowledge-bases/import",
    data,
  );
};

// ==================== 记忆配置导入导出 ====================

/**
 * 导出记忆配置
 * @param memoryId 记忆ID
 * @param format 导出格式（yaml/json）
 */
export const exportMemoryConfig = (
  memoryId: string,
  format: "yaml" | "json" = "yaml",
) => {
  return http.get<ApiResponse<ExportResponse>>(
    `/export/memories/${memoryId}/export`,
    { params: { format } },
  );
};

/**
 * 导入记忆配置
 * @param data 导入请求数据
 */
export const importMemoryConfig = (data: ImportRequest) => {
  return http.post<ApiResponse<ImportResult>>("/export/memories/import", data);
};

// ==================== 预设方案导入导出 ====================

/**
 * 导出预设方案
 * @param presetId 预设方案ID
 * @param format 导出格式（yaml/json）
 * @param includeResources 是否包含引用的资源
 */
export const exportPreset = (
  presetId: string,
  format: "yaml" | "json" = "yaml",
  includeResources: boolean = true,
) => {
  return http.get<ApiResponse<ExportResponse>>(
    `/export/presets/${presetId}/export`,
    { params: { format, include_resources: includeResources } },
  );
};

/**
 * 导入预设方案（支持批量导入包含的资源）
 * @param data 导入请求数据
 */
export const importPreset = (data: ImportRequest) => {
  return http.post<ApiResponse<ImportReport>>("/export/presets/import", data);
};
