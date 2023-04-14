<script lang="ts">
    export let name: string
    export let steam_id: number | null

</script>

<div draggable="true" class="col-lg-2 col-4 pd-item py-2">
    {#if steam_id}
        <img class="float-start" src="/{steam_id}_icon.jpg" alt="icon"/>
    {/if}
    {name}
</div>

<style>
    .pd-item {
        border: 1px solid gray;
    }

    img {
        margin-inline-end: 0.6em;
    }
</style>
