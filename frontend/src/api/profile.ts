import { axiosInstance } from './axios';
import type { PaginatedResponse } from './util';
import defaultPfp from '@/assets/default_pfp.jpg';

export interface Internship {
  company: string;
  role: string;
  time_period: string[];
}

export interface Profile {
  full_name: string | null;
  major: string | null;
  grad_year: number | null;
  linkedin_url: string | null;
  bio: string | null;
  image_url: string | null;
  prev_internships: Internship[];
  public: boolean;
  email?: string;
}

export interface ProfileUpdate {
  full_name?: string | null;
  major?: string | null;
  grad_year?: number | null;
  linkedin_url?: string | null;
  bio?: string | null;
  image_url?: string | null;
  prev_internships?: Internship[];
  public?: boolean;
}

export const getProfile = async (): Promise<Profile | null> => {
  try {
    const response = await axiosInstance.get<Profile>('/profiles/me');
    const profile = response.data;

    // Fallback image
    if (!profile.image_url) {
      profile.image_url = defaultPfp;
    }

    return profile;
  } catch (error) {
    console.error('Error fetching profile:', error);
    return {
      full_name: null,
      image_url: defaultPfp,
      major: null,
      grad_year: null,
      linkedin_url: null,
      bio: null,
      prev_internships: [],
      public: true
    };
  }
};

export const updateProfile = async (profileData: ProfileUpdate): Promise<Profile> => {
  try {
    const response = await axiosInstance.patch<Profile>('/profiles/me', profileData);
    const profile = response.data;
    if (!profile.image_url) {
      profile.image_url = defaultPfp;
    }
    return profile;
  } catch (error) {
    console.error('Error updating profile:', error);
    throw error;
  }
};

export const uploadProfileImage = async (file: File): Promise<void> => {
  try {
    const response = await axiosInstance.put('/images/profile', file, {
      headers: {
        'Content-Type': file.type
      }
    });
    return response.data;
  } catch (error) {
    console.error('Error uploading profile image:', error);
    throw error;
  }
};

export const deleteProfileImage = async (): Promise<void> => {
  try {
    const response = await axiosInstance.delete('/images/profile');
    return response.data;
  } catch (error) {
    console.error('Error deleting profile image:', error);
    throw error;
  }
};

export const getAllProfiles = async (page: number = 0, pageSize: number = 100): Promise<Profile[]> => {
  try {
    const response = await axiosInstance.get<PaginatedResponse<Profile>>('/profiles/', {
      params: { page, pageSize }
    });
    return response.data.results.map(profile => {
      if (!profile.image_url) profile.image_url = defaultPfp;
      return profile;
    });
  } catch (error) {
    console.error('Error fetching profiles:', error);
    throw error;
  }
};
