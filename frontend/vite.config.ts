import * as path from "node:path";
import * as fs from "node:fs"
import { defineConfig } from "vite"
import { svelte } from "@sveltejs/vite-plugin-svelte"

const envfiles = ["env", "env.txt"]
const env = {
  // Same defaults as in backend/__init__:Settings
  HOST: "0.0.0.0",
  PORT: 8192,
}
function readEnv(file: string) {
  const envfile = path.join(__dirname, "..", file)
  if (fs.existsSync(envfile)) {
    const PAT = /([\w_])=(.*)/
    for (let line of fs.readFileSync(envfile, {encoding: "utf-8"}).split("\n")) {
      line = line.trimStart()
      if (line.startsWith("#")) {
        continue
      }
      const parts = PAT.exec(line)
      if (parts != null) {
        env[parts[1]] = parts[2]
      }
    }
  }
}

for (const f of envfiles) {
  readEnv(f)
}


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
      __IS_DEVELOPMENT__: development ? "true" : "false",
    },
    build: {
      minify: mode !== "production" ? false : "esbuild",
      sourcemap: development,
    },
    resolve: {
      alias: {
        "~bootstrap": path.resolve(__dirname, "node_modules/bootstrap"),
      }
    },
    server: {
      proxy: {
        "^/(api|res)": {
          target: `http://${env.HOST}:${env.PORT}`,
          changeOrigin: true,
        },
      },
    },
   }
})
