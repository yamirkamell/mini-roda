import { useEffect, useState } from 'react';
import { useLoanStore } from '../store/loanStore';
import { Button } from '@mini-roda/ui';
import type { PaymentRegistration } from '../types/loan';
import './PaymentSchedule.css';

export interface PaymentScheduleProps {
  loanId: number;
}

const PaymentSchedule = ({ loanId }: PaymentScheduleProps) => {
  const { paymentSchedule, loading, error, fetchPaymentSchedule, registerPayment } =
    useLoanStore();
  const [showPaymentForm, setShowPaymentForm] = useState(false);
  const [selectedPaymentId, setSelectedPaymentId] = useState<number | null>(null);
  const [paymentData, setPaymentData] = useState<PaymentRegistration>({
    amount: '',
    paid_date: new Date().toISOString().split('T')[0] || '',
  });
  const [showSuccessModal, setShowSuccessModal] = useState(false);

  useEffect(() => {
    fetchPaymentSchedule(loanId);
  }, [loanId, fetchPaymentSchedule]);

  const handlePaymentClick = (paymentId: number, amount: string) => {
    setSelectedPaymentId(paymentId);
    setPaymentData({
      amount,
      paid_date: new Date().toISOString().split('T')[0] || '',
    });
    setShowPaymentForm(true);
  };

  const handlePaymentSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedPaymentId) return;

    try {
      const paidDate = paymentData.paid_date
        ? new Date(paymentData.paid_date + 'T00:00:00').toISOString()
        : new Date().toISOString();

      await registerPayment(loanId, {
        amount: paymentData.amount,
        paid_date: paidDate,
      });
      setShowPaymentForm(false);
      setSelectedPaymentId(null);
      setShowSuccessModal(true);
      fetchPaymentSchedule(loanId);
    } catch (err) {
      // Error is handled by the store
    }
  };

  if (loading && paymentSchedule.length === 0) {
    return <div className="loading">Cargando cronograma...</div>;
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  const paidCount = paymentSchedule.filter((p) => p.paid).length;
  const totalCount = paymentSchedule.length;
  const totalPaid = paymentSchedule
    .filter((p) => p.paid)
    .reduce((sum, p) => sum + parseFloat(p.amount), 0);
  const totalAmount = paymentSchedule.reduce((sum, p) => sum + parseFloat(p.amount), 0);

  return (
    <div className="payment-schedule">
      <div className="payment-schedule-header">
        <h3>Cronograma de Pagos</h3>
        <div className="payment-summary">
          <span>
            Pagos: {paidCount} / {totalCount}
          </span>
          <span>
            Pagado: ${totalPaid.toLocaleString()} / ${totalAmount.toLocaleString()}
          </span>
        </div>
      </div>

      {paymentSchedule.length === 0 ? (
        <div className="empty-state">No hay pagos programados</div>
      ) : (
        <>
          <div className="payment-table-container">
            <table className="payment-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Fecha de Vencimiento</th>
                  <th>Monto</th>
                  <th>Estado</th>
                  <th>Fecha de Pago</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {paymentSchedule.map((payment, index) => (
                  <tr key={payment.id} className={payment.paid ? 'paid' : 'unpaid'}>
                    <td>{index + 1}</td>
                    <td>{new Date(payment.due_date).toLocaleDateString()}</td>
                    <td>${parseFloat(payment.amount).toLocaleString()}</td>
                    <td>
                      <span className={`payment-status ${payment.paid ? 'paid' : 'unpaid'}`}>
                        {payment.paid ? 'Pagado' : 'Pendiente'}
                      </span>
                    </td>
                    <td>
                      {payment.paid_date
                        ? new Date(payment.paid_date).toLocaleDateString()
                        : '-'}
                    </td>
                    <td>
                      {!payment.paid && (
                        <Button
                          size="small"
                          onClick={() => handlePaymentClick(payment.id, payment.amount)}
                        >
                          Registrar Pago
                        </Button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {showPaymentForm && (
            <div className="payment-form-modal">
              <div className="payment-form-content">
                <h4>Registrar Pago</h4>
                <form onSubmit={handlePaymentSubmit}>
                  <div className="form-group">
                    <label htmlFor="payment-amount">
                      Monto <span className="required">*</span>
                    </label>
                    <input
                      id="payment-amount"
                      type="number"
                      step="0.01"
                      min="0"
                      value={paymentData.amount}
                      onChange={(e) =>
                        setPaymentData({ ...paymentData, amount: e.target.value })
                      }
                      required
                      disabled={loading}
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="payment-date">
                      Fecha de Pago <span className="required">*</span>
                    </label>
                    <input
                      id="payment-date"
                      type="date"
                      value={paymentData.paid_date}
                      onChange={(e) =>
                        setPaymentData({ ...paymentData, paid_date: e.target.value })
                      }
                      required
                      disabled={loading}
                    />
                  </div>

                  {error && <div className="form-error">{error}</div>}

                  <div className="form-actions">
                    <Button
                      type="button"
                      variant="secondary"
                      onClick={() => {
                        setShowPaymentForm(false);
                        setSelectedPaymentId(null);
                      }}
                      disabled={loading}
                    >
                      Cancelar
                    </Button>
                    <Button type="submit" disabled={loading}>
                      {loading ? 'Registrando...' : 'Registrar Pago'}
                    </Button>
                  </div>
                </form>
              </div>
            </div>
          )}
        </>
      )}

      {showSuccessModal && (
        <div className="payment-form-modal" onClick={() => setShowSuccessModal(false)}>
          <div className="payment-form-content" onClick={(e) => e.stopPropagation()}>
            <h4>¡Éxito!</h4>
            <p>Pago registrado exitosamente</p>
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

export default PaymentSchedule;


