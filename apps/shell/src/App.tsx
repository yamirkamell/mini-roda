import { lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route, Navigate, NavLink } from 'react-router-dom';
import './App.css';

const CustomerList = lazy(() => import('mfe_customers/CustomerList'));
const CustomerDetail = lazy(() => import('mfe_customers/CustomerDetail'));
const LoanList = lazy(() => import('mfe_loans/LoanList'));
const LoanDetail = lazy(() => import('mfe_loans/LoanDetail'));

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <header className="app-header">
          <div className="container">
            <h1 className="app-title">Mini-Roda</h1>
            <nav className="app-nav">
              <NavLink
                to="/customers"
                className={({ isActive }) =>
                  isActive ? 'nav-link active' : 'nav-link'
                }
              >
                Clientes
              </NavLink>
              <NavLink
                to="/loans"
                className={({ isActive }) =>
                  isActive ? 'nav-link active' : 'nav-link'
                }
              >
                Préstamos
              </NavLink>
            </nav>
          </div>
        </header>

        <main className="app-main">
          <div className="container">
            <Suspense fallback={<div className="loading">Cargando...</div>}>
              <Routes>
                <Route path="/" element={<Navigate to="/customers" replace />} />
                
                {/* Microfrontend Customers */}
                <Route path="/customers" element={<CustomerList />} />
                <Route path="/customers/:id" element={<CustomerDetail />} />
                
                {/* Microfrontend Loans */}
                <Route path="/loans" element={<LoanList />} />
                <Route path="/loans/:id" element={<LoanDetail />} />
                
                <Route path="*" element={<div className="error">Página no encontrada</div>} />
              </Routes>
            </Suspense>
          </div>
        </main>

        <footer className="app-footer">
          <div className="container">
            <p>&copy; 2024 Mini-Roda - Sistema de Financiamiento</p>
          </div>
        </footer>
      </div>
    </BrowserRouter>
  );
}

export default App;

