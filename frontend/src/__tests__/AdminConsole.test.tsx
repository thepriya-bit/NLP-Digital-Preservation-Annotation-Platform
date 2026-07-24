import { render, screen, waitFor } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { MemoryRouter } from "react-router-dom";
import { AuthProvider } from "../context/AuthContext";
import { ToastProvider } from "../components/Toast";
import AdminConsole from "../pages/AdminConsole";

vi.mock("../services/api", () => ({
  adminApi: {
    getUsers: vi.fn().mockResolvedValue([
      { id: 1, username: "admin1", email: "admin@test.com", role: "admin", trust_score: 10, is_banned: false, created_at: "2026-01-01" },
      { id: 2, username: "user1", email: "user@test.com", role: "annotator", trust_score: 5, is_banned: true, created_at: "2026-01-02" },
    ]),
    getStats: vi.fn().mockResolvedValue({
      total_users: 2,
      total_phrases: 10,
      total_annotations: 5,
      verified_annotations: 3,
      pending_verification: 2,
      language_distribution: { assamese: 10 },
    }),
    banUser: vi.fn(),
    unbanUser: vi.fn(),
    cleanupOrphans: vi.fn().mockResolvedValue({ orphans_found: 3, deleted: 2, errors: 0 }),
    getDashboard: vi.fn().mockResolvedValue({ recent_users: [], recent_annotations: [] }),
  },
  exportApi: {
    downloadCsv: vi.fn().mockResolvedValue(new Blob()),
    downloadJson: vi.fn().mockResolvedValue(new Blob()),
    downloadParquet: vi.fn().mockResolvedValue(new Blob()),
    getStats: vi.fn().mockResolvedValue({
      total_annotations: 5,
      verified_annotations: 3,
      pending_verification: 2,
      language_distribution: {},
    }),
  },
  authApi: {
    getMe: vi.fn().mockRejectedValue(new Error("no token")),
  },
}));

const renderAdmin = () =>
  render(
    <MemoryRouter>
      <AuthProvider>
        <ToastProvider>
          <AdminConsole />
        </ToastProvider>
      </AuthProvider>
    </MemoryRouter>,
  );

describe("AdminConsole", () => {
  it("renders admin heading", () => {
    renderAdmin();
    expect(screen.getByText(/Platform Administration/i)).toBeInTheDocument();
  });

  it("shows all tabs", () => {
    renderAdmin();
    expect(screen.getByText("Users")).toBeInTheDocument();
    expect(screen.getByText("Stats")).toBeInTheDocument();
    expect(screen.getByText("Cleanup")).toBeInTheDocument();
    expect(screen.getByText("Export")).toBeInTheDocument();
  });

  it("loads and displays users", async () => {
    renderAdmin();
    await waitFor(() => {
      expect(screen.getByText("admin1")).toBeInTheDocument();
      expect(screen.getByText("user1")).toBeInTheDocument();
    });
  });

  it("shows ban/unban buttons", async () => {
    renderAdmin();
    await waitFor(() => {
      expect(screen.getAllByText(/Ban|Unban/).length).toBeGreaterThan(0);
    });
  });
});
