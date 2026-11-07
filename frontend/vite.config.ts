import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// In development you run `npm run dev` (port 5173) and the Django backend
// separately. The proxy forwards /api and /ws to Django, so the browser only
// ever talks to one origin, exactly as it does behind nginx in Docker.
// Same URLs in dev and in Docker means no environment-specific code.
const backend = process.env.BACKEND_URL ?? "http://localhost:8000";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": backend,
      "/ws": { target: backend, ws: true },
    },
  },
});
