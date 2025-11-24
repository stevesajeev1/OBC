import { ref } from 'vue';
import { ACCESS_TOKEN_KEY, axiosInstance } from '@/api/axios';

type User = {
  admin: boolean;
};

export const user = ref<User | null>(null);

export const clearUserState = () => {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  user.value = null;
};

export const setUserState = (accessToken: string, admin: boolean) => {
  localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
  user.value = { admin };
};

const initUserState = async () => {
  try {
    const response = await axiosInstance.post('/auth/refresh', null, { _init: true });

    const { access_token: accessToken, admin } = response.data;
    setUserState(accessToken, admin);
  } catch (_error) {
    clearUserState();
  }
};

export const initState = async () => {
  await initUserState();
};
