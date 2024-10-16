import React, { useState } from 'react';
import { ArrowLeft, Filter, Sliders, DollarSign, Calendar, Hash } from 'lucide-react';
import { Link } from 'react-router-dom';
import { updateFilters } from '../services/api';
import { getTelegramId } from '../services/telegram';

interface Filters {
  minLiquidity: string;
  maxLiquidity: string;
  minMarketCap: string;
  maxMarketCap: string;
  minFullyDilutedValuation: string;
  maxFullyDilutedValuation: string;
  minAge: string;
  maxAge: string;
  minTransactions: string;
  maxTransactions: string;
}

const FilterPage: React.FC = () => {
  const [filters, setFilters] = useState<Filters>({
    minLiquidity: '',
    maxLiquidity: '',
    minMarketCap: '',
    maxMarketCap: '',
    minFullyDilutedValuation: '',
    maxFullyDilutedValuation: '',
    minAge: '',
    maxAge: '',
    minTransactions: '',
    maxTransactions: '',
  });
  const [message, setMessage] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    if (/^\d*\.?\d*$/.test(value) || value === '') {
      setFilters(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const telegramId = getTelegramId();
      await updateFilters(telegramId, filters);
      setMessage(`Filters updated successfully.`);
    } catch (error) {
      setMessage(`Error updating filters: ${error}`);
    }
  };

  const getIcon = (key: string) => {
    if (key.includes('Liquidity') || key.includes('MarketCap') || key.includes('FullyDilutedValuation')) {
      return <DollarSign className="text-blue-300" size={18} />;
    } else if (key.includes('Age')) {
      return <Calendar className="text-green-300" size={18} />;
    } else if (key.includes('Transactions')) {
      return <Hash className="text-purple-300" size={18} />;
    }
    return null;
  };

  const getLabelText = (key: string) => {
    const prefix = key.startsWith('min') ? 'Min ' : 'Max ';
    const baseText = key.replace(/^(min|max)/, '');
    let label = prefix + baseText.split(/(?=[A-Z])/).join(' ');
    if (key.includes('Age')) {
      label += ' (hours)';
    }
    return label;
  };

  return (
    <div className="min-h-screen bg-gradient-to-r from-blue-500 to-purple-600 text-white p-4 sm:p-8">
      <div className="max-w-4xl mx-auto">
        <Link to="/" className="inline-flex items-center text-white mb-8 hover:text-blue-200 transition duration-300">
          <ArrowLeft className="mr-2" /> Back to Home
        </Link>
        <div className="bg-white bg-opacity-10 backdrop-blur-lg rounded-lg shadow-lg p-6 sm:p-8">
          <h1 className="text-3xl font-bold mb-6 flex items-center">
            <Sliders className="mr-3 text-yellow-300" /> Set Filters
          </h1>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              {Object.entries(filters).map(([key, value]) => (
                <div key={key} className="relative">
                  <label htmlFor={key} className="block text-sm font-medium mb-1 flex items-center">
                    {getIcon(key)}
                    <span className="ml-2">{getLabelText(key)}</span>
                  </label>
                  <input
                    type="text"
                    id={key}
                    name={key}
                    value={value}
                    onChange={handleChange}
                    className="w-full bg-white bg-opacity-20 rounded-md border border-white border-opacity-30 px-3 py-2 text-white placeholder-white placeholder-opacity-50 focus:outline-none focus:ring-2 focus:ring-blue-300 focus:border-transparent transition duration-300"
                    placeholder={`Enter ${getLabelText(key)}`}
                  />
                </div>
              ))}
            </div>
            <button type="submit" className="w-full bg-gradient-to-r from-blue-400 to-purple-500 text-white py-3 px-4 rounded-full hover:from-blue-500 hover:to-purple-600 transition duration-300 flex items-center justify-center shadow-lg">
              <Filter className="mr-2" /> Apply Filters
            </button>
          </form>
          {message && (
            <div className={`mt-6 p-4 rounded-lg ${message.includes('Error') ? 'bg-red-500 bg-opacity-50' : 'bg-green-500 bg-opacity-50'} flex items-center justify-center`}>
              {message.includes('Error') ? (
                <svg className="w-6 h-6 mr-2 text-red-200" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              ) : (
                <svg className="w-6 h-6 mr-2 text-green-200" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              )}
              <span className="text-center">{message}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default FilterPage;
