import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import federation from '@originjs/vite-plugin-federation';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  base: '/customers/',
  root: __dirname,
  plugins: [
    react(),
    federation({
      name: 'mfe_customers',
      filename: 'remoteEntry.js',
      exposes: {
        './CustomerList': './src/components/CustomerList.tsx',
        './CustomerForm': './src/components/CustomerForm.tsx',
        './CustomerDetail': './src/components/CustomerDetail.tsx',
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
    port: 5173,
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
