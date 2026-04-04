import { http } from "./request";

// ==================== 五大资源池信息类型 ====================

/** 模型资源信息 */
export interface ModelInfo {
  model_id: string;
  model_name: string[];
  model_type: string;
  provider: string;
  api_base?: string;
}

/** 提示词/人格资源信息 */
export interface PromptInfo {
  prompt_id: string;
  prompt_name: string;
  system_prompt: string;
  variables?: string[];
  temperature_override?: number;
}

/** 记忆资源配置信息 */
export interface MemoryInfo {
  memory_id: string;
  memory_name: string;
  memory_type: string;
  memory_params?: Record<string, unknown>;
}

/** 知识库资源信息 */
export interface KnowledgeBaseInfo {
  kb_id: string;
  kb_name: string;
  description?: string;
  embedding_model: string;
  document_count: number;
  total_chunks: number;
}

/** 插件资源信息 */
export interface PluginInfo {
  plugin_id: string;
  plugin_name: string;
  class_name: string;
  module_path?: string;
}

// ==================== 预设方案类型 ====================

/** 预设方案基础类型 */
export interface Preset {
  id: number;
  preset_id: string;
  preset_name: string;
  description?: string;
  selected_model: string;
  selected_prompt?: string;
  selected_memory?: string;
  selected_plugins?: string[];
  selected_knowledge_bases?: string[];
  overrides?: Record<string, unknown>;
  channel_config?: Record<string, unknown>;
  is_default: boolean;
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
}

/** 预设方案列表项（包含资源名称摘要） */
export interface PresetListItem {
  preset_id: string;
  preset_name: string;
  description?: string;
  selected_model: string;
  selected_prompt?: string;
  selected_memory?: string;
  selected_plugins?: string[];
  selected_knowledge_bases?: string[];
  is_default: boolean;
  is_active: boolean;
  // 资源名称摘要（用于列表展示）
  model_name?: string;
  prompt_name?: string;
  memory_name?: string;
  knowledge_base_names?: string[];
  plugin_names?: string[];
}

/** 预设方案详情（包含原子化查询的完整资源信息） */
export interface PresetDetail extends Preset {
  // 原子化资源信息 - 从五大资源池查询得到的完整信息
  model_info?: ModelInfo;
  prompt_info?: PromptInfo;
  memory_info?: MemoryInfo;
  knowledge_bases_info?: KnowledgeBaseInfo[];
  plugins_info?: PluginInfo[];
}

// 创建预设方案请求
export interface PresetCreate {
  preset_id: string;
  preset_name: string;
  description?: string;
  selected_model: string;
  selected_prompt?: string;
  selected_memory?: string;
  selected_plugins?: string[];
  selected_knowledge_bases?: string[];
  overrides?: Record<string, unknown>;
  channel_config?: Record<string, unknown>;
  is_default?: boolean;
  is_active?: boolean;
}

// 更新预设方案请求
export interface PresetUpdate {
  preset_name?: string;
  description?: string;
  selected_model?: string;
  selected_prompt?: string;
  selected_memory?: string;
  selected_plugins?: string[];
  selected_knowledge_bases?: string[];
  overrides?: Record<string, unknown>;
  channel_config?: Record<string, unknown>;
  is_default?: boolean;
  is_active?: boolean;
}

// 克隆预设方案请求
export interface PresetCloneRequest {
  new_preset_id: string;
  new_preset_name?: string;
}

// 后端统一响应结构
export interface ApiResponse<T> {
  code?: number;
  message?: string;
  data: T;
}

/**
 * 获取预设方案列表
 * @param skip 跳过数量
 * @param limit 限制数量
 */
export const getPresets = async (skip?: number, limit?: number) => {
  const params: Record<string, number> = {};
  if (skip !== undefined) params.skip = skip;
  if (limit !== undefined) params.limit = limit;
  return http.get<ApiResponse<PresetListItem[]>>("/presets", { params });
};

/**
 * 获取预设方案详情（包含五大资源池完整信息）
 * @param presetId 预设方案ID
 */
export const getPreset = (presetId: string) => {
  return http.get<ApiResponse<PresetDetail>>(`/presets/${presetId}`);
};

/**
 * 创建预设方案
 * @param data 预设方案数据
 */
export const createPreset = (data: PresetCreate) => {
  return http.post<ApiResponse<Preset>>("/presets", data);
};

/**
 * 更新预设方案
 * @param presetId 预设方案ID
 * @param data 更新数据
 */
export const updatePreset = (presetId: string, data: PresetUpdate) => {
  return http.put<ApiResponse<Preset>>(`/presets/${presetId}`, data);
};

/**
 * 删除预设方案
 * @param presetId 预设方案ID
 */
export const deletePreset = (presetId: string) => {
  return http.delete<ApiResponse<null>>(`/presets/${presetId}`);
};

/**
 * 克隆预设方案
 * @param presetId 源预设方案ID
 * @param data 克隆请求数据
 */
export const clonePreset = (presetId: string, data: PresetCloneRequest) => {
  return http.post<ApiResponse<Preset>>(`/presets/${presetId}/clone`, data);
};

/**
 * 设置默认预设方案
 * @param presetId 预设方案ID
 */
export const setDefaultPreset = (presetId: string) => {
  return http.put<ApiResponse<Preset>>(`/presets/${presetId}`, {
    is_default: true,
  });
};
