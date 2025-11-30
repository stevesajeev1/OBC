import { user } from '@/state';
import { axiosInstance } from './axios';

// TODO: Replace with actual logic to get profile
export const getProfile = () => {
  if (user.value === null) return;

  return {
    name: 'John Doe',
    image_url: 'https://cdn.vectorstock.com/i/500p/29/52/faceless-male-avatar-in-hoodie-vector-56412952.jpg'
  };
};

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
}

export interface PaginatedProfileResponse {
  data: Profile[];
  page: number;
  pageSize: number;
  total: number;
}

export const getAllProfiles = async (page: number = 0, pageSize: number = 100): Promise<Profile[]> => {
  try {
    const response = await axiosInstance.get<PaginatedProfileResponse>('/profiles/', {
      params: { page, pageSize }
    });
    return response.data.data;
  } catch (error) {
    console.error('Error fetching profiles:', error);
    throw error;
  }
};
