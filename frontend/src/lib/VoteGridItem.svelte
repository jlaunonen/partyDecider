<script lang="ts">
    import {mountSource} from "./dragLib"
    import type {ItemInfo} from "./models"
    import type {ResourcesApi} from "../api"
    import type {App} from "../api"

    export let item: ItemInfo

    export let resourcesApi: ResourcesApi

    // TODO: Make icon display condition to be explicit instead of deducting from missing steamId.
    function imageSrc(app: App): string {
        return resourcesApi.resIcon_Path({appId: app.id});
    }
</script>

<div draggable="true" class="col-lg-3 col-6 pd-item py-2" use:mountSource data-dragId={item.dragId}>
    {#if item.data.steamId}
        <img draggable="false" class="float-end" src={imageSrc(item.data)} alt="icon" />
    {/if}
    {item.name}
</div>

<style>
    .pd-item {
        border: 1px solid gray;
        border-radius: var(--bs-card-inner-border-radius) var(--bs-card-inner-border-radius) var(--bs-card-inner-border-radius) var(--bs-card-inner-border-radius);
        cursor: move;
    }
    .pd-item:global(.dragging) {
        opacity: 0.5;
    }

    img {
        margin-top: 0.3em;
        margin-inline-start: 0.6em;
    }
</style>
