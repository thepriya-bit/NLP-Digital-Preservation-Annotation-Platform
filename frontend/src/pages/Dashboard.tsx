import { useAuth } from "../context/AuthContext";
import { Link } from "react-router-dom";

const Dashboard = () => {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-slate-50 px-4 py-4 text-slate-800 sm:px-6 lg:px-8">
      <div className="mx-auto flex max-w-6xl flex-col gap-4 sm:gap-6">
        <header className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:rounded-3xl sm:p-6">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-emerald-600 sm:text-sm">
                Dashboard
              </p>
              <h1 className="mt-1 text-2xl font-semibold text-slate-900 sm:mt-2 sm:text-3xl">
                Welcome back{user ? `, ${user.username}` : ""}
              </h1>
              {user && (
                <p className="mt-1 text-xs text-slate-500 sm:text-sm">
                  Role: <span className="font-medium capitalize">{user.role}</span>
                </p>
              )}
            </div>
            <div className="self-start rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1.5 text-xs font-medium text-emerald-700 sm:self-auto sm:px-4 sm:py-2 sm:text-sm">
              Trust Score: {user?.trust_score ?? 0}
            </div>
          </div>
        </header>

        <main className="grid gap-4 sm:gap-6 lg:grid-cols-2">
          <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:rounded-3xl sm:p-6">
            <h2 className="text-lg font-semibold text-slate-900 sm:text-xl">Quick Actions</h2>
            <div className="mt-3 space-y-2 sm:mt-4 sm:space-y-3">
              <Link
                to="/contributor"
                className="block rounded-xl border border-emerald-200 bg-emerald-50 p-3 text-emerald-700 transition hover:bg-emerald-100 sm:rounded-2xl sm:p-4"
              >
                <p className="text-sm font-medium sm:text-base">Start Translating</p>
                <p className="mt-0.5 text-xs text-emerald-600 sm:mt-1 sm:text-sm">Contribute to Assamese digital preservation</p>
              </Link>
              {(user?.role === "verifier" || user?.role === "admin") && (
                <Link
                  to="/verify"
                  className="block rounded-xl border border-indigo-200 bg-indigo-50 p-3 text-indigo-700 transition hover:bg-indigo-100 sm:rounded-2xl sm:p-4"
                >
                  <p className="text-sm font-medium sm:text-base">Verify Translations</p>
                  <p className="mt-0.5 text-xs text-indigo-600 sm:mt-1 sm:text-sm">Review and approve pending contributions</p>
                </Link>
              )}
              {user?.role === "admin" && (
                <Link
                  to="/admin"
                  className="block rounded-xl border border-red-200 bg-red-50 p-3 text-red-700 transition hover:bg-red-100 sm:rounded-2xl sm:p-4"
                >
                  <p className="text-sm font-medium sm:text-base">Admin Console</p>
                  <p className="mt-0.5 text-xs text-red-600 sm:mt-1 sm:text-sm">Manage users, stats, and exports</p>
                </Link>
              )}
            </div>
          </section>

          <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:rounded-3xl sm:p-6">
            <h2 className="text-lg font-semibold text-slate-900 sm:text-xl">Account Info</h2>
            <div className="mt-3 space-y-2 sm:mt-4 sm:space-y-3">
              <div className="rounded-xl border border-slate-200 bg-slate-50 p-3 sm:rounded-2xl sm:p-4">
                <p className="text-xs text-slate-500 sm:text-sm">Username</p>
                <p className="text-sm font-medium text-slate-800 sm:text-base">{user?.username ?? "-"}</p>
              </div>
              <div className="rounded-xl border border-slate-200 bg-slate-50 p-3 sm:rounded-2xl sm:p-4">
                <p className="text-xs text-slate-500 sm:text-sm">Email</p>
                <p className="text-sm font-medium text-slate-800 sm:text-base">{user?.email ?? "-"}</p>
              </div>
              <div className="rounded-xl border border-slate-200 bg-slate-50 p-3 sm:rounded-2xl sm:p-4">
                <p className="text-xs text-slate-500 sm:text-sm">Role</p>
                <p className="text-sm font-medium capitalize text-slate-800 sm:text-base">{user?.role ?? "-"}</p>
              </div>
            </div>
          </section>
        </main>
      </div>
    </div>
  );
};

export default Dashboard;
