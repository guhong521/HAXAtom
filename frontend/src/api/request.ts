import axios, {
  type AxiosInstance,
  type AxiosRequestConfig,
  type AxiosResponse,
  type InternalAxiosRequestConfig,
} from "axios";

// 创建 axios 实例
const request: AxiosInstance = axios.create({
  // 统一使用相对路径，开发和生产环境都通过代理/后端处理
  baseURL: "/api/v1",
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

// 请求拦截器
request.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 可以在这里添加 token 等认证信息
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: unknown) => {
    return Promise.reject(error);
  },
);

// 响应拦截器
request.interceptors.response.use(
  (response: AxiosResponse) => {
    // 直接返回后端返回的数据结构
    return response.data;
  },
  (error) => {
    // 统一错误处理
    const message = error.response?.data?.detail || error.message || "请求失败";
    console.error("API Error:", message);
    return Promise.reject(new Error(message));
  },
);

// 封装通用请求方法
export const http = {
  get: <T>(url: string, config?: AxiosRequestConfig) =>
    request.get<T, T>(url, config),
  post: <T>(url: string, data?: unknown, config?: AxiosRequestConfig) =>
    request.post<T, T>(url, data, config),
  put: <T>(url: string, data?: unknown, config?: AxiosRequestConfig) =>
    request.put<T, T>(url, data, config),
  delete: <T>(url: string, config?: AxiosRequestConfig) =>
    request.delete<T, T>(url, config),
};

export default request;
