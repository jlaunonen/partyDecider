<script lang="ts">
    import VoteGridItem from "./VoteGridItem.svelte";
    import type {ItemInfo} from "./models";

    export let name: string
    export let items: Array<ItemInfo>

</script>

<div class="row pd-row">
    <div draggable="true" class="col-1 pd-head py-2">{name}</div>
    <div class="col">
        <div class="row">
            {#each items as i}
                <VoteGridItem name={i.name} steam_id={i.steam_id}/>
            {/each}
        </div>
    </div>
</div>

<style>
    .pd-head {
        border: 1px solid gray;
    }

    .pd-row + :global(.pd-row) {
        border-top: 1px solid gray;
        margin-top: 2px;
        padding-top: 2px;
    }
</style>
