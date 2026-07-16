import { useState } from "react";

const ContributorDashboard = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [translationText, setTranslationText] = useState("");

  const handleSubmit = () => {
    console.log("Contribution submitted:", translationText);
    console.log("Audio recording saved successfully!");
    alert(`Contribution submitted!\n\nText: ${translationText || "(empty)"}\nAudio recording saved successfully!`);
  };

  const handleSkip = () => {
    setTranslationText("");
  };

  return (
    <div className="min-h-screen bg-slate-50 px-4 py-6 text-slate-800 sm:px-6 lg:px-8">
      <div className="mx-auto flex max-w-7xl flex-col gap-6">
        <header className="flex flex-col gap-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-sm font-medium uppercase tracking-[0.2em] text-emerald-600">
              Contributor workspace
            </p>
            <h1 className="mt-1 text-2xl font-semibold text-slate-900">
              Assamese Translation Review
            </h1>
          </div>

          <div className="flex items-center gap-3">
            <div className="rounded-full border border-emerald-200 bg-emerald-50 px-4 py-2">
              <span className="text-sm font-medium text-emerald-700">
                Trust Score: 92
              </span>
            </div>
            <button className="rounded-full border border-slate-200 px-4 py-2 text-sm font-medium text-slate-600 transition hover:bg-slate-100">
              Logout
            </button>
          </div>
        </header>

        <main className="grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">
          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-500">
                  Current phrase
                </p>
                <h2 className="mt-2 text-xl font-semibold text-slate-900">
                  Assamese Phrase
                </h2>
              </div>
              <span className="rounded-full bg-emerald-100 px-3 py-1 text-sm font-medium text-emerald-700">
                Ready to Review
              </span>
            </div>

            <div className="mt-6 rounded-2xl border border-slate-200 bg-slate-50 p-6">
              <p className="text-lg font-medium leading-8 text-slate-700">
                “নমস্কাৰ, আপোনাৰ ভালনে?”
              </p>
              <div className="mt-4 inline-flex rounded-full bg-indigo-50 px-3 py-1 text-sm font-medium text-indigo-700">
                Context: Casual Greeting
              </div>
            </div>

            <div className="mt-6 rounded-2xl border border-dashed border-slate-300 bg-slate-50 p-5">
              <p className="text-sm font-semibold text-slate-600">Notes</p>
              <p className="mt-2 text-sm leading-7 text-slate-500">
                Preserve the tone and intent of the phrase while keeping the translation natural and readable.
              </p>
            </div>
          </section>

          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-500">
                  Contribution form
                </p>
                <h2 className="mt-2 text-xl font-semibold text-slate-900">
                  Write the English Translation
                </h2>
              </div>
            </div>

            <label className="mt-6 block text-sm font-medium text-slate-700" htmlFor="translation">
              Translation
            </label>
            <textarea
              id="translation"
              rows={6}
              value={translationText}
              onChange={(e) => setTranslationText(e.target.value)}
              className="mt-2 w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-sm text-slate-700 outline-none transition focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200"
              placeholder="Type the English translation here..."
            />

            <div className="mt-6 rounded-2xl border border-slate-200 bg-slate-50 p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-semibold text-slate-700">Audio Recording Widget</p>
                  <p className="mt-1 text-sm text-slate-500">
                    Optional voice note for pronunciation context
                  </p>
                </div>
                <button
                  onClick={() => setIsRecording((prev) => !prev)}
                  className={`rounded-full px-4 py-2 text-sm font-semibold text-white transition ${
                    isRecording
                      ? "bg-slate-700 hover:bg-slate-800"
                      : "bg-red-500 hover:bg-red-600"
                  }`}
                >
                  {isRecording ? "Stop Recording" : "Record"}
                </button>
              </div>

              <div className="mt-4 rounded-2xl border border-slate-200 bg-slate-900 p-4">
                <div className="flex items-center gap-3">
                  <div className={`flex h-10 w-10 items-center justify-center rounded-full ${isRecording ? "bg-red-500/30 text-red-400" : "bg-red-500/20 text-red-400"}`}>
                    <svg viewBox="0 0 24 24" className={`h-5 w-5 ${isRecording ? "animate-pulse" : ""}`} fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M12 3a3 3 0 0 0-3 3v5a3 3 0 0 0 6 0V6a3 3 0 0 0-3-3Z" />
                      <path d="M6 11a6 6 0 0 0 12 0" strokeLinecap="round" />
                      <path d="M12 17v4" strokeLinecap="round" />
                      <path d="M8 21h8" strokeLinecap="round" />
                    </svg>
                  </div>
                  <div className="flex-1">
                    <div className="flex items-end gap-1">
                      {[...Array(12)].map((_, index) => (
                        <div
                          key={index}
                          className="w-1 rounded-full bg-slate-500"
                          style={{ height: `${18 + ((index + 1) % 5) * 6}px` }}
                        />
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </main>

        <div className="flex flex-col gap-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:flex-row sm:justify-end">
          <button
            onClick={handleSkip}
            className="rounded-full border border-slate-300 bg-slate-100 px-5 py-2.5 text-sm font-semibold text-slate-600 transition hover:bg-slate-200"
          >
            Skip Phrase
          </button>
          <button
            onClick={handleSubmit}
            className="rounded-full bg-emerald-600 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-emerald-700"
          >
            Submit Contribution
          </button>
        </div>
      </div>
    </div>
  );
};

export default ContributorDashboard;