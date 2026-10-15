const getBaseUrl = (): string => {
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL.replace(/\/+$/, '');
  }
  if (typeof window !== 'undefined' && process.env.NODE_ENV === 'production') {
    return '/api/v1';
  }
  return 'http://127.0.0.1:8000/api/v1';
};

const API_BASE_URL = getBaseUrl();

export interface BillRecord {
  id: string;
  file_name: string;
  hospital_name?: string;
  invoice_number?: string;
  bill_date?: string;
  patient_identifier?: string;
  total_amount_claimed: number;
  total_amount_calculated: number;
  extraction_status: string;
  is_demo_sample: boolean;
  created_at: string;
}

export interface User {
  id: string;
  email: string;
  full_name?: string;
  is_active: boolean;
  is_demo: boolean;
  created_at: string;
}

export interface TriageResult {
  urgency_level: 'ROUTINE' | 'URGENT' | 'EMERGENCY';
  is_emergency: boolean;
  emergency_warning_signs: string[];
  identified_specialty: string;
  recommended_action_en: string;
  recommended_action_hi: string;
  candidate_procedure_code?: string;
  candidate_procedure_name?: string;
  confidence_score: number;
  safety_disclaimer: string;
}

export interface ReferenceRate {
  id: string;
  procedure_code: string;
  procedure_name: string;
  description?: string;
  specialty: string;
  scheme: string;
  facility_category: string;
  region: string;
  unit_basis: string;
  base_rate: number;
  min_rate: number;
  max_rate: number;
  effective_from: string;
  source_document: string;
  verification_status: 'VERIFIED_OFFICIAL' | 'UNVERIFIED_IMPORTED' | 'SYNTHETIC_DEMO';
  inclusion_notes?: string;
  exclusion_notes?: string;
  is_synthetic: boolean;
}

export interface Estimate {
  id: string;
  symptom_query: string;
  urgency_level: string;
  emergency_warning: boolean;
  identified_specialty: string;
  procedure_code?: string;
  procedure_name?: string;
  estimated_min_cost: number;
  estimated_max_cost: number;
  median_cost: number;
  triage_guidance_en: string;
  triage_guidance_hi?: string;
  reference_data?: ReferenceRate;
  benchmark_status: string;
  assumptions_and_limitations: string;
  disclaimer: string;
  created_at: string;
}

export interface BillLineItem {
  id?: string;
  line_number: number;
  raw_description: string;
  normalized_description: string;
  category: string;
  matched_procedure_code?: string;
  quantity: number;
  unit_price: number;
  line_total: number;
  extracted_line_total: number;
  is_package_component: boolean;
  ocr_confidence: number;
  user_edited: boolean;
}

export interface BillExtractionReview {
  bill_id: string;
  hospital_name?: string;
  invoice_number?: string;
  bill_date?: string;
  patient_identifier?: string;
  total_claimed: number;
  total_calculated: number;
  line_items_count: number;
  line_items: BillLineItem[];
  raw_ocr_preview?: string;
}

export interface AuditFinding {
  id: string;
  rule_type: string;
  finding_status: string;
  severity: 'HIGH' | 'MEDIUM' | 'LOW' | 'INFO';
  line_number?: number;
  item_description: string;
  observed_value: string;
  expected_value: string;
  monetary_difference: number;
  explanation: string;
  evidence_source: string;
  recommended_action: string;
  reference_rate_id?: string;
  created_at: string;
}

export interface AuditRun {
  id: string;
  bill_id: string;
  run_timestamp: string;
  total_line_items_audited: number;
  discrepancies_count: number;
  total_claimed_amount: number;
  total_verified_amount: number;
  total_potential_discrepancy_amount: number;
  overall_status: string;
  summary_notes?: string;
  findings: AuditFinding[];
}

export interface DashboardSummary {
  total_estimates_created: number;
  total_bills_uploaded: number;
  total_audits_completed: number;
  total_discrepancies_identified: number;
  total_potential_savings_identified: number;
  recent_activities: Array<{
    id: string;
    type: string;
    title: string;
    description: string;
    timestamp: string;
    status: string;
    amount?: number;
    discrepancy_amount?: number;
  }>;
  is_demo_data: boolean;
}

export function getAuthToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('medsure_token') || sessionStorage.getItem('medsure_token');
}

