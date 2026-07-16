const Dashboard = () => {
  return (
    <div className="min-h-screen bg-slate-50 px-4 py-6 text-slate-800 sm:px-6 lg:px-8">
      <div className="mx-auto flex max-w-6xl flex-col gap-6">
        <header className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.2em] text-emerald-600">
                Dashboard
              </p>
              <h1 className="mt-2 text-3xl font-semibold text-slate-900">
                Welcome back to the Assamese preservation workspace
              </h1>
            </div>
            <div className="rounded-full border border-emerald-200 bg-emerald-50 px-4 py-2 text-sm font-medium text-emerald-700">
              Trust Score: 92
            </div>
          </div>
        </header>

        <main className="grid gap-6 lg:grid-cols-2">
          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-xl font-semibold text-slate-900">Recent activity</h2>
            <div className="mt-4 space-y-3">
              <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                <p className="font-medium text-slate-800">New phrase reviewed</p>
                <p className="mt-1 text-sm text-slate-500">Casual greeting translated and approved.</p>
              </div>
              <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                <p className="font-medium text-slate-800">Audio note added</p>
                <p className="mt-1 text-sm text-slate-500">Pronunciation context recorded for a new entry.</p>
              </div>
            </div>
          </section>

          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-xl font-semibold text-slate-900">Next actions</h2>
            <div className="mt-4 space-y-3">
              <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-emerald-700">
                Review 3 pending translations
              </div>
              <div className="rounded-2xl border border-indigo-200 bg-indigo-50 p-4 text-indigo-700">
                Continue contributing to Assamese preservation
              </div>
            </div>
          </section>
        </main>
      </div>
    </div>
  );
};

export default Dashboard;