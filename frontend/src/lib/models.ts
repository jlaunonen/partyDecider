import type {App} from "../api";
import {flatEachToMap, Identity, iterToArray, eachToArray, eachToMap, MapIdentity} from "./itertools";

const DEBUG = false

let uniqueIndex = 0;
function newId(prefix: string): string {
    return prefix + (uniqueIndex++).toString();
}

export class ItemInfo {
    constructor(
        readonly data: App,
        readonly dragId: ItemIdType,
    ) {
        if (DEBUG) console.log("Construct", data.name, "with id", dragId)
    }

    get name(): string {
        if (DEBUG) return this.dragId + ": " + this.data.name
        return this.data.name
    }
}

export class Level {
    constructor(
        private _name: string,
        public levelIndex: number,
        readonly items: Array<ItemInfo> = [],
        readonly dropId: DropTargetType = newId("dt:"),
        readonly upOneDropId: DropTargetType = newId("du:"),
    ) {
        if (DEBUG) console.log("Level", _name, "with id", dropId)
    }

    updateIndex(newIndex: number) {
        this.levelIndex = newIndex
        this._name = `${newIndex + 1}.`
    }

    get name(): string {
        if (DEBUG) return this.dropId + ": " + this._name
        return this._name
    }

    copy(): Level {
        return new Level(
            this._name,
            this.levelIndex,
            eachToArray(this.items, Identity),
            this.dropId,
            this.upOneDropId
        )
    }
}

type ItemIdType = string
type DropTargetType = string

export interface PollProps {
    items: Map<ItemIdType, ItemInfo>
    itemLevels: Map<ItemIdType, Level>
    targetLevels: Map<DropTargetType, Level>
    levels: Array<Level>
}

export class Poll {
    private get items(): Map<ItemIdType, ItemInfo> { return this.state.items }
    private get itemLevels(): Map<ItemIdType, Level> { return this.state.itemLevels }
    private get targetLevels(): Map<DropTargetType, Level> { return this.state.targetLevels }
    private get levels(): Array<Level> { return this.state.levels }

    private state: PollProps

    constructor(
        appList: Array<App>,
        props: PollProps | undefined = undefined
    ) {
        if (props) {
            this.state = props
        } else {
            const items = eachToMap(appList, (app, _) => {
                const itemId = newId("ii:")
                return [
                    itemId,
                    new ItemInfo(
                        app,
                        itemId
                    )
                ]
            })
            const noVote = new Level("no vote", -1, iterToArray(items.values()))
            const levels = [
                new Level("1.", 0),
                new Level("2.", 1),
                new Level("3.", 2),
                noVote,
            ]

            this.state = {
                items: items,

                levels: levels,

                targetLevels: flatEachToMap(levels, (e) => [
                    [e.dropId, e],
                    [e.upOneDropId, e],
                ]),

                itemLevels: flatEachToMap(levels, (level) =>
                    level.items.map((e) => [e.dragId, level])
                ),
            }
            if (DEBUG) console.log(this.state)
        }
    }

    copy(): PollProps {
        const newLevels = eachToMap(this.levels, (val, _) => [val, val.copy()])
        return {
            items: eachToMap(this.items, MapIdentity),
            itemLevels: eachToMap(this.itemLevels, (val, key) => [key, newLevels.get(val)]),
            targetLevels: eachToMap(this.targetLevels, (val, key) => [key, newLevels.get(val)]),
            levels: eachToArray(this.levels, (val) => newLevels.get(val)),
        }
    }

    setState(props: PollProps) {
        this.state = props
    }

    getLevels(): Array<Level> {
        return this.levels
    }

    /** Returns `true` if state changed. */
    move(participant: string, target: string): boolean {
        const item = this.items.get(participant)
        if (item !== undefined) {
            return this.moveItem(participant, target, item)
        } else {
            // Dragging whole level
            return this.moveLevel(participant, target)
        }
    }

