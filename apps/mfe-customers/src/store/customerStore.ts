import { create } from 'zustand';
import type { Customer, CustomerCreate } from '../types/customer';
import { customersApi, loansApi } from '../services/api';
import type { LoanRequest } from '../types/customer';

interface CustomerState {
  customers: Customer[];
  selectedCustomer: Customer | null;
  loading: boolean;
  error: string | null;
  fetchCustomers: () => Promise<void>;
  fetchCustomer: (id: number) => Promise<void>;
  createCustomer: (data: CustomerCreate) => Promise<void>;
  selectCustomer: (customer: Customer | null) => void;
  startLoanRequest: (customerId: number, loanData: Omit<LoanRequest, 'customer_id'>) => Promise<unknown>;
  clearError: () => void;
}

export const useCustomerStore = create<CustomerState>((set) => ({
  customers: [],
  selectedCustomer: null,
  loading: false,
  error: null,

  fetchCustomers: async () => {
    set({ loading: true, error: null });
    try {
      const customers = await customersApi.getAll();
      // Ensure customers is always an array
      const customersArray = Array.isArray(customers) ? customers : [];
      set({ customers: customersArray, loading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Error al cargar clientes',
        loading: false,
        customers: [], // Reset to empty array on error
      });
    }
  },

  fetchCustomer: async (id: number) => {
    set({ loading: true, error: null });
    try {
      const customer = await customersApi.getById(id);
      set({ selectedCustomer: customer, loading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Error al cargar cliente',
        loading: false,
      });
    }
  },

  createCustomer: async (data: CustomerCreate) => {
    set({ loading: true, error: null });
    try {
      const newCustomer = await customersApi.create(data);
      set((state) => ({
        customers: [...state.customers, newCustomer],
        loading: false,
      }));
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Error al crear cliente',
        loading: false,
      });
      throw error;
    }
  },

  selectCustomer: (customer: Customer | null) => {
    set({ selectedCustomer: customer });
  },

  startLoanRequest: async (customerId: number, loanData: Omit<LoanRequest, 'customer_id'>) => {
    set({ loading: true, error: null });
    try {
      const loan = await loansApi.createLoan({
        customer_id: customerId,
        ...loanData,
      });
      set({ loading: false });
      return loan;
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Error al crear préstamo',
        loading: false,
      });
      throw error;
    }
  },

  clearError: () => {
    set({ error: null });
  },
}));


