import { Shield, HeartHandshake, CheckCircle2, FileText, Database, Stethoscope, Sparkles } from 'lucide-react';
import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="relative bg-gradient-to-b from-slate-900 via-slate-950 to-slate-950 text-slate-300 border-t border-slate-800/80 mt-24 overflow-hidden">
      {/* Background ambient lighting */}
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-teal-500/5 rounded-full blur-3xl pointer-events-none"></div>
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-emerald-500/5 rounded-full blur-3xl pointer-events-none"></div>

      <div className="w-full px-4 sm:px-8 lg:px-12 xl:px-16 2xl:px-20 py-16 relative z-10">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-10 mb-12">
          {/* Brand Column */}
          <div className="lg:col-span-2 space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-teal-500 to-emerald-600 flex items-center justify-center text-white shadow-md shadow-teal-500/20">
                <Shield className="w-5 h-5 stroke-[2.3]" />
              </div>
              <div className="flex flex-col">
                <span className="text-xl font-extrabold text-white tracking-tight">MEDSURE</span>
                <span className="text-[10px] uppercase font-bold tracking-wider text-teal-400">Healthcare Financial Intelligence</span>
              </div>
            </div>

            <p className="text-sm text-slate-400 leading-relaxed max-w-md">
              AI-Powered Healthcare Cost Transparency, Medical Bill Auditing & Fair-Price Estimation Platform. Built to protect patients and families from unverified charges.
            </p>

            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-800/90 border border-slate-700/80 text-xs">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
              </span>
              <span className="text-emerald-300 font-semibold">सही दाम जानो। हर बिल जांचो।</span>
              <span className="text-slate-400">• Patient-First Standard</span>
            </div>
          </div>

          {/* Quick Platform Navigation */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-white uppercase tracking-wider">Navigation</h4>
            <ul className="space-y-2.5 text-xs text-slate-400">
              <li>
                <Link href="/" className="hover:text-teal-400 transition-colors flex items-center gap-1.5">
                  <span>Home Overview</span>
                </Link>
              </li>
              <li>
                <Link href="/dashboard" className="hover:text-teal-400 transition-colors flex items-center gap-1.5">
                  <span>Patient Dashboard</span>
                </Link>
              </li>
              <li>
                <Link href="/triage" className="hover:text-teal-400 transition-colors flex items-center gap-1.5">
                  <span>Fair Price Estimator</span>
                </Link>
              </li>
              <li>
                <Link href="/bills/upload" className="hover:text-teal-400 transition-colors flex items-center gap-1.5">
                  <span>Audit Medical Bill</span>
                </Link>
              </li>
              <li>
                <Link href="/reference-rates" className="hover:text-teal-400 transition-colors flex items-center gap-1.5">
                  <span>Tariff Benchmarks</span>
                </Link>
              </li>
              <li>
                <Link href="/demo" className="hover:text-amber-400 transition-colors flex items-center gap-1.5 text-amber-300/90 font-medium">
                  <Sparkles className="w-3 h-3 text-amber-400" />
                  <span>2-Min Demo Walkthrough</span>
                </Link>
              </li>
            </ul>
          </div>

          {/* Engine Architecture & Rules */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-white uppercase tracking-wider">Audit Rules</h4>
            <ul className="space-y-2 text-xs text-slate-400">
              <li className="flex items-center gap-2">
                <span className="w-5 h-5 rounded-md bg-emerald-950/80 border border-emerald-800 text-emerald-400 flex items-center justify-center font-bold text-[10px]">A</span>
                <span>Arithmetic Verification</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="w-5 h-5 rounded-md bg-amber-950/80 border border-amber-800 text-amber-400 flex items-center justify-center font-bold text-[10px]">B</span>
                <span>Duplicate OT & Surgery Flags</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="w-5 h-5 rounded-md bg-blue-950/80 border border-blue-800 text-blue-400 flex items-center justify-center font-bold text-[10px]">C</span>
                <span>Government Tariff Benchmarks</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="w-5 h-5 rounded-md bg-purple-950/80 border border-purple-800 text-purple-400 flex items-center justify-center font-bold text-[10px]">D</span>
                <span>Package Unbundling Checks</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="w-5 h-5 rounded-md bg-rose-950/80 border border-rose-800 text-rose-400 flex items-center justify-center font-bold text-[10px]">E</span>
                <span>Incompleteness & Zero Rates</span>
              </li>
            </ul>
          </div>

          {/* Auditable Standard & Safety */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-white uppercase tracking-wider">Integrity Standard</h4>
            <p className="text-xs text-slate-400 leading-relaxed">
              Calculations are computed using Decimal precision. Rates match verified CGHS and NPPA government benchmarks. No clinical diagnosis is provided.
            </p>
            <div className="pt-2 flex flex-wrap gap-2">
              <span className="text-[10px] font-semibold px-2 py-0.5 rounded-md bg-slate-800 text-slate-300 border border-slate-700">
                PyMuPDF OCR
              </span>
              <span className="text-[10px] font-semibold px-2 py-0.5 rounded-md bg-slate-800 text-slate-300 border border-slate-700">
                Decimal Math
              </span>
              <span className="text-[10px] font-semibold px-2 py-0.5 rounded-md bg-slate-800 text-slate-300 border border-slate-700">
                ReportLab PDF
              </span>
            </div>
          </div>
        </div>

        {/* Bottom divider and copyright */}
        <div className="pt-8 border-t border-slate-800/80 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500">
          <div className="flex items-center gap-2">
            <HeartHandshake className="w-4 h-4 text-teal-400" />
            <span>© 2026 MEDSURE Healthcare Intelligence. All Rights Reserved.</span>
          </div>

          <div className="flex items-center gap-4 text-slate-400">
            <span>Deterministic Engine v1.0</span>
            <span className="text-slate-700">•</span>
            <span>Non-Diagnostic Triage</span>
            <span className="text-slate-700">•</span>
            <span className="text-teal-400 font-semibold">100% Mathematical Proof</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
