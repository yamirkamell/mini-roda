/// <reference types="vite/client" />

declare global {
  interface Window {
    __remotes__?: {
      mfe_customers?: string;
      mfe_loans?: string;
    };
    mfe_customers?: {
      init: (shared: any) => Promise<void>;
      get: (module: string) => Promise<() => any>;
    };
    mfe_loans?: {
      init: (shared: any) => Promise<void>;
      get: (module: string) => Promise<() => any>;
    };
    __federation_shared__?: any;
  }
}

declare module 'mfe_customers/CustomerList' {
  import { ComponentType } from 'react';
  const CustomerList: ComponentType;
  export default CustomerList;
}

declare module 'mfe_customers/CustomerDetail' {
  import { ComponentType } from 'react';
  const CustomerDetail: ComponentType;
  export default CustomerDetail;
}

declare module 'mfe_loans/LoanList' {
  import { ComponentType } from 'react';
  const LoanList: ComponentType;
  export default LoanList;
}

declare module 'mfe_loans/LoanDetail' {
  import { ComponentType } from 'react';
  const LoanDetail: ComponentType;
  export default LoanDetail;
}

