import { useState } from "react";
import axios from "axios";

export default function FindMatchesButton() {
  const [jobDescription, setJobDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [matches, setMatches] = useState([]);
  const [error, setError] = useState("");

  const handleFindMatches = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await axios.post(
        "http://localhost:8000/api/mike/match",
        {
          job_description: jobDescription,
        }
      );

      setMatches(response.data.matches || response.data || []);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch candidate matches");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#050816] text-white p-6">
      <div className="max-w-5xl mx-auto space-y-8">
        {/* Header */}
        <div className="bg-gradient-to-r from-indigo-600 via-violet-600 to-fuchsia-600 rounded-3xl p-[1px] shadow-2xl">
          <div className="bg-slate-950 rounded-3xl p-8">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h1 className="text-5xl font-black tracking-tight bg-gradient-to-r from-cyan-300 to-fuchsia-400 bg-clip-text text-transparent">
                  Mike AI Recruiter
                </h1>

                <p className="text-slate-400 mt-3 text-lg">
                  Paste a job description and instantly rank candidates using AI.
                </p>
              </div>

              <div className="hidden md:flex items-center gap-2 bg-fuchsia-500/20 border border-fuchsia-400/20 px-4 py-2 rounded-2xl text-fuchsia-200 font-semibold">
                ✨ AI Matching
              </div>
            </div>

            {/* Input */}
            <div className="space-y-4">
              <textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste job description here..."
                className="w-full h-64 rounded-3xl bg-slate-900 border border-slate-800 text-white p-5 resize-none focus:outline-none focus:ring-4 focus:ring-violet-500/30 placeholder:text-slate-500 text-sm"
              />

              <button
                onClick={handleFindMatches}
                disabled={loading || !jobDescription.trim()}
                className="w-full bg-gradient-to-r from-cyan-500 via-blue-500 to-fuchsia-500 hover:scale-[1.01] active:scale-[0.99] transition-all duration-300 text-white py-4 rounded-2xl font-bold text-lg shadow-lg disabled:opacity-50"
              >
                {loading ? (
                  <div className="flex items-center justify-center gap-3">
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    Finding Best Candidates...
                  </div>
                ) : (
                  "Find Matches"
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Error */}
        {error && (
          <div className="bg-red-500/10 border border-red-500/20 text-red-400 rounded-2xl p-4 font-medium">
            {error}
          </div>
        )}

        {/* Results */}
        {matches.length > 0 && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-3xl font-black">
                  Top Candidate Matches
                </h2>

                <p className="text-slate-400 mt-1">
                  AI-ranked candidates based on semantic relevance
                </p>
              </div>

              <div className="bg-emerald-500/20 text-emerald-300 border border-emerald-400/20 px-4 py-2 rounded-xl font-semibold text-sm">
                {matches.length} Candidates
              </div>
            </div>

            <div className="grid gap-5">
              {matches.map((candidate, index) => (
                <div
                  key={index}
                  className="group relative overflow-hidden rounded-3xl border border-slate-800 bg-slate-900/80 p-6 hover:border-fuchsia-500/40 transition-all duration-300 hover:shadow-2xl hover:shadow-fuchsia-500/10"
                >
                  {/* Glow */}
                  <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity bg-gradient-to-r from-fuchsia-500/5 via-transparent to-cyan-500/5"></div>

                  <div className="relative z-10">
                    {/* Candidate Header */}
                    <div className="flex items-start justify-between gap-5">
                      <div className="flex items-center gap-4">

                        <div>
                          <h3 className="text-2xl font-bold text-white">
                            #{index + 1} {candidate.candidate_name}
                          </h3>

                          <p className="text-slate-400 text-sm mt-1">
                            AI Recommended Candidate
                          </p>
                        </div>
                      </div>

                      <div className="bg-gradient-to-r from-emerald-400 to-cyan-400 text-black px-4 py-2 rounded-2xl text-sm font-black shadow-lg">
                        MATCHED
                      </div>
                    </div>

                    {/* Rationale */}
                    <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-950/60 p-5">
                      <div className="flex items-center gap-2 mb-3">
                        <span className="text-fuchsia-400 text-lg">
                          🧠
                        </span>

                        <h4 className="text-fuchsia-300 uppercase tracking-wide text-sm font-bold">
                          Match Rationale
                        </h4>
                      </div>

                      <p className="text-slate-300 leading-relaxed">
                        {candidate.rationale}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}