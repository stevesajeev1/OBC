import { axiosInstance } from '@/api/axios';

export const getFavorites = async () => {
  const response = await axiosInstance.get('/favorites/');
  return response.data;
};

export const favoriteListing = async (listingId: string) => {
  await axiosInstance.post(`/favorites/${listingId}`);
};

export const unfavoriteListing = async (listingId: string) => {
  await axiosInstance.delete(`/favorites/${listingId}`);
};

export default {
  getFavorites,
  favoriteListing,
  unfavoriteListing
};
