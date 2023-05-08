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
        const [k, v] = map(val, key)
        r.set(k, v)
    })
    return r
}

export function eachToObject<K, V, RV>(src: ForEachable<K, V>, map: (val: V, key: K) => [string, RV]): Record<string, RV> {
    const r = {}
    src.forEach((val, key) => {
        const [k, v] = map(val, key)
        r[k] = v
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

export function mapIterToArray<T, R>(src: Iterable<T>, map: (val: T) => R): Array<R> {
    const r = new Array<R>()
    for (const value of src) {
        r.push(map(value))
    }
    return r
}

export function ValToString<T>(val: T): string {
    return val.toString()
}

export function PairToString<K, V>(val: V, key: K): string {
    return key.toString() + ":" + val.toString()
}

export function joinToString<K, V>(src: ForEachable<K, V>, map: (val: V, key: K) => string, joiner = ","): string {
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

class RepeatIterator implements Iterator<number> {
    private value: number

    constructor(
        private readonly stop: number,
        start: number,
    ) {
        this.value = start
    }

    next(): IteratorResult<number> {
        const val = this.value
        this.value++
        return {
            done: val >= this.stop,
            value: val,
        };
    }
}

export function repeat(stop: number, start = 0): Iterable<number> {
    return {
        [Symbol.iterator](): Iterator<number> {
            return new RepeatIterator(stop, start)
        }
    }
}
