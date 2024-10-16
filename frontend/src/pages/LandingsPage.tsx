import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { DollarSign, Search } from 'lucide-react';
import { getUserInfo, isTelegramWebAppAvailable, getDevTelegramId } from '../services/telegram';
import { WebAppUser } from '@twa-dev/types';

function Logo() {
  return (
    <div className="relative inline-block mb-6">
        <DollarSign size={100} className="text-white" />
        <Search size={40} className="absolute text-yellow-300 transform -translate-y-1/4 translate-x-1/4" style={{ top: '10%', right: '16%' }} />
      </div>
  );
}

const LandingPage: React.FC = () => {
  const [userInfo, setUserInfo] = useState<WebAppUser | null>(null);

  useEffect(() => {
    console.log('LandingPage mounted');
    const isTelegramAvailable = isTelegramWebAppAvailable();
    console.log('Is Telegram available?', isTelegramAvailable);
    
    if (isTelegramAvailable) {
      const user = getUserInfo();
      console.log('User info:', user);
      setUserInfo(user);
      // Remove the setMainButton call
    } else {
      console.log('Using dev Telegram ID:', getDevTelegramId());
    }
  }, []);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-r from-blue-500 to-purple-600 text-white p-4">
      <div className="text-center">
        <Logo />
        <h1 className="text-4xl font-bold mb-4">
          Welcome to ProfitSniffer!
        </h1>
        <p className="text-xl mb-8">Your ultimate tool for tracking crypto opportunities</p>
        <div className="space-y-4">
          <Link to="/filters" className="block w-full bg-white text-blue-600 px-6 py-3 rounded-full font-semibold hover:bg-blue-100 transition duration-300">
            Set Filters
          </Link>
          <Link to="/tokens" className="block w-full bg-purple-500 text-white px-6 py-3 rounded-full font-semibold hover:bg-purple-600 transition duration-300">
            View Tokens
          </Link>
        </div>
      </div>
    </div>
  );
};


export default LandingPage;
