import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCustomerStore } from '../store/customerStore';
import { Button } from '@mini-roda/ui';
import './CustomerList.css';

export const CustomerList = () => {
  const navigate = useNavigate();
  const { customers, loading, error, fetchCustomers } = useCustomerStore();

  useEffect(() => {
    fetchCustomers();
  }, [fetchCustomers]);

  if (loading && customers.length === 0) {
    return <div className="loading">Cargando clientes...</div>;
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  return (
    <div className="customer-list">
      <div className="customer-list-header">
        <h2>Lista de Clientes</h2>
        <Button onClick={() => navigate('/customers/new')}>
          Nuevo Cliente
        </Button>
      </div>

      {customers.length === 0 ? (
        <div className="empty-state">
          <p>No hay clientes registrados</p>
          <Button onClick={() => navigate('/customers/new')}>
            Crear Primer Cliente
          </Button>
        </div>
      ) : (
        <div className="customer-grid">
          {customers.map((customer) => (
            <div
              key={customer.id}
              className="customer-card"
              onClick={() => navigate(`/customers/${customer.id}`)}
            >
              <div className="customer-card-header">
                <h3>{customer.name}</h3>
                <span className="customer-id">#{customer.id}</span>
              </div>
              <div className="customer-card-body">
                <p className="customer-email">{customer.email}</p>
                {customer.phone && (
                  <p className="customer-phone">{customer.phone}</p>
                )}
                <p className="customer-date">
                  Creado: {new Date(customer.created_at).toLocaleDateString()}
                </p>
              </div>
              <div className="customer-card-actions">
                <Button
                  variant="secondary"
                  size="small"
                  onClick={(e) => {
                    e.stopPropagation();
                    navigate(`/customers/${customer.id}`);
                  }}
                >
                  Ver Detalles
                </Button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CustomerList;


