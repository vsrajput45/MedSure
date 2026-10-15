'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { 
  Sparkles, 
  ArrowRight, 
  Scale, 
  Calculator, 
  Copy, 
  Layers,
  RefreshCw
} from 'lucide-react';
import { api } from '@/lib/api';

export default function DemoPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  const steps = [
    {
      num: 1,
      title: 'ACT 1: Before-Admission Clinical Guidance',
      desc: 'Test Hindi and English symptom triage with emergency red-flag safeguards.',
      actionText: 'Explore Fair Price Estimator',
      actionUrl: '/triage',
      badge: 'Bilingual NLP + Red Flags'
    },
    {
      num: 2,
      title: 'ACT 1: Cost Bounds & Tariff Limitations',
      desc: 'Observe deterministic minimum, median, and ceiling bounds calculated from reference rates.',
      actionText: 'View Tariff Benchmarks',
      actionUrl: '/reference-rates',
      badge: 'Zero Rate Hallucination'
    },
    {
      num: 3,
      title: 'ACT 2: Document Processing & Line-Item Review',
      desc: 'Inspect the synthetic Knee Replacement bill extracted by PyMuPDF OCR.',
      actionText: 'Open Synthetic Bill Review',
      actionHandler: async () => {
        setLoading(true);
        try {
          const bills = await api.getBills();
          const demoBill = bills.find((b) => b.is_demo_sample) || bills[0];
          if (demoBill) {
            router.push(`/bills/${demoBill.id}/review`);
          }
        } finally {
          setLoading(false);
        }
      },
      badge: 'PyMuPDF Pipeline'
    },
    {
      num: 4,
      title: 'ACT 2: Deterministic Financial Audit Execution',
      desc: 'Run Rules A through E to uncover multiplication errors, duplicate OT fees, and rate cap breaches.',
      actionText: 'Run Deterministic Audit',
      actionHandler: async () => {
        setLoading(true);
        try {
          const bills = await api.getBills();
          const demoBill = bills.find((b) => b.is_demo_sample) || bills[0];
          if (demoBill) {
            const audit = await api.runAudit(demoBill.id);
            router.push(`/audits/${audit.id}`);
          }
        } finally {
          setLoading(false);
        }
      },
      badge: 'Rules A–E Tested'
    },
    {
      num: 5,
      title: 'ACT 2: Formal PDF Report & Editable Dispute Letter',
      desc: 'Download the ReportLab generated PDF audit report and copy the patient inquiry letter.',
      actionText: 'Jump to Dashboard Metrics',
      actionUrl: '/dashboard',
      badge: 'ReportLab + Markdown'
    }
  ];

  return (
    <div className="w-full px-4 sm:px-8 lg:px-12 xl:px-16 2xl:px-20 py-12 space-y-10">
      {/* Hero */}
      <div className="text-center space-y-3">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-amber-50 border border-amber-300 text-amber-950 text-xs font-bold uppercase tracking-wider">
          <Sparkles className="w-4 h-4 text-amber-600" />
          <span>Interactive Feature Demonstration Guide</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-950 tracking-tight">
          MEDSURE 2-Minute Interactive Walkthrough
        </h1>
        <p className="text-sm sm:text-base text-slate-600 max-w-2xl mx-auto leading-relaxed">
          This guided pathway demonstrates both core patient acts in under two minutes using live backend execution and deterministic verification.
        </p>
      </div>

      {/* Synthetic Scenario Explainer Card */}
      <div className="p-7 sm:p-8 rounded-3xl bg-slate-950 text-white shadow-xl space-y-5 border border-slate-800">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-4">
          <div className="flex items-center gap-2.5">
            <span className="w-3 h-3 rounded-full bg-amber-400 animate-pulse"></span>
            <h2 className="font-extrabold text-base text-amber-300">
              Pre-Configured Scenario: Total Knee Replacement
            </h2>
          </div>
          <span className="text-xs text-slate-400 font-medium">Apex Care Super Specialty Hospital (Invoice #INV-2026-KNEE-8842)</span>
        </div>

        <p className="text-xs text-slate-300 leading-relaxed font-normal">
          The synthetic demonstration invoice contains deliberate, verifiable billing anomalies designed to test each deterministic rule:
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
          <div className="p-3.5 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-1">
            <div className="flex items-center gap-1.5 font-bold text-red-400">
              <Calculator className="w-3.5 h-3.5" />
              <span>Rule A: Math Error</span>
            </div>
            <p className="text-[11px] text-slate-300 font-medium leading-relaxed">
              Surgeon Fee billed as <b>₹85,000</b> instead of 1 × <b>₹70,000</b> (₹15,000 overstatement).
            </p>
          </div>

          <div className="p-3.5 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-1">
            <div className="flex items-center gap-1.5 font-bold text-amber-400">
              <Copy className="w-3.5 h-3.5" />
              <span>Rule B: Duplicate</span>
            </div>
            <p className="text-[11px] text-slate-300 font-medium leading-relaxed">
              Operation Theatre charges of <b>₹35,000</b> billed twice in the same surgical session.
            </p>
          </div>

          <div className="p-3.5 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-1">
            <div className="flex items-center gap-1.5 font-bold text-blue-400">
              <Scale className="w-3.5 h-3.5" />
              <span>Rule C: Price Cap</span>
            </div>
            <p className="text-[11px] text-slate-300 font-medium leading-relaxed">
              Knee Implant billed at <b>₹115,000</b> exceeding NPPA benchmark ceiling of <b>₹85,000</b>.
            </p>
          </div>

          <div className="p-3.5 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-1">
            <div className="flex items-center gap-1.5 font-bold text-purple-400">
              <Layers className="w-3.5 h-3.5" />
              <span>Rule D: Unbundling</span>
            </div>
            <p className="text-[11px] text-slate-300 font-medium leading-relaxed">
              Surgical Drapes Kit (<b>₹12,500</b>) billed separately on top of OT surgical package.
            </p>
          </div>
        </div>
      </div>

      {/* Guided Walkthrough Steps */}
      <div className="space-y-4">
        {steps.map((step) => (
          <div
            key={step.num}
            className="p-6 sm:p-7 rounded-3xl bg-white border border-slate-200/90 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-6 hover:border-teal-300 hover:shadow-md transition-all"
          >
            <div className="flex items-start gap-4">
              <div className="w-11 h-11 rounded-2xl bg-teal-50 text-teal-800 font-extrabold flex items-center justify-center shrink-0 text-base border border-teal-200 shadow-2xs">
                {step.num}
              </div>
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <h3 className="font-extrabold text-slate-950 text-base">{step.title}</h3>
                  <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 border border-slate-200">
                    {step.badge}
                  </span>
                </div>
                <p className="text-xs text-slate-600 leading-relaxed max-w-xl">
                  {step.desc}
                </p>
              </div>
            </div>

            <div className="shrink-0">
              {step.actionUrl ? (
                <Link
                  href={step.actionUrl}
                  className="inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-gradient-to-r from-teal-600 to-emerald-600 hover:from-teal-700 hover:to-emerald-700 text-white font-bold text-xs shadow-xs hover:shadow transition"
                >
                  <span>{step.actionText}</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              ) : (
                <button
                  type="button"
                  onClick={step.actionHandler}
                  disabled={loading}
                  className="inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-amber-600 hover:bg-amber-700 text-white font-bold text-xs shadow-xs hover:shadow transition disabled:opacity-50"
                >
                  {loading ? (
                    <>
                      <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                      <span>Accessing backend...</span>
                    </>
                  ) : (
                    <>
                      <span>{step.actionText}</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </>
                  )}
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
