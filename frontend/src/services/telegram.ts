import { WebAppInitData, WebAppUser } from '@twa-dev/types';

declare global {
  interface Window {
    initTelegramWebApp: () => WebAppInitData | null;
    sendTelegramData: (data: string) => void;
    setMainButton: (text: string, isVisible: boolean) => void;
  }
}

export const initTelegramWebApp = (): WebAppInitData | null => {
  console.log('Initializing Telegram Web App');
  if (typeof window.initTelegramWebApp === 'function') {
    const initData = window.initTelegramWebApp();
    console.log('Telegram Web App init data:', initData);
    return initData;
  }
  console.warn('Telegram Web App initialization function not found');
  return null;
};

export const getTelegramId = (): string => {
  console.log('Attempting to get Telegram ID');
  const initData = initTelegramWebApp();
  if (initData?.user?.id) {
    console.log('Telegram ID found:', initData.user.id);
    return initData.user.id.toString();
  }
  if (process.env.NODE_ENV === 'development') {
    console.warn('Using mock Telegram ID for development');
    return 'mock_user_id_123456789';
  }
  throw new Error('Telegram user ID not available');
};

export const getUserInfo = (): WebAppUser | null => {
  console.log('Attempting to get user info');
  const initData = initTelegramWebApp();
  if (initData?.user) {
    console.log('User info found:', initData.user);
    return initData.user;
  }
  console.warn('Telegram WebApp not available. User info is null.');
  return null;
};

export const isTelegramWebAppAvailable = (): boolean => {
  const isAvailable = !!initTelegramWebApp();
  console.log('Is Telegram WebApp available?', isAvailable);
  return isAvailable;
};

export const sendTelegramData = (data: string): void => {
  if (typeof window.sendTelegramData === 'function') {
    window.sendTelegramData(data);
  } else {
    console.warn('sendTelegramData function not available');
  }
};

export const setMainButton = (text: string, isVisible: boolean): void => {
  if (typeof window.setMainButton === 'function') {
    window.setMainButton(text, isVisible);
  } else {
    console.warn('setMainButton function not available');
  }
};

// Fallback function for development
export const getDevTelegramId = (): string => {
  console.log('Using development Telegram ID');
  return '123456789';
};
