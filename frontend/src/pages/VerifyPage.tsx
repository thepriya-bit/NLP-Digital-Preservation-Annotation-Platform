import { useState, useEffect, useCallback } from "react";
import { useAuth } from "../context/AuthContext";
import { verificationApi, phrasesApi, type PendingAnnotation, type RawPhrase } from "../services/api";
import { useToast } from "../components/Toast";

const VerifyPage = () => {
  const { logout } = useAuth();
  const { showToast } = useToast();
  const [pending, setPending] = useState<PendingAnnotation[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [phrase, setPhrase] = useState<RawPhrase | null>(null);
  const [vote, setVote] = useState<"approve" | "reject" | null>(null);
  const [comment, setComment] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [approvedCount, setApprovedCount] = useState(0);
  const [rejectedCount, setRejectedCount] = useState(0);

  const fetchPending = useCallback(async () => {
    setLoading(true);
    try {
      const data = await verificationApi.getPending();
      setPending(data);
      setCurrentIndex(0);
    } catch {
      showToast("Failed to load pending annotations", "error");
    } finally {
      setLoading(false);
    }
  }, [showToast]);

  useEffect(() => {
    fetchPending();
  }, [fetchPending]);

  const currentItem = pending[currentIndex];

  const fetchPhrase = useCallback(async (rawPhraseId: number) => {
    try {
      const allPhrases = await phrasesApi.list();
      const found = allPhrases.find((p) => p.id === rawPhraseId);
      if (found) setPhrase(found);
    } catch {
      /* non-critical */
    }
  }, []);

  useEffect(() => {
    if (currentItem) {
      setPhrase(null);
      fetchPhrase(currentItem.raw_phrase_id);
      setVote(null);
      setComment("");
    }
  }, [currentItem, fetchPhrase]);

  const handleVote = async () => {
    if (!currentItem || !vote) return;
    setSubmitting(true);
    try {
      const result = await verificationApi.castVote(currentItem.id, vote, comment || undefined);
      if (result.success) {
        if (vote === "approve") setApprovedCount((c) => c + 1);
        else setRejectedCount((c) => c + 1);
        showToast(
          result.annotation_status
            ? `Vote recorded! Annotation is now ${result.annotation_status}.`
            : "Vote recorded. Waiting for more votes.",
          "success",
        );
        if (currentIndex < pending.length - 1) {
          setCurrentIndex((i) => i + 1);
        } else {
          fetchPending();
        }
      }
    } catch (err: unknown) {
      const msg =
        err instanceof Object && "response" in err
          ? (err as { response: { data: { detail: string } } }).response?.data?.detail || "Failed to submit vote"
          : "Failed to submit vote";
      showToast(msg, "error");
    } finally {
      setSubmitting(false);
    }
  };

  const handleSkip = () => {
    if (currentIndex < pending.length - 1) {
      setCurrentIndex((i) => i + 1);
    } else {
      fetchPending();
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 px-4 py-4 text-slate-800 sm:px-6 lg:px-8">
      <div className="mx-auto flex max-w-5xl flex-col gap-4 sm:gap-6">
        <header className="flex flex-col gap-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:flex-row sm:items-center sm:justify-between sm:p-5">
          <div>
            <p className="text-xs font-medium uppercase tracking-[0.2em] text-indigo-600 sm:text-sm">
              Verification workspace
            </p>
            <h1 className="mt-1 text-xl font-semibold text-slate-900 sm:text-2xl">
              Review Translations
            </h1>
          </div>
          <div className="flex flex-wrap items-center gap-2 sm:gap-3">
            <div className="rounded-full border border-emerald-200 bg-emerald-50 px-2.5 py-1 text-xs font-medium text-emerald-700 sm:px-4 sm:py-2 sm:text-sm">
              Approved: {approvedCount}
            </div>
            <div className="rounded-full border border-red-200 bg-red-50 px-2.5 py-1 text-xs font-medium text-red-700 sm:px-4 sm:py-2 sm:text-sm">
              Rejected: {rejectedCount}
            </div>
            <div className="rounded-full border border-slate-200 bg-slate-100 px-2.5 py-1 text-xs font-medium text-slate-600 sm:px-4 sm:py-2 sm:text-sm">
              Pending: {pending.length}
            </div>
            <button onClick={logout} className="rounded-full border border-slate-200 px-2.5 py-1 text-xs font-medium text-slate-600 hover:bg-slate-100 sm:px-4 sm:py-2 sm:text-sm">
              Logout
            </button>
          </div>
        </header>

        {loading ? (
          <div className="flex items-center justify-center py-16 sm:py-20">
            <div className="h-10 w-10 animate-spin rounded-full border-4 border-indigo-200 border-t-indigo-600" />
          </div>
        ) : !currentItem ? (
          <div className="rounded-2xl border border-slate-200 bg-white p-8 text-center shadow-sm sm:rounded-3xl sm:p-12">
            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-emerald-100 sm:h-16 sm:w-16">
              <svg viewBox="0 0 24 24" className="h-7 w-7 text-emerald-600 sm:h-8 sm:w-8" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M9 11.5 11 13.5 15.5 9" strokeLinecap="round" strokeLinejoin="round" />
                <path d="M5 5.5A2.5 2.5 0 0 1 7.5 3h9A2.5 2.5 0 0 1 19 5.5v13A2.5 2.5 0 0 1 16.5 21h-9A2.5 2.5 0 0 1 5 18.5z" />
              </svg>
            </div>
            <h2 className="mt-4 text-lg font-semibold text-slate-900 sm:text-xl">All caught up!</h2>
            <p className="mt-2 text-sm text-slate-500">No pending translations to review right now.</p>
            <button onClick={fetchPending} className="mt-6 rounded-full bg-indigo-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-indigo-700">
              Refresh
            </button>
          </div>
        ) : (
          <>
            <div className="grid gap-4 sm:gap-6 lg:grid-cols-2">
              <section className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:rounded-3xl sm:p-6">
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500 sm:text-sm">
                  Original Phrase
                </p>
                <div className="mt-3 rounded-xl border border-slate-200 bg-slate-50 p-4 sm:mt-4 sm:rounded-2xl sm:p-5">
                  <p className="text-base font-medium leading-7 text-slate-700 sm:text-lg sm:leading-8">
                    &ldquo;{phrase?.phrase ?? "Loading..."}&rdquo;
                  </p>
                  {phrase && (
                    <div className="mt-2 inline-flex rounded-full bg-indigo-50 px-2.5 py-0.5 text-xs font-medium text-indigo-700 sm:mt-3 sm:px-3 sm:py-1 sm:text-sm">
                      {phrase.language}
                    </div>
                  )}
                </div>
              </section>

              <section className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:rounded-3xl sm:p-6">
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500 sm:text-sm">
                  Translation
                </p>
                <div className="mt-3 rounded-xl border border-slate-200 bg-slate-50 p-4 sm:mt-4 sm:rounded-2xl sm:p-5">
                  <p className="text-sm leading-7 text-slate-700 sm:text-base sm:leading-8">
                    {currentItem.translated_text}
                  </p>
                </div>
              </section>
            </div>

            <section className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:rounded-3xl sm:p-6">
              <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500 sm:text-sm">
                  Your Verdict
                </p>
                <div className="flex items-center gap-3 text-xs text-slate-500 sm:text-sm">
                  <span>Approve: {currentItem.approve_count}</span>
                  <span>Reject: {currentItem.reject_count}</span>
                  <span>#{currentIndex + 1} of {pending.length}</span>
                </div>
              </div>

              <div className="mt-3 flex gap-2 sm:mt-4 sm:gap-3">
                <button
                  onClick={() => setVote("approve")}
                  className={`flex-1 rounded-xl border-2 px-3 py-2.5 text-sm font-semibold transition sm:px-4 sm:py-3 ${
                    vote === "approve"
                      ? "border-emerald-500 bg-emerald-50 text-emerald-700"
                      : "border-slate-200 bg-slate-50 text-slate-600 hover:border-emerald-300"
                  }`}
                >
                  Approve
                </button>
                <button
                  onClick={() => setVote("reject")}
                  className={`flex-1 rounded-xl border-2 px-3 py-2.5 text-sm font-semibold transition sm:px-4 sm:py-3 ${
                    vote === "reject"
                      ? "border-red-500 bg-red-50 text-red-700"
                      : "border-slate-200 bg-slate-50 text-slate-600 hover:border-red-300"
                  }`}
                >
                  Reject
                </button>
              </div>

              <div className="mt-3 sm:mt-4">
                <label htmlFor="comment" className="block text-xs font-medium text-slate-700 sm:text-sm">
                  Comment (optional)
                </label>
                <textarea
                  id="comment"
                  rows={2}
                  value={comment}
                  onChange={(e) => setComment(e.target.value)}
                  className="mt-1 w-full rounded-xl border border-slate-300 bg-slate-50 px-3 py-2 text-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 sm:px-4 sm:py-2.5"
                  placeholder="Add context for your vote..."
                />
              </div>

              <div className="mt-4 flex gap-2 sm:mt-6 sm:gap-3">
                <button
                  onClick={handleSkip}
                  disabled={loading}
                  className="rounded-full border border-slate-300 bg-slate-100 px-4 py-2 text-sm font-semibold text-slate-600 hover:bg-slate-200 disabled:opacity-50"
                >
                  Skip
                </button>
                <button
                  onClick={handleVote}
                  disabled={!vote || submitting}
                  className="flex-1 rounded-full bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-700 disabled:opacity-50"
                >
                  {submitting ? "Submitting..." : "Submit Vote"}
                </button>
              </div>
            </section>
          </>
        )}
      </div>
    </div>
  );
};

export default VerifyPage;
