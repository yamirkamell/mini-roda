# Loans Microfrontend

React + Vite microfrontend for loan management with Module Federation.

## Features

- ✅ View loan list
- ✅ Approve/reject loans
- ✅ View payment schedule
- ✅ Register payments
- ✅ Module Federation (exposes LoanList, LoanDetail, ApprovalActions)
- ✅ Zustand for state management
- ✅ Shared UI components from @mini-roda/ui

## Module Federation

This microfrontend exposes the following components via Module Federation:

- `./LoanList` - Loan list component
- `./LoanDetail` - Loan detail component
- `./ApprovalActions` - Loan approval/rejection actions component

## Development

```bash
pnpm dev
```

The app will be available at http://localhost:5174

## Environment Variables

Create a `.env` file:

```
VITE_API_BASE_URL=http://localhost
```

## Usage in Host Application

To use this microfrontend in a host application:

```tsx
import { lazy, Suspense } from 'react';

const LoanList = lazy(() => import('mfe_loans/LoanList'));
const LoanDetail = lazy(() => import('mfe_loans/LoanDetail'));
const ApprovalActions = lazy(() => import('mfe_loans/ApprovalActions'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <LoanList />
    </Suspense>
  );
}
```

## Build

```bash
pnpm build
```

The build will generate:
- `dist/remoteEntry.js` - Module Federation entry point
- `dist/assets/*` - Static assets

## Routes

- `/loans` - Loan list
- `/loans/:id` - Loan detail with approval actions and payment schedule

## API Endpoints

All endpoints are accessed through the gateway at `/loans/...`:

- `GET /loans/api/v1/loans` - Get all loans
- `GET /loans/api/v1/loans/:id` - Get loan by ID
- `POST /loans/api/v1/loans/:id/approve` - Approve loan
- `POST /loans/api/v1/loans/:id/reject` - Reject loan
- `GET /loans/api/v1/loans/:id/payment-schedule` - Get payment schedule
- `POST /loans/api/v1/loans/:id/payments` - Register payment
