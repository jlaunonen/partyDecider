import {joinToString, ValToString} from "./itertools";

const MAX_LENGTH = 30

export class EditHistory<Item> {
    private states: Array<Item> = []
    private undoPos = -1

    listener: ((history: EditHistory<Item>) => void) | null = null

    get pos(): number {
        return this.undoPos
    }

    replaceWith(state: Item) {
        this.states = [state]
        this.undoPos = -1
        this.listener?.call(null, this)
    }

    current(): Item | null {
        if (this.undoPos < 0) {
            if (this.states.length == 0) {
                return null
            } else {
                return this.states[this.states.length - 1]
            }
        } else {
            return this.states[this.undoPos]
        }
    }

    push(state: Item): Item {
        if (this.undoPos > -1) {
            this.states.splice(this.undoPos + 1, this.states.length - this.undoPos - 1)
        }
        this.states.push(state)
        if (this.states.length > MAX_LENGTH) {
            this.states.shift()
        }
        this.undoPos = -1
        this.listener?.call(null, this)
        return state
    }

    undo(): Item | null {
        if (this.undoPos > 0) {
            this.undoPos--
        } else if (this.states.length > 1) {
            // -2, as -1 is already the default latest state.
            this.undoPos = this.states.length - 2
        } else {
            return null
        }
        this.listener?.call(null, this)
        return this.states[this.undoPos]
    }

    redo(): Item | null {
        if (this.undoPos < 0) {
            return null
        }
        if (this.undoPos + 2 < this.states.length) {
            this.undoPos++
            this.listener?.call(null, this)
            return this.states[this.undoPos]
        } else {
            this.undoPos = -1
            this.listener?.call(null, this)
            if (this.states.length > 0) {
                return this.states[this.states.length - 1]
            } else {
                return null
            }
        }
    }

    canUndo(): boolean {
        return this.undoPos != 0 && this.states.length > 1
    }

    canRedo(): boolean {
        return this.undoPos >= 0 && this.undoPos + 1 < this.states.length
    }

    toString(): string {
        return `pos=${this.undoPos.toString()}, len=${this.states.length}/${MAX_LENGTH}, states=` + joinToString(this.states, ValToString)
    }
}
