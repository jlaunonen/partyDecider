<script>
    import GameList from "../lib/GameList.svelte";
    import Shutdown from "../lib/Shutdown.svelte";
    import RescanSteam from "../lib/RescanSteam.svelte";
    import AddPoll from "../lib/AddPoll.svelte";
</script>

<AddPoll />

<GameList />

<RescanSteam />

<div class="row my-4">
    <div class="col">
        <Shutdown/>
    </div>
</div>
