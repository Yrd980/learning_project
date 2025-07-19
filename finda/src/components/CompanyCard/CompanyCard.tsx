import React from 'react';
import type { Company } from '../../types/company';
import styles from './company-card.module.css';

interface CompanyCardProps {
  company: Company;
  onDetails?: (company: Company) => void;
}

export const CompanyCard: React.FC<CompanyCardProps> = ({ company, onDetails }) => {
  return (
    <div className={styles['company-card']} tabIndex={0} aria-label={`View details for ${company.name}`}>
      <img
        src={company.logo}
        alt={company.name}
        className="w-16 h-16 object-contain mb-4 rounded bg-gray-100"
        loading="lazy"
        decoding="async"
      />
      <div className="mb-4">
        <div className="font-bold text-lg text-gray-900 mb-1">{company.name}</div>
        <div className="text-primary-600 text-sm font-medium mb-1">{company.category}</div>
        <div className="text-gray-500 text-sm mb-1">{company.location}</div>
        <div className="text-gray-400 text-xs">{company.employees} employees</div>
      </div>
      <button
        className="mt-auto px-4 py-2 rounded-full bg-primary-500 text-white font-semibold hover:bg-primary-600 transition-colors"
        onClick={() => onDetails?.(company)}
      >
        Details
      </button>
    </div>
  );
}; 
