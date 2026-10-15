'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { 
  AlertTriangle, 
  Trash2, 
  Plus, 
  ArrowRight, 
  ShieldCheck, 
  Building, 
  Calendar, 
  Hash, 
  RefreshCw
} from 'lucide-react';
import { api, BillExtractionReview, BillLineItem } from '@/lib/api';

export default function BillReviewPage() {
  const params = useParams();
  const router = useRouter();
  const billId = params.id as string;

  const [data, setData] = useState<BillExtractionReview | null>(null);
  const [items, setItems] = useState<BillLineItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Configurable Audit Benchmark Parameters
  const [selectedScheme, setSelectedScheme] = useState('STANDARDIZED_BENCHMARK');
  const [selectedFacility, setSelectedFacility] = useState('NABH_ACCREDITED');
  const [selectedRegion, setSelectedRegion] = useState('National');

  useEffect(() => {
    const fetchBill = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await api.getBillExtraction(billId);
        setData(res);
        setItems(res.line_items || []);
      } catch (err: any) {
        setError(err.message || 'Failed to load bill extraction.');
      } finally {
        setLoading(false);
      }
    };
    if (billId) {
      fetchBill();
    }
  }, [billId]);

  const handleItemChange = (index: number, field: keyof BillLineItem, value: any) => {
    const updated = [...items];
    const current = { ...updated[index], [field]: value };
    // Automatically recalculate line total when quantity or rate changes
    if (field === 'quantity' || field === 'unit_price') {
      const q = parseFloat(field === 'quantity' ? value : current.quantity.toString()) || 0;
      const u = parseFloat(field === 'unit_price' ? value : current.unit_price.toString()) || 0;
      current.line_total = parseFloat((q * u).toFixed(2));
    }
    updated[index] = current;
    setItems(updated);
  };

  const handleDeleteItem = (index: number) => {
    const filtered = items.filter((_, idx) => idx !== index);
    const renumbered = filtered.map((item, idx) => ({ ...item, line_number: idx + 1 }));
    setItems(renumbered);
  };

  const handleAddItem = () => {
    const newItem: BillLineItem = {
      line_number: items.length + 1,
      raw_description: 'Custom Billed Item',
      normalized_description: 'Custom Billed Item',
      category: 'OTHER',
      quantity: 1.0,
      unit_price: 0.0,
      line_total: 0.0,
      extracted_line_total: 0.0,
      is_package_component: false,
      ocr_confidence: 1.0,
      user_edited: true
    };
    setItems([...items, newItem]);
  };

  const handleConfirmAndAudit = async () => {
    setSubmitting(true);
    setError(null);
    try {
      // 1. Save corrected items
      await api.updateBillLineItems(billId, items);

      // 2. Trigger deterministic audit run with user-selected parameters
      const audit = await api.runAudit(billId, {
        scheme: selectedScheme,
        facility_category: selectedFacility,
        region: selectedRegion
      });

      // 3. Navigate to audit findings report
      router.push(`/audits/${audit.id}`);
    } catch (err: any) {
      setError(err.message || 'Failed to run bill audit.');
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-24 text-center space-y-4">
        <RefreshCw className="w-8 h-8 text-teal-600 animate-spin mx-auto" />
        <p className="text-sm text-slate-600 font-semibold">Extracting and normalizing bill line items via PyMuPDF...</p>
      </div>
    );
  }

  if (error && !data) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-20 text-center space-y-4">
        <AlertTriangle className="w-12 h-12 text-red-500 mx-auto" />
        <h2 className="text-xl font-bold text-slate-900">Failed to load invoice</h2>
        <p className="text-sm text-slate-500">{error}</p>
        <Link href="/bills/upload" className="inline-block px-4 py-2 rounded-xl bg-teal-600 text-white text-xs font-bold">
          Return to Upload
        </Link>
      </div>
    );
  }

  const currentTotal = items.reduce((sum, item) => sum + (parseFloat(item.line_total?.toString() || '0') || 0), 0);
  const roundedTotal = Math.round(currentTotal * 100) / 100;

  return (
    <div className="w-full px-4 sm:px-8 lg:px-12 xl:px-16 2xl:px-20 py-10 space-y-8">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-200">
        <div>
          <span className="text-xs font-bold px-3 py-1 rounded-full bg-teal-50 text-teal-800 border border-teal-200">
            Step 2 of 3: OCR Review & Verification
          </span>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-950 tracking-tight mt-1.5">
            Review Extracted Hospital Line Items
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-0.5">
            Verify the extracted quantities and rates below. You can correct any OCR typos or add/remove items before running the deterministic financial audit.
          </p>
        </div>

        <button
          onClick={handleConfirmAndAudit}
          disabled={submitting}
          className="inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl bg-gradient-to-r from-teal-600 to-emerald-600 hover:from-teal-700 hover:to-emerald-700 text-white font-bold text-sm shadow-md shadow-teal-600/25 transition disabled:opacity-50 shrink-0"
        >
          {submitting ? (
            <>
              <RefreshCw className="w-4 h-4 animate-spin" />
              <span>Running Audit...</span>
            </>
          ) : (
            <>
              <span>Run Deterministic Audit</span>
              <ArrowRight className="w-4 h-4" />
            </>
          )}
        </button>
      </div>

      {/* Invoice Metadata Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 rounded-2xl bg-white border border-slate-200/90 shadow-2xs space-y-1">
          <span className="text-xs text-slate-500 font-semibold flex items-center gap-1.5">
            <Building className="w-3.5 h-3.5 text-slate-400" />
            Hospital Name
          </span>
          <div className="text-sm font-extrabold text-slate-900 truncate">
            {data?.hospital_name || 'Healthcare Provider'}
          </div>
        </div>

        <div className="p-5 rounded-2xl bg-white border border-slate-200/90 shadow-2xs space-y-1">
          <span className="text-xs text-slate-500 font-semibold flex items-center gap-1.5">
            <Hash className="w-3.5 h-3.5 text-slate-400" />
            Invoice Number
          </span>
          <div className="text-sm font-extrabold text-slate-900 font-mono">
            {data?.invoice_number || 'INV-REF'}
          </div>
        </div>

        <div className="p-5 rounded-2xl bg-white border border-slate-200/90 shadow-2xs space-y-1">
          <span className="text-xs text-slate-500 font-semibold flex items-center gap-1.5">
            <Calendar className="w-3.5 h-3.5 text-slate-400" />
            Bill Date
          </span>
          <div className="text-sm font-extrabold text-slate-900">
            {data?.bill_date ? new Date(data.bill_date).toLocaleDateString('en-IN') : 'Recent Admission'}
          </div>
        </div>

        <div className="p-5 rounded-2xl bg-slate-950 text-white shadow-2xs space-y-1 border border-slate-800">
          <span className="text-xs text-slate-400 font-semibold">Billed Amount Claimed</span>
          <div className="text-xl font-extrabold text-teal-400 font-tabular">
            ₹{roundedTotal.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
          </div>
        </div>
      </div>

      {/* Audit Benchmark Selection Configuration */}
      <div className="p-5 rounded-3xl bg-slate-50 border border-slate-200/90 shadow-2xs space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-teal-600" />
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-800">
              Audit Benchmark Tariff & Facility Parameters
            </h3>
          </div>
          <span className="text-[11px] text-slate-500 font-medium hidden sm:inline">
            Deterministic rules evaluate line items against this benchmark
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div>
            <label className="block text-[11px] font-bold text-slate-700 mb-1">
              Reference Tariff Scheme
            </label>
            <select
              value={selectedScheme}
              onChange={(e) => setSelectedScheme(e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-white border border-slate-200 text-xs font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-teal-500"
            >
              <option value="STANDARDIZED_BENCHMARK">Standardized Benchmark (National Tariff Model)</option>
              <option value="CGHS">CGHS (Central Government Health Scheme Tariff)</option>
              <option value="PMJAY">PM-JAY (Ayushman Bharat Health Benefit Packages)</option>
            </select>
          </div>

          <div>
            <label className="block text-[11px] font-bold text-slate-700 mb-1">
              Facility Accreditation Grade
            </label>
            <select
              value={selectedFacility}
              onChange={(e) => setSelectedFacility(e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-white border border-slate-200 text-xs font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-teal-500"
            >
              <option value="NABH_ACCREDITED">NABH Accredited (Apex Quality Tariff Tier)</option>
              <option value="NON_NABH">Non-NABH (Base Hospital Rate Tier)</option>
            </select>
          </div>

          <div>
            <label className="block text-[11px] font-bold text-slate-700 mb-1">
              Geographic Region
            </label>
            <select
              value={selectedRegion}
              onChange={(e) => setSelectedRegion(e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-white border border-slate-200 text-xs font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-teal-500"
            >
              <option value="National">National Benchmark</option>
              <option value="Delhi-NCR">Delhi-NCR Metro Zone</option>
              <option value="Mumbai Metropolitan">Mumbai Metropolitan Zone</option>
              <option value="South Zone">South Zone (Bengaluru / Chennai / Hyd)</option>
            </select>
          </div>
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-2xl bg-red-50 border border-red-200 text-xs text-red-800 font-medium">
          {error}
        </div>
      )}

      {/* Line Items Table */}
      <div className="bg-white rounded-3xl border border-slate-200/90 shadow-xs overflow-hidden">
        <div className="p-5 border-b border-slate-200/80 flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-slate-50/70">
          <div>
            <h2 className="text-sm font-extrabold text-slate-900">
              Itemized Hospital Charges ({items.length} Extracted Items)
            </h2>
            <p className="text-xs text-slate-500 font-medium mt-0.5">
              Editable prior to running audit. Adjust quantities or rates if OCR misread characters.
            </p>
          </div>

          <button
            type="button"
            onClick={handleAddItem}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white border border-slate-300 hover:border-teal-500 hover:text-teal-700 text-xs font-bold text-slate-700 shadow-2xs transition shrink-0"
          >
            <Plus className="w-3.5 h-3.5 text-teal-600" />
            <span>Add Line Item</span>
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="bg-slate-100/80 border-b border-slate-200 text-slate-700 font-bold uppercase tracking-wider">
                <th className="py-3 px-3 w-12 text-center">#</th>
                <th className="py-3 px-4">Item Description</th>
                <th className="py-3 px-3 w-32">Category</th>
                <th className="py-3 px-3 w-20 text-right">Qty</th>
                <th className="py-3 px-4 w-32 text-right">Unit Rate (₹)</th>
                <th className="py-3 px-4 w-36 text-right">Claimed Total (₹)</th>
                <th className="py-3 px-3 w-20 text-center">Confidence</th>
                <th className="py-3 px-3 w-14 text-center">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {items.map((item, idx) => (
                <tr key={idx} className="hover:bg-slate-50/80 transition">
                  <td className="py-3 px-3 text-center text-slate-700 font-bold font-mono">
                    {item.line_number || idx + 1}
                  </td>
                  <td className="py-3 px-4">
                    <input
                      type="text"
                      value={item.normalized_description}
                      onChange={(e) => handleItemChange(idx, 'normalized_description', e.target.value)}
                      className="w-full px-2.5 py-1.5 rounded-lg border border-slate-200 hover:border-slate-400 focus:border-teal-500 focus:bg-white text-xs text-slate-950 font-semibold"
                    />
                  </td>
                  <td className="py-3 px-3">
                    <select
                      value={item.category}
                      onChange={(e) => handleItemChange(idx, 'category', e.target.value)}
                      className="w-full px-2 py-1.5 rounded-lg border border-slate-200 text-xs text-slate-800 font-medium bg-white"
                    >
                      <option value="SURGERY">Surgery</option>
                      <option value="IMPLANT">Implant</option>
                      <option value="ROOM_RENT">Room Rent</option>
                      <option value="PHARMACY">Pharmacy</option>
                      <option value="INVESTIGATION">Investigation</option>
                      <option value="CONSUMABLE">Consumable</option>
                      <option value="OTHER">Other</option>
                    </select>
                  </td>
                  <td className="py-3 px-3 text-right">
                    <input
                      type="number"
                      step="any"
                      value={item.quantity}
                      onChange={(e) => handleItemChange(idx, 'quantity', parseFloat(e.target.value) || 0)}
                      className="w-full px-2 py-1.5 rounded-lg border border-slate-200 hover:border-slate-400 focus:border-teal-500 focus:bg-white text-right text-xs text-slate-950 font-bold font-mono"
                    />
                  </td>
                  <td className="py-3 px-4 text-right">
                    <input
                      type="number"
                      step="any"
                      value={item.unit_price}
                      onChange={(e) => handleItemChange(idx, 'unit_price', parseFloat(e.target.value) || 0)}
                      className="w-full px-2 py-1.5 rounded-lg border border-slate-200 hover:border-slate-400 focus:border-teal-500 focus:bg-white text-right text-xs text-slate-950 font-bold font-mono"
                    />
                  </td>
                  <td className="py-3 px-4 text-right">
                    <input
                      type="number"
                      step="any"
                      value={item.line_total}
                      onChange={(e) => handleItemChange(idx, 'line_total', parseFloat(e.target.value) || 0)}
                      className="w-full px-2 py-1.5 rounded-lg border border-slate-200 hover:border-slate-400 focus:border-teal-500 focus:bg-white text-right text-xs font-extrabold text-slate-950 font-mono"
                    />
                  </td>
                  <td className="py-3 px-3 text-center">
                    <span className="inline-block px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-800 text-[10px] font-bold border border-emerald-200">
                      {Math.round((item.ocr_confidence || 0.95) * 100)}%
                    </span>
                  </td>
                  <td className="py-3 px-3 text-center">
                    <button
                      type="button"
                      onClick={() => handleDeleteItem(idx)}
                      title="Delete item"
                      className="p-1.5 rounded-lg text-slate-400 hover:text-red-600 hover:bg-red-50 transition"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="p-5 bg-slate-50/80 border-t border-slate-200/80 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="text-xs text-slate-600">
            Total Claimed from Line Items: <span className="font-extrabold text-slate-950 font-tabular">₹{roundedTotal.toLocaleString('en-IN', { minimumFractionDigits: 2 })}</span>
          </div>

          <button
            onClick={handleConfirmAndAudit}
            disabled={submitting}
            className="w-full sm:w-auto px-6 py-2.5 rounded-xl bg-gradient-to-r from-teal-600 to-emerald-600 hover:from-teal-700 hover:to-emerald-700 text-white font-bold text-xs shadow-xs hover:shadow transition flex items-center justify-center gap-2"
          >
            <span>Proceed to Audit Findings</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
