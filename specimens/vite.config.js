import { resolve } from 'node:path';
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  define: {
    'process.env.NODE_ENV': '"production"',
    'process.env': '{}',
  },
  build: {
    outDir: resolve(__dirname, '../assets/specimens'),
    emptyOutDir: true,
    lib: {
      entry: resolve(__dirname, 'src/main.jsx'),
      formats: ['es'],
      fileName: () => 'framewell-specimens.js',
      cssFileName: 'style',
    },
    rollupOptions: {
      output: {
        assetFileNames: assetInfo => assetInfo.name === 'style.css' ? 'style.css' : '[name][extname]',
      },
    },
  },
});
