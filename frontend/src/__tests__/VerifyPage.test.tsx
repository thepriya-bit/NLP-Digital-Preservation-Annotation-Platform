import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { MemoryRouter } from "react-router-dom";
import { AuthProvider } from "../context/AuthContext";
import { ToastProvider } from "../components/Toast";
import VerifyPage from "../pages/VerifyPage";

const mockPending = [
  {
    id: 1,
    raw_phrase_id: 1,
    translated_text: "Hello",
    created_by: 2,
    created_at: "2026-01-01T00:00:00",
    approve_count: 0,
    reject_count: 0,
  },
];

vi.mock("../services/api", () => ({
  verificationApi: {
    getPending: vi.fn().mockResolvedValue(mockPending),
    castVote: vi.fn().mockResolvedValue({ success: true, annotation_status: null }),
    getMyVotes: vi.fn().mockResolvedValue([]),
  },
  phrasesApi: {
    list: vi.fn().mockResolvedValue([{ id: 1, phrase: "নমস্কাৰ", language: "assamese" }]),
    getRandom: vi.fn().mockResolvedValue({ id: 1, phrase: "নমস্কাৰ", language: "assamese" }),
  },
  authApi: {
    getMe: vi.fn().mockRejectedValue(new Error("no token")),
  },
}));

const renderVerify = () =>
  render(
    <MemoryRouter>
      <AuthProvider>
        <ToastProvider>
          <VerifyPage />
        </ToastProvider>
      </AuthProvider>
    </MemoryRouter>,
  );

describe("VerifyPage", () => {
  it("renders verification workspace heading", async () => {
    renderVerify();
    await waitFor(() => {
      expect(screen.getByText(/Verification workspace/i)).toBeInTheDocument();
    });
  });

  it("shows the pending translation", async () => {
    renderVerify();
    await waitFor(() => {
      expect(screen.getByText("Hello")).toBeInTheDocument();
    });
  });

  it("shows approve and reject buttons", async () => {
    renderVerify();
    await waitFor(() => {
      expect(screen.getByText("Approve")).toBeInTheDocument();
      expect(screen.getByText("Reject")).toBeInTheDocument();
    });
  });

  it("allows selecting approve vote", async () => {
    renderVerify();
    await waitFor(() => {
      expect(screen.getByText("Approve")).toBeInTheDocument();
    });
    fireEvent.click(screen.getByText("Approve"));
    const submitBtn = screen.getByText("Submit Vote");
    expect(submitBtn).not.toBeDisabled();
  });

  it("submit vote triggers api call", async () => {
    renderVerify();
    await waitFor(() => {
      expect(screen.getByText("Hello")).toBeInTheDocument();
    });
    fireEvent.click(screen.getByText("Approve"));
    fireEvent.click(screen.getByText("Submit Vote"));
    await waitFor(() => {
      const { verificationApi } = require("../services/api");
      expect(verificationApi.castVote).toHaveBeenCalledWith(1, "approve", undefined);
    });
  });
});
