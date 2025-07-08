import { create } from "zustand";
import { UserState } from "@/types/user";

export const useUserStore = create<UserState>()((set) => ({
  userId: null,
  useName: null,
  login: (id: string, name: string) => set({ userId: id, userName: name }),
  logout: () => set({ userId: null, userName: null }),
}));
