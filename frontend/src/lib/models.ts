export class ItemInfo {
    constructor(
        readonly name: string,
        readonly steam_id: number | null = null,
    ) {
    }
}

export class Level {
    constructor(
        readonly name: string,
        readonly items: Array<ItemInfo> = [],
    ) {
    }
}
