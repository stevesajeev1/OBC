import { axiosInstance } from './axios';

export interface Company {
  id: number;
  name: string;
  logo_url?: string | null;
}

export interface PaginatedCompaniesResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Company[];
}

export const getAllCompanies = async (page: number = 0, pageSize: number = 200): Promise<Company[]> => {
  const res = await axiosInstance.get<PaginatedCompaniesResponse>('/companies/', { params: { page, pageSize } });
  return res.data.results;
};
