import React from 'react';
import { SearchBar } from '../SearchBar/SearchBar';

interface HeroSectionProps {
  onSearch?: (query: string) => void;
}

export const HeroSection: React.FC<HeroSectionProps> = ({ onSearch }) => {
  return (
    <section className="bg-gray-50 py-16 md:py-24 border-b border-gray-100" aria-label="Search companies">
      <div className="max-w-3xl mx-auto px-4 text-center">
        <span className="inline-block bg-primary-50 text-primary-700 font-semibold px-4 py-1 rounded-full text-sm mb-6">
          Enjoy a 40% discount on early bird prices 🎉
        </span>
        <h1 className="text-4xl md:text-5xl font-extrabold text-gray-900 mb-8 leading-tight">
          Find
          <span className="text-primary-600 mx-1">Company</span>
          Worldwide You Want.<br />
          Power by <span className="text-primary-600">AI</span>
        </h1>
        <div className="mt-8">
          <SearchBar onSearch={onSearch} />
        </div>
      </div>
    </section>
  );
}; 