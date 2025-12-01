import { axiosInstance } from './axios';
import type { PaginatedResponse } from './util';

export interface Company {
  id: number;
  name: string;
  logo_url?: string | null;
}

export const getAllCompanies = async (page: number = 0, pageSize: number = 200): Promise<Company[]> => {
  const res = await axiosInstance.get<PaginatedResponse<Company>>('/companies/', { params: { page, pageSize } });
  return res.data.results;
};
