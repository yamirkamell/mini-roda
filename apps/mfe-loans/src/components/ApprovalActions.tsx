import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLoanStore } from '../store/loanStore';
import { Button } from '@mini-roda/ui';
import './ApprovalActions.css';

export interface ApprovalActionsProps {
  loanId: number;
}

const ApprovalActions = ({ loanId }: ApprovalActionsProps) => {
  const navigate = useNavigate();
  const { approveLoan, rejectLoan, loading, error, clearError } = useLoanStore();
  const [showRejectForm, setShowRejectForm] = useState(false);
  const [rejectReason, setRejectReason] = useState('');
  const [showConfirmApprove, setShowConfirmApprove] = useState(false);
  const [showSuccessModal, setShowSuccessModal] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [showErrorModal, setShowErrorModal] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleApprove = () => {
    setShowConfirmApprove(true);
  };

  const confirmApprove = async () => {
    setShowConfirmApprove(false);
    try {
      await approveLoan(loanId);
      setSuccessMessage('Préstamo aprobado exitosamente');
      setShowSuccessModal(true);
      setTimeout(() => {
        navigate('/loans');
      }, 1500);
    } catch (err) {
      // Error is handled by the store
    }
  };

  const handleReject = async (e: React.FormEvent) => {
    e.preventDefault();
    clearError();

    if (!rejectReason.trim()) {
      setErrorMessage('Por favor, proporcione una razón para el rechazo');
      setShowErrorModal(true);
      return;
    }

    try {
      await rejectLoan(loanId, rejectReason);
      setSuccessMessage('Préstamo rechazado exitosamente');
      setShowSuccessModal(true);
      setShowRejectForm(false);
      setRejectReason('');
      setTimeout(() => {
        navigate('/loans');
      }, 1500);
    } catch (err) {
      // Error is handled by the store
    }
  };

  return (
    <div className="approval-actions">
      <h3>Acciones de Aprobación</h3>
      {error && <div className="error-message">{error}</div>}
      
      <div className="approval-buttons">
        <Button variant="primary" onClick={handleApprove} disabled={loading || showRejectForm}>
          {loading ? 'Procesando...' : 'Aprobar Préstamo'}
        </Button>
        <Button
          variant="danger"
          onClick={() => {
            setShowRejectForm(!showRejectForm);
            clearError();
          }}
          disabled={loading}
        >
          {showRejectForm ? 'Cancelar' : 'Rechazar Préstamo'}
        </Button>
      </div>

      {showRejectForm && (
        <form className="reject-form" onSubmit={handleReject}>
          <div className="form-group">
            <label htmlFor="reject-reason">
              Razón del Rechazo <span className="required">*</span>
            </label>
            <textarea
              id="reject-reason"
              value={rejectReason}
              onChange={(e) => setRejectReason(e.target.value)}
              rows={4}
              required
              disabled={loading}
              placeholder="Ingrese la razón del rechazo..."
            />
          </div>
          <div className="form-actions">
            <Button
              type="button"
              variant="secondary"
              onClick={() => {
                setShowRejectForm(false);
                setRejectReason('');
              }}
              disabled={loading}
            >
              Cancelar
            </Button>
            <Button type="submit" variant="danger" disabled={loading || !rejectReason.trim()}>
              {loading ? 'Procesando...' : 'Confirmar Rechazo'}
            </Button>
          </div>
        </form>
      )}

      {showConfirmApprove && (
        <div className="payment-form-modal" onClick={() => setShowConfirmApprove(false)}>
          <div className="payment-form-content" onClick={(e) => e.stopPropagation()}>
            <h4>Confirmar Aprobación</h4>
            <p>¿Está seguro de aprobar este préstamo?</p>
            <div className="form-actions">
              <Button variant="secondary" onClick={() => setShowConfirmApprove(false)} size="medium">
                Cancelar
              </Button>
              <Button onClick={confirmApprove} disabled={loading} size="medium">
                {loading ? 'Procesando...' : 'Confirmar'}
              </Button>
            </div>
          </div>
        </div>
      )}

      {showSuccessModal && (
        <div className="payment-form-modal" onClick={() => setShowSuccessModal(false)}>
          <div className="payment-form-content" onClick={(e) => e.stopPropagation()}>
            <h4>¡Éxito!</h4>
            <p>{successMessage}</p>
            <div className="form-actions">
              <Button onClick={() => setShowSuccessModal(false)} size="medium">
                Aceptar
              </Button>
            </div>
          </div>
        </div>
      )}

      {showErrorModal && (
        <div className="payment-form-modal" onClick={() => setShowErrorModal(false)}>
          <div className="payment-form-content" onClick={(e) => e.stopPropagation()}>
            <h4>Error</h4>
            <p>{errorMessage}</p>
            <div className="form-actions">
              <Button onClick={() => setShowErrorModal(false)} size="medium">
                Aceptar
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ApprovalActions;


