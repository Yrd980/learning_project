import React from 'react';
import type { Partner } from '../../types/partner';
import { LogoGrid } from '../LogoGrid/LogoGrid';

interface TrustSectionProps {
  partners: Partner[];
}

export const TrustSection: React.FC<TrustSectionProps> = ({ partners }) => {
  return (
    <section className="py-12 md:py-20 bg-white border-t border-gray-100" aria-label="Trusted by leaders and innovators">
      <div className="max-w-5xl mx-auto px-4 text-center">
        <h2 className="text-xl md:text-2xl font-semibold text-gray-900 mb-4">Trusted by leaders and innovators</h2>
        <LogoGrid partners={partners} />
      </div>
    </section>
  );
}; 