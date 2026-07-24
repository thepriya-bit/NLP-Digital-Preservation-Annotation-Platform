import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { MemoryRouter } from "react-router-dom";
import { AuthProvider } from "../context/AuthContext";
import ContributorDashboard from "../pages/ContributorDashboard";

const mockPhrase = { id: 1, phrase: "নমস্কাৰ", language: "assamese" };

vi.mock("../services/api", () => ({
  phrasesApi: {
    getRandom: vi.fn().mockResolvedValue(mockPhrase),
    list: vi.fn().mockResolvedValue([]),
  },
  annotationsApi: {
    create: vi.fn().mockResolvedValue({ id: 1 }),
    getMy: vi.fn().mockResolvedValue([{ id: 1 }]),
  },
  authApi: {
    getMe: vi.fn().mockRejectedValue(new Error("no token")),
  },
  audioApi: {
    upload: vi.fn().mockResolvedValue({ audio_url: "http://example.com/audio.webm", filename: "test.webm" }),
  },
}));

const renderDashboard = () =>
  render(
    <MemoryRouter>
      <AuthProvider>
        <ContributorDashboard />
      </AuthProvider>
    </MemoryRouter>,
  );

describe("ContributorDashboard", () => {
  it("renders loading state then shows phrase", async () => {
    renderDashboard();
    expect(screen.getByText(/Contributor workspace/i)).toBeInTheDocument();
    await waitFor(() => {
      expect(screen.getByText(/নমস্কাৰ/)).toBeInTheDocument();
    });
  });

  it("shows submit button disabled without text", async () => {
    renderDashboard();
    await waitFor(() => {
      expect(screen.getByText("Skip Phrase")).toBeInTheDocument();
    });
    const submitBtn = screen.getByRole("button", { name: /submit contribution/i });
    expect(submitBtn).toBeDisabled();
  });

  it("enables submit when translation is entered", async () => {
    renderDashboard();
    await waitFor(() => {
      expect(screen.getByPlaceholderText(/Type the English translation/)).toBeInTheDocument();
    });
    const textarea = screen.getByPlaceholderText(/Type the English translation/);
    fireEvent.change(textarea, { target: { value: "Hello" } });
    const submitBtn = screen.getByRole("button", { name: /submit contribution/i });
    expect(submitBtn).not.toBeDisabled();
  });

  it("simulates successful submission", async () => {
    renderDashboard();
    await waitFor(() => {
      expect(screen.getByPlaceholderText(/Type the English translation/)).toBeInTheDocument();
    });
    const textarea = screen.getByPlaceholderText(/Type the English translation/);
    fireEvent.change(textarea, { target: { value: "Hello" } });
    const submitBtn = screen.getByRole("button", { name: /submit contribution/i });
    fireEvent.click(submitBtn);
    await waitFor(() => {
      expect(screen.getByText(/Translation submitted successfully/i)).toBeInTheDocument();
    });
  });
});
