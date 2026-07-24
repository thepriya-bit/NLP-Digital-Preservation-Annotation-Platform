import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const api = axios.create({ baseURL: API_BASE, timeout: 30000 });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem("access_token");
      window.location.href = "/login";
    }
    if (err.code === "ECONNABORTED") {
      err.message = "Request timed out. Please check your connection.";
    }
    return Promise.reject(err);
  },
);

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: {
    id: number;
    username: string;
    email: string;
    role: string;
    trust_score: number;
    is_banned: boolean;
    created_at: string;
  };
}

export interface RawPhrase {
  id: number;
  language: string;
  phrase: string;
  audio_url: string | null;
  submitted_by: number;
  status: string;
  created_at?: string;
}

export interface AnnotationCreate {
  raw_phrase_id: number;
  translated_text: string;
  pos_tags?: Record<string, unknown> | null;
  named_entities?: Record<string, unknown> | null;
  syntax?: Record<string, unknown> | null;
}

export interface Annotation {
  id: number;
  raw_phrase_id: number;
  translated_text: string;
  pos_tags: Record<string, unknown> | null;
  named_entities: Record<string, unknown> | null;
  syntax: Record<string, unknown> | null;
  created_by: number;
  created_at?: string;
}

export interface SyntaxTagResponse {
  tokens: string[];
  pos_tags: { token: string; pos: string }[];
  named_entities: { token: string; label: string }[];
  syntax_tree: Record<string, unknown> | null;
}

export interface PendingAnnotation {
  id: number;
  raw_phrase_id: number;
  translated_text: string;
  created_by: number;
  created_at: string;
  approve_count: number;
  reject_count: number;
}

export interface VerificationResult {
  success: boolean;
  verification: {
    id: number;
    annotation_id: number;
    verifier_id: number;
    vote: string;
    comment: string | null;
    created_at: string;
  } | null;
  annotation_status: string | null;
  error: string | null;
}

export interface PlatformStats {
  total_users: number;
  total_phrases: number;
  total_annotations: number;
  verified_annotations: number;
  pending_verification: number;
  language_distribution: Record<string, number>;
}

export interface AdminUser {
  id: number;
  username: string;
  email: string;
  role: string;
  trust_score: number;
  is_banned: boolean;
  created_at: string;
}

export interface DashboardData {
  recent_users: { id: number; username: string; role: string; trust_score: number; is_banned: boolean }[];
  recent_annotations: { id: number; translated_text: string; created_by: number }[];
}

export const authApi = {
  login: async (username: string, password: string): Promise<TokenResponse> => {
    const { data } = await api.post<TokenResponse>("/auth/login", { username, password });
    return data;
  },
  register: async (username: string, email: string, password: string, role: string): Promise<TokenResponse> => {
    const { data } = await api.post<TokenResponse>("/auth/register", { username, email, password, role });
    return data;
  },
  getMe: async () => {
    const { data } = await api.get<TokenResponse["user"]>("/auth/me");
    return data;
  },
};

export const phrasesApi = {
  getRandom: async (): Promise<RawPhrase> => {
    const { data } = await api.get<RawPhrase>("/phrases/random");
    return data;
  },
  list: async (params?: { status?: string; language?: string; skip?: number; limit?: number }): Promise<RawPhrase[]> => {
    const { data } = await api.get<RawPhrase[]>("/phrases", { params });
    return data;
  },
};

export const annotationsApi = {
  create: async (payload: AnnotationCreate): Promise<Annotation> => {
    const { data } = await api.post<Annotation>("/annotations", payload);
    return data;
  },
  list: async (params?: { raw_phrase_id?: number; created_by?: number; skip?: number; limit?: number }): Promise<Annotation[]> => {
    const { data } = await api.get<Annotation[]>("/annotations", { params });
    return data;
  },
  getMy: async (): Promise<Annotation[]> => {
    const { data } = await api.get<Annotation[]>("/annotations/my");
    return data;
  },
};

export const syntaxApi = {
  tag: async (text: string, language = "assamese"): Promise<SyntaxTagResponse> => {
    const { data } = await api.post<SyntaxTagResponse>("/syntax/tag", { text, language });
    return data;
  },
};

export const audioApi = {
  upload: async (file: Blob, filename: string): Promise<{ audio_url: string; filename: string }> => {
    const form = new FormData();
    form.append("file", file, filename);
    const { data } = await api.post<{ audio_url: string; filename: string }>("/audio/upload", form, {
      timeout: 120000,
    });
    return data;
  },
};

export const verificationApi = {
  getPending: async (skip = 0, limit = 20): Promise<PendingAnnotation[]> => {
    const { data } = await api.get<PendingAnnotation[]>("/verifications/pending", { params: { skip, limit } });
    return data;
  },
  castVote: async (annotation_id: number, vote: "approve" | "reject", comment?: string): Promise<VerificationResult> => {
    const { data } = await api.post<VerificationResult>("/verifications", { annotation_id, vote, comment });
    return data;
  },
  getMyVotes: async (skip = 0, limit = 20) => {
    const { data } = await api.get("/verifications/my", { params: { skip, limit } });
    return data;
  },
  getVotesForAnnotation: async (annotation_id: number) => {
    const { data } = await api.get(`/verifications/${annotation_id}`);
    return data;
  },
};

export const exportApi = {
  downloadCsv: async (params?: { language?: string; date_from?: string; date_to?: string; min_trust_score?: number }): Promise<Blob> => {
    const { data } = await api.get("/export/csv", { params, responseType: "blob", timeout: 60000 });
    return data;
  },
  downloadJson: async (params?: { language?: string; date_from?: string; date_to?: string; min_trust_score?: number }): Promise<Blob> => {
    const { data } = await api.get("/export/json", { params, responseType: "blob", timeout: 60000 });
    return data;
  },
  downloadParquet: async (params?: { language?: string; date_from?: string; date_to?: string; min_trust_score?: number }): Promise<Blob> => {
    const { data } = await api.get("/export/parquet", { params, responseType: "blob", timeout: 60000 });
    return data;
  },
  getStats: async (): Promise<PlatformStats> => {
    const { data } = await api.get<PlatformStats>("/export/stats");
    return data;
  },
};

export const adminApi = {
  getUsers: async (): Promise<AdminUser[]> => {
    const { data } = await api.get<AdminUser[]>("/admin/users");
    return data;
  },
  banUser: async (userId: number): Promise<{ message: string }> => {
    const { data } = await api.post<{ message: string }>(`/admin/users/${userId}/ban`);
    return data;
  },
  unbanUser: async (userId: number): Promise<{ message: string }> => {
    const { data } = await api.post<{ message: string }>(`/admin/users/${userId}/unban`);
    return data;
  },
  getStats: async (): Promise<PlatformStats> => {
    const { data } = await api.get<PlatformStats>("/admin/stats");
    return data;
  },
  getDashboard: async (): Promise<DashboardData> => {
    const { data } = await api.get<DashboardData>("/admin/dashboard");
    return data;
  },
  cleanupOrphans: async (): Promise<{ orphans_found: number; deleted: number; errors: number }> => {
    const { data } = await api.post<{ orphans_found: number; deleted: number; errors: number }>("/admin/cleanup/orphans");
    return data;
  },
};
