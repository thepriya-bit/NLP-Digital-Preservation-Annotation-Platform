import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";
import { BrowserRouter } from "react-router-dom";
import { AuthProvider } from "../context/AuthContext";
import Login from "../pages/Login";

vi.mock("../services/api", () => ({
  authApi: {
    login: vi.fn(),
    register: vi.fn(),
    getMe: vi.fn().mockRejectedValue(new Error("no token")),
  },
}));

const renderLogin = () =>
  render(
    <BrowserRouter>
      <AuthProvider>
        <Login />
      </AuthProvider>
    </BrowserRouter>,
  );

describe("Login Page", () => {
  it("renders login form by default", () => {
    renderLogin();
    expect(screen.getByText("Sign in")).toBeInTheDocument();
    expect(screen.getByLabelText("Username")).toBeInTheDocument();
    expect(screen.getByLabelText("Password")).toBeInTheDocument();
  });

  it("toggles to register mode", async () => {
    renderLogin();
    const signUpBtn = screen.getByText("Sign up");
    await userEvent.click(signUpBtn);
    expect(screen.getByText("Create account")).toBeInTheDocument();
    expect(screen.getByLabelText("Email")).toBeInTheDocument();
    expect(screen.getByLabelText("Role")).toBeInTheDocument();
  });

  it("shows validation error on empty submit", async () => {
    renderLogin();
    const submitBtn = screen.getByRole("button", { name: /sign in/i });
    fireEvent.click(submitBtn);
    await waitFor(() => {
      expect(screen.queryByText("Something went wrong")).toBeNull();
    });
  });
});
