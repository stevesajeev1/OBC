// See https://medium.com/@velja/token-refresh-with-axios-interceptors-for-a-seamless-authentication-experience-854b06064bde

import axios, { isAxiosError, type AxiosRequestConfig } from 'axios';
import { getApiHost } from '@/api/util';
import { clearUserState, setUserState } from '@/state';
import { router } from '@/router/index';

export const axiosInstance = axios.create({
  baseURL: getApiHost(),
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: true
});

const refreshAxiosInstance = axios.create({
  baseURL: getApiHost(),
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: true
});

export const ACCESS_TOKEN_KEY = 'accessToken';

axiosInstance.interceptors.request.use(
  request => {
    const accessToken = localStorage.getItem(ACCESS_TOKEN_KEY);
    if (accessToken) {
      request.headers['Authorization'] = `Bearer ${accessToken}`;
    }
    return request;
  },
  error => {
    return Promise.reject(error);
  }
);

axiosInstance.interceptors.response.use(
  response => response, // Directly return successful responses.
  async error => {
    const originalRequest: AxiosRequestConfig = error.config;
    if (error.response.status === 401 && !originalRequest._retry && !originalRequest._init) {
      originalRequest._retry = true; // Mark the request as retried to avoid infinite loops.
      try {
        // Make a request to your auth server to refresh the token.
        const response = await refreshAxiosInstance.post('/auth/refresh');
        const { access_token: accessToken, admin } = response.data;
        // Store the new access and refresh tokens.
        setUserState(accessToken, admin);
        return axiosInstance(originalRequest); // Retry the original request with the new access token.
      } catch (_refreshError) {
        // Handle refresh token errors by clearing stored tokens and redirecting to the login page.
        clearUserState();

        if (router.currentRoute.value.name !== 'login') {
          router.push({ name: 'login' });
        }
        return Promise.reject(error);
      }
    }
    return Promise.reject(error); // For all other errors, return the error as is.
  }
);

export const getErrorMessage = (error: unknown) => {
  let message = 'An error occurred';

  if (isAxiosError(error)) {
    message = error.response?.data?.detail ?? message;
  }
  return message;
};
