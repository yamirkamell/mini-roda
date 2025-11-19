import { useState, FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCustomerStore } from '../store/customerStore';
import { Button } from '@mini-roda/ui';
import type { CustomerCreate } from '../types/customer';
import './CustomerForm.css';

export interface CustomerFormProps {
  initialData?: Partial<CustomerCreate>;
  onSubmit?: (data: CustomerCreate) => void;
}

export const CustomerForm = ({ initialData, onSubmit }: CustomerFormProps) => {
  const navigate = useNavigate();
  const { createCustomer, loading, error, clearError } = useCustomerStore();
  const [formData, setFormData] = useState<CustomerCreate>({
    name: initialData?.name || '',
    email: initialData?.email || '',
    phone: initialData?.phone || '',
  });
  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({});

  const validate = (): boolean => {
    const errors: Record<string, string> = {};

    if (!formData.name.trim()) {
      errors.name = 'El nombre es requerido';
    }

    if (!formData.email.trim()) {
      errors.email = 'El email es requerido';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      errors.email = 'El email no es válido';
    }

    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    clearError();

    if (!validate()) {
      return;
    }

    try {
      if (onSubmit) {
        onSubmit(formData);
      } else {
        await createCustomer(formData);
        navigate('/customers');
      }
    } catch (err) {
      // Error is handled by the store
    }
  };

  const handleChange = (field: keyof CustomerCreate) => (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    setFormData((prev) => ({ ...prev, [field]: e.target.value }));
    if (validationErrors[field]) {
      setValidationErrors((prev) => {
        const newErrors = { ...prev };
        delete newErrors[field];
        return newErrors;
      });
    }
  };

  return (
    <div className="customer-form">
      <h2>Nuevo Cliente</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">
            Nombre <span className="required">*</span>
          </label>
          <input
            id="name"
            type="text"
            value={formData.name}
            onChange={handleChange('name')}
            className={validationErrors.name ? 'error' : ''}
            disabled={loading}
          />
          {validationErrors.name && (
            <span className="error-message">{validationErrors.name}</span>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="email">
            Email <span className="required">*</span>
          </label>
          <input
            id="email"
            type="email"
            value={formData.email}
            onChange={handleChange('email')}
            className={validationErrors.email ? 'error' : ''}
            disabled={loading}
          />
          {validationErrors.email && (
            <span className="error-message">{validationErrors.email}</span>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="phone">Teléfono</label>
          <input
            id="phone"
            type="tel"
            value={formData.phone || ''}
            onChange={handleChange('phone')}
            disabled={loading}
            placeholder="Opcional"
          />
        </div>

        {error && <div className="form-error">{error}</div>}

        <div className="form-actions">
          <Button
            type="button"
            variant="secondary"
            onClick={() => navigate('/customers')}
            disabled={loading}
          >
            Cancelar
          </Button>
          <Button type="submit" disabled={loading}>
            {loading ? 'Guardando...' : 'Guardar Cliente'}
          </Button>
        </div>
      </form>
    </div>
  );
};

export default CustomerForm;


