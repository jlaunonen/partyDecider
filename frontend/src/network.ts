import {Configuration} from "./api";
import {ALLOW_ALT_PORT} from "./lib/build";

function initPort() {
    if (ALLOW_ALT_PORT) {
        return new URL(location.href).searchParams.get("port")
    }
}

const port: string | null | undefined = initPort()

export function getBaseUrl(): string {
    // Set by vite.config.ts, true only on dev server.
    if (ALLOW_ALT_PORT) {
        if (port !== null && port !== undefined) {
            return location.protocol + "//" + location.hostname + ":" + port
        }
    }

    return location.origin;
}

export const apiConfig = new Configuration({
    basePath: getBaseUrl(),
});

export function makeLink(link: string): string {
    if (ALLOW_ALT_PORT) {
        if (port !== null && port !== undefined) {
            const newUrl = new URL(link, location.href)
            newUrl.searchParams.set("port", port)
            return newUrl.pathname + newUrl.search + newUrl.hash
        }
    }
    return link
}
