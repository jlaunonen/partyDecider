import type {App} from "../api";
import {
    flatEachToMap,
    Identity,
    iterToArray,
    eachToArray,
    eachToMap,
    repeat,
    mapIterToArray
} from "./itertools";

const DEBUG = false

const MIN_LEVEL_COUNT = 3

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
    itemLevels: Map<ItemIdType, Level>
    targetLevels: Map<DropTargetType, Level>
    levels: Array<Level>
    toString(): string
}

function copyProps(src: PollProps): PollProps {
    const newLevels = eachToMap(src.levels, (val) => [val, val.copy()])
    const id = newId("state:")
    return {
        itemLevels: eachToMap(src.itemLevels, (val, key) => [key, newLevels.get(val)]),
        targetLevels: eachToMap(src.targetLevels, (val, key) => [key, newLevels.get(val)]),
        levels: eachToArray(src.levels, (val) => newLevels.get(val)),
        toString(): string {
            return id
        }
    }
}

export class Poll {
    private get itemLevels(): Map<ItemIdType, Level> { return this.state.itemLevels }
    private get targetLevels(): Map<DropTargetType, Level> { return this.state.targetLevels }
    private get levels(): Array<Level> { return this.state.levels }

    private readonly items: ReadonlyMap<ItemIdType, ItemInfo>
    private state: PollProps

    constructor(
        appList: Array<App>,
        props: PollProps | undefined = undefined
    ) {
        this.items = eachToMap(appList, (app) => {
            const itemId = newId("ii:")
            return [
                itemId,
                new ItemInfo(
                    app,
                    itemId
                )
            ]
        })

        if (props) {
            this.state = props
        } else {
            const levels: Array<Level> = mapIterToArray(repeat(MIN_LEVEL_COUNT), (index) =>
                new Level(`${index + 1}.`, index)
            )
            const noVote = new Level("no vote", -1, iterToArray(this.items.values()))
            levels.push(noVote)

            this.state = {
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
        return copyProps(this.state)
    }

    setState(props: PollProps) {
        this.state = copyProps(props)
    }

    getLevels(): Array<Level> {
        return this.levels
    }

    getBallot(): Map<number, number> {
        const ballot: Map<number, number> = new Map()
        this.levels.forEach((level) => {
            // We don't care items that are not voted.
            if (level.levelIndex >= 0) {
                level.items.forEach((e) => {
                    ballot.set(e.data.id, level.levelIndex + 1)
                })
            }
        })
        return ballot
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
            // Logically same place: Between this and one above.
            return false
        }

        if (dropTargetLevel.upOneDropId === target) {
            if (this.levels.indexOf(dropTargetLevel) == originalIndex + 1) {
                // Logically same place: Between this and one below.
                return false
            }

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
            itemLevel.items.splice(0)

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
            itemLevel.items.splice(0)
        }

        if (DEBUG) console.log(this.copy())
        return true
    }

    private addLevel(newLevel: Level, newIndex: number) {
        this.registerLevel(newLevel)
        this.levels.splice(newIndex, 0, newLevel)
        this.updateLevelIndices()
    }

    private registerLevel(newLevel: Level) {
        this.targetLevels.set(newLevel.dropId, newLevel)
        this.targetLevels.set(newLevel.upOneDropId, newLevel)
    }

    private removeLevel(level: Level, update = true) {
        this.unregisterLevel(level)
        this.levels.splice(this.levels.indexOf(level), 1)
        if (update) {
            this.updateLevelIndices()
        }
    }

    private unregisterLevel(level: Level) {
        this.targetLevels.delete(level.dropId)
        this.targetLevels.delete(level.upOneDropId)
    }

    private updateLevelIndices() {
        this.levels.forEach((e, index) => {
            if (e.levelIndex >= 0) {
                // Update only real levels, not "no vote".
                e.updateIndex(index)
            }
        })
    }

    collapseEmpty(): boolean {
        const removeStack: Array<Level> = []
        const toRemove: Array<Level> = []
        const newLevels: Array<Level> = []
        this.levels.forEach((e) => {
            if (e.levelIndex >= 0) {
                if (e.items.length == 0) {
                    removeStack.push(e)
                } else {
                    newLevels.push(e)
                    if (removeStack.length) {
                        toRemove.push(...removeStack)
                        removeStack.splice(0)
                    }
                }
            }
        })

        // If needed, firstly add already existing empty levels back.
        if (removeStack.length) {
            for (let i: number = newLevels.length; i < MIN_LEVEL_COUNT && removeStack.length; i++) {
                newLevels.push(removeStack.shift())
            }
            toRemove.push(...removeStack)
        }
        // If needed, add new empty levels.
        for (let i: number = newLevels.length; i < MIN_LEVEL_COUNT; i++) {
            const newLevel = new Level("", 0)
            newLevels.push(newLevel)
            this.registerLevel(newLevel)
        }

        newLevels.push(this.levels[this.levels.length - 1])  // "no vote" level
        toRemove.forEach((e) => {
            this.unregisterLevel(e)
        })
        this.state.levels = newLevels
        this.updateLevelIndices()

        if (toRemove.length) {
            this.updateLevelIndices()
            return true
        }
        return false
    }
}
