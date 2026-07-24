import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { MemoryRouter } from "react-router-dom";
import { AuthProvider } from "../context/AuthContext";
import Navbar from "../components/layout/Navbar";

vi.mock("../services/api", () => ({
  authApi: {
    getMe: vi.fn().mockRejectedValue(new Error("no token")),
  },
}));

const renderNavbar = () =>
  render(
    <MemoryRouter>
      <AuthProvider>
        <Navbar />
      </AuthProvider>
    </MemoryRouter>,
  );

describe("Navbar", () => {
  it("renders home link", () => {
    renderNavbar();
    expect(screen.getByText("Home")).toBeInTheDocument();
  });

  it("shows login button when not authenticated", () => {
    renderNavbar();
    expect(screen.getByText("Login")).toBeInTheDocument();
  });

  it("shows the project title", () => {
    renderNavbar();
    expect(screen.getByText(/NLP & Digital Preservation/i)).toBeInTheDocument();
  });
});
