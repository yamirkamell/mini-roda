import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';
import '@mini-roda/ui/style.css';

if (!(window as any).__remotes__) {
  (window as any).__remotes__ = {
    mfe_customers: window.location.origin + '/customers/remoteEntry.js',
    mfe_loans: window.location.origin + '/loans/remoteEntry.js',
  };
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

