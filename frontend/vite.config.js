import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// LOCAL STAND-IN FOR: Azure Static Web Apps / Container Apps frontend host.
export default defineConfig({
  plugins: [react()],
  server: { port: 5173 },
});
