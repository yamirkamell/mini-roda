import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import LoanList from './components/LoanList';
import LoanDetail from './components/LoanDetail';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <header className="app-header">
          <h1>Loans Microfrontend</h1>
          <p>Gestión de préstamos</p>
        </header>
        <main className="app-main">
          <Routes>
            <Route path="/loans" element={<LoanList />} />
            <Route path="/loans/:id" element={<LoanDetail />} />
            <Route path="/" element={<Navigate to="/loans" replace />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
