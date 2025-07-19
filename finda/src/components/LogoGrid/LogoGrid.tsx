import React from 'react';
import type { Partner } from '../../types/partner';

interface LogoGridProps {
  partners: Partner[];
}

export const LogoGrid: React.FC<LogoGridProps> = ({ partners }) => {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6 items-center justify-items-center mt-6">
      {partners.map(partner => (
        <img
          key={partner.id}
          src={partner.logo}
          alt={partner.name}
          className="h-10 w-auto object-contain grayscale opacity-80 hover:grayscale-0 hover:opacity-100 transition"
          loading="lazy"
          decoding="async"
        />
      ))}
    </div>
  );
}; 