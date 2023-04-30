<script>
    import GameList from "../lib/GameList.svelte";
    import Shutdown from "../lib/Shutdown.svelte";

    // Set by svelte-routing.
    // svelte-ignore unused-export-let
    export let location

</script>

<GameList />

<div class="row my-4">
    <div class="col">
        <Shutdown/>
    </div>
</div>
