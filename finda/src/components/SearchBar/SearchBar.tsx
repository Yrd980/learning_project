import React, { useState, useEffect } from 'react';
import { Search } from 'lucide-react';
import { useDebounce } from '../../hooks/useDebounce';
import styles from './search-bar.module.css';

interface SearchBarProps {
  onSearch?: (query: string) => void;
}

export const SearchBar: React.FC<SearchBarProps> = ({ onSearch }) => {
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebounce(query, 300);

  useEffect(() => {
    if (onSearch) onSearch(debouncedQuery);
  }, [debouncedQuery, onSearch]);

  return (
    <form
      className={styles['search-container']}
      role="search"
      onSubmit={e => {
        e.preventDefault();
        if (onSearch) onSearch(query);
      }}
    >
      <input
        className={styles['search-input']}
        type="search"
        aria-label="Search for companies"
        placeholder="Search for companies..."
        value={query}
        onChange={e => setQuery(e.target.value)}
      />
      <button
        className={styles['search-button']}
        type="submit"
        aria-label="Search"
      >
        <Search />
      </button>
    </form>
  );
}; 
