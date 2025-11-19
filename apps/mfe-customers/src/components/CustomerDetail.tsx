import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useCustomerStore } from '../store/customerStore';
import { Button } from '@mini-roda/ui';
import './CustomerDetail.css';

export const CustomerDetail = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { selectedCustomer, loading, error, fetchCustomer, startLoanRequest } =
    useCustomerStore();
  const [showLoanForm, setShowLoanForm] = useState(false);
  const [loanData, setLoanData] = useState({
    amount: '',
    interest_rate: '',
    term_months: 12,
  });
  const [loanLoading, setLoanLoading] = useState(false);
  const [showSuccessModal, setShowSuccessModal] = useState(false);

  useEffect(() => {
    if (id) {
      fetchCustomer(Number.parseInt(id, 10));
    }
  }, [id, fetchCustomer]);

  const handleLoanSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!id || !selectedCustomer) return;

    setLoanLoading(true);
    try {
      await startLoanRequest(selectedCustomer.id, {
        amount: loanData.amount,
        interest_rate: loanData.interest_rate,
        term_months: loanData.term_months,
      });
      setShowLoanForm(false);
      setLoanData({ amount: '', interest_rate: '', term_months: 12 });
      setShowSuccessModal(true);
    } catch (err) {
      // Error is handled by the store
    } finally {
      setLoanLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Cargando cliente...</div>;
  }

  if (error) {
    return (
      <div className="error">
        <p>Error: {error}</p>
        <Button onClick={() => navigate('/customers')}>Volver a la lista</Button>
      </div>
    );
  }

  if (!selectedCustomer) {
    return (
      <div className="error">
        <p>Cliente no encontrado</p>
        <Button onClick={() => navigate('/customers')}>Volver a la lista</Button>
      </div>
    );
  }

  return (
    <div className="customer-detail">
      <div className="customer-detail-header">
        <Button variant="secondary" onClick={() => navigate('/customers')}>
          ← Volver
        </Button>
        <h2>Detalles del Cliente</h2>
      </div>

      <div className="customer-detail-card">
        <div className="customer-detail-info">
          <div className="info-row">
            <span className="info-label">ID:</span>
            <span className="info-value">#{selectedCustomer.id}</span>
          </div>
          <div className="info-row">
            <span className="info-label">Nombre:</span>
            <span className="info-value">{selectedCustomer.name}</span>
          </div>
          <div className="info-row">
            <span className="info-label">Email:</span>
            <span className="info-value">{selectedCustomer.email}</span>
          </div>
          {selectedCustomer.phone && (
            <div className="info-row">
              <span className="info-label">Teléfono:</span>
              <span className="info-value">{selectedCustomer.phone}</span>
            </div>
          )}
          <div className="info-row">
            <span className="info-label">Fecha de Creación:</span>
            <span className="info-value">
              {new Date(selectedCustomer.created_at).toLocaleString()}
            </span>
          </div>
        </div>

        <div className="customer-detail-actions">
          <Button
            variant="primary"
            onClick={() => setShowLoanForm(!showLoanForm)}
          >
            {showLoanForm ? 'Cancelar Solicitud' : 'Solicitar Préstamo'}
          </Button>
        </div>

        {showLoanForm && (
          <div className="loan-form-section">
            <h3>Solicitar Préstamo</h3>
            <form onSubmit={handleLoanSubmit}>
              <div className="form-group">
                <label htmlFor="amount">
                  Monto <span className="required">*</span>
                </label>
                <input
                  id="amount"
                  type="number"
                  step="0.01"
                  min="0"
                  value={loanData.amount}
                  onChange={(e) =>
                    setLoanData({ ...loanData, amount: e.target.value })
                  }
                  required
                  disabled={loanLoading}
                  placeholder="10000.00"
                />
              </div>

              <div className="form-group">
                <label htmlFor="interest_rate">
                  Tasa de Interés (%) <span className="required">*</span>
                </label>
                <input
                  id="interest_rate"
                  type="number"
                  step="0.01"
                  min="0"
                  max="100"
                  value={loanData.interest_rate}
                  onChange={(e) =>
                    setLoanData({ ...loanData, interest_rate: e.target.value })
                  }
                  required
                  disabled={loanLoading}
                  placeholder="5.5"
                />
              </div>

              <div className="form-group">
                <label htmlFor="term_months">
                  Plazo (meses) <span className="required">*</span>
                </label>
                <input
                  id="term_months"
                  type="number"
                  min="1"
                  max="360"
                  value={loanData.term_months}
                  onChange={(e) =>
                    setLoanData({
                      ...loanData,
                      term_months: Number.parseInt(e.target.value, 10),
                    })
                  }
                  required
                  disabled={loanLoading}
                />
              </div>

              <div className="form-actions">
                <Button
                  type="button"
                  variant="secondary"
                  onClick={() => setShowLoanForm(false)}
                  disabled={loanLoading}
                >
                  Cancelar
                </Button>
                <Button type="submit" disabled={loanLoading}>
                  {loanLoading ? 'Enviando...' : 'Enviar Solicitud'}
                </Button>
              </div>
            </form>
          </div>
        )}
      </div>

      {showSuccessModal && (
        <div className="payment-form-modal" onClick={() => setShowSuccessModal(false)}>
          <div className="payment-form-content" onClick={(e) => e.stopPropagation()}>
            <h4>¡Éxito!</h4>
            <p>Solicitud de préstamo creada exitosamente</p>
            <div className="form-actions">
              <Button onClick={() => setShowSuccessModal(false)} size="medium">
                Aceptar
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CustomerDetail;


