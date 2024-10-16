import axios, { AxiosError } from 'axios';

// Use the BACKEND environment variable for the API base URL
const API_BASE_URL = process.env.BACKEND || 'http://localhost:8000'; // Fallback to localhost for local development

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
