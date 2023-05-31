<script>
    import GameList from "../lib/GameList.svelte"
    import Shutdown from "../lib/Shutdown.svelte"
    import RescanSteam from "../lib/RescanSteam.svelte"
    import AddPoll from "../lib/AddPoll.svelte"
    import ManagePolls from "../lib/ManagePolls.svelte"
</script>

<AddPoll />

<ManagePolls />

<GameList asAdmin={true}/>

<RescanSteam />

<div class="row my-4">
    <div class="col">
        <Shutdown />
    </div>
</div>
