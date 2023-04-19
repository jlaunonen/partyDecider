<script lang="ts">
    import VoteGridItem from "./VoteGridItem.svelte";
    import {mountSource} from "./dragLib";
    import type {DragTargetManager} from "./dragLib";
    import {Level} from "./models";
    import {ResourcesApi} from "../api";

    export let level: Level

    export let dropTargetHandler: DragTargetManager

    const dropTarget = (n) => dropTargetHandler.mount(n)

    export let resourcesApi: ResourcesApi
</script>

<div class="row pd-sep align-items-center" use:dropTarget data-dragId={level.upOneDropId}>
    <hr/>
</div>

<div class="card">
    <div class="row pd-row g-0" use:dropTarget data-dragId={level.dropId}>
        <div draggable="true" class="col-xl-1 col-2 pd-head py-2 card-header" use:mountSource data-dragId={level.dropId}>{level.name}</div>
        <div class="col">
            <div class="card-body">
                <div class="row px-2">
                    {#each level.items as el}
                        <VoteGridItem item={el} resourcesApi={resourcesApi}/>
                    {/each}
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    .pd-head {
        /* swap border: invisible but same size as on .over, but still displaying the original at right. */
        border: 2px solid #0000;
        border-right: var(--bs-card-border-width) solid var(--bs-card-border-color);
        border-radius: var(--bs-card-inner-border-radius) 0 0 var(--bs-card-inner-border-radius);
        cursor: move;
    }

    .pd-row:global(.over) .pd-head {
        border: 2px solid blue;
    }
    .pd-head:global(.dragging) {
        border: var(--bs-card-border-width) solid var(--bs-card-border-color);
        opacity: 0.5;
    }

    .pd-sep hr {
        margin-top: auto;
        /*margin-bottom: auto;*/
        /*padding-top: 1em;*/
        /*padding-bottom: 1em;*/
    }

    .pd-sep {
        height: 2em;
    }
    .pd-sep:global(.over) hr {
        opacity: 1;
        border-top: 2px solid blue;
    }

    .pd-row + :global(.pd-row) {
        border-top: 1px solid gray;
        margin-top: 2px;
        padding-top: 2px;
    }
</style>
