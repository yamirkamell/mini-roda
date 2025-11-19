import axios from 'axios';
import type { Loan, PaymentSchedule, PaymentRegistration } from '../types/loan';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 
  (typeof window !== 'undefined' ? window.location.origin : 'http://localhost');

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-API-Request': 'true', 
  },
});

export const loansApi = {
  getAll: async (customerId?: number): Promise<Loan[]> => {
    const params = customerId ? { customer_id: customerId } : {};
    const response = await api.get<Loan[]>('/api/v1/loans', { params });
    return response.data;
  },

  getById: async (id: number): Promise<Loan> => {
    const response = await api.get<Loan>(`/api/v1/loans/${id}`);
    return response.data;
  },

  approve: async (id: number): Promise<Loan> => {
    const response = await api.post<Loan>(`/api/v1/loans/${id}/approve`);
    return response.data;
  },

  reject: async (id: number, reason: string): Promise<Loan> => {
    const response = await api.post<Loan>(`/api/v1/loans/${id}/reject`, {
      reason,
    });
    return response.data;
  },

  getPaymentSchedule: async (id: number): Promise<PaymentSchedule[]> => {
    const response = await api.get<PaymentSchedule[]>(
      `/api/v1/loans/${id}/payment-schedule`
    );
    return response.data;
  },

  registerPayment: async (loanId: number, data: PaymentRegistration): Promise<PaymentSchedule> => {
    const response = await api.post<PaymentSchedule>(
      `/api/v1/loans/${loanId}/payments`,
      data
    );
    return response.data;
  },
};


