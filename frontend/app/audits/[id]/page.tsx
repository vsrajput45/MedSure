'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { 
  ShieldAlert, 
  AlertTriangle, 
  CheckCircle2, 
  Download, 
  FileEdit, 
  Info, 
  RefreshCw, 
  Scale, 
  FileText, 
  Calculator, 
  Copy, 
  Layers, 
  ChevronRight,
  Sparkles,
  ArrowRight
} from 'lucide-react';
import { api, AuditRun, AuditFinding } from '@/lib/api';

export default function AuditResultsPage() {
  const params = useParams();
  const auditId = params.id as string;

  const [audit, setAudit] = useState<AuditRun | null>(null);
  const [findings, setFindings] = useState<AuditFinding[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filterRule, setFilterRule] = useState<string>('ALL');

  useEffect(() => {
    const fetchAudit = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await api.getAudit(auditId);
        setAudit(res);
        const findRes = await api.getAuditFindings(auditId);
        setFindings(findRes);
      } catch (err: any) {
        setError(err.message || 'Failed to retrieve audit findings.');
      } finally {
        setLoading(false);
      }
    };
    if (auditId) {
      fetchAudit();
    }
  }, [auditId]);

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-24 text-center space-y-4">
        <RefreshCw className="w-8 h-8 text-teal-600 animate-spin mx-auto" />
        <p className="text-sm text-slate-600 font-semibold">Recalculating deterministic audit findings with Decimal math...</p>
      </div>
    );
  }

  if (error || !audit) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-20 text-center space-y-4">
        <AlertTriangle className="w-12 h-12 text-red-500 mx-auto" />
        <h2 className="text-xl font-bold text-slate-900">Audit Not Found</h2>
        <p className="text-sm text-slate-500">{error || 'Unable to load audit report.'}</p>
        <Link href="/dashboard" className="inline-block px-4 py-2 rounded-xl bg-teal-600 text-white text-xs font-bold">
          Return to Dashboard
        </Link>
      </div>
    );
  }

  const filteredFindings = filterRule === 'ALL' 
    ? findings 
    : findings.filter(f => f.rule_type === filterRule);

  const getRuleIcon = (rule: string) => {
    switch(rule) {
      case 'RULE_A_ARITHMETIC': return <Calculator className="w-4 h-4 text-red-600" />;
      case 'RULE_B_DUPLICATE': return <Copy className="w-4 h-4 text-amber-600" />;
      case 'RULE_C_REFERENCE_RATE': return <Scale className="w-4 h-4 text-blue-600" />;
      case 'RULE_D_CODING_MISMATCH': return <Layers className="w-4 h-4 text-purple-600" />;
      case 'RULE_E_MISSING_INFO': return <FileText className="w-4 h-4 text-emerald-600" />;
      default: return <Info className="w-4 h-4 text-slate-600" />;
    }
  };

  return (
    <div className="w-full px-4 sm:px-8 lg:px-12 xl:px-16 2xl:px-20 py-10 space-y-8">
      {/* Header Banner */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 pb-6 border-b border-slate-200">
        <div>
          <div className="flex items-center gap-2.5">
            <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-800 border border-slate-300 font-mono">
              Audit ID: {audit.id.slice(0, 8)}
            </span>
            <span className={`text-xs font-bold px-2.5 py-0.5 rounded-full ${
              audit.overall_status === 'HIGH_DISCREPANCY'
                ? 'bg-red-100 text-red-800 border border-red-200'
                : 'bg-amber-100 text-amber-900 border border-amber-200'
            }`}>
              {audit.overall_status.replace('_', ' ')}
            </span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-950 tracking-tight mt-1.5">
            Deterministic Bill Audit Results
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-0.5">
            Verified {audit.total_line_items_audited} itemized hospital charges using high-precision Decimal rules.
          </p>
        </div>

        {/* Action Buttons: Report & Dispute Letter */}
        <div className="flex flex-wrap items-center gap-3">
          <a
            href={api.getReportPdfUrl(audit.id)}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-white border border-slate-200 hover:bg-slate-50 text-slate-800 font-bold text-xs shadow-xs hover:border-slate-300 transition"
          >
            <Download className="w-4 h-4 text-teal-600" />
            <span>Download Official PDF Report</span>
          </a>

          <Link
            href={`/audits/${audit.id}/dispute-letter`}
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-teal-600 to-emerald-600 hover:from-teal-700 hover:to-emerald-700 text-white font-bold text-xs shadow-md shadow-teal-600/25 transition"
          >
            <FileEdit className="w-4 h-4" />
            <span>Generate Hospital Dispute Letter</span>
          </Link>
        </div>
      </div>

      {/* Summary KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 rounded-2xl bg-white border border-slate-200/90 shadow-2xs space-y-1">
          <span className="text-xs text-slate-500 font-bold uppercase tracking-wider">Total Amount Claimed</span>
          <div className="text-2xl font-extrabold text-slate-950 font-tabular">
            ₹{audit.total_claimed_amount.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
          </div>
          <p className="text-[11px] text-slate-500">Total hospital invoice sum</p>
        </div>

        <div className="p-5 rounded-2xl bg-white border border-slate-200/90 shadow-2xs space-y-1">
          <span className="text-xs text-slate-500 font-bold uppercase tracking-wider">Verified Legitimate Base</span>
          <div className="text-2xl font-extrabold text-emerald-600 font-tabular">
            ₹{audit.total_verified_amount.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
          </div>
          <p className="text-[11px] text-slate-500">Mathematically verified items</p>
        </div>

        <div className="p-5 rounded-2xl bg-gradient-to-br from-white to-red-50/80 border border-red-200 shadow-2xs space-y-1">
          <span className="text-xs text-red-700 font-bold uppercase tracking-wider">Potential Overstatement</span>
          <div className="text-2xl font-extrabold text-red-600 font-tabular">
            ₹{audit.total_potential_discrepancy_amount.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
          </div>
          <p className="text-[11px] text-red-700 font-medium">{audit.discrepancies_count} findings requiring clarification</p>
        </div>

        <div className="p-5 rounded-2xl bg-slate-950 text-white shadow-2xs space-y-1 border border-slate-800">
          <span className="text-xs text-slate-400 font-bold uppercase tracking-wider">Audit Protocol</span>
          <div className="text-lg font-bold text-teal-400">
            Deterministic Engine
          </div>
          <p className="text-[11px] text-slate-400">Zero AI rate hallucination</p>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2 border-b border-slate-200 text-xs">
        {[
          { label: 'All Findings', value: 'ALL', count: findings.length },
          { label: 'Rule A (Arithmetic)', value: 'RULE_A_ARITHMETIC', count: findings.filter(f => f.rule_type === 'RULE_A_ARITHMETIC').length },
          { label: 'Rule B (Duplicates)', value: 'RULE_B_DUPLICATE', count: findings.filter(f => f.rule_type === 'RULE_B_DUPLICATE').length },
          { label: 'Rule C (Reference Rates)', value: 'RULE_C_REFERENCE_RATE', count: findings.filter(f => f.rule_type === 'RULE_C_REFERENCE_RATE').length },
          { label: 'Rule D (Unbundling)', value: 'RULE_D_CODING_MISMATCH', count: findings.filter(f => f.rule_type === 'RULE_D_CODING_MISMATCH').length },
          { label: 'Rule E (Completeness)', value: 'RULE_E_MISSING_INFO', count: findings.filter(f => f.rule_type === 'RULE_E_MISSING_INFO').length },
        ].map((tab) => (
          <button
            key={tab.value}
            onClick={() => setFilterRule(tab.value)}
            className={`px-3.5 py-2 rounded-xl font-bold transition shrink-0 flex items-center gap-2 ${
              filterRule === tab.value
                ? 'bg-slate-900 text-white shadow-xs'
                : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-50'
            }`}
          >
            <span>{tab.label}</span>
            <span className={`text-[10px] px-1.5 py-0.5 rounded-full font-mono ${
              filterRule === tab.value ? 'bg-slate-800 text-teal-300' : 'bg-slate-100 text-slate-600'
            }`}>
              {tab.count}
            </span>
          </button>
        ))}
      </div>

      {/* Findings List */}
      <div className="space-y-4">
        {filteredFindings.length > 0 ? (
          filteredFindings.map((finding) => (
            <div 
              key={finding.id} 
              className={`p-6 sm:p-7 rounded-3xl bg-white border transition-all shadow-xs space-y-4 ${
                finding.severity === 'HIGH' ? 'border-red-200/90 hover:border-red-300' : 'border-slate-200/90 hover:border-slate-300'
              }`}
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
                <div className="flex items-center gap-3">
                  <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200/80 shadow-2xs">
                    {getRuleIcon(finding.rule_type)}
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
                        Line {finding.line_number || 'N/A'}:
                      </span>
                      <h4 className="font-bold text-slate-900 text-base">
                        {finding.item_description}
                      </h4>
                    </div>
                    <span className="text-[11px] font-semibold text-slate-500">
                      Rule Type: {finding.rule_type.replace('RULE_', '').replace('_', ' ')}
                    </span>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <span className={`text-xs font-bold px-2.5 py-0.5 rounded-full ${
                    finding.severity === 'HIGH' 
                      ? 'bg-red-50 text-red-700 border border-red-200' 
                      : 'bg-amber-50 text-amber-800 border border-amber-200'
                  }`}>
                    {finding.severity} Severity
                  </span>

                  {finding.monetary_difference > 0 && (
                    <div className="text-right">
                      <span className="text-[10px] text-slate-400 block leading-none font-medium">Variance Impact</span>
                      <span className="text-base font-extrabold text-red-600 font-tabular">
                        ₹{finding.monetary_difference.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                      </span>
                    </div>
                  )}
                </div>
              </div>

              {/* Observed vs Expected Comparison Box */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs bg-slate-50/80 p-4 rounded-2xl border border-slate-200/80">
                <div>
                  <span className="text-slate-500 font-bold block uppercase tracking-wide">Observed in Invoice:</span>
                  <span className="font-bold text-slate-950 mt-1 block text-sm font-tabular">{finding.observed_value}</span>
                </div>
                <div>
                  <span className="text-slate-500 font-bold block uppercase tracking-wide">Expected Verification Standard:</span>
                  <span className="font-bold text-teal-900 mt-1 block text-sm font-tabular">{finding.expected_value}</span>
                </div>
              </div>

              {/* Mathematical Proof & Evidence */}
              <div className="space-y-1.5 text-xs text-slate-800">
                <div className="font-bold text-slate-900">Explanation & Mathematical Proof:</div>
                <p className="leading-relaxed bg-slate-50 p-4 rounded-xl border border-slate-200 text-slate-800 font-normal">
                  {finding.explanation}
                </p>
              </div>

              {/* Action Recommendation */}
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 pt-2 text-xs">
                <div className="text-slate-500 font-medium">
                  <span className="font-bold text-slate-800">Source:</span> {finding.evidence_source}
                </div>

                <div className="text-teal-800 font-bold bg-teal-50 px-3 py-1 rounded-xl border border-teal-200">
                  Recommended Action: {finding.recommended_action}
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="bg-white rounded-3xl border border-slate-200/90 p-12 text-center text-sm text-slate-500">
            No findings matching the selected filter.
          </div>
        )}
      </div>
    </div>
  );
}
