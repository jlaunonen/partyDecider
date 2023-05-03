export function Identity<T>(val: T): T {
    return val
}

/** "Identity" function for map forEach. Note reversed arguments vs. return value. */
export function MapIdentity<K, V>(val: V, key: K): [K, V] {
    return [key, val]
}

type ForEachable<K, V> = {forEach: (cb: (val: V, key: K) => void) => void}

export function eachToArray<K, V, R>(src: ForEachable<K, V>, map: (val: V, key: K) => R): Array<R> {
    const r = new Array<R>()
    src.forEach((val, key) => r.push(map(val, key)))
    return r
}

export function eachToMap<K, V, RK, RV>(src: ForEachable<K, V>, map: (val: V, key: K) => [RK, RV]): Map<RK, RV> {
    const r = new Map<RK, RV>()
    src.forEach((val, key) => {
        let [k, v] = map(val, key)
        r.set(k, v)
    })
    return r
}

export function flatEachToMap<K, V, RK, RV>(src: ForEachable<K, V>, map: (val: V, key: K) => Array<[RK, RV]>): Map<RK, RV> {
    const r = new Map<RK, RV>()
    src.forEach((val, key) => {
        map(val, key).forEach(([k, v]) => {
            r.set(k, v)
        })
    })
    return r
}

export function iterToArray<T>(src: Iterable<T>): Array<T> {
    const r = new Array<T>()
    for (const value of src) {
        r.push(value)
    }
    return r
}

export function ValToString<T>(val: T): string {
    return val.toString()
}

export function PairToString<K, V>(val: V, key: K): string {
    return key.toString() + ":" + val.toString()
}

export function joinToString<K, V>(src: ForEachable<K, V>, map: (val: V, key: K) => string, joiner: string = ","): string {
    let r = ""
    let notFirst = false
    src.forEach((val, key) => {
        if (notFirst) {
            r += joiner
        } else {
            notFirst = true
        }
        r += map(val, key)
    })
    return r
}
