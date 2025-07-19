import React from 'react';
import type { Company } from '../../types/company';
import { CompanyCard } from '../CompanyCard/CompanyCard';
import styles from '../../styles/company-grid.module.css';

interface CompanyGridProps {
  companies: Company[];
  onDetails?: (company: Company) => void;
}

export const CompanyGrid: React.FC<CompanyGridProps> = ({ companies, onDetails }) => {
  if (!companies.length) {
    return (
      <div className="flex flex-col items-center justify-center py-16 text-center text-gray-500">
        <svg width="64" height="64" fill="none" viewBox="0 0 64 64" aria-hidden="true" className="mb-4">
          <rect x="8" y="24" width="48" height="32" rx="4" fill="#f3f4f6" />
          <rect x="16" y="32" width="32" height="8" rx="2" fill="#e5e7eb" />
          <rect x="16" y="44" width="20" height="4" rx="2" fill="#e5e7eb" />
        </svg>
        <div className="text-lg font-semibold mb-2">No companies found</div>
        <div className="text-sm text-gray-400">Try adjusting your search or filters.</div>
      </div>
    );
  }
  return (
    <div className={styles['company-grid']}>
      {companies.map(company => (
        <CompanyCard key={company.id} company={company} onDetails={onDetails} />
      ))}
    </div>
  );
}; 