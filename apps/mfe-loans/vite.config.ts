import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import federation from '@originjs/vite-plugin-federation';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  base: '/loans/',
  root: __dirname,
  plugins: [
    react(),
    federation({
      name: 'mfe_loans',
      filename: 'remoteEntry.js',
      exposes: {
        './LoanList': './src/components/LoanList.tsx',
        './LoanDetail': './src/components/LoanDetail.tsx',
        './ApprovalActions': './src/components/ApprovalActions.tsx',
        './types': './src/components/index.ts',
      },
      shared: {
        react: { singleton: true, requiredVersion: false },
        'react-dom': { singleton: true, requiredVersion: false },
        'react-router-dom': { singleton: true, requiredVersion: false },
        zustand: { singleton: true, requiredVersion: false },
      },
    }),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  css: {
    modules: {
      generateScopedName: '[name]__[local]___[hash:base64:5]',
    },
  },
  server: {
    port: 5174,
    host: true,
    cors: true,
  },
  build: {
    target: 'esnext',
    minify: false,
    cssCodeSplit: false,
    sourcemap: true,
  },
});
