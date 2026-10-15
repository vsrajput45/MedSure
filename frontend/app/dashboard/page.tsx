'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { 
  Stethoscope, 
  FileSearch, 
  AlertTriangle, 
  ArrowRight, 
  Clock, 
  FileText, 
  ShieldCheck, 
  RefreshCw,
  Sparkles,
  Scale,
  Activity
} from 'lucide-react';
import { api, DashboardSummary } from '@/lib/api';

export default function DashboardPage() {
  const [data, setData] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchSummary = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.getDashboardSummary();
      setData(res);
    } catch (err: any) {
      setError(err.message || 'Failed to connect to MEDSURE backend.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSummary();
  }, []);

  return (
    <div className="w-full px-4 sm:px-8 lg:px-12 xl:px-16 2xl:px-20 py-10 space-y-8">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-200/90">
        <div>
          <div className="flex items-center gap-2.5">
            <h1 className="text-3xl font-extrabold text-slate-950 tracking-tight">Patient Audit Dashboard</h1>
            <span className="inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-0.5 rounded-full bg-teal-50 text-teal-800 border border-teal-200">
              <span className="w-1.5 h-1.5 rounded-full bg-teal-500 animate-pulse"></span>
              Live Backend
            </span>
          </div>
          <p className="text-sm text-slate-500 mt-1">
            Real-time healthcare cost estimates, document OCR status, and deterministic bill audit discrepancies.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={fetchSummary}
            disabled={loading}
            className="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 text-xs font-semibold shadow-xs hover:border-slate-300 transition"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin text-teal-600' : ''}`} />
            <span>Refresh</span>
          </button>
          
          <Link
            href="/demo"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-600 text-slate-950 text-xs font-bold shadow-xs hover:shadow transition"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Run 2-Min Demo</span>
          </Link>
        </div>
      </div>

      {/* Error state */}
      {error && (
        <div className="p-4 rounded-2xl bg-red-50 border border-red-200 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <AlertTriangle className="w-5 h-5 text-red-600 shrink-0" />
            <span className="text-sm text-red-800 font-medium">{error}</span>
          </div>
          <button
            onClick={fetchSummary}
            className="text-xs font-bold px-3 py-1.5 rounded-lg bg-red-600 text-white hover:bg-red-700 transition"
          >
            Retry
          </button>
        </div>
      )}

      {/* Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {/* Metric 1 */}
        <div className="bg-white p-6 rounded-3xl border border-slate-200/90 shadow-xs hover:shadow-md transition space-y-2">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-xs font-bold uppercase tracking-wider">Estimates Created</span>
            <div className="w-8 h-8 rounded-xl bg-teal-50 text-teal-700 flex items-center justify-center">
              <Stethoscope className="w-4 h-4" />
            </div>
          </div>
          <div className="text-3xl font-extrabold text-slate-950 font-tabular">
            {loading ? '—' : data?.total_estimates_created}
          </div>
          <p className="text-xs text-slate-500 font-medium">Before-admission inquiries</p>
        </div>

        {/* Metric 2 */}
        <div className="bg-white p-6 rounded-3xl border border-slate-200/90 shadow-xs hover:shadow-md transition space-y-2">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-xs font-bold uppercase tracking-wider">Bills Processed</span>
            <div className="w-8 h-8 rounded-xl bg-blue-50 text-blue-700 flex items-center justify-center">
              <FileText className="w-4 h-4" />
            </div>
          </div>
          <div className="text-3xl font-extrabold text-slate-950 font-tabular">
            {loading ? '—' : data?.total_bills_uploaded}
          </div>
          <p className="text-xs text-slate-500 font-medium">PyMuPDF extracted invoices</p>
        </div>

        {/* Metric 3 */}
        <div className="bg-white p-6 rounded-3xl border border-slate-200/90 shadow-xs hover:shadow-md transition space-y-2">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-xs font-bold uppercase tracking-wider">Audits Completed</span>
            <div className="w-8 h-8 rounded-xl bg-indigo-50 text-indigo-700 flex items-center justify-center">
              <ShieldCheck className="w-4 h-4" />
            </div>
          </div>
          <div className="text-3xl font-extrabold text-slate-950 font-tabular">
            {loading ? '—' : data?.total_audits_completed}
          </div>
          <p className="text-xs text-slate-500 font-medium">Rules A–E verification runs</p>
        </div>

        {/* Metric 4 */}
        <div className="bg-gradient-to-br from-white to-red-50/70 p-6 rounded-3xl border border-red-200/90 shadow-xs hover:shadow-md transition space-y-2">
          <div className="flex items-center justify-between text-red-700">
            <span className="text-xs font-bold uppercase tracking-wider">Potential Overcharges</span>
            <div className="w-8 h-8 rounded-xl bg-red-100 text-red-700 flex items-center justify-center">
              <AlertTriangle className="w-4 h-4" />
            </div>
          </div>
          <div className="text-3xl font-extrabold text-red-600 font-tabular">
            {loading ? '—' : `₹${(data?.total_potential_savings_identified || 0).toLocaleString('en-IN')}`}
          </div>
          <p className="text-xs text-red-800 font-semibold">
            {data?.total_discrepancies_identified || 0} line-item discrepancies flagged
          </p>
        </div>
      </div>

      {/* Two Action Columns */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Recent Activities */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white rounded-3xl border border-slate-200/90 shadow-xs p-6 sm:p-7 space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div className="flex items-center gap-2">
                <Activity className="w-4 h-4 text-teal-600" />
                <h3 className="font-bold text-slate-900 text-base">Recent Verified Activities</h3>
              </div>
              <span className="text-xs text-slate-500 font-medium">Live Database Stream</span>
            </div>

            {loading ? (
              <div className="py-14 text-center space-y-2">
                <RefreshCw className="w-6 h-6 text-teal-600 animate-spin mx-auto" />
                <p className="text-xs text-slate-500 font-medium">Loading audit feed...</p>
              </div>
            ) : data?.recent_activities && data.recent_activities.length > 0 ? (
              <div className="divide-y divide-slate-100">
                {data.recent_activities.map((act) => (
                  <div key={act.id} className="py-4 flex items-start justify-between gap-4 hover:bg-slate-50/70 px-2 rounded-xl transition">
                    <div className="flex items-start gap-3.5">
                      <div className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 mt-0.5 shadow-xs ${
                        act.type === 'AUDIT_RUN' ? 'bg-red-50 text-red-600 border border-red-200/80' : 'bg-teal-50 text-teal-600 border border-teal-200/80'
                      }`}>
                        {act.type === 'AUDIT_RUN' ? <ShieldCheck className="w-5 h-5" /> : <Stethoscope className="w-5 h-5" />}
                      </div>
                      <div>
                        <h4 className="text-sm font-bold text-slate-900">{act.title}</h4>
                        <p className="text-xs text-slate-600 mt-0.5 leading-relaxed">{act.description}</p>
                        <span className="text-[11px] text-slate-500 flex items-center gap-1.5 mt-1 font-medium">
                          <Clock className="w-3 h-3" />
                          {new Date(act.timestamp).toLocaleString('en-IN')}
                        </span>
                      </div>
                    </div>

                    <div className="text-right shrink-0">
                      {act.discrepancy_amount ? (
                        <div className="text-sm font-extrabold text-red-600 font-tabular">
                          -₹{act.discrepancy_amount.toLocaleString('en-IN')}
                        </div>
                      ) : act.amount ? (
                        <div className="text-sm font-extrabold text-slate-900 font-tabular">
                          ₹{act.amount.toLocaleString('en-IN')}
                        </div>
                      ) : null}
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full inline-block mt-1 ${
                        act.status === 'HIGH_DISCREPANCY'
                          ? 'bg-red-100 text-red-800'
                          : act.status === 'EMERGENCY'
                          ? 'bg-amber-100 text-amber-900'
                          : 'bg-slate-100 text-slate-700'
                      }`}>
                        {act.status.replace('_', ' ')}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="py-14 text-center text-sm text-slate-500">
                No recent activities recorded yet. Start by generating an estimate or auditing a bill!
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Quick Workflows */}
        <div className="space-y-6">
          <div className="bg-white rounded-3xl border border-slate-200/90 shadow-xs p-6 space-y-4">
            <h3 className="font-bold text-slate-900 text-base">Quick Workflows</h3>
            
            <div className="space-y-3">
              <Link
                href="/triage"
                className="block p-4 rounded-2xl border border-teal-200/80 bg-teal-50/50 hover:bg-teal-50 transition-all group"
              >
                <div className="flex items-center justify-between text-teal-950 font-bold text-sm">
                  <span className="flex items-center gap-2">
                    <Stethoscope className="w-4 h-4 text-teal-600" />
                    Estimate Fair Treatment Cost
                  </span>
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </div>
                <p className="text-xs text-teal-800 mt-1 font-medium leading-relaxed">
                  Describe symptoms in English or Hindi to obtain standardized hospital rate bounds.
                </p>
              </Link>

              <Link
                href="/bills/upload"
                className="block p-4 rounded-2xl border border-slate-200 bg-white hover:bg-slate-50 transition-all group"
              >
                <div className="flex items-center justify-between text-slate-900 font-bold text-sm">
                  <span className="flex items-center gap-2">
                    <FileSearch className="w-4 h-4 text-slate-700" />
                    Audit Medical Bill
                  </span>
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </div>
                <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                  Upload an itemized hospital bill (PDF or image) to detect arithmetic and duplicate errors.
                </p>
              </Link>

              <Link
                href="/reference-rates"
                className="block p-4 rounded-2xl border border-slate-200 bg-white hover:bg-slate-50 transition-all group"
              >
                <div className="flex items-center justify-between text-slate-900 font-bold text-sm">
                  <span className="flex items-center gap-2">
                    <Scale className="w-4 h-4 text-slate-700" />
                    Tariff Price Benchmarks
                  </span>
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </div>
                <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                  Browse CGHS schedules, NPPA caps, and NABH reference rates.
                </p>
              </Link>
            </div>
          </div>

          {/* Integrity Assurance Card */}
          <div className="p-6 rounded-3xl bg-slate-950 text-white space-y-3 shadow-md border border-slate-800">
            <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-teal-400">
              <ShieldCheck className="w-4 h-4" />
              <span>Audit Integrity Policy</span>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              MEDSURE never fabricates benchmark sources or patient savings. All calculations adhere to Decimal precision and official government reference tariffs.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
