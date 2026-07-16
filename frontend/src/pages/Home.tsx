import { Link } from "react-router-dom";

import Navbar from "../components/layout/Navbar";

const highlights = [
  {
    title: "Community-driven annotation",
    description:
      "Contributors help build richer Assamese datasets with context-aware linguistic labels.",
    icon: (
      <svg viewBox="0 0 24 24" className="h-6 w-6" fill="none" stroke="currentColor" strokeWidth="1.8">
        <path d="M12 3v18" strokeLinecap="round" />
        <path d="M3 7h18" strokeLinecap="round" />
        <path d="M6 17c1.5-2 3-3 6-3s4.5 1 6 3" strokeLinecap="round" />
      </svg>
    ),
  },
  {
    title: "Preserve cultural memory",
    description:
      "Every translation and annotation contributes to the long-term preservation of Assamese knowledge.",
    icon: (
      <svg viewBox="0 0 24 24" className="h-6 w-6" fill="none" stroke="currentColor" strokeWidth="1.8">
        <path d="M4 6.5A2.5 2.5 0 0 1 6.5 4h11A2.5 2.5 0 0 1 20 6.5v11a2.5 2.5 0 0 1-2.5 2.5h-11A2.5 2.5 0 0 1 4 17.5z" />
        <path d="M8 8h8" strokeLinecap="round" />
        <path d="M8 12h5" strokeLinecap="round" />
      </svg>
    ),
  },
  {
    title: "Trusted review flow",
    description:
      "Verified contributions ensure that high-quality annotations are ready for downstream use.",
    icon: (
      <svg viewBox="0 0 24 24" className="h-6 w-6" fill="none" stroke="currentColor" strokeWidth="1.8">
        <path d="M9 11.5 11 13.5 15.5 9" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M5 5.5A2.5 2.5 0 0 1 7.5 3h9A2.5 2.5 0 0 1 19 5.5v13A2.5 2.5 0 0 1 16.5 21h-9A2.5 2.5 0 0 1 5 18.5z" />
      </svg>
    ),
  },
];

const Home = () => {
  return (
    <>
      <Navbar />

      <main className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(16,185,129,0.18),_transparent_28%),linear-gradient(135deg,_#020617_0%,_#111827_45%,_#1e1b4b_100%)] text-slate-50">
        <section className="mx-auto flex max-w-7xl flex-col gap-12 px-6 py-20 lg:flex-row lg:items-center lg:px-8 lg:py-28">
          <div className="max-w-2xl">
            <div className="inline-flex items-center gap-2 rounded-full border border-emerald-400/30 bg-emerald-500/10 px-3 py-1 text-sm font-medium text-emerald-300">
              <svg viewBox="0 0 24 24" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M12 3l2.3 4.7 5.2.8-3.8 3.7.9 5.2-4.6-2.4-4.6 2.4.9-5.2-3.8-3.7 5.2-.8L12 3Z" />
              </svg>
              Assamese language annotation and preservation
            </div>

            <h1 className="mt-6 text-4xl font-semibold tracking-tight sm:text-5xl lg:text-6xl">
              Build a lasting digital record of the
              <span className="mt-3 block bg-gradient-to-r from-emerald-300 via-cyan-200 to-indigo-300 bg-clip-text text-transparent">
                Assamese language.
              </span>
            </h1>

            <p className="mt-6 max-w-xl text-lg leading-8 text-slate-300">
              This platform brings together contributors, reviewers, and linguists to annotate,
              verify, and preserve Assamese text with care, clarity, and cultural context.
            </p>

            <div className="mt-8 flex flex-col gap-3 sm:flex-row">
              <Link
                to="/dashboard"
                className="inline-flex items-center justify-center rounded-full bg-emerald-500 px-6 py-3 text-sm font-semibold text-slate-950 transition hover:bg-emerald-400"
              >
                <svg viewBox="0 0 24 24" className="mr-2 h-5 w-5" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M12 5v14" strokeLinecap="round" />
                  <path d="M5 12h14" strokeLinecap="round" />
                </svg>
                Start Contributing
              </Link>

              <Link
                to="/verify"
                className="inline-flex items-center justify-center rounded-full border border-slate-700 bg-slate-900/70 px-6 py-3 text-sm font-semibold text-slate-100 transition hover:border-indigo-400 hover:bg-slate-800"
              >
                <svg viewBox="0 0 24 24" className="mr-2 h-5 w-5" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M9 11.5 11 13.5 15.5 9" strokeLinecap="round" strokeLinejoin="round" />
                  <path d="M5 5.5A2.5 2.5 0 0 1 7.5 3h9A2.5 2.5 0 0 1 19 5.5v13A2.5 2.5 0 0 1 16.5 21h-9A2.5 2.5 0 0 1 5 18.5z" />
                </svg>
                Verify Translations
              </Link>
            </div>

            <div className="mt-8 flex flex-wrap gap-4 text-sm text-slate-300">
              <span className="rounded-full border border-slate-800 bg-slate-900/60 px-3 py-1">✓ Human-reviewed quality</span>
              <span className="rounded-full border border-slate-800 bg-slate-900/60 px-3 py-1">✓ Cultural preservation focus</span>
              <span className="rounded-full border border-slate-800 bg-slate-900/60 px-3 py-1">✓ Open for collaboration</span>
            </div>
          </div>

          <div className="w-full max-w-xl">
            <div className="rounded-3xl border border-slate-800/80 bg-slate-900/70 p-5 shadow-2xl shadow-indigo-950/60 backdrop-blur">
              <div className="rounded-2xl border border-slate-800 bg-slate-950/80 p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-emerald-300">Live preservation workspace</p>
                    <p className="mt-1 text-xl font-semibold text-white">Assamese annotation pipeline</p>
                  </div>
                  <div className="rounded-full border border-indigo-400/30 bg-indigo-500/10 px-3 py-1 text-sm text-indigo-200">
                    24/7 ready
                  </div>
                </div>

                <div className="mt-6 grid gap-4 sm:grid-cols-2">
                  <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-4">
                    <p className="text-3xl font-semibold text-white">1.2K+</p>
                    <p className="mt-1 text-sm text-slate-400">Annotated phrases</p>
                  </div>
                  <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-4">
                    <p className="text-3xl font-semibold text-white">320</p>
                    <p className="mt-1 text-sm text-slate-400">Verified translations</p>
                  </div>
                </div>

                <div className="mt-6 rounded-2xl border border-indigo-500/30 bg-indigo-500/10 p-4">
                  <div className="flex items-center gap-2 text-indigo-200">
                    <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M6 6h12" strokeLinecap="round" />
                      <path d="M6 12h8" strokeLinecap="round" />
                      <path d="M6 18h5" strokeLinecap="round" />
                    </svg>
                    <span className="text-sm font-semibold">Why it matters</span>
                  </div>
                  <p className="mt-3 text-sm leading-7 text-slate-300">
                    Every annotation protects meaning, context, and cultural memory for future generations.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="mx-auto max-w-7xl px-6 pb-20 lg:px-8">
          <div className="grid gap-4 md:grid-cols-3">
            {highlights.map((item) => (
              <div key={item.title} className="rounded-2xl border border-slate-800/80 bg-slate-900/60 p-6 shadow-lg shadow-slate-950/30">
                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-500/10 text-emerald-300">
                  {item.icon}
                </div>
                <h3 className="mt-4 text-lg font-semibold text-white">{item.title}</h3>
                <p className="mt-2 text-sm leading-7 text-slate-400">{item.description}</p>
              </div>
            ))}
          </div>
        </section>
      </main>
    </>
  );
};

export default Home;