    private moveItem(participant: string, target: string, item: ItemInfo): boolean {
        const itemLevel = this.itemLevels.get(participant)

        const dropTargetLevel = this.targetLevels.get(target)
        const originalIndex = itemLevel.items.indexOf(item)
        if (originalIndex < 0) {
            throw `Index error: ${originalIndex} on ${itemLevel.items}`
        }

        if (dropTargetLevel.upOneDropId === target) {
            // Dropped on separator above dropTargetLevel.
            let newIndex: number
            if (dropTargetLevel.levelIndex === -1) {
                // New after last real level.
                newIndex = Math.max(...this.levels.map((e) => e.levelIndex)) + 1
            } else {
                newIndex = dropTargetLevel.levelIndex
            }
            if (DEBUG) console.log("New level:", newIndex)
            const newLevel = new Level("", newIndex, [item])
            this.addLevel(newLevel, newIndex)
            this.itemLevels.set(participant, newLevel)
        } else {
            // Dropped on the level.
            if (itemLevel === dropTargetLevel) {
                // Dropped to original level. Nothing to do.
                if (DEBUG) console.log("Already at level", itemLevel.name)
                return false
            }

            if (DEBUG) console.log("On level", dropTargetLevel)
            dropTargetLevel.items.push(item)
            this.itemLevels.set(participant, dropTargetLevel)
        }

        // Remove from original place
        itemLevel.items.splice(originalIndex, 1)

        if (DEBUG) console.log(this.copy())
        return true
    }

    private moveLevel(level: string, target: string): boolean {
        const itemLevel = this.targetLevels.get(level)
        const dropTargetLevel = this.targetLevels.get(target)
        const originalIndex = this.levels.indexOf(itemLevel)

        if (DEBUG) console.log(itemLevel, originalIndex, "->", dropTargetLevel)
        if (itemLevel === dropTargetLevel) {
            // Logically same place.
            return false
        }

        if (dropTargetLevel.upOneDropId === target) {
            // TODO: If level from one above is moved to this, nothing really changes and state should not be considered changed.
            // Level moved between levels (or to first)
            let newIndex: number
            if (dropTargetLevel.levelIndex === -1) {
                // New after last real level.
                newIndex = Math.max(...this.levels.map((e) => e.levelIndex)) + 1
            } else {
                newIndex = dropTargetLevel.levelIndex
            }

            // Move items to new level
            const newLevel = new Level("", newIndex, iterToArray(itemLevel.items))
            itemLevel.items.splice(0, itemLevel.items.length)

            // Update items' level
            newLevel.items.forEach((e) => {
                this.itemLevels.set(e.dragId, newLevel)
            })

            this.addLevel(newLevel, newIndex)
            if (itemLevel.levelIndex > -1) {
                // Not "no vote" level, remove its contents.
                // "No vote" must exist even if empty as it is the last slot.
                this.removeLevel(itemLevel)
            }
        } else {
            // Level moved into another level
            // Update items' level (even though they are still in the original place)
            itemLevel.items.forEach((e) => {
                this.itemLevels.set(e.dragId, dropTargetLevel)
            })

            // Move the items to the new level.
            dropTargetLevel.items.push(...itemLevel.items)
            itemLevel.items.splice(0, itemLevel.items.length)
        }

        if (DEBUG) console.log(this.copy())
        return true
    }

    private addLevel(newLevel: Level, newIndex: number) {
        this.targetLevels.set(newLevel.dropId, newLevel)
        this.targetLevels.set(newLevel.upOneDropId, newLevel)
        this.levels.splice(newIndex, 0, newLevel)
        this.updateLevelIndices()
    }

    private removeLevel(level: Level, update: boolean = true) {
        this.targetLevels.delete(level.dropId)
        this.targetLevels.delete(level.upOneDropId)
        this.levels.splice(this.levels.indexOf(level), 1)
        if (update) {
            this.updateLevelIndices()
        }
    }

    private updateLevelIndices() {
        this.levels.forEach((e, index) => {
            if (e.levelIndex >= 0) {
                // Update only real levels, not "no vote".
                e.updateIndex(index)
            }
        })
    }
}
