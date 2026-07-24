import { useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

const Navbar = () => {
  const { isAuthenticated, user, logout } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);

  const navLinks = [
    { to: "/", label: "Home", show: true },
    { to: "/dashboard", label: "Dashboard", show: isAuthenticated },
    { to: "/contributor", label: "Contribute", show: isAuthenticated && (user?.role === "annotator" || user?.role === "verifier") },
    { to: "/verify", label: "Verify", show: isAuthenticated && (user?.role === "verifier" || user?.role === "admin") },
    { to: "/admin", label: "Admin", show: isAuthenticated && user?.role === "admin" },
  ];

  return (
    <nav className="relative bg-blue-600 px-4 py-4 text-white shadow-md sm:px-6">
      <div className="flex items-center justify-between">
        <h1 className="text-lg font-bold sm:text-xl">NLP & Digital Preservation</h1>

        <button
          onClick={() => setMenuOpen(!menuOpen)}
          className="flex items-center justify-center rounded-lg p-2 transition hover:bg-white/10 sm:hidden"
          aria-label="Toggle menu"
        >
          <svg viewBox="0 0 24 24" className="h-6 w-6" fill="none" stroke="currentColor" strokeWidth="2">
            {menuOpen ? (
              <path d="M6 6l12 12M18 6l-12 12" strokeLinecap="round" />
            ) : (
              <>
                <path d="M4 6h16" strokeLinecap="round" />
                <path d="M4 12h16" strokeLinecap="round" />
                <path d="M4 18h16" strokeLinecap="round" />
              </>
            )}
          </svg>
        </button>

        <ul className="hidden items-center gap-6 sm:flex">
          {navLinks.map(
            (link) =>
              link.show && (
                <li key={link.to}>
                  <Link to={link.to} className="cursor-pointer whitespace-nowrap transition hover:text-gray-200">
                    {link.label}
                  </Link>
                </li>
              ),
          )}
          {isAuthenticated ? (
            <li className="flex items-center gap-3">
              <span className="text-sm text-blue-200">{user?.username}</span>
              <button onClick={logout} className="rounded-full border border-white/30 px-4 py-1.5 text-sm transition hover:bg-white/10">
                Logout
              </button>
            </li>
          ) : (
            <li>
              <Link to="/login" className="rounded-full border border-white/30 px-4 py-1.5 text-sm transition hover:bg-white/10">
                Login
              </Link>
            </li>
          )}
        </ul>
      </div>

      {menuOpen && (
        <div className="mt-4 rounded-xl border border-white/20 bg-blue-700 p-3 sm:hidden">
          {navLinks.map(
            (link) =>
              link.show && (
                <Link
                  key={link.to}
                  to={link.to}
                  onClick={() => setMenuOpen(false)}
                  className="block rounded-lg px-3 py-2.5 text-sm font-medium transition hover:bg-white/10"
                >
                  {link.label}
                </Link>
              ),
          )}
          <hr className="my-2 border-blue-500" />
          {isAuthenticated ? (
            <>
              <div className="px-3 py-2 text-sm text-blue-200">{user?.username}</div>
              <button
                onClick={() => { logout(); setMenuOpen(false); }}
                className="block w-full rounded-lg px-3 py-2.5 text-left text-sm font-medium transition hover:bg-white/10"
              >
                Logout
              </button>
            </>
          ) : (
            <Link
              to="/login"
              onClick={() => setMenuOpen(false)}
              className="block rounded-lg px-3 py-2.5 text-sm font-medium transition hover:bg-white/10"
            >
              Login
            </Link>
          )}
        </div>
      )}
    </nav>
  );
};

export default Navbar;
