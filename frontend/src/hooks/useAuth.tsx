import React, { createContext, ReactNode, useContext, useEffect, useState } from 'react';
import { api } from '../lib/api';

interface AuthContextValue {
  token: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  login: (access: string, refresh: string) => void;
  logout: () => void;
  refresh: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('token'));
  const [refreshToken, setRefreshToken] = useState<string | null>(() => localStorage.getItem('refreshToken'));

  // Persist changes
  useEffect(() => {
    if (token) localStorage.setItem('token', token);
    else localStorage.removeItem('token');
  }, [token]);

  useEffect(() => {
    if (refreshToken) localStorage.setItem('refreshToken', refreshToken);
    else localStorage.removeItem('refreshToken');
  }, [refreshToken]);

  const login = (access: string, refresh: string) => {
    setToken(access);
    setRefreshToken(refresh);
  };

  const logout = () => {
    setToken(null);
    setRefreshToken(null);
  };

  const refresh = async () => {
    if (!refreshToken) throw new Error('No refresh token');
    const { data } = await api.post<{ access: string; refresh?: string }>('/token/refresh/', {
      refresh: refreshToken,
    });
    setToken(data.access);
    if (data.refresh) {
      setRefreshToken(data.refresh);
    }
  };

  const value: AuthContextValue = {
    token,
    refreshToken,
    isAuthenticated: Boolean(token),
    login,
    logout,
    refresh,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within an AuthProvider');
  return ctx;
} 