export interface Loan {
  id: number;
  customer_id: number;
  amount: string;
  interest_rate: string;
  term_months: number;
  total_amount: string;
  status: 'pending' | 'approved' | 'rejected';
  created_at: string;
}

export interface PaymentSchedule {
  id: number;
  loan_id: number;
  due_date: string;
  amount: string;
  paid: boolean;
  paid_date: string | null;
}

export interface LoanReject {
  reason: string;
}

export interface PaymentRegistration {
  amount: string;
  paid_date: string;
}


