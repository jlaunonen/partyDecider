const PORT_MATCH = /\?port=(\d+)/;

export function getBaseUrl(): string {
    // Set by vite.config.ts, true only on dev server.
    if (__ALLOW_ALT_PORT__) {
        const match = PORT_MATCH.exec(location.search);
        if (match !== null) {
            return location.protocol + "//" + location.hostname + ":" + match[1];
        }
    }

    return location.origin;
}
