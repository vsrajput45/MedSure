'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { 
  UploadCloud, 
  FileText, 
  AlertCircle, 
  Sparkles, 
  ShieldCheck, 
  CheckCircle2, 
  ArrowRight,
  FileCheck,
  RefreshCw,
  Lock,
  FileCode2
} from 'lucide-react';
import { api } from '@/lib/api';

export default function BillUploadPage() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selected = e.target.files[0];
      setFile(selected);
      setError(null);
    }
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a PDF or image medical bill file to audit.');
      return;
    }

    setUploading(true);
    setError(null);

    try {
      const res = await api.uploadBill(file);
      router.push(`/bills/${res.bill_id}/review`);
    } catch (err: any) {
      setError(err.message || 'Failed to process document upload.');
      setUploading(false);
    }
  };

  // Instant demo bill loader
  const handleLoadDemoBill = async () => {
    setUploading(true);
    setError(null);
    try {
      const bills = await api.getBills();
      const demoBill = bills.find((b: any) => b.is_demo_sample) || bills[0];
      if (demoBill) {
        router.push(`/bills/${demoBill.id}/review`);
      } else {
        setError('Demo bill not found. Please upload a PDF file.');
        setUploading(false);
      }
    } catch (err: any) {
      setError(err.message || 'Error accessing demo bill.');
      setUploading(false);
    }
  };

  return (
    <div className="w-full max-w-6xl mx-auto px-4 sm:px-8 lg:px-12 xl:px-16 2xl:px-20 py-12 space-y-8">
      {/* Header */}
      <div className="text-center space-y-2.5">
        <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-slate-100 text-slate-800 text-xs font-bold border border-slate-300">
          <FileCheck className="w-3.5 h-3.5 text-teal-600" />
          <span>ACT 2 • AFTER DISCHARGE</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-950 tracking-tight">
          Upload Medical Bill for Audit
        </h1>
        <p className="text-base text-slate-600 max-w-xl mx-auto">
          Upload an itemized hospital bill (PDF or image). Our OCR pipeline extracts individual charges for your review before running the deterministic audit engine.
        </p>
      </div>

      {/* Main Upload Box */}
      <div className="bg-white rounded-3xl border border-slate-200/90 shadow-xs p-8 sm:p-10 space-y-8">
        {/* Synthetic Sample Banner */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 p-5 rounded-2xl bg-amber-50/90 border border-amber-200/90 shadow-2xs">
          <div className="flex items-center gap-3.5">
            <div className="w-10 h-10 rounded-xl bg-amber-100 text-amber-800 flex items-center justify-center shrink-0">
              <Sparkles className="w-5 h-5 text-amber-600" />
            </div>
            <div>
              <h3 className="font-bold text-amber-950 text-sm">Synthetic Evaluation Bill Sample</h3>
              <p className="text-xs text-amber-900 font-medium">
                Test the pre-seeded synthetic Knee Replacement invoice (with arithmetic error, duplicate OT charge, and rate cap violation).
              </p>
            </div>
          </div>

          <button
            type="button"
            onClick={handleLoadDemoBill}
            disabled={uploading}
            className="w-full sm:w-auto px-4 py-2.5 rounded-xl bg-amber-600 hover:bg-amber-700 text-white font-bold text-xs shadow-xs hover:shadow transition shrink-0"
          >
            {uploading ? 'Loading Demo...' : 'Load Synthetic Bill Demo'}
          </button>
        </div>

        {/* Upload Drop Zone Form */}
        <form onSubmit={handleUpload} className="space-y-6">
          <div className="border-2 border-dashed border-slate-300 hover:border-teal-500 rounded-3xl p-8 sm:p-12 text-center transition-all cursor-pointer bg-slate-50/50 hover:bg-teal-50/20 group">
            <input
              type="file"
              id="file-upload"
              accept=".pdf,.png,.jpg,.jpeg"
              onChange={handleFileChange}
              className="hidden"
            />
            <label htmlFor="file-upload" className="cursor-pointer space-y-4 block">
              <div className="w-16 h-16 rounded-2xl bg-teal-50 text-teal-600 mx-auto flex items-center justify-center group-hover:scale-105 group-hover:bg-teal-100/80 transition-all">
                <UploadCloud className="w-8 h-8" />
              </div>
              <div className="space-y-1">
                <div className="text-sm font-bold text-slate-800">
                  {file ? (
                    <span className="text-teal-700 font-bold">{file.name}</span>
                  ) : (
                    <span>Click to select or drag and drop your invoice</span>
                  )}
                </div>
                <p className="text-xs text-slate-500">
                  Supported formats: PDF, PNG, JPG, JPEG (Max 15MB)
                </p>
              </div>
            </label>
          </div>

          {error && (
            <div className="p-4 rounded-2xl bg-red-50 border border-red-200 flex items-center gap-3 text-xs text-red-800">
              <AlertCircle className="w-4 h-4 shrink-0 text-red-600" />
              <span>{error}</span>
            </div>
          )}

          <button
            type="submit"
            disabled={!file || uploading}
            className="w-full py-4 rounded-2xl bg-gradient-to-r from-teal-600 to-emerald-600 hover:from-teal-700 hover:to-emerald-700 text-white font-bold text-sm shadow-md shadow-teal-600/25 transition disabled:opacity-50 flex items-center justify-center gap-2"
          >
            {uploading ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin" />
                <span>Extracting document charges with PyMuPDF OCR...</span>
              </>
            ) : (
              <>
                <span>Extract Charges & Review</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        {/* Security & Privacy Footer */}
        <div className="border-t border-slate-100 pt-6 grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs text-slate-500">
          <div className="flex items-center gap-2">
            <Lock className="w-4 h-4 text-teal-600" />
            <span>Private secure document storage</span>
          </div>
          <div className="flex items-center gap-2">
            <FileCode2 className="w-4 h-4 text-teal-600" />
            <span>SHA-256 duplicate detection</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-teal-600" />
            <span>Patient editable line items</span>
          </div>
        </div>
      </div>
    </div>
  );
}
