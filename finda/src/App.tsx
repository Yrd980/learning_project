import React, { useState, useMemo, useCallback } from 'react';
import { Header } from './components/Header/Header';
import { HeroSection } from './components/HeroSection/HeroSection';
import { CompanyGrid } from './components/CompanyGrid/CompanyGrid';
import { TrustSection } from './components/TrustSection/TrustSection';
import type { Company } from './types/company';
import type { Partner } from './types/partner';
import { useInfiniteScroll } from './hooks/useInfiniteScroll';

const mockCompanies: Company[] = [
  {
    id: '1',
    name: 'OpenAI',
    logo: 'https://logo.clearbit.com/openai.com',
    category: 'Artificial Intelligence',
    location: 'San Francisco, CA',
    employees: 375,
  },
  {
    id: '2',
    name: 'Stripe',
    logo: 'https://logo.clearbit.com/stripe.com',
    category: 'Fintech',
    location: 'San Francisco, CA',
    employees: 7000,
  },
  {
    id: '3',
    name: 'Shopify',
    logo: 'https://logo.clearbit.com/shopify.com',
    category: 'E-commerce',
    location: 'Ottawa, Canada',
    employees: 10000,
  },
  {
    id: '4',
    name: 'Figma',
    logo: 'https://logo.clearbit.com/figma.com',
    category: 'Design',
    location: 'San Francisco, CA',
    employees: 1200,
  },
  {
    id: '5',
    name: 'Notion',
    logo: 'https://logo.clearbit.com/notion.so',
    category: 'Productivity',
    location: 'San Francisco, CA',
    employees: 500,
  },
  // Add more for demo
  ...Array.from({ length: 30 }, (_, i) => ({
    id: `${i + 6}`,
    name: `Demo Company ${i + 6}`,
    logo: 'https://logo.clearbit.com/example.com',
    category: 'Demo Category',
    location: 'Demo City',
    employees: 100 + i * 10,
  })),
];

const mockPartners: Partner[] = [
  { id: '1', name: 'Google', logo: 'https://logo.clearbit.com/google.com' },
  { id: '2', name: 'Microsoft', logo: 'https://logo.clearbit.com/microsoft.com' },
  { id: '3', name: 'Amazon', logo: 'https://logo.clearbit.com/amazon.com' },
  { id: '4', name: 'Meta', logo: 'https://logo.clearbit.com/meta.com' },
  { id: '5', name: 'Netflix', logo: 'https://logo.clearbit.com/netflix.com' },
  { id: '6', name: 'Slack', logo: 'https://logo.clearbit.com/slack.com' },
  { id: '7', name: 'Dropbox', logo: 'https://logo.clearbit.com/dropbox.com' },
  { id: '8', name: 'Zoom', logo: 'https://logo.clearbit.com/zoom.us' },
];

const PAGE_SIZE = 12;

function App() {
  const [companies] = useState<Company[]>(mockCompanies);
  const [partners] = useState<Partner[]>(mockPartners);
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);

  const filteredCompanies = useMemo(() => {
    if (!search.trim()) return companies;
    const q = search.trim().toLowerCase();
    return companies.filter(c =>
      c.name.toLowerCase().includes(q) ||
      c.category.toLowerCase().includes(q) ||
      c.location.toLowerCase().includes(q)
    );
  }, [companies, search]);

  const pagedCompanies = useMemo(
    () => filteredCompanies.slice(0, page * PAGE_SIZE),
    [filteredCompanies, page]
  );
  const hasMore = pagedCompanies.length < filteredCompanies.length;

  const loadMore = useCallback(() => {
    if (!hasMore || loading) return;
    setLoading(true);
    setTimeout(() => {
      setPage(p => p + 1);
      setLoading(false);
    }, 600); // Simulate network delay
  }, [hasMore, loading]);

  const lastElementRef = useInfiniteScroll({
    loading,
    hasMore,
    onLoadMore: loadMore,
  });

  // Reset page on new search
  React.useEffect(() => {
    setPage(1);
  }, [search]);

  return (
    <>
      <Header />
      <HeroSection onSearch={setSearch} />
      <main className="max-w-7xl mx-auto px-4 py-12">
        <CompanyGrid companies={pagedCompanies} />
        {pagedCompanies.length > 0 && (
          <div ref={hasMore ? lastElementRef : undefined} className="flex justify-center py-8">
            {loading && (
              <span className="text-primary-600 font-medium animate-pulse">Loading more companies...</span>
            )}
          </div>
        )}
      </main>
      <TrustSection partners={partners} />
    </>
  );
}

export default App; 