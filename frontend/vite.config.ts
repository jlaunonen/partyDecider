import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vitejs.dev/config/
export default defineConfig(({command, mode}) => {
  // Consider both development and preview to not be final, production code.
  // Preview can be used to test zipapp, however.
  const development = mode !== "production";

  return {
    clearScreen: false,
    plugins: [svelte()],
    define: {
      __ALLOW_ALT_PORT__: development ? "true" : "false",
    },
    build: {
      minify: mode !== "production" ? false : "esbuild",
      sourcemap: development,
    },
  }
})
