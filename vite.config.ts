import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [sveltekit()],
  server: { host: "127.0.0.1", port: 5173 },
  preview: { host: "0.0.0.0", port: 3000 }
});
