// pages/LoginPage.tsx
import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { Spinner } from "../../../shared/ui/Spinner";

type Mode = "signin" | "signup";

const LoginPage = () => {
  const { login, register } = useAuth();
  const [mode, setMode] = useState<Mode>("signin");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const isSignup = mode === "signup";

  const switchMode = (next: Mode) => {
    setMode(next);
    setError(null);
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);
    try {
      if (isSignup) {
        await register(username, email, password);
      } else {
        await login(email, password);
      }
    } catch (err: any) {
      setError(err?.response?.data?.message ?? "Something went wrong. Try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-[#0B0E14] px-4">
      <style>{`
        @media (prefers-reduced-motion: no-preference) {
          .sparkline-path { animation: draw 3.5s ease-in-out infinite alternate; }
          @keyframes draw {
            0% { stroke-dashoffset: 340; }
            100% { stroke-dashoffset: 0; }
          }
        }
      `}</style>

      <div className="w-full max-w-sm overflow-hidden rounded-2xl border border-[#232733] bg-[#12151C] shadow-[0_0_0_1px_rgba(255,255,255,0.02),0_20px_40px_-15px_rgba(0,0,0,0.5)]">
        {/* Signature: sparkline header */}
        <div className="relative h-16 border-b border-[#232733] bg-[#0E1117]">
          <svg viewBox="0 0 400 64" className="h-full w-full" preserveAspectRatio="none">
            <defs>
              <linearGradient id="sparkStroke" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%" stopColor="#2DD4BF" />
                <stop offset="100%" stopColor="#60A5FA" />
              </linearGradient>
              <linearGradient id="sparkFill" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#2DD4BF" stopOpacity="0.18" />
                <stop offset="100%" stopColor="#2DD4BF" stopOpacity="0" />
              </linearGradient>
            </defs>
            <path
              d="M0,42 L30,38 L55,46 L80,24 L110,30 L140,14 L170,26 L200,18 L230,32 L260,20 L290,28 L320,12 L350,22 L400,16 L400,64 L0,64 Z"
              fill="url(#sparkFill)"
              stroke="none"
            />
            <path
              className="sparkline-path"
              d="M0,42 L30,38 L55,46 L80,24 L110,30 L140,14 L170,26 L200,18 L230,32 L260,20 L290,28 L320,12 L350,22 L400,16"
              fill="none"
              stroke="url(#sparkStroke)"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeDasharray="340"
            />
          </svg>
          <div className="absolute right-3 top-3 flex items-center gap-1.5">
            <span className="relative flex h-1.5 w-1.5">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-teal-400 opacity-75" />
              <span className="relative inline-flex h-1.5 w-1.5 rounded-full bg-teal-400" />
            </span>
            <span className="font-mono text-[10px] uppercase tracking-wider text-slate-500">Live</span>
          </div>
        </div>

        <div className="p-8">
          <div className="mb-6 flex items-center gap-2">
            <div className="flex h-7 w-7 items-center justify-center rounded-md bg-gradient-to-br from-teal-400 to-blue-500">
              <svg viewBox="0 0 24 24" className="h-3.5 w-3.5 text-[#0B0E14]" fill="currentColor">
                <path d="M12 2l1.8 5.6L19 9l-5.2 1.4L12 16l-1.8-5.6L5 9l5.2-1.4L12 2z" />
              </svg>
            </div>
            <span className="text-sm font-medium text-slate-100">DataLens - Your AI Analytics Companion</span>
          </div>

          {/* Segmented toggle with sliding indicator */}
          <div className="relative mb-6 flex rounded-lg border border-[#232733] bg-[#0B0E14] p-1">
            <div
              className={`absolute inset-y-1 w-[calc(50%-4px)] rounded-md bg-[#1C212C] transition-transform duration-200 ease-out ${
                isSignup ? "translate-x-[calc(100%+8px)]" : "translate-x-0"
              }`}
            />
            <button
              type="button"
              onClick={() => switchMode("signin")}
              className={`relative z-10 flex-1 rounded-md py-1.5 text-sm font-medium transition-colors ${
                !isSignup ? "text-slate-100" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              Sign in
            </button>
            <button
              type="button"
              onClick={() => switchMode("signup")}
              className={`relative z-10 flex-1 rounded-md py-1.5 text-sm font-medium transition-colors ${
                isSignup ? "text-slate-100" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              Sign up
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="rounded-lg border border-red-900/50 bg-red-950/40 px-3 py-2 text-sm text-red-400">
                {error}
              </div>
            )}

            {isSignup && (
              <div>
                <label
                  htmlFor="username"
                  className="mb-1.5 block font-mono text-[11px] uppercase tracking-wider text-white"
                >
                  Username
                </label>
                <input
                  id="username"
                  type="text"
                  required
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="mehak"
                  className="w-full rounded-lg border border-[#232733] bg-[#0B0E14] px-3.5 py-2.5 text-sm text-slate-100 placeholder:text-slate-600 focus:border-teal-500/50 focus:outline-none focus:ring-2 focus:ring-teal-500/10"
                />
              </div>
            )}

            <div>
              <label
                htmlFor="email"
                className="mb-1.5 block font-mono text-[11px] uppercase tracking-wider text-white"
              >
                Email
              </label>
              <input
                id="email"
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="hello@company.com"
                className="w-full rounded-lg border border-[#232733] bg-[#0B0E14] px-3.5 py-2.5 text-sm text-slate-100 placeholder:text-slate-600 focus:border-teal-500/50 focus:outline-none focus:ring-2 focus:ring-teal-500/10"
              />
            </div>

            <div>
              <label
                htmlFor="password"
                className="mb-1.5 block font-mono text-[11px] uppercase tracking-wider text-white"
              >
                Password
              </label>
              <div className="relative">
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  required
                  minLength={8}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••••"
                  className="w-full rounded-lg border border-[#232733] bg-[#0B0E14] px-3.5 py-2.5 pr-10 text-sm text-slate-100 placeholder:text-slate-600 focus:border-teal-500/50 focus:outline-none focus:ring-2 focus:ring-teal-500/10"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((s) => !s)}
                  aria-label={showPassword ? "Hide password" : "Show password"}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-600 hover:text-slate-400"
                >
                  {showPassword ? (
                    <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M3 3l18 18M10.6 10.6a2 2 0 002.8 2.8M9.5 5.3A9.8 9.8 0 0112 5c5 0 9 4 10 7-.4 1.2-1.2 2.5-2.3 3.7M6.5 6.7C4.6 8 3.2 9.8 2 12c1 3 5 7 10 7 1.3 0 2.6-.3 3.7-.8" />
                    </svg>
                  ) : (
                    <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7-10-7-10-7z" />
                      <circle cx="12" cy="12" r="3" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                  )}
                </button>
              </div>
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="flex w-full items-center justify-center gap-2 rounded-lg bg-gradient-to-r from-teal-400 to-blue-500 py-2.5 text-sm font-medium text-[#0B0E14] transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {isSubmitting ? (
                <>
                  <Spinner size="sm" className="border-[#0B0E14]/30 border-t-[#0B0E14]" />
                  {isSignup ? "Creating account…" : "Signing in…"}
                </>
              ) : isSignup ? (
                "Create account"
              ) : (
                "Sign in"
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;