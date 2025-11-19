import axios from 'axios';
import type { Customer, CustomerCreate, LoanRequest } from '../types/customer';


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

export const customersApi = {
  getAll: async (): Promise<Customer[]> => {
    const response = await api.get<Customer[]>('/api/v1/customers');
    return response.data;
  },

  getById: async (id: number): Promise<Customer> => {
    const response = await api.get<Customer>(`/api/v1/customers/${id}`);
    return response.data;
  },

  create: async (data: CustomerCreate): Promise<Customer> => {
    const response = await api.post<Customer>('/api/v1/customers', data);
    return response.data;
  },
};

export const loansApi = {
  createLoan: async (data: LoanRequest): Promise<unknown> => {
    const response = await api.post('/api/v1/loans', data);
    return response.data;
  },
};


