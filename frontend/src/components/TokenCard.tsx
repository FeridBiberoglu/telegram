import React from 'react';
import { DollarSign, Droplet, BarChart3 } from 'lucide-react';

interface TokenCardProps {
  token: {
    name: string;
    symbol: string;
    image_url: string;
    price_usd: number;
    liquidity_usd: number;
    volume_24h: number;
  };
}

const TokenCard: React.FC<TokenCardProps> = ({ token }) => {
  return (
    <div className="bg-white bg-opacity-10 backdrop-blur-lg rounded-lg shadow-lg p-6 hover:bg-opacity-20 transition duration-300">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-semibold flex items-center">
          {token.name}
          <span className="text-blue-300 ml-2 text-lg">({token.symbol})</span>
        </h2>
        {token.image_url && (
          <img 
            src={token.image_url} 
            alt={`${token.name} logo`} 
            className="w-10 h-10 rounded-full object-cover"
            onError={(e) => {
              (e.target as HTMLImageElement).onerror = null;
              (e.target as HTMLImageElement).src = 'https://via.placeholder.com/40';
            }}
          />
        )}
      </div>
      <div className="grid grid-cols-1 gap-3 text-sm">
        <div className="flex items-center justify-between bg-white bg-opacity-5 rounded-lg p-3">
          <div className="flex items-center">
            <DollarSign className="mr-2 text-green-400" size={18} />
            <span className="font-medium">Price:</span>
          </div>
          <p className="font-bold">${token.price_usd?.toFixed(6) || 'N/A'}</p>
        </div>
        <div className="flex items-center justify-between bg-white bg-opacity-5 rounded-lg p-3">
          <div className="flex items-center">
            <Droplet className="mr-2 text-blue-400" size={18} />
            <span className="font-medium">Liquidity:</span>
          </div>
          <p className="font-bold">${token.liquidity_usd?.toLocaleString() || 'N/A'}</p>
        </div>
        <div className="flex items-center justify-between bg-white bg-opacity-5 rounded-lg p-3">
          <div className="flex items-center">
            <BarChart3 className="mr-2 text-purple-400" size={18} />
            <span className="font-medium">24h Volume:</span>
          </div>
          <p className="font-bold">${token.volume_24h?.toLocaleString() || 'N/A'}</p>
        </div>
      </div>
    </div>
  );
};

export default TokenCard;