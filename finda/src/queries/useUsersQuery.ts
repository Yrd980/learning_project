import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { userApi } from '../services/api';

// Query keys
export const userKeys = {
  all: ['users'] as const,
  lists: () => [...userKeys.all, 'list'] as const,
  list: (filters: any) => [...userKeys.lists(), filters] as const,
  details: () => [...userKeys.all, 'detail'] as const,
  detail: (id: string) => [...userKeys.details(), id] as const,
};

// Types
export interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string;
  role: string;
  createdAt: string;
  updatedAt: string;
}

export interface UserFilters {
  page?: number;
  limit?: number;
  search?: string;
  role?: string;
}

// Queries
export const useUsers = (filters: UserFilters = {}) => {
  return useQuery({
    queryKey: userKeys.list(filters),
    queryFn: () => userApi.getUsers(filters),
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
};

export const useUser = (id: string) => {
  return useQuery({
    queryKey: userKeys.detail(id),
    queryFn: () => userApi.getUser(id),
    enabled: !!id,
    staleTime: 1000 * 60 * 10, // 10 minutes
  });
};

// Mutations
export const useCreateUser = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (userData: Omit<User, 'id' | 'createdAt' | 'updatedAt'>) =>
      userApi.createUser(userData),
    onSuccess: () => {
      // Invalidate and refetch users list
      queryClient.invalidateQueries({ queryKey: userKeys.lists() });
    },
  });
};

export const useUpdateUser = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, userData }: { id: string; userData: Partial<User> }) =>
      userApi.updateUser(id, userData),
    onSuccess: (data, { id }) => {
      // Update the user in cache
      queryClient.setQueryData(userKeys.detail(id), data);
      // Invalidate users list
      queryClient.invalidateQueries({ queryKey: userKeys.lists() });
    },
  });
};

export const useDeleteUser = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (id: string) => userApi.deleteUser(id),
    onSuccess: (_, id) => {
      // Remove user from cache
      queryClient.removeQueries({ queryKey: userKeys.detail(id) });
      // Invalidate users list
      queryClient.invalidateQueries({ queryKey: userKeys.lists() });
    },
  });
};

