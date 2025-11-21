import { clearUserState, setUserState } from "@/state";
import { axiosInstance, getErrorMessage } from "@/api/axios";
import { isAxiosError, type AxiosRequestConfig } from "axios";

type AuthResponse =
  | {
      success: true;
    }
  | {
      success: false;
      message: string;
    };

export const signIn = async (username: string, password: string): Promise<AuthResponse> => {
  const payload = {
    username,
    password
  }

  const config: AxiosRequestConfig = {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  }

  try {
    const response = await axiosInstance.post("/auth/login", payload, config);

    const { access_token: accessToken, admin } = response.data;
    setUserState(accessToken, admin);

    return { success: true };
  } catch (error: any) {
    clearUserState();

    return { success: false, message: getErrorMessage(error) };
  }
};

export const signOut = async (): Promise<void> => {
  await axiosInstance.post("/auth/logout");
  clearUserState();
};

export const register = async (username: string, password: string): Promise<AuthResponse> => {
  const payload = {
    username,
    password
  }

  const config: AxiosRequestConfig = {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  }

  try {
    const response = await axiosInstance.post("/auth/register", payload, config);

    const { access_token: accessToken, admin } = response.data;
    setUserState(accessToken, admin);

    return { success: true };
  } catch (error: any) {
    clearUserState();

    return { success: false, message: getErrorMessage(error) };
  }
}