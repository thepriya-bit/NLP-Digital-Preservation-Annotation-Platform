import { createContext, useContext, useState, useEffect, useCallback, type ReactNode } from "react";
import { useNavigate } from "react-router-dom";
import { authApi } from "../services/api";

export interface User {
  id: number;
  username: string;
  email: string;
  role: string;
  trust_score: number;
  created_at: string;
}

interface AuthContextValue {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string, role: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(() => localStorage.getItem("access_token"));
  const navigate = useNavigate();

  useEffect(() => {
    if (token) {
      authApi.getMe().then(setUser).catch(() => {
        localStorage.removeItem("access_token");
        setToken(null);
        setUser(null);
      });
    }
  }, [token]);

  const login = useCallback(async (username: string, password: string) => {
    const res = await authApi.login(username, password);
    localStorage.setItem("access_token", res.access_token);
    setToken(res.access_token);
    setUser(res.user);
    navigate("/dashboard");
  }, [navigate]);

  const register = useCallback(async (username: string, email: string, password: string, role: string) => {
    const res = await authApi.register(username, email, password, role);
    localStorage.setItem("access_token", res.access_token);
    setToken(res.access_token);
    setUser(res.user);
    navigate("/dashboard");
  }, [navigate]);

  const logout = useCallback(() => {
    localStorage.removeItem("access_token");
    setToken(null);
    setUser(null);
    navigate("/");
  }, [navigate]);

  return (
    <AuthContext.Provider value={{ user, token, isAuthenticated: !!token && !!user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
  return ctx;
};
