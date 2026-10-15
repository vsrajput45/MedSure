'use client';

import { useEffect, useState, useCallback } from 'react';
import { 
  Database, 
  Search, 
  RefreshCw
} from 'lucide-react';
import { api, ReferenceRate } from '@/lib/api';

export default function ReferenceRatesPage() {
  const [rates, setRates] = useState<ReferenceRate[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [specialty, setSpecialty] = useState('');
  const [scheme, setScheme] = useState('');

  const fetchRates = useCallback(async () => {
    setLoading(true);
    try {
      const res = await api.getReferenceRates({
        search: search || undefined,
        specialty: specialty || undefined,
        scheme: scheme || undefined
      });
      setRates(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [search, specialty, scheme]);

  useEffect(() => {
    fetchRates();
  }, [fetchRates]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchRates();
  };

  return (
    <div className="w-full px-4 sm:px-8 lg:px-12 xl:px-16 2xl:px-20 py-10 space-y-8">
      {/* Header */}
      <div className="max-w-3xl space-y-2">
        <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-teal-50 text-teal-800 text-xs font-bold border border-teal-200">
          <Database className="w-3.5 h-3.5 text-teal-600" />
          <span>REFERENCE DATASET TRANSPARENCY</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-950 tracking-tight">
          Tariff Benchmarks & Official Reference Rates
        </h1>
        <p className="text-base text-slate-600">
          Search verifiable government tariffs (CGHS, NPPA price caps) and standardized healthcare reference benchmarks used by the MEDSURE deterministic audit engine.
        </p>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-white p-4 sm:p-5 rounded-3xl border border-slate-200/90 shadow-xs flex flex-col md:flex-row items-center gap-3">
        <form onSubmit={handleSearch} className="flex-1 flex items-center gap-2 w-full">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search by procedure name, code (e.g. PROC-KNEE-TKR-01), or implant..."
              className="w-full pl-10 pr-4 py-2.5 rounded-2xl border border-slate-200 text-xs sm:text-sm focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
            />
          </div>
          <button
            type="submit"
            className="px-5 py-2.5 rounded-2xl bg-gradient-to-r from-teal-600 to-emerald-600 hover:from-teal-700 hover:to-emerald-700 text-white font-bold text-xs shadow-xs transition"
          >
            Search
          </button>
        </form>

        <div className="flex items-center gap-2 w-full md:w-auto">
          <select
            value={specialty}
            onChange={(e) => setSpecialty(e.target.value)}
            className="px-3.5 py-2.5 rounded-2xl border border-slate-200 text-xs bg-white text-slate-800 font-medium"
          >
            <option value="">All Specialties</option>
            <option value="Orthopedics">Orthopedics</option>
            <option value="General Surgery">General Surgery</option>
            <option value="Gastroenterology">Gastroenterology</option>
            <option value="Ophthalmology">Ophthalmology</option>
            <option value="Critical Care">Critical Care</option>
          </select>

          <select
            value={scheme}
            onChange={(e) => setScheme(e.target.value)}
            className="px-3.5 py-2.5 rounded-2xl border border-slate-200 text-xs bg-white text-slate-800 font-medium"
          >
            <option value="">All Schemes</option>
            <option value="STANDARDIZED_BENCHMARK">Standard Benchmark</option>
            <option value="CGHS">CGHS Schedule</option>
            <option value="PMJAY">PM-JAY Package</option>
          </select>
        </div>
      </div>

      {/* Status Explainer */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
        <div className="p-3.5 rounded-2xl bg-emerald-50/90 border border-emerald-200 text-emerald-950 flex items-center gap-2.5">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-600 shrink-0"></span>
          <span><b>Verified Official:</b> Official CGHS/NPPA published price orders</span>
        </div>
        <div className="p-3.5 rounded-2xl bg-amber-50/90 border border-amber-200 text-amber-950 flex items-center gap-2.5">
          <span className="w-2.5 h-2.5 rounded-full bg-amber-600 shrink-0"></span>
          <span><b>Synthetic Demo:</b> Demonstration benchmarks for audit evaluation</span>
        </div>
        <div className="p-3.5 rounded-2xl bg-slate-100 border border-slate-200 text-slate-800 flex items-center gap-2.5">
          <span className="w-2.5 h-2.5 rounded-full bg-slate-400 shrink-0"></span>
          <span><b>Standard Tariff:</b> NABH reference rate schedules</span>
        </div>
      </div>

      {/* Rates Grid */}
      {loading ? (
        <div className="py-20 text-center space-y-3">
          <RefreshCw className="w-6 h-6 text-teal-600 animate-spin mx-auto" />
          <p className="text-xs text-slate-500 font-medium">Querying reference rates database...</p>
        </div>
      ) : rates.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {rates.map((rate) => (
            <div
              key={rate.id}
              className="p-6 rounded-3xl bg-white border border-slate-200/90 shadow-xs hover:shadow-md hover:-translate-y-0.5 transition-all space-y-4 flex flex-col justify-between"
            >
              <div className="space-y-3">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-[10px] font-mono px-2.5 py-0.5 rounded-lg bg-slate-100 text-slate-700 font-bold">
                    {rate.procedure_code}
                  </span>
                  <span className={`text-[10px] font-bold px-2.5 py-0.5 rounded-full ${
                    rate.verification_status === 'VERIFIED_OFFICIAL'
                      ? 'bg-emerald-50 text-emerald-800 border border-emerald-200'
                      : 'bg-amber-50 text-amber-900 border border-amber-200'
                  }`}>
                    {rate.verification_status.replace('_', ' ')}
                  </span>
                </div>

                <div>
                  <h3 className="font-extrabold text-slate-950 text-base leading-snug">
                    {rate.procedure_name}
                  </h3>
                  <p className="text-xs text-slate-500 mt-1 line-clamp-2">
                    {rate.description || 'Standard medical tariff item.'}
                  </p>
                </div>

                <div className="p-3.5 bg-slate-50/80 rounded-2xl border border-slate-100 space-y-1.5 text-xs">
                  <div className="flex justify-between text-slate-500">
                    <span>Base Rate:</span>
                    <span className="font-extrabold text-slate-950 font-tabular">₹{rate.base_rate.toLocaleString('en-IN')}</span>
                  </div>
                  <div className="flex justify-between text-slate-500">
                    <span>Benchmark Range:</span>
                    <span className="font-bold text-teal-800 font-tabular">
                      ₹{rate.min_rate.toLocaleString('en-IN')} – ₹{rate.max_rate.toLocaleString('en-IN')}
                    </span>
                  </div>
                  <div className="flex justify-between text-slate-500">
                    <span>Unit Basis:</span>
                    <span className="text-slate-700 font-medium">{rate.unit_basis}</span>
                  </div>
                </div>

                {rate.inclusion_notes && (
                  <div className="text-[11px] text-slate-700 bg-teal-50/60 p-3 rounded-xl border border-teal-100">
                    <span className="font-bold text-teal-950">Inclusions: </span>
                    {rate.inclusion_notes}
                  </div>
                )}
              </div>

              <div className="pt-3 border-t border-slate-100 text-[11px] text-slate-400 flex items-center justify-between">
                <span className="truncate max-w-[200px] text-slate-500">{rate.source_document}</span>
                <span className="font-bold text-slate-700">{rate.scheme}</span>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-white p-12 rounded-3xl border border-slate-200 text-center text-sm text-slate-500">
          No matching tariff benchmarks found. Try adjusting your search query.
        </div>
      )}
    </div>
  );
}