export function setAuthToken(token: string, persist: boolean = true) {
  if (typeof window === 'undefined') return;
  if (persist) {
    localStorage.setItem('medsure_token', token);
  } else {
    sessionStorage.setItem('medsure_token', token);
  }
}

export function clearAuthToken() {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('medsure_token');
  sessionStorage.removeItem('medsure_token');
}

function getAuthHeaders(additionalHeaders: Record<string, string> = {}): Record<string, string> {
  const headers: Record<string, string> = { ...additionalHeaders };
  const token = getAuthToken();
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
}

export const api = {
  async getDashboardSummary(): Promise<DashboardSummary> {
    const res = await fetch(`${API_BASE_URL}/dashboard/summary`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch dashboard summary');
    return res.json();
  },

  async assessSymptoms(description: string, language: string = 'en'): Promise<TriageResult> {
    const res = await fetch(`${API_BASE_URL}/triage/assess`, {
      method: 'POST',
      headers: getAuthHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({ symptom_description: description, preferred_language: language }),
    });
    if (!res.ok) throw new Error('Triage assessment failed');
    return res.json();
  },

  async createEstimate(params: {
    symptom_description: string;
    procedure_code?: string;
    scheme?: string;
    facility_category?: string;
    region?: string;
    preferred_language?: string;
  }): Promise<Estimate> {
    const res = await fetch(`${API_BASE_URL}/estimates`, {
      method: 'POST',
      headers: getAuthHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify(params),
    });
    if (!res.ok) throw new Error('Failed to create estimate');
    return res.json();
  },

  async getEstimates(): Promise<Estimate[]> {
    const res = await fetch(`${API_BASE_URL}/estimates`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch estimates');
    return res.json();
  },

  async uploadBill(file: File): Promise<BillExtractionReview> {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE_URL}/bills/upload`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: formData,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Bill upload failed');
    }
    return res.json();
  },

  async getBillExtraction(billId: string): Promise<BillExtractionReview> {
    const res = await fetch(`${API_BASE_URL}/bills/${billId}/extraction`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch bill extraction');
    return res.json();
  },

  async updateBillLineItems(billId: string, items: BillLineItem[]): Promise<BillExtractionReview> {
    const res = await fetch(`${API_BASE_URL}/bills/${billId}/line-items`, {
      method: 'PATCH',
      headers: getAuthHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({ items }),
    });
    if (!res.ok) throw new Error('Failed to update line items');
    return res.json();
  },

  async runAudit(billId: string, params?: { scheme?: string; facility_category?: string; region?: string }): Promise<AuditRun> {
    const res = await fetch(`${API_BASE_URL}/bills/${billId}/audit`, {
      method: 'POST',
      headers: getAuthHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify(params || {}),
    });
    if (!res.ok) throw new Error('Failed to run audit');
    return res.json();
  },

  async getAudit(auditId: string): Promise<AuditRun> {
    const res = await fetch(`${API_BASE_URL}/audits/${auditId}`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch audit');
    return res.json();
  },

  async getAuditFindings(auditId: string): Promise<AuditFinding[]> {
    const res = await fetch(`${API_BASE_URL}/audits/${auditId}/findings`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch audit findings');
    return res.json();
  },

  async getDisputeLetter(auditId: string): Promise<{ dispute_letter: string; hospital_name: string; invoice_number: string }> {
    const res = await fetch(`${API_BASE_URL}/audits/${auditId}/dispute-letter`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch dispute letter');
    return res.json();
  },

  getReportPdfUrl(auditId: string): string {
    return `${API_BASE_URL}/audits/${auditId}/report`;
  },

  async getReferenceRates(params?: { specialty?: string; scheme?: string; search?: string }): Promise<ReferenceRate[]> {
    const searchParams = new URLSearchParams();
    if (params?.specialty) searchParams.set('specialty', params.specialty);
    if (params?.scheme) searchParams.set('scheme', params.scheme);
    if (params?.search) searchParams.set('search', params.search);
    const res = await fetch(`${API_BASE_URL}/reference-rates?${searchParams.toString()}`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch reference rates');
    return res.json();
  },

  async getBills(): Promise<BillRecord[]> {
    const res = await fetch(`${API_BASE_URL}/bills`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch bills');
    return res.json();
  }
};
