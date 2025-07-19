export interface User {
  name: string;
}

export type Name = string;

export interface GetUsersRequestParams {
  page?: number;
  pageSize?: number;
  searchQuery?: string;
}

export interface GetUsersResponse {
  data: User[];
  total: number;
}

export interface UserState {
  userId: string | null;
  userName: string | null;
  login: (id: string, name: string) => void;
  logout: () => void;
}
