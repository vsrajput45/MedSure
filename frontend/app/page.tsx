'use client';

import { useState } from 'react';
import Link from 'next/link';
import { 
  ShieldCheck, 
  Stethoscope, 
  FileSearch, 
  ArrowRight, 
  Calculator, 
  AlertTriangle, 
  FileCheck, 
  BadgePercent, 
  CheckCircle2, 
  Sparkles,
  Search,
  Scale,
  Copy,
  Layers,
  FileText,
  Activity,
  HeartPulse,
  Clock,
  Download,
  HelpCircle,
  TrendingDown,
  ChevronRight,
  ShieldAlert,
  Building2,
  Lock,
  Check,
  X,
  ExternalLink,
  Zap,
  SlidersHorizontal,
  ChevronDown,
  Info
} from 'lucide-react';

export default function HomePage() {
  // Interactive Simulator State: 'audited' vs 'raw'
  const [auditMode, setAuditMode] = useState<'audited' | 'raw'>('audited');
  
  // Interactive Procedure Estimator Teaser
  const [selectedSpecialty, setSelectedSpecialty] = useState<string>('Orthopedics');
  const [selectedProcedure, setSelectedProcedure] = useState<string>('TKR');

  const procedurePresets: Record<string, { name: string; min: string; median: string; max: string; code: string; scheme: string }> = {
    'TKR': {
      name: 'Total Knee Replacement (Unilateral)',
      min: '₹1,25,000',
      median: '₹1,45,000',
      max: '₹1,85,000',
      code: 'PROC-ORTHO-TKR-01',
      scheme: 'CGHS / NPPA Implants Cap'
    },
    'CABG': {
      name: 'Coronary Artery Bypass Graft (CABG)',
      min: '₹1,80,000',
      median: '₹2,35,000',
      max: '₹3,10,000',
      code: 'PROC-CARD-CABG-04',
      scheme: 'National Health Tariff Ceiling'
    },
    'CATARACT': {
      name: 'Cataract Phacoemulsification with Foldable IOL',
      min: '₹18,500',
      median: '₹28,000',
      max: '₹42,000',
      code: 'PROC-OPHTH-CAT-02',
      scheme: 'Standard Tier-1 Registry'
    },
    'APP': {
      name: 'Laparoscopic Appendectomy',
      min: '₹45,000',
      median: '₹62,000',
      max: '₹85,000',
      code: 'PROC-SURG-APP-03',
      scheme: 'NABH Super Specialty Guideline'
    }
  };

  const activeProcedure = procedurePresets[selectedProcedure] || procedurePresets['TKR'];

  return (
    <div className="space-y-24 pb-24 overflow-x-hidden">
      {/* ========================================================= */}
      {/* HERO SECTION: High-impact typography, dual CTAs, & ambient glow */}
      {/* ========================================================= */}
      <section className="relative overflow-hidden pt-12 pb-20 lg:pt-20 lg:pb-28 bg-ambient-light">
        {/* Ambient background light bursts */}
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[500px] bg-gradient-to-tr from-teal-400/15 via-emerald-400/10 to-transparent rounded-full blur-[100px] pointer-events-none" />
        <div className="absolute top-10 right-10 w-96 h-96 bg-cyan-400/10 rounded-full blur-[90px] pointer-events-none" />

        <div className="w-full px-4 sm:px-8 lg:px-12 xl:px-16 2xl:px-20 relative z-10">
          <div className="text-center max-w-4xl mx-auto space-y-6">
            {/* Live Indicator Pill */}
            <div className="inline-flex items-center gap-2.5 px-4 py-1.5 rounded-full bg-white/95 border border-teal-200/90 shadow-xs text-xs font-semibold text-slate-800 backdrop-blur-md">
              <span className="relative flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-teal-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-teal-600"></span>
              </span>
              <span className="text-teal-950 font-bold tracking-tight">Patient-First Cost Transparency</span>
              <span className="text-slate-300">•</span>
              <span className="text-emerald-700 font-bold">Zero LLM Rate Hallucinations</span>
            </div>

            {/* Main Headline with Curated Gradient */}
            <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold text-slate-950 tracking-tight leading-[1.08]">
              Know the Fair Price. <br />
              <span className="bg-gradient-to-r from-teal-600 via-teal-700 to-emerald-600 bg-clip-text text-transparent">
                Verify Every Bill.
              </span>
            </h1>

            {/* Bilingual Slogan Badge */}
            <div className="inline-flex items-center gap-3 px-5 py-2.5 rounded-2xl bg-teal-50/90 border border-teal-200/90 shadow-xs backdrop-blur-sm">
              <HeartPulse className="w-4 h-4 text-teal-600 animate-pulse" />
              <p className="text-base sm:text-lg font-extrabold text-teal-950 tracking-wide font-sans">
                सही दाम जानो। हर बिल जांचो।
              </p>
              <span className="text-[11px] font-bold text-teal-800 bg-teal-100/90 px-2.5 py-0.5 rounded-md hidden sm:inline-block">
                Bilingual Clinical Guidance
              </span>
            </div>

            {/* Subtitle */}
            <p className="text-base sm:text-lg text-slate-600 leading-relaxed max-w-2xl mx-auto font-normal">
              Healthcare costs shouldn’t be a high-stakes mystery. MEDSURE empowers patients to estimate procedural cost benchmarks <b>before admission</b> and audit itemized hospital invoices <b>after discharge</b> with deterministic mathematical proof.
            </p>

            {/* Primary Action Buttons */}
            <div className="flex flex-col sm:flex-row items-center justify-center gap-3.5 pt-4">
              <Link
                href="/triage"
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-6 py-4 rounded-xl bg-gradient-to-r from-teal-600 to-emerald-600 hover:from-teal-700 hover:to-emerald-700 text-white font-bold text-sm shadow-lg shadow-teal-700/25 hover:shadow-teal-700/35 hover:-translate-y-0.5 transition-all"
              >
                <Stethoscope className="w-4 h-4" />
                <span>Act 1: Before Admission</span>
                <ArrowRight className="w-4 h-4 ml-0.5" />
              </Link>

              <Link
                href="/bills/upload"
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-6 py-4 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-sm shadow-lg shadow-slate-950/20 hover:shadow-slate-950/30 hover:-translate-y-0.5 transition-all"
              >
                <FileSearch className="w-4 h-4 text-teal-400" />
                <span>Act 2: Audit Hospital Bill</span>
                <ArrowRight className="w-4 h-4 ml-0.5" />
              </Link>

              <Link
                href="/demo"
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-5 py-4 rounded-xl bg-amber-50 hover:bg-amber-100 text-amber-950 border border-amber-300/80 font-bold text-sm shadow-xs hover:-translate-y-0.5 transition-all"
              >
                <Sparkles className="w-4 h-4 text-amber-600" />
                <span>2-Min Live Walkthrough</span>
              </Link>
            </div>
          </div>

          {/* ========================================================= */}
          {/* INTERACTIVE HERO SIMULATOR: Live Hospital Bill Audit Card */}
          {/* ========================================================= */}
          <div className="mt-14 w-full max-w-6xl mx-auto">
            <div className="relative rounded-3xl p-1 bg-gradient-to-b from-teal-500/30 via-slate-200 to-slate-200/70 shadow-2xl">
              <div className="bg-white rounded-[22px] p-6 sm:p-8 space-y-6">
                {/* Header of preview card with Toggle */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-100">
                  <div className="flex items-center gap-3.5">
                    <div className="w-11 h-11 rounded-xl bg-teal-50 border border-teal-200 flex items-center justify-center text-teal-700 shadow-xs">
                      <FileCheck className="w-6 h-6 stroke-[2.2]" />
                    </div>
                    <div>
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className="text-sm font-bold text-slate-900">Apex Care Super Specialty Hospital</span>
                        <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-700 font-mono">
                          INV-2026-KNEE-8842
                        </span>
                      </div>
                      <p className="text-xs text-slate-500">Patient: Rajesh Kumar • Total Knee Replacement (TKR)</p>
                    </div>
                  </div>

                  {/* Mode Selector Toggle */}
                  <div className="flex items-center bg-slate-100 p-1 rounded-xl border border-slate-200/80 shrink-0 self-start sm:self-auto">
                    <button
                      onClick={() => setAuditMode('raw')}
                      className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                        auditMode === 'raw'
                          ? 'bg-white text-slate-900 shadow-xs'
                          : 'text-slate-500 hover:text-slate-800'
                      }`}
                    >
                      Original Hospital Invoice
                    </button>
                    <button
                      onClick={() => setAuditMode('audited')}
                      className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5 ${
                        auditMode === 'audited'
                          ? 'bg-teal-600 text-white shadow-xs'
                          : 'text-slate-500 hover:text-slate-800'
                      }`}
                    >
                      <Sparkles className="w-3 h-3 text-teal-200" />
                      <span>MEDSURE Audit Engine</span>
                    </button>
                  </div>
                </div>

                {/* Audit Summary Counters */}
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-slate-50 p-4 rounded-2xl border border-slate-200/80">
                  <div>
                    <span className="text-[11px] font-medium text-slate-500 block">Total Claimed</span>
                    <span className="text-base sm:text-lg font-bold text-slate-900 font-tabular">₹3,45,000.00</span>
                  </div>
                  <div>
                    <span className="text-[11px] font-medium text-slate-500 block">Verified Fair Total</span>
                    <span className="text-base sm:text-lg font-bold text-teal-700 font-tabular">₹2,52,500.00</span>
                  </div>
                  <div>
                    <span className="text-[11px] font-medium text-slate-500 block">Unjustified Charges</span>
                    <span className="text-base sm:text-lg font-extrabold text-red-600 font-tabular">-₹92,500.00</span>
                  </div>
                  <div>
                    <span className="text-[11px] font-medium text-slate-500 block">Audit Precision</span>
                    <span className="text-base sm:text-lg font-bold text-emerald-700 flex items-center gap-1">
                      <ShieldCheck className="w-4 h-4" />
                      <span>Decimal Exact</span>
                    </span>
                  </div>
                </div>

                {/* Line Items Table Showcase */}
                <div className="space-y-2.5">
                  {/* Line Item 1 */}
                  <div className={`p-4 rounded-2xl border transition-all ${
                    auditMode === 'audited'
                      ? 'bg-red-50/50 border-red-200/80'
                      : 'bg-white border-slate-200'
                  }`}>
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs">
                      <div className="flex items-start gap-3">
                        <span className={`w-6 h-6 rounded-lg font-bold flex items-center justify-center shrink-0 text-xs ${
                          auditMode === 'audited' ? 'bg-red-100 text-red-700' : 'bg-slate-100 text-slate-600'
                        }`}>
                          01
                        </span>
                        <div>
                          <div className="flex items-center gap-2">
                            <span className="font-bold text-slate-900 text-sm">Primary Knee Implant Prosthesis</span>
                            {auditMode === 'audited' && (
                              <span className="px-2 py-0.5 rounded-full bg-red-100 text-red-800 text-[10px] font-bold">
                                Rule C: Statutory Cap Breach
                              </span>
                            )}
                          </div>
                          <span className="text-slate-500 block text-[11px] mt-0.5">
                            {auditMode === 'audited'
                              ? 'Claimed ₹1,15,000 vs National NPPA Statutory Price Cap of ₹85,000'
                              : 'High-flex femoral component with titanium tibial tray (Qty: 1)'}
                          </span>
                        </div>
                      </div>
                      <div className="text-left sm:text-right shrink-0">
                        <span className="font-mono text-sm font-bold text-slate-900">₹1,15,000.00</span>
                        {auditMode === 'audited' && (
                          <span className="block font-bold text-red-600 text-xs font-tabular">-₹30,000 Overcharge</span>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Line Item 2 */}
                  <div className={`p-4 rounded-2xl border transition-all ${
                    auditMode === 'audited'
                      ? 'bg-amber-50/50 border-amber-200/80'
                      : 'bg-white border-slate-200'
                  }`}>
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs">
                      <div className="flex items-start gap-3">
                        <span className={`w-6 h-6 rounded-lg font-bold flex items-center justify-center shrink-0 text-xs ${
                          auditMode === 'audited' ? 'bg-amber-100 text-amber-800' : 'bg-slate-100 text-slate-600'
                        }`}>
                          02
                        </span>
                        <div>
                          <div className="flex items-center gap-2">
                            <span className="font-bold text-slate-900 text-sm">Operation Theatre Session Fee (OT Rental)</span>
                            {auditMode === 'audited' && (
                              <span className="px-2 py-0.5 rounded-full bg-amber-100 text-amber-900 text-[10px] font-bold">
                                Rule B: Redundant Duplicate
                              </span>
                            )}
                          </div>
                          <span className="text-slate-500 block text-[11px] mt-0.5">
                            {auditMode === 'audited'
                              ? 'Duplicate one-time procedural facility fee billed twice for the same surgical slot'
                              : 'Major Laminar Flow OT Facility Charge (Slot A & Slot B)'}
                          </span>
                        </div>
                      </div>
                      <div className="text-left sm:text-right shrink-0">
                        <span className="font-mono text-sm font-bold text-slate-900">₹35,000.00</span>
                        {auditMode === 'audited' && (
                          <span className="block font-bold text-amber-700 text-xs font-tabular">-₹35,000 Duplicate Fee</span>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Line Item 3 */}
                  <div className={`p-4 rounded-2xl border transition-all ${
                    auditMode === 'audited'
                      ? 'bg-red-50/50 border-red-200/80'
                      : 'bg-white border-slate-200'
                  }`}>
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs">
                      <div className="flex items-start gap-3">
                        <span className={`w-6 h-6 rounded-lg font-bold flex items-center justify-center shrink-0 text-xs ${
                          auditMode === 'audited' ? 'bg-red-100 text-red-700' : 'bg-slate-100 text-slate-600'
                        }`}>
                          03
                        </span>
                        <div>
                          <div className="flex items-center gap-2">
                            <span className="font-bold text-slate-900 text-sm">Lead Surgeon Operating Fee</span>
                            {auditMode === 'audited' && (
                              <span className="px-2 py-0.5 rounded-full bg-red-100 text-red-800 text-[10px] font-bold">
                                Rule A: Arithmetic Overstatement
                              </span>
                            )}
                          </div>
                          <span className="text-slate-500 block text-[11px] mt-0.5">
                            {auditMode === 'audited'
                              ? 'Multiplication error: 1 × ₹70,000 claimed as ₹85,000 (discrepancy: ₹15,000)'
                              : 'Consultant Orthopedic Surgeon operative fee (Qty: 1 @ ₹70,000)'}
                          </span>
                        </div>
                      </div>
                      <div className="text-left sm:text-right shrink-0">
                        <span className="font-mono text-sm font-bold text-slate-900">₹85,000.00</span>
                        {auditMode === 'audited' && (
                          <span className="block font-bold text-red-600 text-xs font-tabular">-₹15,000 Arithmetic Error</span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Footer Actions of Sample Card */}
                <div className="pt-2 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs border-t border-slate-100">
                  <div className="flex items-center gap-2 text-slate-600">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                    <span>Pure Python Decimal calculation — zero LLM hallucination</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <Link
                      href="/bills/upload"
                      className="inline-flex items-center gap-1.5 font-bold text-teal-700 hover:text-teal-900 transition"
                    >
                      <span>Upload Your Own Bill</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ========================================================= */}
      {/* TRUST METRICS STRIP: Verifiable mathematical guarantees */}
      {/* ========================================================= */}
      <section className="w-full px-4 sm:px-8 lg:px-12 xl:px-16 2xl:px-20">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
          <div className="p-6 rounded-2xl bg-white border border-slate-200/90 shadow-xs hover:shadow-md transition space-y-1.5">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Hallucinated Rates</span>
              <ShieldCheck className="w-4 h-4 text-teal-600" />
            </div>
            <div className="text-3xl font-extrabold text-teal-600">0%</div>
            <p className="text-xs text-slate-600">Deterministic tariff lookups only</p>
          </div>

          <div className="p-6 rounded-2xl bg-white border border-slate-200/90 shadow-xs hover:shadow-md transition space-y-1.5">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Decimal Exact</span>
              <Calculator className="w-4 h-4 text-emerald-600" />
            </div>
            <div className="text-3xl font-extrabold text-emerald-600">100%</div>
            <p className="text-xs text-slate-600">Audit-grade arithmetic to the paisa</p>
          </div>

          <div className="p-6 rounded-2xl bg-white border border-slate-200/90 shadow-xs hover:shadow-md transition space-y-1.5">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Audit Rules</span>
              <Scale className="w-4 h-4 text-indigo-600" />
            </div>
            <div className="text-3xl font-extrabold text-indigo-600">Rules A–E</div>
            <p className="text-xs text-slate-600">Statutory & procedural verification</p>
          </div>

          <div className="p-6 rounded-2xl bg-white border border-slate-200/90 shadow-xs hover:shadow-md transition space-y-1.5">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Audit Latency</span>
              <Clock className="w-4 h-4 text-amber-600" />
            </div>
            <div className="text-3xl font-extrabold text-amber-600">&lt; 300ms</div>
            <p className="text-xs text-slate-600">In-process PyMuPDF extraction</p>
          </div>
        </div>
      </section>

      {/* ========================================================= */}
      {/* ARCHITECTURAL CORE PRINCIPLE: The Technical Moat */}
      {/* ========================================================= */}
      <section className="w-full px-4 sm:px-8 lg:px-12 xl:px-16 2xl:px-20">
        <div className="relative overflow-hidden p-8 sm:p-12 rounded-3xl bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-white shadow-2xl border border-slate-800">
          <div className="absolute top-0 right-0 w-96 h-96 bg-teal-500/10 rounded-full blur-3xl pointer-events-none" />

          <div className="space-y-8 relative z-10">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="space-y-2">
                <span className="text-xs font-bold uppercase tracking-wider text-teal-400 bg-teal-950/80 px-3 py-1 rounded-full border border-teal-800/80">
                  Architectural Core Principle
                </span>
                <h2 className="text-2xl sm:text-4xl font-extrabold tracking-tight">
                  AI understands. Deterministic rules decide. Every calculation is verified.
                </h2>
              </div>
              <div className="shrink-0 flex items-center gap-2">
                <span className="text-xs font-semibold px-3 py-1.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                  Decoupled Pipeline Architecture
                </span>
              </div>
            </div>

            <p className="text-sm sm:text-base text-slate-300 max-w-3xl leading-relaxed">
              Unlike generic conversational wrappers that hallucinate medical tariffs, MEDSURE decouples clinical linguistic comprehension and OCR vision from arithmetic audit calculation. Financial outputs are guaranteed with exact mathematical proof.
            </p>

            {/* 4-Step Technical Workflow */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-2.5">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-bold text-teal-400 uppercase tracking-wider">Step 01</span>
                  <FileText className="w-4 h-4 text-slate-400" />
                </div>
                <h4 className="font-bold text-white text-base">PyMuPDF OCR</h4>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Extracts tabular line items, unit rates, quantities, and claimed totals with confidence scores.
                </p>
              </div>

              <div className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-2.5">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-bold text-teal-400 uppercase tracking-wider">Step 02</span>
                  <Stethoscope className="w-4 h-4 text-slate-400" />
                </div>
                <h4 className="font-bold text-white text-base">Clinical NLP</h4>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Interprets bilingual symptoms (Hindi/English) and screens for emergency red flags before pricing.
                </p>
              </div>

              <div className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-2.5">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-bold text-emerald-400 uppercase tracking-wider">Step 03</span>
                  <Calculator className="w-4 h-4 text-emerald-400" />
                </div>
                <h4 className="font-bold text-white text-base">Deterministic Engine</h4>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Executes Rules A through E using pure Python Decimal precision. Zero hallucination allowed.
                </p>
              </div>

              <div className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-2.5">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-bold text-teal-400 uppercase tracking-wider">Step 04</span>
                  <Download className="w-4 h-4 text-slate-400" />
                </div>
                <h4 className="font-bold text-white text-base">ReportLab PDF</h4>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Generates an official signed audit report and an editable hospital dispute letter ready to send.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ========================================================= */}
      {/* THE TWO ACTS: End-To-End Patient Journey */}
      {/* ========================================================= */}
      <section className="w-full px-4 sm:px-8 lg:px-12 xl:px-16 2xl:px-20 space-y-10">
        <div className="text-center max-w-2xl mx-auto space-y-3">
          <span className="text-xs font-bold uppercase tracking-wider text-teal-700 bg-teal-50 px-3.5 py-1 rounded-full border border-teal-200">
            End-To-End Patient Journey
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-950">
            Protected Before Admission. Verified After Discharge.
          </h2>
          <p className="text-sm sm:text-base text-slate-600">
            Complete financial and clinical clarity across both critical phases of healthcare delivery.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* ACT 1 Card */}
          <div className="bg-white rounded-3xl p-8 sm:p-10 border border-slate-200/90 shadow-sm hover:shadow-md transition-all space-y-8 flex flex-col justify-between">
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <div className="w-14 h-14 rounded-2xl bg-teal-50 border border-teal-200 flex items-center justify-center text-teal-700 shadow-xs">
                  <Stethoscope className="w-7 h-7 stroke-[2.2]" />
                </div>
                <span className="text-xs font-bold px-3.5 py-1.5 rounded-full bg-teal-50 text-teal-800 border border-teal-200">
                  ACT 1 • BEFORE ADMISSION
                </span>
              </div>

              <div>
                <h3 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">Symptom Guidance & Fair Cost Estimator</h3>
                <p className="text-sm text-slate-600 mt-2 leading-relaxed">
                  Understand the appropriate clinical specialty, check emergency red flags, and receive transparent procedure cost ranges before setting foot in a hospital.
                </p>
              </div>

              <ul className="space-y-3.5 text-sm text-slate-700">
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-4 h-4 text-teal-600 shrink-0 mt-0.5" />
                  <span><b>Bilingual Input:</b> Colloquial Hindi & English symptom description understanding.</span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-4 h-4 text-teal-600 shrink-0 mt-0.5" />
                  <span><b>Emergency Red Flags:</b> Life-threatening symptoms immediately route to 112/108 emergency services.</span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-4 h-4 text-teal-600 shrink-0 mt-0.5" />
                  <span><b>Deterministic Tariff Bounds:</b> Minimum, expected median, and ceiling bounds based on CGHS & NPPA benchmarks.</span>
                </li>
              </ul>
            </div>

            <div className="pt-4 border-t border-slate-100">
              <Link
                href="/triage"
                className="inline-flex items-center gap-2 text-sm font-bold text-teal-700 hover:text-teal-900 group"
              >
                <span>Calculate Fair Price Range</span>
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </Link>
            </div>
          </div>

          {/* ACT 2 Card */}
          <div className="bg-white rounded-3xl p-8 sm:p-10 border border-slate-200/90 shadow-sm hover:shadow-md transition-all space-y-8 flex flex-col justify-between">
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <div className="w-14 h-14 rounded-2xl bg-slate-100 border border-slate-300 flex items-center justify-center text-slate-900 shadow-xs">
                  <FileSearch className="w-7 h-7 stroke-[2.2]" />
                </div>
                <span className="text-xs font-bold px-3.5 py-1.5 rounded-full bg-slate-100 text-slate-800 border border-slate-300">
                  ACT 2 • AFTER DISCHARGE
                </span>
              </div>

              <div>
                <h3 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">Medical Bill Audit & Dispute Drafts</h3>
                <p className="text-sm text-slate-600 mt-2 leading-relaxed">
                  Upload itemized hospital invoices in PDF or image format. Our deterministic rules detect multiplication discrepancies, duplicates, and rate cap violations.
                </p>
              </div>

              <ul className="space-y-3.5 text-sm text-slate-700">
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-4 h-4 text-teal-600 shrink-0 mt-0.5" />
                  <span><b>PyMuPDF OCR Extraction:</b> Extracts line items with quantities, rates, and claimed amounts.</span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-4 h-4 text-teal-600 shrink-0 mt-0.5" />
                  <span><b>Deterministic Audit Rules (A–E):</b> Rigorously checks arithmetic, duplicates, and reference rates.</span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-4 h-4 text-teal-600 shrink-0 mt-0.5" />
                  <span><b>Formal PDF & Dispute Letter:</b> Exports a signed audit report and an editable inquiry letter for the billing desk.</span>
                </li>
              </ul>
            </div>

            <div className="pt-4 border-t border-slate-100">
              <Link
                href="/bills/upload"
                className="inline-flex items-center gap-2 text-sm font-bold text-teal-700 hover:text-teal-900 group"
              >
                <span>Upload & Audit Hospital Invoice</span>
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* ========================================================= */}
      {/* INTERACTIVE PROCEDURE TARIFF ESTIMATOR TEASER */}
      {/* ========================================================= */}
      <section className="w-full px-4 sm:px-8 lg:px-12 xl:px-16 2xl:px-20">
        <div className="bg-slate-900 text-white rounded-3xl p-8 sm:p-12 border border-slate-800 shadow-xl space-y-8">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-teal-400 bg-teal-950/80 px-3 py-1 rounded-full border border-teal-800/80">
                Act 1 Live Estimator Teaser
              </span>
              <h3 className="text-2xl sm:text-3xl font-extrabold tracking-tight mt-2 text-white">
                Explore Benchmark Tariffs for Common Surgeries
              </h3>
            </div>
            <Link
              href="/triage"
              className="px-5 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold text-xs inline-flex items-center gap-1.5 transition self-start md:self-auto"
            >
              <span>Custom Symptom Triage</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          {/* Procedure Tabs */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
            {[
              { id: 'TKR', label: 'Knee Replacement', specialty: 'Orthopedics' },
              { id: 'CABG', label: 'Bypass Surgery (CABG)', specialty: 'Cardiology' },
              { id: 'CATARACT', label: 'Cataract Surgery', specialty: 'Ophthalmology' },
              { id: 'APP', label: 'Appendectomy', specialty: 'General Surgery' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setSelectedProcedure(tab.id)}
                className={`p-3.5 rounded-xl text-left border transition-all ${
                  selectedProcedure === tab.id
                    ? 'bg-teal-600/20 border-teal-500 text-white'
                    : 'bg-slate-800/60 border-slate-700/60 text-slate-400 hover:text-white hover:bg-slate-800'
                }`}
              >
                <span className="text-[10px] font-bold block text-teal-400 uppercase tracking-wider">{tab.specialty}</span>
                <span className="text-xs sm:text-sm font-bold block mt-0.5">{tab.label}</span>
              </button>
            ))}
          </div>

          {/* Bounds Display Box */}
          <div className="bg-slate-950 p-6 rounded-2xl border border-slate-800 flex flex-col lg:flex-row lg:items-center justify-between gap-6">
            <div className="space-y-1">
              <span className="text-xs font-mono text-slate-400">{activeProcedure.code} • {activeProcedure.scheme}</span>
              <h4 className="text-lg sm:text-xl font-bold text-white">{activeProcedure.name}</h4>
              <p className="text-xs text-slate-400">Includes OT charges, standard surgical consumables, routine nursing, and surgeon fees.</p>
            </div>

            <div className="grid grid-cols-3 gap-4 text-center shrink-0">
              <div className="bg-slate-900/80 p-3 rounded-xl border border-slate-800">
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Min Bound</span>
                <span className="text-base sm:text-lg font-bold text-slate-200 font-tabular">{activeProcedure.min}</span>
              </div>
              <div className="bg-teal-950/60 p-3 rounded-xl border border-teal-800/60">
                <span className="text-[10px] font-bold text-teal-300 uppercase tracking-wider block">Expected Median</span>
                <span className="text-base sm:text-lg font-extrabold text-teal-300 font-tabular">{activeProcedure.median}</span>
              </div>
              <div className="bg-slate-900/80 p-3 rounded-xl border border-slate-800">
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Ceiling Cap</span>
                <span className="text-base sm:text-lg font-bold text-amber-300 font-tabular">{activeProcedure.max}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ========================================================= */}
      {/* 5 RIGOROUS FINANCIAL AUDIT RULES */}
      {/* ========================================================= */}
      <section className="w-full px-4 sm:px-8 lg:px-12 xl:px-16 2xl:px-20 py-6 space-y-10">
        <div className="text-center max-w-2xl mx-auto space-y-3">
          <span className="text-xs font-bold uppercase tracking-wider text-teal-700 bg-teal-50 px-3.5 py-1 rounded-full border border-teal-200">
            Deterministic Engine Standards
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-950">Five Rigorous Financial Audit Rules</h2>
          <p className="text-sm sm:text-base text-slate-600">
            Every rupee flagged by MEDSURE is tied to verifiable mathematical proof and documented reference benchmarks.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Rule A */}
          <div className="p-6 rounded-2xl bg-white border border-slate-200/90 shadow-xs hover:shadow-md hover:-translate-y-0.5 transition-all space-y-3 flex flex-col justify-between">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="w-10 h-10 rounded-xl bg-red-50 text-red-700 font-bold text-sm flex items-center justify-center border border-red-200">
                  Rule A
                </div>
                <span className="text-[11px] font-semibold text-red-700 bg-red-50 px-2.5 py-0.5 rounded-md">
                  Arithmetic Math
                </span>
              </div>
              <h4 className="font-bold text-slate-900 text-base">Arithmetic Validation</h4>
              <p className="text-xs text-slate-600 leading-relaxed">
                Recalculates every single line item using high-precision Decimal math (<code className="bg-slate-100 px-1 py-0.5 rounded font-mono">Qty × Rate = Total</code>) to uncover manual hospital arithmetic overstatements.
              </p>
            </div>
            <div className="pt-2 text-[11px] text-slate-500 font-mono bg-slate-50 p-2.5 rounded-xl border border-slate-100">
              Discrepancy = Claimed Total - (Qty × Unit Price)
            </div>
          </div>

          {/* Rule B */}
          <div className="p-6 rounded-2xl bg-white border border-slate-200/90 shadow-xs hover:shadow-md hover:-translate-y-0.5 transition-all space-y-3 flex flex-col justify-between">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="w-10 h-10 rounded-xl bg-amber-50 text-amber-800 font-bold text-sm flex items-center justify-center border border-amber-200">
                  Rule B
                </div>
                <span className="text-[11px] font-semibold text-amber-800 bg-amber-50 px-2.5 py-0.5 rounded-md">
                  Duplicate Items
                </span>
              </div>
              <h4 className="font-bold text-slate-900 text-base">Candidate Duplicate Charges</h4>
              <p className="text-xs text-slate-600 leading-relaxed">
                Detects repeated high-value one-time surgical fees, OT bookings, and consumable packs billed multiple times in the same continuous surgical session.
              </p>
            </div>
            <div className="pt-2 text-[11px] text-slate-500 font-mono bg-slate-50 p-2.5 rounded-xl border border-slate-100">
              Flags same-date procedural & OT slot redundancy
            </div>
          </div>

          {/* Rule C */}
          <div className="p-6 rounded-2xl bg-white border border-slate-200/90 shadow-xs hover:shadow-md hover:-translate-y-0.5 transition-all space-y-3 flex flex-col justify-between">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-800 font-bold text-sm flex items-center justify-center border border-blue-200">
                  Rule C
                </div>
                <span className="text-[11px] font-semibold text-blue-800 bg-blue-50 px-2.5 py-0.5 rounded-md">
                  Official Price Caps
                </span>
              </div>
              <h4 className="font-bold text-slate-900 text-base">Reference-Rate Comparison</h4>
              <p className="text-xs text-slate-600 leading-relaxed">
                Compares billed implants and procedural fees against official price caps (e.g. NPPA implant caps, CGHS schedules, and standardized tariffs).
              </p>
            </div>
            <div className="pt-2 text-[11px] text-slate-500 font-mono bg-slate-50 p-2.5 rounded-xl border border-slate-100">
              Flags Claimed Rate &gt; Legal Benchmark Ceiling
            </div>
          </div>

          {/* Rule D */}
          <div className="p-6 rounded-2xl bg-white border border-slate-200/90 shadow-xs hover:shadow-md hover:-translate-y-0.5 transition-all space-y-3 flex flex-col justify-between">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="w-10 h-10 rounded-xl bg-purple-50 text-purple-800 font-bold text-sm flex items-center justify-center border border-purple-200">
                  Rule D
                </div>
                <span className="text-[11px] font-semibold text-purple-800 bg-purple-50 px-2.5 py-0.5 rounded-md">
                  Unbundling
                </span>
              </div>
              <h4 className="font-bold text-slate-900 text-base">Unbundling & Coding Mismatch</h4>
              <p className="text-xs text-slate-600 leading-relaxed">
                Identifies routine consumables, gloves, or nursing charges billed separately when an all-inclusive surgery package was already claimed.
              </p>
            </div>
            <div className="pt-2 text-[11px] text-slate-500 font-mono bg-slate-50 p-2.5 rounded-xl border border-slate-100">
              Flags double-dipping on package component items
            </div>
          </div>

          {/* Rule E */}
          <div className="p-6 rounded-2xl bg-white border border-slate-200/90 shadow-xs hover:shadow-md hover:-translate-y-0.5 transition-all space-y-3 flex flex-col justify-between">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="w-10 h-10 rounded-xl bg-rose-50 text-rose-800 font-bold text-sm flex items-center justify-center border border-rose-200">
                  Rule E
                </div>
                <span className="text-[11px] font-semibold text-rose-800 bg-rose-50 px-2.5 py-0.5 rounded-md">
                  Missing Details
                </span>
              </div>
              <h4 className="font-bold text-slate-900 text-base">Incompleteness & Missing Info</h4>
              <p className="text-xs text-slate-600 leading-relaxed">
                Flags line items with missing quantities, zero unit rates, or unreadable OCR tokens requiring billing office clarification.
              </p>
            </div>
            <div className="pt-2 text-[11px] text-slate-500 font-mono bg-slate-50 p-2.5 rounded-xl border border-slate-100">
              Requires hospital itemized tariff disclosure
            </div>
          </div>

          {/* Output Card */}
          <div className="p-6 rounded-2xl bg-gradient-to-br from-teal-50 to-emerald-50/50 border border-teal-200/80 shadow-xs hover:shadow-md hover:-translate-y-0.5 transition-all space-y-3 flex flex-col justify-between">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="w-10 h-10 rounded-xl bg-teal-600 text-white font-bold text-sm flex items-center justify-center shadow-xs">
                  Output
                </div>
                <span className="text-[11px] font-semibold text-teal-800 bg-teal-100/80 px-2.5 py-0.5 rounded-md">
                  ReportLab PDF + Dispute
                </span>
              </div>
              <h4 className="font-bold text-teal-950 text-base">Formal Dispute Draft</h4>
              <p className="text-xs text-teal-800 leading-relaxed">
                Generates a respectful, legally sound letter and PDF audit report with itemized questions for the hospital billing department.
              </p>
            </div>
            <Link 
              href="/demo" 
              className="text-xs font-bold text-teal-700 hover:text-teal-950 flex items-center gap-1.5 pt-2"
            >
              <span>View sample dispute draft</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </section>

      {/* ========================================================= */}
      {/* COMPARISON MATRIX: Chatbot Wrapper vs MEDSURE */}
      {/* ========================================================= */}
      <section className="w-full px-4 sm:px-8 lg:px-12 xl:px-16 2xl:px-20">
        <div className="bg-white rounded-3xl p-8 sm:p-12 border border-slate-200/90 shadow-sm space-y-8">
          <div className="text-center max-w-2xl mx-auto space-y-2">
            <span className="text-xs font-bold uppercase tracking-wider text-teal-700 bg-teal-50 px-3 py-1 rounded-full border border-teal-200">
              Architectural Superiority
            </span>
            <h3 className="text-2xl sm:text-3xl font-extrabold text-slate-950">
              Why Generic LLMs Fail at Medical Bills
            </h3>
            <p className="text-sm text-slate-600">
              Prompting an LLM with a 10-page hospital bill leads to fabricated rates and math errors.
            </p>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs sm:text-sm">
              <thead>
                <tr className="border-b border-slate-200">
                  <th className="py-3 px-4 font-bold text-slate-500 uppercase tracking-wider text-[11px]">Feature / Dimension</th>
                  <th className="py-3 px-4 font-bold text-red-600 uppercase tracking-wider text-[11px] bg-red-50/50 rounded-tl-xl">Generic LLM Chatbot</th>
                  <th className="py-3 px-4 font-bold text-teal-700 uppercase tracking-wider text-[11px] bg-teal-50/80 rounded-tr-xl">MEDSURE Platform</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700">
                <tr>
                  <td className="py-3.5 px-4 font-bold text-slate-900">Arithmetic Precision</td>
                  <td className="py-3.5 px-4 text-red-700 bg-red-50/30">Prone to floating-point and rounding hallucinations</td>
                  <td className="py-3.5 px-4 text-teal-900 font-bold bg-teal-50/40">100% exact Python Decimal math to the paisa</td>
                </tr>
                <tr>
                  <td className="py-3.5 px-4 font-bold text-slate-900">Reference Benchmark Caps</td>
                  <td className="py-3.5 px-4 text-red-700 bg-red-50/30">Invents plausible-sounding but outdated tariff bounds</td>
                  <td className="py-3.5 px-4 text-teal-900 font-bold bg-teal-50/40">Mapped to verified statutory CGHS & NPPA schedules</td>
                </tr>
                <tr>
                  <td className="py-3.5 px-4 font-bold text-slate-900">Clinical Safety Filtering</td>
                  <td className="py-3.5 px-4 text-red-700 bg-red-50/30">May offer price estimates for life-threatening acute emergencies</td>
                  <td className="py-3.5 px-4 text-teal-900 font-bold bg-teal-50/40">Strict red-flag shield immediately routes acute symptoms to 112/108</td>
                </tr>
                <tr>
                  <td className="py-3.5 px-4 font-bold text-slate-900">Audit Documentation</td>
                  <td className="py-3.5 px-4 text-red-700 bg-red-50/30">Unstructured chat text; rejected by hospital billing desks</td>
                  <td className="py-3.5 px-4 text-teal-900 font-bold bg-teal-50/40">Signed ReportLab PDF + itemized hospital dispute letter</td>
                </tr>
                <tr>
                  <td className="py-3.5 px-4 font-bold text-slate-900">Human-In-The-Loop Verification</td>
                  <td className="py-3.5 px-4 text-red-700 bg-red-50/30">Audits blind OCR output without letting patient correct errors</td>
                  <td className="py-3.5 px-4 text-teal-900 font-bold bg-teal-50/40">Interactive correction screen before running financial rules</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* ========================================================= */}
      {/* FINAL CALL TO ACTION BANNER */}
      {/* ========================================================= */}
      <section className="w-full px-4 sm:px-8 lg:px-12 xl:px-16 2xl:px-20">
        <div className="rounded-3xl bg-gradient-to-r from-teal-900 via-teal-800 to-emerald-900 p-8 sm:p-14 text-white shadow-2xl relative overflow-hidden">
          <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-teal-500/10 rounded-full blur-3xl pointer-events-none" />

          <div className="max-w-3xl space-y-5 relative z-10">
            <span className="text-xs font-bold uppercase tracking-wider text-teal-300 bg-teal-950/80 px-3.5 py-1 rounded-full border border-teal-700">
              Free & Confidential Patient Protection
            </span>
            <h2 className="text-3xl sm:text-5xl font-extrabold tracking-tight">
              Ready to verify your hospital charges?
            </h2>
            <p className="text-sm sm:text-base text-teal-100 leading-relaxed max-w-2xl">
              Whether you are preparing for a planned elective surgery or holding an unexpected post-discharge hospital bill, MEDSURE provides immediate mathematical clarity and dispute leverage.
            </p>
            <div className="flex flex-wrap items-center gap-4 pt-3">
              <Link
                href="/bills/upload"
                className="px-7 py-4 rounded-xl bg-white text-teal-950 font-bold text-sm shadow-lg hover:bg-teal-50 hover:shadow-xl hover:-translate-y-0.5 transition-all"
              >
                Audit My Medical Bill
              </Link>
              <Link
                href="/triage"
                className="px-7 py-4 rounded-xl bg-teal-950/80 hover:bg-teal-950 border border-teal-500/50 text-white font-bold text-sm hover:-translate-y-0.5 transition-all"
              >
                Estimate Fair Treatment Costs
              </Link>
              <Link
                href="/demo"
                className="px-5 py-4 rounded-xl text-teal-200 hover:text-white font-bold text-sm inline-flex items-center gap-1.5 transition"
              >
                <span>Watch 2-Minute Demo</span>
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
