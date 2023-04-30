function initPort() {
    if (__ALLOW_ALT_PORT__) {
        return new URL(location.href).searchParams.get("port")
    }
}

let port: string | null | undefined = initPort()

export function getBaseUrl(): string {
    // Set by vite.config.ts, true only on dev server.
    if (__ALLOW_ALT_PORT__) {
        if (port !== null && port !== undefined) {
            return location.protocol + "//" + location.hostname + ":" + port
        }
    }

    return location.origin;
}


export function makeLink(link: string): string {
    if (__ALLOW_ALT_PORT__) {
        if (port !== null && port !== undefined) {
            const newUrl = new URL(link, location.href)
            newUrl.searchParams.set("port", port)
            return newUrl.pathname + newUrl.search + newUrl.hash
        }
    }
    return link
}
