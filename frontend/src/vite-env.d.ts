/// <reference types="svelte" />
/// <reference types="vite/client" />

/**
 * Set by vite.config.ts.
 * Only when this is `true`, we parse ?port= argument from URL and communicate to that port.
 * See also network.ts.
 */
declare const __ALLOW_ALT_PORT__: boolean

declare const __IS_DEVELOPMENT__: boolean
