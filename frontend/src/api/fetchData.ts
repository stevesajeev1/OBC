const apiHost = import.meta.env.VITE_API_HOST;

export const fetchData = async (): Promise<string> => {
  const response = await fetch(apiHost);
  return response.json();
};
