<script lang="ts">
    import GameList from "../lib/GameList.svelte"
    import Shutdown from "../lib/Shutdown.svelte"
    import RescanSteam from "../lib/RescanSteam.svelte"
    import AddPoll from "../lib/AddPoll.svelte"
    import ManagePolls from "../lib/ManagePolls.svelte"
    import type {VotingSession} from "../api"

    let newSessionInfo: VotingSession
</script>

<div class="mb-5">
    <AddPoll bind:newSessionInfo />
</div>

<div class="mb-5">
    <ManagePolls bind:newSessionInfo />
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
