import { http } from "./request";

// 模型配置类型
export interface ModelConfig {
  id: number;
  model_id: string;
  model_name: string[];
  model_type: "chat" | "embedding" | "tts" | "stt" | "rerank";
  provider: string;
  api_base?: string;
  api_key?: string;
  default_params?: Record<string, unknown>;
  is_active: boolean;
  disabled_models?: string[];
}

// 创建模型配置请求
export interface ModelConfigCreate {
  model_id: string;
  model_name: string[];
  model_type: "chat" | "embedding" | "tts" | "stt" | "rerank";
  provider: string;
  api_base?: string;
  api_key?: string;
  default_params?: Record<string, unknown>;
  is_active?: boolean;
  disabled_models?: string[];
}

// 更新模型配置请求
export interface ModelConfigUpdate {
  model_name?: string[];
  api_base?: string;
  api_key?: string;
  default_params?: Record<string, unknown>;
  is_active?: boolean;
  disabled_models?: string[];
}

// 列表项
export interface ModelConfigListItem {
  id: number;
  model_id: string;
  model_name: string[];
  model_type: string;
  provider: string;
  api_base?: string;
  api_key?: string;
  is_active: boolean;
  disabled_models?: string[];
}

// 后端统一响应结构
export interface ApiResponse<T> {
  code?: number;
  message?: string;
  data: T;
}

/**
 * 获取模型配置列表
 * @param modelType 模型类型过滤（chat/embedding/tts/stt/rerank）
 */
export const getModelConfigs = async (modelType?: string) => {
  const params = modelType ? { model_type: modelType } : {};
  return http.get<ApiResponse<ModelConfigListItem[]>>("/models", { params });
};

/**
 * 获取模型配置详情
 * @param modelId 模型ID
 */
export const getModelConfig = (modelId: string) => {
  return http.get<ApiResponse<ModelConfig>>(`/models/${modelId}`);
};

/**
 * 创建模型配置
 * @param data 模型配置数据
 */
export const createModelConfig = (data: ModelConfigCreate) => {
  return http.post<ApiResponse<ModelConfig>>("/models", data);
};

/**
 * 更新模型配置
 * @param modelId 模型ID
 * @param data 更新数据
 */
export const updateModelConfig = (modelId: string, data: ModelConfigUpdate) => {
  return http.put<ApiResponse<ModelConfig>>(`/models/${modelId}`, data);
};

/**
 * 删除模型配置
 * @param modelId 模型ID
 */
export const deleteModelConfig = (modelId: string) => {
  return http.delete<ApiResponse<null>>(`/models/${modelId}`);
};

/**
 * 获取供应商的模型列表
 * @param provider 供应商名称
 * @param modelConfigId 可选的模型配置 ID
 */
export const getProviderModels = async (
  provider: string,
  modelConfigId?: string,
) => {
  const params = modelConfigId ? { model_config_id: modelConfigId } : {};
  return http.get<
    ApiResponse<Array<{ id: string; name: string; owned_by: string }>>
  >(`/models/providers/${provider}/models`, { params });
};

/**
 * 根据标签页类型获取对应的模型类型
 */
export const getModelTypeByTab = (tab: string): string | undefined => {
  const map: Record<string, string> = {
    chat: "chat",
    embedding: "embedding",
    tts: "tts",
    stt: "stt",
    rerank: "rerank",
  };
  return map[tab];
};
