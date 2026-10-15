'use client';

import { useState } from 'react';
import Link from 'next/link';
import { 
  Stethoscope, 
  AlertTriangle, 
  ShieldCheck, 
  ArrowRight, 
  Sparkles, 
  Info, 
  Building,
  MapPin,
  Languages,
  Activity,
  RefreshCw
} from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Cell } from 'recharts';
import { api, Estimate, TriageResult } from '@/lib/api';

export default function TriagePage() {
  const [symptom, setSymptom] = useState('');
  const [language, setLanguage] = useState<'en' | 'hi'>('en');
  const [region, setRegion] = useState('National');
  const [facility, setFacility] = useState('NABH_ACCREDITED');
  const [scheme, setScheme] = useState('STANDARDIZED_BENCHMARK');

  const [loading, setLoading] = useState(false);
  const [estimate, setEstimate] = useState<Estimate | null>(null);
  const [triage, setTriage] = useState<TriageResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Quick preset scenarios for hackathon judges & users
  const presets = [
    {
      title: 'Orthopedic Knee Replacement (Hindi)',
      query: 'मेरे घुटने में बहुत तेज दर्द है और चलने में परेशानी हो रही है, डॉक्टर ने नी रिप्लेसमेंट की सलाह दी है',
      lang: 'hi' as const,
      category: 'Orthopedics (~₹1.45L)'
    },
    {
      title: 'Dengue & Low Platelets (Hindi)',
      query: 'तेज बुखार, बदन दर्द और प्लेटलेट्स 40,000 हो गए हैं, डॉक्टर ने डेंगू के लिए भर्ती होने को कहा है',
      lang: 'hi' as const,
      category: 'Inpatient Medicine (~₹22K)'
    },
    {
      title: 'Cardiac Angioplasty & Stent (English)',
      query: 'Severe angina on exertion, angiogram revealed 85% single vessel coronary artery blockage requiring angioplasty with drug-eluting stent',
      lang: 'en' as const,
      category: 'Cardiology (~₹1.55L)'
    },
    {
      title: 'Kidney Stone Laser Removal (English)',
      query: 'Excruciating right flank pain radiating to groin, CT KUB confirmed 8mm ureteric calculus requiring laser lithotripsy / PCNL',
      lang: 'en' as const,
      category: 'Urology (~₹48K)'
    },
    {
      title: 'Cataract Eye Surgery (English)',
      query: 'Cloudy blurred vision in both eyes with glare at night, diagnosed with senile cataract needing phacoemulsification with foldable IOL',
      lang: 'en' as const,
      category: 'Ophthalmology (~₹26K)'
    },
    {
      title: 'Emergency Red-Flag Test',
      query: 'Crushing severe chest pain radiating to left arm with shortness of breath and cold sweating',
      lang: 'en' as const,
      category: 'Emergency (Critical Alert)'
    }
  ];

  const handleAssessAndEstimate = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!symptom.trim() || symptom.trim().length < 3) {
      setError('Please provide a symptom description of at least 3 characters.');
      return;
    }

    setLoading(true);
    setError(null);
    setEstimate(null);
    setTriage(null);

    try {
      // Step 1: Run triage assessment
      const triageRes = await api.assessSymptoms(symptom, language);
      setTriage(triageRes);

      // Step 2: Create deterministic cost estimate
      const estRes = await api.createEstimate({
        symptom_description: symptom,
        procedure_code: triageRes.candidate_procedure_code,
        scheme: scheme,
        facility_category: facility,
        region: region,
        preferred_language: language
      });
      setEstimate(estRes);
    } catch (err: any) {
      setError(err.message || 'Error communicating with estimation service.');
    } finally {
      setLoading(false);
    }
  };

  const chartData = estimate ? [
    { name: 'Lower Bound', amount: estimate.estimated_min_cost, fill: '#0D9488' },
    { name: 'Expected Median', amount: estimate.median_cost, fill: '#0F766E' },
    { name: 'Ceiling Bound', amount: estimate.estimated_max_cost, fill: '#134E4A' }
  ] : [];

  return (
    <div className="w-full px-4 sm:px-8 lg:px-12 xl:px-16 2xl:px-20 py-10 space-y-10">
      {/* Header */}
      <div className="max-w-3xl space-y-2">
        <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-teal-50 text-teal-800 text-xs font-bold border border-teal-200">
          <Stethoscope className="w-3.5 h-3.5 text-teal-600" />
          <span>ACT 1 • BEFORE ADMISSION</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-950 tracking-tight">
          Symptom Guidance & Fair Price Estimator
        </h1>
        <p className="text-base text-slate-600">
          Understand which clinical specialty to consult and explore transparent hospital procedural cost ranges before scheduling surgery.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Column: Form & Presets */}
        <div className="lg:col-span-5 space-y-6">
          <div className="bg-white rounded-3xl border border-slate-200/90 shadow-xs p-6 sm:p-7 space-y-5">
            <h2 className="font-bold text-slate-900 text-base flex items-center justify-between pb-3 border-b border-slate-100">
              <span className="flex items-center gap-2">
                <Activity className="w-4 h-4 text-teal-600" />
                Patient Symptom Query
              </span>
              <span className="text-[11px] font-semibold text-slate-500 bg-slate-100 px-2 py-0.5 rounded-md">
                Non-diagnostic
              </span>
            </h2>

            {/* Presets */}
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-500 uppercase tracking-wider block">
                Quick Demonstration Scenarios:
              </label>
              <div className="grid grid-cols-1 gap-2">
                {presets.map((p, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => {
                      setSymptom(p.query);
                      setLanguage(p.lang);
                    }}
                    className="text-left p-2.5 rounded-xl bg-slate-50 hover:bg-teal-50/80 border border-slate-200/80 hover:border-teal-300 text-xs text-slate-700 transition group flex items-center justify-between"
                  >
                    <div className="flex items-center gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-teal-500"></span>
                      <span className="font-semibold text-slate-900 group-hover:text-teal-900">{p.title}</span>
                    </div>
                    <span className="text-[10px] px-2 py-0.5 rounded-md bg-white border border-slate-200 uppercase font-mono font-bold text-slate-600">
                      {p.lang}
                    </span>
                  </button>
                ))}
              </div>
            </div>

            <form onSubmit={handleAssessAndEstimate} className="space-y-4 pt-1">
              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                  Describe Symptoms or Diagnosis:
                </label>
                <textarea
                  rows={4}
                  value={symptom}
                  onChange={(e) => setSymptom(e.target.value)}
                  placeholder="e.g. Severe knee osteoarthritis with stiffness, pain walking, doctor advised surgery..."
                  className="w-full px-3.5 py-2.5 rounded-2xl border border-slate-200 text-sm focus:ring-2 focus:ring-teal-500 focus:border-teal-500 transition resize-none placeholder:text-slate-400"
                />
              </div>

              {/* Configurations Grid */}
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-600 mb-1 flex items-center gap-1.5">
                    <Languages className="w-3.5 h-3.5 text-slate-400" />
                    <span>Language</span>
                  </label>
                  <select
                    value={language}
                    onChange={(e: any) => setLanguage(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 text-xs bg-white text-slate-800"
                  >
                    <option value="en">English</option>
                    <option value="hi">हिंदी (Hindi)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-600 mb-1 flex items-center gap-1.5">
                    <MapPin className="w-3.5 h-3.5 text-slate-400" />
                    <span>Region</span>
                  </label>
                  <select
                    value={region}
                    onChange={(e) => setRegion(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 text-xs bg-white text-slate-800"
                  >
                    <option value="National">National Benchmark</option>
                    <option value="Delhi-NCR">Delhi-NCR</option>
                    <option value="Mumbai">Mumbai</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-600 mb-1 flex items-center gap-1.5">
                    <Building className="w-3.5 h-3.5 text-slate-400" />
                    <span>Facility Standard</span>
                  </label>
                  <select
                    value={facility}
                    onChange={(e) => setFacility(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 text-xs bg-white text-slate-800"
                  >
                    <option value="NABH_ACCREDITED">NABH Accredited</option>
                    <option value="NON_NABH">Non-NABH Facility</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-600 mb-1 flex items-center gap-1.5">
                    <ShieldCheck className="w-3.5 h-3.5 text-slate-400" />
                    <span>Reference Tariff</span>
                  </label>
                  <select
                    value={scheme}
                    onChange={(e) => setScheme(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 text-xs bg-white text-slate-800"
                  >
                    <option value="STANDARDIZED_BENCHMARK">Standard Benchmark</option>
                    <option value="CGHS">CGHS Schedule</option>
                    <option value="PMJAY">PM-JAY Package</option>
                  </select>
                </div>
              </div>

              {error && (
                <div className="p-3.5 rounded-xl bg-red-50 text-red-700 text-xs border border-red-200 flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 shrink-0 text-red-600" />
                  <span>{error}</span>
                </div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="w-full py-3.5 rounded-xl bg-gradient-to-r from-teal-600 to-emerald-600 hover:from-teal-700 hover:to-emerald-700 text-white font-bold text-sm shadow-md shadow-teal-600/25 transition flex items-center justify-center gap-2 disabled:opacity-70"
              >
                {loading ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" />
                    <span>Analyzing clinical benchmarks...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4" />
                    <span>Calculate Fair Price Range</span>
                  </>
                )}
              </button>
            </form>
          </div>
        </div>

        {/* Right Column: Guidance & Price Bounds Output */}
        <div className="lg:col-span-7 space-y-6">
          {/* Emergency Red Flag Notice if detected */}
          {triage?.is_emergency && (
            <div className="p-6 rounded-3xl bg-red-600 text-white shadow-xl space-y-3 border border-red-500">
              <div className="flex items-center gap-2.5 font-bold text-lg">
                <AlertTriangle className="w-6 h-6 shrink-0 animate-bounce" />
                <span>CRITICAL EMERGENCY RED FLAG DETECTED</span>
              </div>
              <p className="text-sm leading-relaxed text-red-100">
                {language === 'hi' ? triage.recommended_action_hi : triage.recommended_action_en}
              </p>
              <div className="text-xs bg-red-700/90 p-3.5 rounded-2xl text-red-100 border border-red-500/50">
                <b>Emergency Protocol:</b> Do not delay clinical intervention for administrative cost estimation. Please proceed to the nearest emergency department or call 112 / 102 immediately.
              </div>
            </div>
          )}

          {/* Results Card - Only displayed for non-emergency guidance */}
          {estimate && !triage?.is_emergency ? (
            <div className="bg-white rounded-3xl border border-slate-200/90 shadow-xs p-6 sm:p-8 space-y-6">
              <div className="flex flex-wrap items-center justify-between gap-3 pb-4 border-b border-slate-100">
                <div>
                  <span className="text-xs font-bold text-teal-600 uppercase tracking-wider">
                    {estimate.identified_specialty}
                  </span>
                  <h3 className="text-2xl font-extrabold text-slate-950 mt-0.5">
                    {estimate.procedure_name || 'Clinical Care Guidance'}
                  </h3>
                </div>

                <span className={`text-xs font-bold px-3 py-1 rounded-full ${
                  estimate.benchmark_status === 'VERIFIED_OFFICIAL'
                    ? 'bg-emerald-50 text-emerald-800 border border-emerald-200'
                    : estimate.benchmark_status === 'SYNTHETIC_DEMO'
                    ? 'bg-amber-50 text-amber-900 border border-amber-200'
                    : 'bg-slate-100 text-slate-700 border border-slate-200'
                }`}>
                  {estimate.benchmark_status.replace('_', ' ')}
                </span>
              </div>

              {/* Price Range Display */}
              <div className="bg-slate-50/80 rounded-2xl p-6 border border-slate-200/80 space-y-5">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-700">
                    Deterministic Fair Price Range
                  </span>
                  <span className="text-xs text-slate-500 font-medium">Standardized Benchmarks</span>
                </div>

                <div className="grid grid-cols-3 gap-3 text-center">
                  <div className="p-3.5 bg-white rounded-2xl border border-slate-200 shadow-2xs">
                    <span className="text-xs text-slate-500 font-semibold block">Lower Bound</span>
                    <span className="text-base sm:text-2xl font-bold text-slate-950 font-tabular">
                      ₹{estimate.estimated_min_cost.toLocaleString('en-IN')}
                    </span>
                  </div>

                  <div className="p-3.5 bg-teal-50/90 rounded-2xl border border-teal-200 shadow-2xs">
                    <span className="text-xs text-teal-800 font-bold block">Expected Median</span>
                    <span className="text-base sm:text-2xl font-extrabold text-teal-950 font-tabular">
                      ₹{estimate.median_cost.toLocaleString('en-IN')}
                    </span>
                  </div>

                  <div className="p-3.5 bg-white rounded-2xl border border-slate-200 shadow-2xs">
                    <span className="text-xs text-slate-500 font-semibold block">Ceiling Bound</span>
                    <span className="text-base sm:text-2xl font-bold text-slate-950 font-tabular">
                      ₹{estimate.estimated_max_cost.toLocaleString('en-IN')}
                    </span>
                  </div>
                </div>

                {/* Visual Chart */}
                <div className="h-44 w-full pt-3">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                      <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#475569' }} />
                      <YAxis tick={{ fontSize: 10, fill: '#475569' }} tickFormatter={(val) => `₹${val / 1000}k`} />
                      <Tooltip formatter={(value: any) => [`₹${value.toLocaleString('en-IN')}`, 'Benchmark Rate']} />
                      <Bar dataKey="amount" radius={[8, 8, 0, 0]}>
                        {chartData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.fill} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Clinical Guidance Text */}
              <div className="space-y-2">
                <h4 className="font-bold text-slate-950 text-sm">Care Guidance & Triage Note</h4>
                <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 text-sm text-slate-800 leading-relaxed font-normal">
                  {language === 'hi' && estimate.triage_guidance_hi ? (
                    <div>{estimate.triage_guidance_hi}</div>
                  ) : (
                    <div>{estimate.triage_guidance_en}</div>
                  )}
                </div>
              </div>

              {/* Assumptions & Limitations */}
              <div className="p-4 rounded-2xl bg-blue-50/80 border border-blue-200/90 text-xs text-blue-950 space-y-2">
                <div className="flex items-center gap-1.5 font-bold text-blue-900">
                  <Info className="w-4 h-4 text-blue-800" />
                  <span>Tariff Assumptions & Package Inclusions</span>
                </div>
                <p className="leading-relaxed font-normal">
                  {estimate.assumptions_and_limitations}
                </p>
                <p className="text-[11px] text-blue-900 italic pt-1 border-t border-blue-200 font-medium">
                  {estimate.disclaimer}
                </p>
              </div>

              {/* Next Step Link */}
              <div className="pt-2 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs border-t border-slate-100">
                <span className="text-slate-500">Holding a medical invoice from a recent discharge?</span>
                <Link
                  href="/bills/upload"
                  className="inline-flex items-center gap-1.5 font-bold text-teal-700 hover:text-teal-900 transition"
                >
                  <span>Proceed to Act 2: Audit Hospital Bill</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-3xl border border-slate-200/90 shadow-xs p-12 text-center space-y-4">
              <div className="w-16 h-16 rounded-2xl bg-teal-50 text-teal-700 mx-auto flex items-center justify-center">
                <Stethoscope className="w-8 h-8" />
              </div>
              <div className="max-w-md mx-auto space-y-1.5">
                <h3 className="text-lg font-bold text-slate-900">Awaiting Clinical Description</h3>
                <p className="text-xs text-slate-500 leading-relaxed">
                  Select one of the sample scenarios on the left or enter a custom description to calculate deterministic procedural price bounds.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
