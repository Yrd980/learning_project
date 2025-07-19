import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { companyApi } from '../services/api';

// Query keys
export const companyKeys = {
  all: ['companies'] as const,
  lists: () => [...companyKeys.all, 'list'] as const,
  list: (filters: any) => [...companyKeys.lists(), filters] as const,
  details: () => [...companyKeys.all, 'detail'] as const,
  detail: (id: string) => [...companyKeys.details(), id] as const,
};

// Types
export interface Company {
  id: string;
  name: string;
  description: string;
  logo?: string;
  website?: string;
  industry: string;
  size: 'startup' | 'small' | 'medium' | 'large';
  location: string;
  founded?: string;
  createdAt: string;
  updatedAt: string;
}

export interface CompanyFilters {
  page?: number;
  limit?: number;
  search?: string;
  industry?: string;
  size?: string;
  location?: string;
}

// Queries
export const useCompanies = (filters: CompanyFilters = {}) => {
  return useQuery({
    queryKey: companyKeys.list(filters),
    queryFn: () => companyApi.getCompanies(filters),
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
};

export const useCompany = (id: string) => {
  return useQuery({
    queryKey: companyKeys.detail(id),
    queryFn: () => companyApi.getCompany(id),
    enabled: !!id,
    staleTime: 1000 * 60 * 10, // 10 minutes
  });
};

// Mutations
export const useCreateCompany = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (companyData: Omit<Company, 'id' | 'createdAt' | 'updatedAt'>) =>
      companyApi.createCompany(companyData),
    onSuccess: () => {
      // Invalidate and refetch companies list
      queryClient.invalidateQueries({ queryKey: companyKeys.lists() });
    },
  });
};

export const useUpdateCompany = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, companyData }: { id: string; companyData: Partial<Company> }) =>
      companyApi.updateCompany(id, companyData),
    onSuccess: (data, { id }) => {
      // Update the company in cache
      queryClient.setQueryData(companyKeys.detail(id), data);
      // Invalidate companies list
      queryClient.invalidateQueries({ queryKey: companyKeys.lists() });
    },
  });
};

export const useDeleteCompany = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (id: string) => companyApi.deleteCompany(id),
    onSuccess: (_, id) => {
      // Remove company from cache
      queryClient.removeQueries({ queryKey: companyKeys.detail(id) });
      // Invalidate companies list
      queryClient.invalidateQueries({ queryKey: companyKeys.lists() });
    },
  });
}; 