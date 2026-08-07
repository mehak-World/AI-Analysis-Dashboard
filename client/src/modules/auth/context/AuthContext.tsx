// context/AuthContext.tsx
import { createContext, useContext, useEffect, useState } from "react";
import type { ReactNode } from "react";
import apiClient from "../../../api/apiClient"
import { tokenStore } from "../tokenStore";

type User = { id: string; email: string; username: string };

type AuthContextType = {
  user: User | null;
  isLoading: boolean;       // true only during the initial bootstrap check
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  register: (username: string, email: string, password: string) => Promise<void>;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Silent refresh on mount — this is the box in the diagram above
  useEffect(() => {
    const bootstrap = async () => {
      try {
        const { data } = await apiClient.get("/auth/refresh");
        tokenStore.setAccessToken(data.data.accessToken);
        const { data: userData } = await apiClient.get("/auth/me");
        setUser(userData.data);
      } catch {
        tokenStore.clearAccessToken();
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };
    bootstrap();
  }, []);

  const login = async (email: string, password: string) => {
    const { data } = await apiClient.post("/auth/login", { email, password });
    tokenStore.setAccessToken(data.data.accessToken);
    setUser(data.data.user);
    console.log("login() set user to:", data.data.user);
  };

  const register = async (username: string, email: string, password: string) => {
    const { data } = await apiClient.post("/auth/register", { username, email, password });
    tokenStore.setAccessToken(data.data.accessToken);
    setUser(data.data.user);
  };

  const logout = async () => {
    await apiClient.post("/auth/logout").catch(() => {});
    tokenStore.clearAccessToken();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, isAuthenticated: !!user, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
};