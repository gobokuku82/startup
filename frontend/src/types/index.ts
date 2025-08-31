// User and Authentication Types
export interface User {
  id: number;
  email: string;
  role: 'admin' | 'manager' | 'rep';
  department: string;
  is_active: boolean;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

// Client Types
export interface Client {
  id: number;
  name: string;
  type: 'hospital' | 'clinic' | 'pharmacy';
  address: string;
  owner_user_id: number;
  tier: 'platinum' | 'gold' | 'silver';
  phone?: string;
  email?: string;
  created_at: string;
  updated_at: string;
}

// Product Types
export interface Product {
  id: number;
  code: string;
  name: string;
  category: string;
  unit_price: number;
  description?: string;
  is_active: boolean;
}

// Sales Types
export interface Sales {
  id: number;
  client_id: number;
  product_id: number;
  rep_user_id: number;
  yyyymm: string;
  quantity: number;
  revenue: number;
  target?: number;
}

// Analytics Types
export interface KPISummary {
  total_revenue: number;
  total_quantity: number;
  num_clients: number;
  avg_deal_size: number;
  yoy_growth?: number;
  ytd_achievement?: number;
  target_achievement_rate?: number;
}

export interface AnalyticsData {
  kpi_summary: KPISummary;
  sales_by_client: Array<{
    client_id: number;
    client_name: string;
    revenue: number;
    quantity: number;
    growth_rate: number;
  }>;
  sales_by_product: Array<{
    product_code: string;
    product_name: string;
    revenue: number;
    quantity: number;
    market_share: number;
  }>;
  trends?: {
    revenue_trend: string;
    growth_areas: string[];
    declining_areas: string[];
  };
}

// Document Types
export interface Document {
  id: number;
  doc_type: 'visit_report' | 'proposal' | 'application';
  client_id?: number;
  user_id: number;
  status: 'draft' | 'reviewing' | 'approved' | 'archived';
  current_version: number;
  storage_uri?: string;
  doc_metadata?: any;
  created_at: string;
  updated_at: string;
}

// Compliance Types
export interface ComplianceCheck {
  id: number;
  document_id: number;
  version: number;
  status: 'green' | 'yellow' | 'red' | 'inconclusive';
  violations?: Array<{
    rule: string;
    severity: string;
    description: string;
    suggestion: string;
  }>;
  citations?: Array<{
    source: string;
    page: number;
    excerpt: string;
    relevance: number;
  }>;
  suggestions?: Array<{
    type: string;
    action: string;
    reference: string;
  }>;
}

// Workflow Types
export interface WorkflowRequest {
  query: string;
  context?: Record<string, any>;
  product_codes?: string[];
  client_ids?: number[];
  period?: {
    start: string;
    end: string;
  };
}

export interface WorkflowResponse {
  result: any;
  artifacts: Record<string, any>;
  session_id: string;
  status: string;
  messages?: Array<{
    role: string;
    content: string;
  }>;
}

// Event Types
export interface Event {
  id: number;
  user_id: number;
  client_id?: number;
  title: string;
  starts_at: string;
  ends_at: string;
  location?: string;
  description?: string;
  source: 'internal' | 'google' | 'outlook';
  status: 'confirmed' | 'tentative' | 'cancelled';
}