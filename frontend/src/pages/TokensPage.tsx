// import React, { useState, useEffect } from 'react';
// import { Link } from 'react-router-dom';
// import { ArrowLeft, Loader, DollarSign, Droplet, BarChart3, RefreshCw } from 'lucide-react';
// import { getTokenSet } from '../services/api';
// import { getTelegramId } from '../services/telegram';

// interface Token {
//   _id: string;
//   address: string;
//   chain: string;
//   name: string;
//   symbol: string;
//   price_usd: number;
//   liquidity_usd: number;
//   volume_24h: number;
//   image_url: string;
// }

// interface TokenSet {
//   user_id: string;
//   telegram_id: string;
//   tokens: Token[];
//   created_at: string;
//   updated_at: string;
// }

// const TokensPage: React.FC = () => {
//   const [tokenSet, setTokenSet] = useState<TokenSet | null>(null);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState('');

//   const loadTokens = async () => {
//     try {
//       setLoading(true);
//       setError('');
//       const telegramId = getTelegramId();
//       const result = await getTokenSet(telegramId);
//       console.log('Token set:', result);
//       setTokenSet(result);
//     } catch (error) {
//       console.error('Error loading tokens:', error);
//       setError(error instanceof Error ? error.message : 'An unknown error occurred');
//     } finally {
//       setLoading(false);
//     }
//   };

//   useEffect(() => {
//     loadTokens();

//     if (window.Telegram?.WebApp) {
//       const webApp = window.Telegram.WebApp;
//       webApp.MainButton.setText('Refresh Tokens').show().onClick(loadTokens);

//       return () => {
//         webApp.MainButton.offClick(loadTokens);
//         webApp.MainButton.hide();
//       };
//     }
//   }, []);

//   if (loading) {
//     return (
//       <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-blue-500 to-purple-600 text-white">
//         <Loader className="animate-spin mr-2" size={32} /> Loading...
//       </div>
//     );
//   }

//   if (error) {
//     return (
//       <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-blue-500 to-purple-600 text-white">
//         <div className="bg-red-500 bg-opacity-50 p-6 rounded-lg text-center">
//           <p className="text-xl mb-4">Error loading tokens: {error}</p>
//           <button
//             onClick={loadTokens}
//             className="bg-white text-red-500 px-4 py-2 rounded-full flex items-center justify-center hover:bg-red-100 transition duration-300"
//           >
//             <RefreshCw className="mr-2" size={18} /> Retry
//           </button>
//         </div>
//       </div>
//     );
//   }

//   if (!tokenSet || !tokenSet.tokens || tokenSet.tokens.length === 0) {
//     return (
//       <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-blue-500 to-purple-600 text-white">
//         <p className="text-xl text-center bg-white bg-opacity-10 backdrop-blur-lg rounded-lg p-8">
//           No tokens found. Try adjusting your filters.
//         </p>
//       </div>
//     );
//   }

