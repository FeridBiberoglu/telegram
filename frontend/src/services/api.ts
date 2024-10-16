import axios, { AxiosError } from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // This matches your API running on port 8000

const api = axios.create({
  baseURL: API_BASE_URL,
});

const handleError = (error: unknown) => {
  if (axios.isAxiosError(error)) {
    return `API Error: ${error.response?.data?.detail || error.message}`;
  }
  return 'An unexpected error occurred';
};

export const updateFilters = async (telegramId: string, filters: any) => {
  try {
    await api.put(`/users/${telegramId}/filters`, filters);
    return "Filters updated successfully";
  } catch (error) {
    throw handleError(error);
  }
};

export const getTokenSet = async (telegramId: string) => {
  try {
    const response = await api.get(`/token_sets/${telegramId}`);
    return response.data;
  } catch (error) {
    throw handleError(error);
  }
};