/**
 * 系统日志 API
 *
 * 提供日志查看、过滤、下载等功能
 */

import { http } from "./request";

export interface LogStats {
  total: number;
  info: number;
  warning: number;
  error: number;
  debug: number;
  file_exists: boolean;
  file_size?: number;
}

/**
 * 获取系统日志
 * @param lines 返回最近 N 行（默认 100）
 * @param level 日志级别过滤（INFO/WARNING/ERROR/DEBUG）
 * @param search 关键词搜索
 */
export const getLogs = (lines?: number, level?: string, search?: string) => {
  return http.get<string[]>("/logs", {
    params: { lines, level, search },
  });
};

/**
 * 获取日志统计信息
 */
export const getLogStats = () => {
  return http.get<LogStats>("/logs/stats");
};

/**
 * 下载日志文件
 */
export const downloadLogs = () => {
  window.open("/api/v1/logs/download", "_blank");
};

export default {
  getLogs,
  getLogStats,
  downloadLogs,
};
