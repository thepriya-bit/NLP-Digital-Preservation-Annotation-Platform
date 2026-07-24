import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import { adminApi, exportApi, type AdminUser, type PlatformStats } from "../services/api";
import { useToast } from "../components/Toast";

type Tab = "users" | "stats" | "cleanup" | "export";

const AdminConsole = () => {
  const { logout } = useAuth();
  const { showToast } = useToast();
  const [tab, setTab] = useState<Tab>("users");
  const [users, setUsers] = useState<AdminUser[]>([]);
  const [stats, setStats] = useState<PlatformStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [cleanupResult, setCleanupResult] = useState<string | null>(null);
  const [exportFormat, setExportFormat] = useState("csv");
  const [exporting, setExporting] = useState(false);

  useEffect(() => {
    if (tab === "users") {
      setLoading(true);
      adminApi.getUsers()
        .then(setUsers)
        .catch(() => showToast("Failed to load users", "error"))
        .finally(() => setLoading(false));
    } else if (tab === "stats") {
      setLoading(true);
      adminApi.getStats()
        .then(setStats)
        .catch(() => showToast("Failed to load stats", "error"))
        .finally(() => setLoading(false));
    }
  }, [tab, showToast]);

  const handleBan = async (userId: number) => {
    try {
      await adminApi.banUser(userId);
      setUsers((prev) => prev.map((u) => (u.id === userId ? { ...u, is_banned: true } : u)));
      showToast("User banned successfully", "success");
    } catch {
      showToast("Failed to ban user", "error");
    }
  };

  const handleUnban = async (userId: number) => {
    try {
      await adminApi.unbanUser(userId);
      setUsers((prev) => prev.map((u) => (u.id === userId ? { ...u, is_banned: false } : u)));
      showToast("User unbanned successfully", "success");
    } catch {
      showToast("Failed to unban user", "error");
    }
  };

  const handleCleanup = async () => {
    setCleanupResult(null);
    try {
      const result = await adminApi.cleanupOrphans();
      setCleanupResult(`Found ${result.orphans_found} orphans, deleted ${result.deleted}, errors ${result.errors}`);
      showToast("Orphan cleanup completed", "success");
    } catch {
      showToast("Cleanup failed", "error");
    }
  };

  const handleExport = async () => {
    setExporting(true);
    try {
      let blob: Blob;
      const ext = exportFormat;
      if (ext === "csv") blob = await exportApi.downloadCsv();
      else if (ext === "json") blob = await exportApi.downloadJson();
      else blob = await exportApi.downloadParquet();

      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `verified_dataset.${ext}`;
      a.click();
      window.URL.revokeObjectURL(url);
      showToast(`Dataset exported as ${ext.toUpperCase()}`, "success");
    } catch {
      showToast("Export failed. Check backend is running.", "error");
    } finally {
      setExporting(false);
    }
  };

  const tabs: { key: Tab; label: string }[] = [
    { key: "users", label: "Users" },
    { key: "stats", label: "Stats" },
    { key: "cleanup", label: "Cleanup" },
    { key: "export", label: "Export" },
  ];

  return (
    <div className="min-h-screen bg-slate-50 px-4 py-4 text-slate-800 sm:px-6 lg:px-8">
      <div className="mx-auto flex max-w-6xl flex-col gap-4 sm:gap-6">
        <header className="flex flex-col gap-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:flex-row sm:items-center sm:justify-between sm:p-5">
          <div>
            <p className="text-xs font-medium uppercase tracking-[0.2em] text-red-600 sm:text-sm">
              Admin Console
            </p>
            <h1 className="mt-1 text-xl font-semibold text-slate-900 sm:text-2xl">
              Platform Administration
            </h1>
          </div>
          <button onClick={logout} className="self-start rounded-full border border-slate-200 px-3 py-1.5 text-xs font-medium text-slate-600 hover:bg-slate-100 sm:self-auto sm:px-4 sm:py-2 sm:text-sm">
            Logout
          </button>
        </header>

        <div className="flex gap-2 overflow-x-auto rounded-2xl border border-slate-200 bg-white p-2 shadow-sm">
          {tabs.map((t) => (
            <button
              key={t.key}
              onClick={() => setTab(t.key)}
              className={`rounded-xl px-3 py-1.5 text-xs font-semibold transition whitespace-nowrap sm:px-4 sm:py-2 sm:text-sm ${
                tab === t.key ? "bg-red-600 text-white" : "text-slate-600 hover:bg-slate-100"
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>

        {tab === "users" && (
          <div className="rounded-2xl border border-slate-200 bg-white shadow-sm sm:rounded-3xl">
            {loading ? (
              <div className="flex items-center justify-center py-12 sm:py-16">
                <div className="h-8 w-8 animate-spin rounded-full border-4 border-red-200 border-t-red-600" />
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-xs sm:text-sm">
                  <thead>
                    <tr className="border-b border-slate-200 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
                      <th className="px-3 py-3 sm:px-5 sm:py-4">ID</th>
                      <th className="px-3 py-3 sm:px-5 sm:py-4">Username</th>
                      <th className="hidden px-3 py-3 sm:table-cell sm:px-5 sm:py-4">Email</th>
                      <th className="px-3 py-3 sm:px-5 sm:py-4">Role</th>
                      <th className="hidden px-3 py-3 sm:table-cell sm:px-5 sm:py-4">Trust</th>
                      <th className="px-3 py-3 sm:px-5 sm:py-4">Status</th>
                      <th className="px-3 py-3 sm:px-5 sm:py-4">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {users.map((u) => (
                      <tr key={u.id} className="border-b border-slate-100 last:border-0">
                        <td className="px-3 py-3 font-mono text-xs text-slate-500 sm:px-5 sm:py-4">{u.id}</td>
                        <td className="px-3 py-3 font-medium sm:px-5 sm:py-4">{u.username}</td>
                        <td className="hidden px-3 py-3 text-slate-500 sm:table-cell sm:px-5 sm:py-4">{u.email}</td>
                        <td className="px-3 py-3 sm:px-5 sm:py-4">
                          <span className="rounded-full bg-slate-100 px-2 py-0.5 text-xs font-medium capitalize">
                            {u.role}
                          </span>
                        </td>
                        <td className="hidden px-3 py-3 sm:table-cell sm:px-5 sm:py-4">
                          <span className={`font-medium ${u.trust_score >= 0 ? "text-emerald-600" : "text-red-600"}`}>
                            {u.trust_score}
                          </span>
                        </td>
                        <td className="px-3 py-3 sm:px-5 sm:py-4">
                          {u.is_banned ? (
                            <span className="rounded-full bg-red-100 px-2 py-0.5 text-xs font-medium text-red-700">Banned</span>
                          ) : (
                            <span className="rounded-full bg-emerald-100 px-2 py-0.5 text-xs font-medium text-emerald-700">Active</span>
                          )}
                        </td>
                        <td className="px-3 py-3 sm:px-5 sm:py-4">
                          {u.is_banned ? (
                            <button onClick={() => handleUnban(u.id)} className="rounded-lg border border-emerald-300 px-2 py-1 text-xs font-medium text-emerald-700 hover:bg-emerald-50 sm:px-3">
                              Unban
                            </button>
                          ) : (
                            <button onClick={() => handleBan(u.id)} className="rounded-lg border border-red-300 px-2 py-1 text-xs font-medium text-red-700 hover:bg-red-50 sm:px-3">
                              Ban
                            </button>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {tab === "stats" && (
          <div className="grid grid-cols-2 gap-3 sm:gap-4 lg:grid-cols-4">
            {[
              { label: "Total Users", value: stats?.total_users ?? "-", color: "bg-blue-50 text-blue-700 border-blue-200" },
              { label: "Total Phrases", value: stats?.total_phrases ?? "-", color: "bg-indigo-50 text-indigo-700 border-indigo-200" },
              { label: "Verified", value: stats?.verified_annotations ?? "-", color: "bg-emerald-50 text-emerald-700 border-emerald-200" },
              { label: "Pending Review", value: stats?.pending_verification ?? "-", color: "bg-amber-50 text-amber-700 border-amber-200" },
            ].map((card) => (
              <div key={card.label} className={`rounded-xl border p-4 shadow-sm sm:rounded-2xl sm:p-5 ${card.color}`}>
                <p className="text-2xl font-semibold sm:text-3xl">{card.value}</p>
                <p className="mt-1 text-xs sm:text-sm">{card.label}</p>
              </div>
            ))}
          </div>
        )}

        {tab === "cleanup" && (
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:rounded-3xl sm:p-6">
            <h2 className="text-base font-semibold text-slate-900 sm:text-lg">Orphaned Audio Cleanup</h2>
            <p className="mt-1 text-xs text-slate-500 sm:text-sm">
              Find and delete audio files in Firebase/Storage that are not referenced in the database.
            </p>
            <button
              onClick={handleCleanup}
              className="mt-3 rounded-full bg-red-600 px-4 py-2 text-xs font-semibold text-white hover:bg-red-700 sm:mt-4 sm:px-5 sm:py-2.5 sm:text-sm"
            >
              Run Cleanup
            </button>
            {cleanupResult && (
              <div className="mt-3 rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-xs text-slate-700 sm:mt-4 sm:px-4 sm:py-3 sm:text-sm">
                {cleanupResult}
              </div>
            )}
          </div>
        )}

        {tab === "export" && (
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:rounded-3xl sm:p-6">
            <h2 className="text-base font-semibold text-slate-900 sm:text-lg">Dataset Export</h2>
            <p className="mt-1 text-xs text-slate-500 sm:text-sm">
              Export verified annotations for AI/ML use.
            </p>
            <div className="mt-3 flex flex-wrap gap-2 sm:mt-4 sm:gap-3">
              {(["csv", "json", "parquet"] as const).map((fmt) => (
                <button
                  key={fmt}
                  onClick={() => setExportFormat(fmt)}
                  className={`rounded-xl border-2 px-3 py-1.5 text-xs font-semibold capitalize transition sm:px-4 sm:py-2 sm:text-sm ${
                    exportFormat === fmt
                      ? "border-red-500 bg-red-50 text-red-700"
                      : "border-slate-200 text-slate-600 hover:border-slate-300"
                  }`}
                >
                  {fmt}
                </button>
              ))}
            </div>
            <button
              onClick={handleExport}
              disabled={exporting}
              className="mt-3 rounded-full bg-red-600 px-4 py-2 text-xs font-semibold text-white hover:bg-red-700 disabled:opacity-50 sm:mt-4 sm:px-5 sm:py-2.5 sm:text-sm"
            >
              {exporting ? "Exporting..." : `Download as ${exportFormat.toUpperCase()}`}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminConsole;
