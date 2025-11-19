export interface Customer {
  id: number;
  name: string;
  email: string;
  phone: string | null;
  created_at: string;
}

export interface CustomerCreate {
  name: string;
  email: string;
  phone?: string;
}

export interface LoanRequest {
  customer_id: number;
  amount: string;
  interest_rate: string;
  term_months: number;
}


