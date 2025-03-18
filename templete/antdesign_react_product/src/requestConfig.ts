import { BACKEND_HOST_LOCAL, BACKEND_HOST_PROD } from '@/constant';
import type { RequestOptions } from '@@/plugin-request/request';
import type { RequestConfig } from '@umijs/max';

// 与后端约定的响应数据格式
interface ResponseStructure {
  success: boolean;
  data: any;
  errorCode?: number;
  errorMessage?: string;
}

const isDev = process.env.NODE_ENV === 'development';

export const requestConfig: RequestConfig = {
  baseURL: isDev ? BACKEND_HOST_LOCAL : BACKEND_HOST_PROD,

  withCredentials: true,

  // 请求拦截器
  requestInterceptors: [
    (config: RequestOptions) => {
      // 拦截请求配置，进行个性化处理。
      return config;
    },
  ],

  // 响应拦截器
  responseInterceptors: [
    (response) => {
      const requestPath: string = response.config.url ?? '';
      const { data } = response as unknown as ResponseStructure;
      if (!data) {
        throw new Error('server error');
      }
      const code: number = data.errorCode;
      if (
        code === 40100 &&
        !requestPath.includes('user/get/login') &&
        !location.pathname.includes('user/login')
      ) {
        window.location.href = '/user/login?redirect=$(window.location.href)';
        throw new Error('please login');
      }
      if (code !== 0) {
        throw new Error(data.message ?? 'server error');
      }
      return response;
    },
  ],
};
