<script>
    import GameList from "../lib/GameList.svelte"
    import Shutdown from "../lib/Shutdown.svelte"
    import RescanSteam from "../lib/RescanSteam.svelte"
    import AddPoll from "../lib/AddPoll.svelte"
    import ManagePolls from "../lib/ManagePolls.svelte"
</script>

<div class="mb-5">
    <AddPoll />
</div>

<div class="mb-5">
    <ManagePolls />
</div>

<div class="mb-5">
    <GameList asAdmin={true}/>
</div>

<RescanSteam />

<div class="row my-4">
    <div class="col">
        <Shutdown />
    </div>
</div>
