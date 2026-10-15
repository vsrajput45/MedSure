'use client';

import { useState, useEffect, useCallback } from 'react';
import { Shield, Sparkles, Activity, CheckCircle2 } from 'lucide-react';

interface LogoIntroProps {
  /** Duration in milliseconds before starting exit animation */
  durationMs?: number;
}

export default function LogoIntro({ durationMs = 900 }: LogoIntroProps) {
  const [mounted, setMounted] = useState(false);
  const [exiting, setExiting] = useState(false);
  const [progress, setProgress] = useState(0);

  const handleDismiss = useCallback(() => {
    setExiting(true);
    try {
      if (typeof window !== 'undefined') {
        sessionStorage.setItem('medsure_intro_dismissed', 'true');
        localStorage.setItem('medsure_intro_seen', 'true');
      }
    } catch {}
    setTimeout(() => {
      setMounted(false);
    }, 150);
  }, []);

  useEffect(() => {
    // Check if already seen or dismissed
    try {
      if (
        typeof window !== 'undefined' &&
        (sessionStorage.getItem('medsure_intro_dismissed') === 'true' ||
          localStorage.getItem('medsure_intro_seen') === 'true')
      ) {
        return;
      }
    } catch {
      return;
    }

    setMounted(true);

    // Fast progress ticker
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(progressInterval);
          return 100;
        }
        return prev + 25;
      });
    }, 70);

    // Guaranteed auto-exit transition
    const exitTimer = setTimeout(() => {
      setExiting(true);
      try {
        sessionStorage.setItem('medsure_intro_dismissed', 'true');
        localStorage.setItem('medsure_intro_seen', 'true');
      } catch {}
    }, durationMs);

    // Guaranteed unmount after exit
    const unmountTimer = setTimeout(() => {
      setMounted(false);
    }, durationMs + 350);

    // Hard fallback safety unmount: NEVER allow intro to stay past 1.6 seconds
    const hardFallbackTimer = setTimeout(() => {
      setExiting(true);
      setMounted(false);
    }, 1600);

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' || e.key === 'Enter' || e.key === ' ') {
        handleDismiss();
      }
    };
    window.addEventListener('keydown', handleKeyDown);

    return () => {
      clearInterval(progressInterval);
      clearTimeout(exitTimer);
      clearTimeout(unmountTimer);
      clearTimeout(hardFallbackTimer);
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [durationMs, handleDismiss]);

  if (!mounted) return null;

  return (
    <div
      role="dialog"
      aria-label="MedSure Initializing Intro"
      onClick={handleDismiss}
      className={`fixed inset-0 z-[9999] flex flex-col items-center justify-center bg-slate-950/95 backdrop-blur-md text-white overflow-hidden transition-all duration-300 ease-out select-none cursor-pointer ${
        exiting ? 'opacity-0 scale-105 pointer-events-none' : 'opacity-100 scale-100'
      }`}
    >
      {/* Ambient background glow orbs */}
      <div className="absolute -top-32 -left-32 w-96 h-96 bg-teal-500/20 rounded-full blur-[120px] pointer-events-none animate-pulse" />
      <div className="absolute -bottom-32 -right-32 w-96 h-96 bg-emerald-500/20 rounded-full blur-[120px] pointer-events-none animate-pulse" />
      <div className="absolute inset-0 bg-[radial-gradient(#14b8a6_1px,transparent_1px)] [background-size:32px_32px] opacity-15 pointer-events-none" />

      {/* Skip button in top corner */}
      <button
        type="button"
        onClick={(e) => {
          e.stopPropagation();
          handleDismiss();
        }}
        className="absolute top-6 right-6 px-4 py-1.5 rounded-full bg-slate-900/90 hover:bg-slate-800 border border-slate-700 text-xs text-slate-300 hover:text-white transition-all cursor-pointer backdrop-blur-md shadow-lg"
      >
        Skip to Website ➔
      </button>

      {/* Centerpiece Emblem & Branding */}
      <div className="relative z-10 flex flex-col items-center text-center px-4 max-w-md w-full" onClick={(e) => e.stopPropagation()}>
        {/* Animated Shield Emblem */}
        <div className="relative mb-6">
          {/* Sonic Radar Rings */}
          <div className="absolute -inset-4 rounded-3xl bg-teal-500/20 blur-xl animate-ping opacity-60" />
          <div className="absolute -inset-8 rounded-full border border-teal-500/30 animate-pulse pointer-events-none" />

          {/* Core Shield Box */}
          <div className="relative w-20 h-20 sm:w-24 sm:h-24 rounded-3xl bg-gradient-to-br from-teal-400 via-teal-600 to-emerald-700 p-0.5 shadow-2xl shadow-teal-500/30">
            <div className="w-full h-full rounded-[22px] bg-slate-950/80 backdrop-blur-sm flex items-center justify-center relative overflow-hidden group">
              {/* Inner ambient shine */}
              <div className="absolute inset-0 bg-gradient-to-tr from-teal-500/20 via-transparent to-emerald-400/20" />
              
              <Shield className="w-10 h-10 sm:w-12 sm:h-12 text-teal-400 stroke-[2.3] filter drop-shadow-[0_0_12px_rgba(45,212,191,0.6)] animate-pulse" />
              
              <span className="absolute bottom-2 right-2 flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500" />
              </span>
            </div>
          </div>
        </div>

        {/* Brand Name with Shimmer */}
        <div className="flex items-center gap-2 mb-2">
          <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-white">
            MEDSURE
          </h1>
          <span className="inline-flex items-center gap-1 text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-teal-500/20 text-teal-300 border border-teal-500/30">
            <Sparkles className="w-2.5 h-2.5" />
            v1.0
          </span>
        </div>

        {/* Slogan */}
        <p className="text-xs sm:text-sm font-medium text-teal-300 tracking-wide mb-1">
          Know the Fair Price. Verify Every Bill.
        </p>
        <p className="text-xs font-semibold text-slate-400 tracking-wide mb-6">
          सही दाम जानो। हर बिल जांचो।
        </p>

        {/* High-tech Loading & Verification Ticker */}
        <div className="w-full max-w-xs space-y-3">
          <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden p-0.5">
            <div
              className="h-full bg-gradient-to-r from-teal-400 via-teal-500 to-emerald-400 rounded-full transition-all duration-150 ease-out shadow-[0_0_10px_rgba(20,184,166,0.8)]"
              style={{ width: `${Math.min(progress, 100)}%` }}
            />
          </div>

          <div className="flex items-center justify-between text-[11px] text-slate-400 font-mono">
            <span className="flex items-center gap-1 text-teal-400">
              <Activity className="w-3 h-3 animate-spin" />
              <span>Initializing Verified Engine...</span>
            </span>
            <span className="tabular-nums font-bold text-slate-300">{Math.min(progress, 100)}%</span>
          </div>

          <button
            type="button"
            onClick={handleDismiss}
            className="w-full py-2.5 px-4 rounded-xl bg-gradient-to-r from-teal-500 to-emerald-600 hover:from-teal-600 hover:to-emerald-700 text-slate-950 font-bold text-xs shadow-lg shadow-teal-500/25 transition-all cursor-pointer flex items-center justify-center gap-1.5 mt-2"
          >
            <span>Enter Platform Now</span>
            <span>➔</span>
          </button>

          <div className="flex items-center justify-center gap-2 pt-1 text-[10px] text-slate-400">
            <CheckCircle2 className="w-3 h-3 text-emerald-400" />
            <span>Zero Rate Hallucinations • Decimal Exact</span>
          </div>
        </div>
      </div>
    </div>
  );
}