//   return (
//     <div className="min-h-screen bg-gradient-to-r from-blue-500 to-purple-600 text-white p-4">
//       <div className="max-w-4xl mx-auto">
//         <Link to="/" className="inline-flex items-center text-white mb-6 hover:text-blue-200 transition duration-300">
//           <ArrowLeft className="mr-2" /> Back to Home
//         </Link>
//         <h1 className="text-3xl font-bold mb-6">Tokens</h1>
//         <div className="space-y-4">
//           {tokenSet.tokens.map((token) => (
//             <div key={token._id} className="bg-white bg-opacity-10 backdrop-blur-lg rounded-lg shadow-lg p-4 hover:bg-opacity-20 transition duration-300">
//               <div className="flex items-center mb-4">
//                 <h2 className="text-2xl font-semibold flex items-center">
//                   {token.name} <span className="text-blue-300 ml-1">({token.symbol})</span>
//                   {token.image_url && (
//                     <img 
//                       src={token.image_url} 
//                       alt={`${token.name} logo`} 
//                       className="w-6 h-6 rounded-full ml-2 object-cover"
//                       onError={(e) => {
//                         (e.target as HTMLImageElement).onerror = null;
//                         (e.target as HTMLImageElement).src = 'https://via.placeholder.com/24';
//                       }}
//                     />
//                   )}
//                 </h2>
//               </div>
//               <div className="grid grid-cols-2 gap-2 text-sm">
//                 <div className="flex items-center">
//                   <DollarSign className="mr-1 text-green-400" size={16} />
//                   <p>Price: ${token.price_usd?.toFixed(6) || 'N/A'}</p>
//                 </div>
//                 <div className="flex items-center">
//                   <Droplet className="mr-1 text-blue-400" size={16} />
//                   <p>Liquidity: ${token.liquidity_usd?.toLocaleString() || 'N/A'}</p>
//                 </div>
//                 <div className="flex items-center col-span-2">
//                   <BarChart3 className="mr-1 text-purple-400" size={16} />
//                   <p>24h Volume: ${token.volume_24h?.toLocaleString() || 'N/A'}</p>
//                 </div>
//               </div>
//             </div>
//           ))}
//         </div>
//       </div>
//     </div>
//   );
// };

// export default TokensPage;

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, Loader, RefreshCw } from 'lucide-react';
import { getTokenSet } from '../services/api';
import { getTelegramId } from '../services/telegram';
import TokenCard from '../components/TokenCard';

interface Token {
  _id: string;
  address: string;
  chain: string;
  name: string;
  symbol: string;
  price_usd: number;
  liquidity_usd: number;
  volume_24h: number;
  image_url: string;
}

interface TokenSet {
  user_id: string;
  telegram_id: string;
  tokens: Token[];
  created_at: string;
  updated_at: string;
}

const TokensPage: React.FC = () => {
  const [tokenSet, setTokenSet] = useState<TokenSet | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const loadTokens = async () => {
    try {
      setLoading(true);
      setError('');
      const telegramId = getTelegramId();
      const result = await getTokenSet(telegramId);
      console.log('Token set:', result);
      setTokenSet(result);
    } catch (error) {
      console.error('Error loading tokens:', error);
      setError(error instanceof Error ? error.message : 'An unknown error occurred');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTokens();

    if (window.Telegram?.WebApp) {
      const webApp = window.Telegram.WebApp;
      webApp.MainButton.setText('Refresh Tokens').show().onClick(loadTokens);

      return () => {
        webApp.MainButton.offClick(loadTokens);
        webApp.MainButton.hide();
      };
    }
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-blue-500 to-purple-600 text-white">
        <Loader className="animate-spin mr-2" size={32} /> Loading...
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-blue-500 to-purple-600 text-white">
        <div className="bg-red-500 bg-opacity-50 p-6 rounded-lg text-center">
          <p className="text-xl mb-4">Error loading tokens: {error}</p>
          <button
            onClick={loadTokens}
            className="bg-white text-red-500 px-4 py-2 rounded-full flex items-center justify-center hover:bg-red-100 transition duration-300"
          >
            <RefreshCw className="mr-2" size={18} /> Retry
          </button>
        </div>
      </div>
    );
  }

  if (!tokenSet || !tokenSet.tokens || tokenSet.tokens.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-blue-500 to-purple-600 text-white">
        <p className="text-xl text-center bg-white bg-opacity-10 backdrop-blur-lg rounded-lg p-8">
          No tokens found. Try adjusting your filters.
        </p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-r from-blue-500 to-purple-600 text-white p-4">
      <div className="max-w-4xl mx-auto">
        <Link to="/" className="inline-flex items-center text-white mb-6 hover:text-blue-200 transition duration-300">
          <ArrowLeft className="mr-2" /> Back to Home
        </Link>
        <h1 className="text-3xl font-bold mb-6">Tokens</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {tokenSet.tokens.map((token) => (
            <TokenCard key={token._id} token={token} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default TokensPage;
