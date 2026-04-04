import { http } from "./request";

/** 预设对话项 */
export interface PresetDialogue {
  role: "user" | "assistant";
  content: string;
}

/** 提示词配置基础类型 */
export interface PromptConfig {
  id: number;
  prompt_id: string;
  prompt_name: string;
  description?: string;
  system_prompt: string;
  variables?: string[];
  temperature_override?: number;
  is_active: boolean;
  selected_tools?: string[];
  use_all_tools: boolean;
  preset_dialogues?: PresetDialogue[];
  created_at?: string;
  updated_at?: string;
}

/** 提示词配置列表项 */
export interface PromptConfigListItem {
  prompt_id: string;
  prompt_name: string;
  description?: string;
  is_active: boolean;
}

/** 创建提示词配置请求 */
export interface CreatePromptConfigRequest {
  prompt_id: string;
  prompt_name: string;
  description?: string;
  system_prompt: string;
  variables?: string[];
  temperature_override?: number;
  is_active?: boolean;
  selected_tools?: string[];
  use_all_tools?: boolean;
  preset_dialogues?: PresetDialogue[];
}

/** 更新提示词配置请求 */
export interface UpdatePromptConfigRequest {
  prompt_name?: string;
  description?: string;
  system_prompt?: string;
  variables?: string[];
  temperature_override?: number;
  is_active?: boolean;
  selected_tools?: string[];
  use_all_tools?: boolean;
  preset_dialogues?: PresetDialogue[];
}

/** API 响应包装 */
export interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
}

/**
 * 获取提示词配置列表
 */
export const getPromptConfigList = async (): Promise<
  PromptConfigListItem[]
> => {
  const response = await http.get<ApiResponse<PromptConfigListItem[]>>(
    "/prompt-configs",
  );
  return response.data;
};

/**
 * 获取提示词配置详情
 */
export const getPromptConfigDetail = async (
  promptId: string,
): Promise<PromptConfig> => {
  const response = await http.get<ApiResponse<PromptConfig>>(
    `/prompt-configs/${promptId}`,
  );
  return response.data;
};

/**
 * 创建提示词配置
 */
export const createPromptConfig = async (
  data: CreatePromptConfigRequest,
): Promise<PromptConfig> => {
  const response = await http.post<ApiResponse<PromptConfig>>(
    "/prompt-configs",
    data,
  );
  return response.data;
};

/**
 * 更新提示词配置
 */
export const updatePromptConfig = async (
  promptId: string,
  data: UpdatePromptConfigRequest,
): Promise<PromptConfig> => {
  const response = await http.put<ApiResponse<PromptConfig>>(
    `/prompt-configs/${promptId}`,
    data,
  );
  return response.data;
};

/**
 * 删除提示词配置
 */
export const deletePromptConfig = async (promptId: string): Promise<void> => {
  await http.delete<ApiResponse<void>>(`/prompt-configs/${promptId}`);
};
