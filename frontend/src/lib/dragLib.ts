const DEBUG = false

const DRAG_MIME: string = "application/x-dragLib";
export const DRAG_ID_ATTR = "data-dragId";


function bindEvent<T extends (Event) => boolean | void>(node: HTMLElement, eventType: string, cb: T): {eventType: string, cb: T} {
    node.addEventListener(eventType, cb)
    return {eventType, cb}
}


function handleStart(e: DragEvent) {
    const element = e.target as HTMLElement;
    element.classList.add("dragging")

    e.dataTransfer.effectAllowed = "move";

    const value = element.getAttribute(DRAG_ID_ATTR)
    e.dataTransfer.setData(DRAG_MIME, value);
    e.dataTransfer.setData("text/plain", element.innerText);

    if (DEBUG) console.log("Start:", value, debugElement(element));
}

export const handlers : {onEnd: (() => void) | null} = {
    onEnd: null
}

function handleEnd(e: DragEvent) {
    // XXX: Event points to an element whose content and attributes have been (or are being) moved to a new element.
    // If you log the element, it will show the place where the drag started instead of the end position.
    const element = e.target as HTMLElement
    element.classList.remove("dragging")
    if (DEBUG) console.log("End:", debugElement(this), e)
    if (handlers.onEnd) {
        handlers.onEnd()
    }
}

export function mountSource(node: HTMLElement) {
    const listeners = [
        bindEvent(node, "dragstart", handleStart),
        bindEvent(node, "dragend", handleEnd),
    ]
    return {
        destroy() {
            listeners.forEach((e) => node.removeEventListener(e.eventType, e.cb))
        }
    }
}


/** Get text from immediate text children of HTML Element, excluding any text from descendant elements. */
function getNodeText(node: HTMLElement): string {
    const children = node.childNodes
    let out = ""
    for (let i = 0; i < children.length; i++) {
        const child = children.item(i)
        if (child.nodeType == child.TEXT_NODE) {
            out += child.nodeValue
        }
    }
    return out.trim()
}

function debugElement(node: HTMLElement) {
    // if (true) return node
    const id = node.getAttribute(DRAG_ID_ATTR)
    if (id) {
        return id
    }
    const selfText = getNodeText(node)
    if (selfText) {
        return selfText
    }
    return node.innerText
}

export interface DragElement {
    dragId: string
    node: Element
}


export class DragTargetManager {
    private overed: RefCountSet = new RefCountSet()
    private dropTargetNodes: Set<HTMLElement> = new Set()

    onComplete: (dragged: DragElement, onto: DragElement) => void

    private dragOver(e: DragEvent, _: HTMLElement) {
        e.preventDefault()
        e.dataTransfer.dropEffect = "move"
        return false
    }

    private handleDragEnter(e: DragEvent, el: HTMLElement) {
        this.overed.add(el)
        el.classList.add("over")
        // Needed for at least Chrome 112 to avoid randomly failing to proceed to drop.
        e.preventDefault()
    }

    private handleDragLeave(_: DragEvent, el: HTMLElement) {
        if (this.overed.delete(el)) {
            el.classList.remove("over")
        }
    }

    private handleDrop(e: DragEvent, el: HTMLElement) {
        e.preventDefault()

        const dragInfo = e.dataTransfer.getData(DRAG_MIME)
        const draggedEl = document.querySelector(`[${DRAG_ID_ATTR}="${dragInfo}"]`)
        const thisInfo = el.getAttribute(DRAG_ID_ATTR)
        if (DEBUG) console.log("Drop", e, dragInfo)
        if (this.overed.delete(el)) {
            el.classList.remove("over")
        }

        if (this.onComplete) {
            this.onComplete({
                dragId: dragInfo,
                node: draggedEl,
            }, {
                dragId: thisInfo,
                node: el,
            })
        } else {
            console.log("Dropped", (dragInfo ?? e.dataTransfer.getData("text/plain")), "on", debugElement(el))
        }
    }

    mount(node: HTMLElement) {
        // setDragInfo(node, dragData)
        const listeners = [
            bindEvent(node, "dragover", (e) => this.dragOver(e, node)),
            bindEvent(node, "dragenter", (e) => this.handleDragEnter(e, node)),
            bindEvent(node, "dragleave", (e) => this.handleDragLeave(e, node)),
            bindEvent(node, "drop", (e) => this.handleDrop(e, node)),
        ]
        this.dropTargetNodes.add(node)
        return {
            destroy: () => {
                this.dropTargetNodes.delete(node);
                listeners.forEach((e) => node.removeEventListener(e.eventType, e.cb))
            }
        }
    }
}

class RefCountSet {
    private refcount = new Map<HTMLElement, number>();

    add(value: HTMLElement): this {
        let refs: number | undefined = this.refcount.get(value);
        if (refs === undefined) {
            refs = 1;
        } else {
            refs += 1;
        }
        this.refcount.set(value, refs);
        return this;
    }

    delete(value: HTMLElement): boolean {
        let refs: number | undefined = this.refcount.get(value);
        if (refs === undefined) {
            throw new Error("Reference count underflow");
        }
        let r: boolean;
        if (refs == 1) {
            // always true at this point.
            r = this.refcount.delete(value);
        } else {
            this.refcount.set(value, refs - 1);
            r = false;
        }
        return r;
    }
}
