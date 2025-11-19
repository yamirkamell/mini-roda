import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useLoanStore } from '../store/loanStore';
import { Button } from '@mini-roda/ui';
import ApprovalActions from './ApprovalActions';
import PaymentSchedule from './PaymentSchedule';
import './LoanDetail.css';

export const LoanDetail = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { selectedLoan, loading, error, fetchLoan, fetchPaymentSchedule } = useLoanStore();
  const [activeTab, setActiveTab] = useState<'details' | 'schedule'>('details');

  useEffect(() => {
    if (id) {
      const loanId = Number.parseInt(id, 10);
      fetchLoan(loanId);
      if (selectedLoan?.status === 'approved') {
        fetchPaymentSchedule(loanId);
      }
    }
  }, [id, fetchLoan, fetchPaymentSchedule]);

  useEffect(() => {
    if (selectedLoan?.status === 'approved' && id) {
      fetchPaymentSchedule(Number.parseInt(id, 10));
    }
  }, [selectedLoan?.status, id, fetchPaymentSchedule]);

  if (loading && !selectedLoan) {
    return <div className="loading">Cargando préstamo...</div>;
  }

  if (error) {
    return (
      <div className="error">
        <p>Error: {error}</p>
        <Button onClick={() => navigate('/loans')}>Volver a la lista</Button>
      </div>
    );
  }

  if (!selectedLoan) {
    return (
      <div className="error">
        <p>Préstamo no encontrado</p>
        <Button onClick={() => navigate('/loans')}>Volver a la lista</Button>
      </div>
    );
  }

  return (
    <div className="loan-detail">
      <div className="loan-detail-header">
        <Button variant="secondary" onClick={() => navigate('/loans')}>
          ← Volver
        </Button>
        <h2>Detalles del Préstamo #{selectedLoan.id}</h2>
      </div>

      <div className="loan-detail-card">
        <div className="loan-detail-info">
          <div className="info-row">
            <span className="info-label">ID:</span>
            <span className="info-value">#{selectedLoan.id}</span>
          </div>
          <div className="info-row">
            <span className="info-label">Cliente ID:</span>
            <span className="info-value">{selectedLoan.customer_id}</span>
          </div>
          <div className="info-row">
            <span className="info-label">Monto:</span>
            <span className="info-value">${parseFloat(selectedLoan.amount).toLocaleString()}</span>
          </div>
          <div className="info-row">
            <span className="info-label">Tasa de Interés:</span>
            <span className="info-value">{selectedLoan.interest_rate}%</span>
          </div>
          <div className="info-row">
            <span className="info-label">Plazo:</span>
            <span className="info-value">{selectedLoan.term_months} meses</span>
          </div>
          <div className="info-row">
            <span className="info-label">Monto Total:</span>
            <span className="info-value">${parseFloat(selectedLoan.total_amount).toLocaleString()}</span>
          </div>
          <div className="info-row">
            <span className="info-label">Estado:</span>
            <span className={`info-value status-${selectedLoan.status}`}>
              {selectedLoan.status === 'pending' && 'Pendiente'}
              {selectedLoan.status === 'approved' && 'Aprobado'}
              {selectedLoan.status === 'rejected' && 'Rechazado'}
            </span>
          </div>
          <div className="info-row">
            <span className="info-label">Fecha de Creación:</span>
            <span className="info-value">
              {new Date(selectedLoan.created_at).toLocaleString()}
            </span>
          </div>
        </div>

        {selectedLoan.status === 'pending' && (
          <div className="loan-detail-actions">
            <ApprovalActions loanId={selectedLoan.id} />
          </div>
        )}

        {selectedLoan.status === 'approved' && (
          <div className="loan-tabs">
            <div className="tab-buttons">
              <button
                className={activeTab === 'details' ? 'active' : ''}
                onClick={() => setActiveTab('details')}
              >
                Detalles
              </button>
              <button
                className={activeTab === 'schedule' ? 'active' : ''}
                onClick={() => setActiveTab('schedule')}
              >
                Cronograma de Pagos
              </button>
            </div>
            <div className="tab-content">
              {activeTab === 'schedule' && id && (
                <PaymentSchedule loanId={Number.parseInt(id, 10)} />
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default LoanDetail;


