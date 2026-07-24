import { useState, useEffect, useCallback, useRef } from "react";
import { useAuth } from "../context/AuthContext";
import { phrasesApi, annotationsApi, audioApi } from "../services/api";
import { useToast } from "../components/Toast";

const ContributorDashboard = () => {
  const { user, logout } = useAuth();
  const { showToast } = useToast();
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  const [phrase, setPhrase] = useState<{ id: number; phrase: string; language: string } | null>(null);
  const [translationText, setTranslationText] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [audioUploading, setAudioUploading] = useState(false);
  const [hasMicPermission, setHasMicPermission] = useState<boolean | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [contributionCount, setContributionCount] = useState(0);

  const fetchRandomPhrase = useCallback(async () => {
    setLoading(true);
    setTranslationText("");
    setAudioUrl(null);
    try {
      const data = await phrasesApi.getRandom();
      setPhrase({ id: data.id, phrase: data.phrase, language: data.language });
    } catch (err: unknown) {
      const status = err instanceof Object && "response" in err
        ? (err as { response: { status: number } }).response?.status
        : null;
      if (status === 404) {
        showToast("No phrases available for review right now.", "info");
      } else {
        showToast("Failed to load phrase. Please try again.", "error");
      }
      setPhrase(null);
    } finally {
      setLoading(false);
    }
  }, [showToast]);

  const fetchStats = useCallback(async () => {
    try {
      const myAnnotations = await annotationsApi.getMy();
      setContributionCount(myAnnotations.length);
    } catch {
      /* stats are non-critical */
    }
  }, []);

  useEffect(() => {
    fetchRandomPhrase();
    fetchStats();
  }, [fetchRandomPhrase, fetchStats]);

  const startRecording = async () => {
    setAudioUrl(null);
    audioChunksRef.current = [];
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      setHasMicPermission(true);
      const recorder = new MediaRecorder(stream);
      mediaRecorderRef.current = recorder;

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) audioChunksRef.current.push(e.data);
      };

      recorder.onstop = async () => {
        stream.getTracks().forEach((t) => t.stop());
        const blob = new Blob(audioChunksRef.current, { type: "audio/webm" });
        setAudioUploading(true);
        try {
          const result = await audioApi.upload(blob, `recording_${Date.now()}.webm`);
          setAudioUrl(result.audio_url);
          showToast("Audio uploaded successfully", "success");
        } catch {
          showToast("Audio upload failed. Your recording was saved locally but not uploaded.", "error");
        } finally {
          setAudioUploading(false);
        }
      };

      recorder.start();
      setIsRecording(true);
    } catch {
      setHasMicPermission(false);
      showToast("Microphone access denied. Recording unavailable.", "error");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== "inactive") {
      mediaRecorderRef.current.stop();
    }
    setIsRecording(false);
  };

  const toggleRecording = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  const handleSubmit = async () => {
    if (!phrase || !translationText.trim()) return;
    setSubmitting(true);
    try {
      await annotationsApi.create({
        raw_phrase_id: phrase.id,
        translated_text: translationText.trim(),
        ...(audioUrl ? { syntax: { audio_url: audioUrl } } : {}),
      });
      showToast("Translation submitted successfully!", "success");
      setContributionCount((c) => c + 1);
      fetchRandomPhrase();
    } catch (err: unknown) {
      const msg =
        err instanceof Object && "response" in err
          ? (err as { response: { data: { detail: string } } }).response?.data?.detail || "Submission failed"
          : "Submission failed. Please try again.";
      showToast(msg, "error");
    } finally {
      setSubmitting(false);
    }
  };

  const handleSkip = () => {
    fetchRandomPhrase();
  };

  const showSimulated = hasMicPermission === false;

  return (
    <div className="min-h-screen bg-slate-50 px-4 py-4 text-slate-800 sm:px-6 lg:px-8">
      <div className="mx-auto flex max-w-7xl flex-col gap-4 sm:gap-6">
        <header className="flex flex-col gap-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:flex-row sm:items-center sm:justify-between sm:p-5">
          <div className="min-w-0">
            <p className="text-xs font-medium uppercase tracking-[0.2em] text-emerald-600 sm:text-sm">
              Contributor workspace
            </p>
            <h1 className="mt-1 text-xl font-semibold text-slate-900 sm:text-2xl">
              Assamese Translation Review
            </h1>
          </div>
          <div className="flex flex-wrap items-center gap-2 sm:gap-3">
            <div className="rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1.5 sm:px-4 sm:py-2">
              <span className="text-xs font-medium text-emerald-700 sm:text-sm">Trust: {user?.trust_score ?? 0}</span>
            </div>
            <div className="rounded-full border border-indigo-200 bg-indigo-50 px-3 py-1.5 sm:px-4 sm:py-2">
              <span className="text-xs font-medium text-indigo-700 sm:text-sm">Done: {contributionCount}</span>
            </div>
            <button onClick={logout} className="rounded-full border border-slate-200 px-3 py-1.5 text-xs font-medium text-slate-600 transition hover:bg-slate-100 sm:px-4 sm:py-2 sm:text-sm">
              Logout
            </button>
          </div>
        </header>

        <main className="grid gap-4 sm:gap-6 lg:grid-cols-[1.05fr_0.95fr]">
          <section className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:rounded-3xl sm:p-6">
            <div className="flex items-center justify-between">
              <div className="min-w-0">
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500 sm:text-sm">Current phrase</p>
                <h2 className="mt-1 text-lg font-semibold text-slate-900 sm:mt-2 sm:text-xl">
                  {loading ? "Loading..." : phrase ? "Assamese Phrase" : "No phrase"}
                </h2>
              </div>
              <span className="shrink-0 rounded-full bg-emerald-100 px-2.5 py-1 text-xs font-medium text-emerald-700 sm:px-3 sm:text-sm">
                {loading ? "Loading" : phrase ? "Ready" : "Unavailable"}
              </span>
            </div>

            <div className="mt-4 rounded-xl border border-slate-200 bg-slate-50 p-4 sm:mt-6 sm:rounded-2xl sm:p-6">
              {loading ? (
                <div className="flex items-center justify-center py-6 sm:py-8">
                  <div className="h-8 w-8 animate-spin rounded-full border-4 border-emerald-200 border-t-emerald-600" />
                </div>
              ) : phrase ? (
                <>
                  <p className="text-base font-medium leading-7 text-slate-700 sm:text-lg sm:leading-8">
                    &ldquo;{phrase.phrase}&rdquo;
                  </p>
                  <div className="mt-3 inline-flex rounded-full bg-indigo-50 px-2.5 py-1 text-xs font-medium text-indigo-700 sm:px-3 sm:text-sm">
                    Language: {phrase.language}
                  </div>
                </>
              ) : (
                <p className="text-center text-sm text-slate-500">No phrase available.</p>
              )}
            </div>

            <div className="mt-4 rounded-xl border border-dashed border-slate-300 bg-slate-50 p-4 sm:mt-6 sm:rounded-2xl sm:p-5">
              <p className="text-xs font-semibold text-slate-600 sm:text-sm">Notes</p>
              <p className="mt-1 text-xs leading-6 text-slate-500 sm:mt-2 sm:text-sm sm:leading-7">
                Preserve the tone and intent of the phrase while keeping the translation natural and readable.
              </p>
            </div>
          </section>

          <section className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:rounded-3xl sm:p-6">
            <div className="flex items-start justify-between gap-3">
              <div className="min-w-0">
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500 sm:text-sm">Contribution form</p>
                <h2 className="mt-1 text-lg font-semibold text-slate-900 sm:mt-2 sm:text-xl">Write Translation</h2>
              </div>
            </div>

            <label className="mt-4 block text-xs font-medium text-slate-700 sm:mt-6 sm:text-sm" htmlFor="translation">Translation</label>
            <textarea
              id="translation"
              rows={5}
              value={translationText}
              onChange={(e) => setTranslationText(e.target.value)}
              disabled={!phrase || loading}
              className="mt-1 w-full rounded-xl border border-slate-300 bg-slate-50 px-3 py-2.5 text-sm text-slate-700 outline-none transition focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 disabled:cursor-not-allowed disabled:opacity-50 sm:mt-2 sm:rounded-2xl sm:px-4"
              placeholder="Type the English translation here..."
            />

            <div className="mt-4 rounded-xl border border-slate-200 bg-slate-50 p-3 sm:mt-6 sm:rounded-2xl sm:p-4">
              <div className="flex items-center justify-between gap-2">
                <div className="min-w-0">
                  <p className="text-xs font-semibold text-slate-700 sm:text-sm">Audio Recording</p>
                  <p className="mt-0.5 text-xs text-slate-500 sm:mt-1 sm:text-sm">
                    {audioUrl ? "Uploaded successfully" : "Optional voice note"}
                  </p>
                </div>
                <button
                  onClick={toggleRecording}
                  disabled={!phrase || audioUploading}
                  className={`shrink-0 rounded-full px-3 py-1.5 text-xs font-semibold text-white transition disabled:opacity-50 sm:px-4 sm:py-2 sm:text-sm ${
                    audioUploading ? "bg-amber-500" : isRecording ? "bg-slate-700 hover:bg-slate-800" : "bg-red-500 hover:bg-red-600"
                  }`}
                >
                  {audioUploading ? "Uploading..." : isRecording ? "Stop" : audioUrl ? "Re-record" : "Record"}
                </button>
              </div>

              <div className="mt-3 rounded-xl border border-slate-200 bg-slate-900 p-3 sm:mt-4 sm:rounded-2xl sm:p-4">
                <div className="flex items-center gap-3">
                  <div className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-full sm:h-10 sm:w-10 ${isRecording ? "bg-red-500/30 text-red-400" : "bg-red-500/20 text-red-400"}`}>
                    <svg viewBox="0 0 24 24" className={`h-4 w-4 sm:h-5 sm:w-5 ${isRecording ? "animate-pulse" : ""}`} fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M12 3a3 3 0 0 0-3 3v5a3 3 0 0 0 6 0V6a3 3 0 0 0-3-3Z" />
                      <path d="M6 11a6 6 0 0 0 12 0" strokeLinecap="round" />
                      <path d="M12 17v4" strokeLinecap="round" />
                      <path d="M8 21h8" strokeLinecap="round" />
                    </svg>
                  </div>
                  <div className="min-w-0 flex-1">
                    {showSimulated ? (
                      <div className="flex items-end gap-0.5 sm:gap-1">
                        {[...Array(12)].map((_, index) => (
                          <div key={index} className="w-1 rounded-full bg-slate-500" style={{ height: `${18 + ((index + 1) % 5) * 6}px` }} />
                        ))}
                      </div>
                    ) : audioUrl ? (
                      <audio src={audioUrl} controls className="w-full h-8" />
                    ) : (
                      <div className="flex items-center gap-2 text-xs text-slate-400 sm:text-sm">
                        {isRecording ? (
                          <span className="flex items-center gap-2">
                            <span className="inline-block h-2 w-2 animate-pulse rounded-full bg-red-500" />
                            Recording...
                          </span>
                        ) : (
                          <span>Click Record to start</span>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </section>
        </main>

        <div className="flex flex-col gap-2 rounded-2xl border border-slate-200 bg-white p-3 shadow-sm sm:flex-row sm:justify-end sm:gap-3 sm:p-4">
          <button
            onClick={handleSkip}
            disabled={loading || !phrase}
            className="rounded-full border border-slate-300 bg-slate-100 px-4 py-2 text-sm font-semibold text-slate-600 transition hover:bg-slate-200 disabled:opacity-50"
          >
            Skip Phrase
          </button>
          <button
            onClick={handleSubmit}
            disabled={submitting || !phrase || !translationText.trim()}
            className="rounded-full bg-emerald-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-emerald-700 disabled:opacity-50"
          >
            {submitting ? "Submitting..." : "Submit Contribution"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ContributorDashboard;
