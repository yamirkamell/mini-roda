import { create } from 'zustand';
import type { Loan, PaymentSchedule, PaymentRegistration } from '../types/loan';
import { loansApi } from '../services/api';

interface LoanState {
  loans: Loan[];
  selectedLoan: Loan | null;
  paymentSchedule: PaymentSchedule[];
  loading: boolean;
  error: string | null;
  fetchLoans: (customerId?: number) => Promise<void>;
  fetchLoan: (id: number) => Promise<void>;
  approveLoan: (id: number) => Promise<void>;
  rejectLoan: (id: number, reason: string) => Promise<void>;
  fetchPaymentSchedule: (id: number) => Promise<void>;
  registerPayment: (loanId: number, data: PaymentRegistration) => Promise<void>;
  selectLoan: (loan: Loan | null) => void;
  clearError: () => void;
}

export const useLoanStore = create<LoanState>((set) => ({
  loans: [],
  selectedLoan: null,
  paymentSchedule: [],
  loading: false,
  error: null,

  fetchLoans: async (customerId?: number) => {
    set({ loading: true, error: null });
    try {
      const loans = await loansApi.getAll(customerId);
      // Ensure loans is always an array
      const loansArray = Array.isArray(loans) ? loans : [];
      set({ loans: loansArray, loading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Error al cargar préstamos',
        loading: false,
        loans: [], // Reset to empty array on error
      });
    }
  },

  fetchLoan: async (id: number) => {
    set({ loading: true, error: null });
    try {
      const loan = await loansApi.getById(id);
      set({ selectedLoan: loan, loading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Error al cargar préstamo',
        loading: false,
      });
    }
  },

  approveLoan: async (id: number) => {
    set({ loading: true, error: null });
    try {
      const approvedLoan = await loansApi.approve(id);
      set((state) => ({
        loans: state.loans.map((loan) => (loan.id === id ? approvedLoan : loan)),
        selectedLoan: state.selectedLoan?.id === id ? approvedLoan : state.selectedLoan,
        loading: false,
      }));
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Error al aprobar préstamo',
        loading: false,
      });
      throw error;
    }
  },

  rejectLoan: async (id: number, reason: string) => {
    set({ loading: true, error: null });
    try {
      const rejectedLoan = await loansApi.reject(id, reason);
      set((state) => ({
        loans: state.loans.map((loan) => (loan.id === id ? rejectedLoan : loan)),
        selectedLoan: state.selectedLoan?.id === id ? rejectedLoan : state.selectedLoan,
        loading: false,
      }));
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Error al rechazar préstamo',
        loading: false,
      });
      throw error;
    }
  },

  fetchPaymentSchedule: async (id: number) => {
    set({ loading: true, error: null });
    try {
      const schedule = await loansApi.getPaymentSchedule(id);
      set({ paymentSchedule: schedule, loading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Error al cargar cronograma',
        loading: false,
      });
    }
  },

  registerPayment: async (loanId: number, data: PaymentRegistration) => {
    set({ loading: true, error: null });
    try {
      const payment = await loansApi.registerPayment(loanId, data);
      set((state) => ({
        paymentSchedule: state.paymentSchedule.map((p) =>
          p.id === payment.id ? payment : p
        ),
        loading: false,
      }));
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Error al registrar pago',
        loading: false,
      });
      throw error;
    }
  },

  selectLoan: (loan: Loan | null) => {
    set({ selectedLoan: loan });
  },

  clearError: () => {
    set({ error: null });
  },
}));


