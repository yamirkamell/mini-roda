import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLoanStore } from '../store/loanStore';
import { Button } from '@mini-roda/ui';
import './LoanList.css';

export const LoanList = () => {
  const navigate = useNavigate();
  const { loans, loading, error, fetchLoans } = useLoanStore();

  useEffect(() => {
    fetchLoans();
  }, [fetchLoans]);

  const getStatusBadge = (status: string) => {
    const statusClasses = {
      pending: 'status-pending',
      approved: 'status-approved',
      rejected: 'status-rejected',
    };
    return (
      <span className={`status-badge ${statusClasses[status as keyof typeof statusClasses] || ''}`}>
        {status === 'pending' && 'Pendiente'}
        {status === 'approved' && 'Aprobado'}
        {status === 'rejected' && 'Rechazado'}
      </span>
    );
  };

  if (loading && loans.length === 0) {
    return <div className="loading">Cargando préstamos...</div>;
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  return (
    <div className="loan-list">
      <div className="loan-list-header">
        <h2>Lista de Préstamos</h2>
        <Button onClick={() => fetchLoans()}>Actualizar</Button>
      </div>

      {loans.length === 0 ? (
        <div className="empty-state">
          <p>No hay préstamos registrados</p>
        </div>
      ) : (
        <div className="loan-table-container">
          <table className="loan-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Cliente ID</th>
                <th>Monto</th>
                <th>Tasa de Interés</th>
                <th>Plazo (meses)</th>
                <th>Monto Total</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {loans.map((loan) => (
                <tr key={loan.id}>
                  <td>#{loan.id}</td>
                  <td>{loan.customer_id}</td>
                  <td>${parseFloat(loan.amount).toLocaleString()}</td>
                  <td>{loan.interest_rate}%</td>
                  <td>{loan.term_months}</td>
                  <td>${parseFloat(loan.total_amount).toLocaleString()}</td>
                  <td>{getStatusBadge(loan.status)}</td>
                  <td>
                    <div className="loan-actions">
                      <Button
                        variant="secondary"
                        size="small"
                        onClick={() => navigate(`/loans/${loan.id}`)}
                      >
                        Ver
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default LoanList;


