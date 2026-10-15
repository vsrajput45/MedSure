'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { 
  Download, 
  Copy, 
  Check, 
  Printer, 
  ArrowLeft, 
  ShieldCheck, 
  AlertTriangle,
  RefreshCw
} from 'lucide-react';
import { api } from '@/lib/api';

export default function DisputeLetterPage() {
  const params = useParams();
  const auditId = params.id as string;

  const [letterContent, setLetterContent] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchLetter = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await api.getDisputeLetter(auditId);
        setLetterContent(res.dispute_letter);
      } catch (err: any) {
        setError(err.message || 'Failed to generate dispute letter draft.');
      } finally {
        setLoading(false);
      }
    };
    if (auditId) {
      fetchLetter();
    }
  }, [auditId]);

  const handleCopy = () => {
    navigator.clipboard.writeText(letterContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handlePrint = () => {
    window.print();
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-24 text-center space-y-4">
        <RefreshCw className="w-8 h-8 text-teal-600 animate-spin mx-auto" />
        <p className="text-sm text-slate-600 font-semibold">Generating formal inquiry draft from audit evidence...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-20 text-center space-y-4">
        <AlertTriangle className="w-12 h-12 text-red-500 mx-auto" />
        <h2 className="text-xl font-bold text-slate-900">Error Generating Letter</h2>
        <p className="text-sm text-slate-500">{error}</p>
        <Link href={`/audits/${auditId}`} className="inline-block px-4 py-2 rounded-xl bg-teal-600 text-white text-xs font-bold">
          Return to Audit Findings
        </Link>
      </div>
    );
  }

  return (
    <div className="w-full px-4 sm:px-8 lg:px-12 xl:px-16 2xl:px-20 py-10 space-y-8">
      {/* Top Navigation */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-200">
        <Link
          href={`/audits/${auditId}`}
          className="inline-flex items-center gap-1.5 text-xs font-bold text-slate-600 hover:text-slate-900 transition"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Audit Findings</span>
        </Link>

        <div className="flex items-center gap-3">
          <a
            href={api.getReportPdfUrl(auditId)}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl bg-white border border-slate-200 hover:bg-slate-50 text-slate-800 font-bold text-xs transition shadow-2xs hover:border-slate-300"
          >
            <Download className="w-4 h-4 text-teal-600" />
            <span>Download PDF Report</span>
          </a>

          <button
            onClick={handleCopy}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-teal-600 to-emerald-600 hover:from-teal-700 hover:to-emerald-700 text-white font-bold text-xs transition shadow-xs"
          >
            {copied ? <Check className="w-4 h-4 text-white" /> : <Copy className="w-4 h-4" />}
            <span>{copied ? 'Copied to Clipboard!' : 'Copy Letter Draft'}</span>
          </button>
        </div>
      </div>

      {/* Intro Banner */}
      <div className="space-y-1.5">
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-950 tracking-tight">
          Hospital Billing Inquiry & Dispute Letter
        </h1>
        <p className="text-xs sm:text-sm text-slate-600">
          This editable letter draft presents verified mathematical proof and questions for the hospital billing department in a neutral, respectful manner.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Editable Letter Area */}
        <div className="lg:col-span-2 space-y-4">
          <div className="bg-white rounded-3xl border border-slate-200/90 shadow-xs p-6 sm:p-7 space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
                Editable Letter Draft (Markdown / Text)
              </span>
              <button
                onClick={handlePrint}
                className="text-xs text-slate-600 hover:text-slate-950 flex items-center gap-1 font-semibold transition"
              >
                <Printer className="w-3.5 h-3.5" />
                <span>Print Draft</span>
              </button>
            </div>

            <textarea
              rows={22}
              value={letterContent}
              onChange={(e) => setLetterContent(e.target.value)}
              className="w-full p-4 rounded-2xl border border-slate-200 text-xs sm:text-sm font-mono text-slate-800 bg-slate-50/60 focus:bg-white focus:border-teal-500 focus:ring-1 focus:ring-teal-500 leading-relaxed resize-none shadow-inner"
            />
          </div>
        </div>

        {/* Right Column: Guidance & Patient Checklist */}
        <div className="space-y-6">
          <div className="bg-white rounded-3xl border border-slate-200/90 shadow-xs p-6 space-y-4">
            <h3 className="text-sm font-extrabold text-slate-950">Patient Action Checklist</h3>
            
            <ol className="space-y-3.5 text-xs text-slate-600">
              <li className="flex items-start gap-2.5">
                <span className="w-5 h-5 rounded-full bg-teal-100 text-teal-800 font-bold flex items-center justify-center shrink-0 text-[11px]">1</span>
                <span><b>Customize Placeholders:</b> Fill in your patient name, contact number, and UHID at the bottom of the letter.</span>
              </li>
              <li className="flex items-start gap-2.5">
                <span className="w-5 h-5 rounded-full bg-teal-100 text-teal-800 font-bold flex items-center justify-center shrink-0 text-[11px]">2</span>
                <span><b>Attach PDF Audit Report:</b> Download and attach the official MEDSURE PDF audit report as supporting technical evidence.</span>
              </li>
              <li className="flex items-start gap-2.5">
                <span className="w-5 h-5 rounded-full bg-teal-100 text-teal-800 font-bold flex items-center justify-center shrink-0 text-[11px]">3</span>
                <span><b>Submit to Billing Desk:</b> Send via email to the hospital accounts desk or hand a physical copy to the patient advocate.</span>
              </li>
              <li className="flex items-start gap-2.5">
                <span className="w-5 h-5 rounded-full bg-teal-100 text-teal-800 font-bold flex items-center justify-center shrink-0 text-[11px]">4</span>
                <span><b>Request Revised Invoice:</b> Request an updated invoice before final settlement or insurance reimbursement filing.</span>
              </li>
            </ol>
          </div>

          <div className="p-5 rounded-3xl bg-teal-50/80 border border-teal-200 space-y-2">
            <div className="flex items-center gap-2 text-xs font-bold text-teal-900 uppercase tracking-wider">
              <ShieldCheck className="w-4 h-4 text-teal-700" />
              <span>Tone & Professionalism Standard</span>
            </div>
            <p className="text-xs text-teal-800 leading-relaxed font-normal">
              MEDSURE drafts maintain an objective, respectful, and cooperative tone. We never state unproven accusations as facts, keeping negotiations collaborative and constructive.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
