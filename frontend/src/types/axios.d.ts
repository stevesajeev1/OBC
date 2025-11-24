import 'axios';

declare module 'axios' {
  interface AxiosRequestConfig {
    _init?: boolean;
    _retry?: boolean;
  }
}
