<script lang="ts">
    import VoteGridLevel from "./VoteGridLevel.svelte"
    import {DragTargetManager, handlers} from "./dragLib"
    import {Level, Poll} from "./models"
    import type {PollProps} from "./models"

    import {apiConfig} from "../network"
    import {PublicApi, ResourcesApi} from "../api"
    import {EditHistory} from "./editHistory"

    const api = new PublicApi(apiConfig)
    const resourcesApi = new ResourcesApi(apiConfig)

    let poll: Poll
    let voteGrid: Array<Level> = []
    const history = new EditHistory<PollProps>()

    async function fetchGames(): Promise<void> {
        const enabled = await api.getApps();
        poll = new Poll(enabled)
        voteGrid = poll.getLevels()
        // Push initial state.
        history.replaceWith(poll.copy())
        updateButtons()
    }

    let promise = fetchGames();

    function updateGames() {
        promise = fetchGames();
    }

    handlers.onEnd = () => {
        voteGrid = poll.getLevels()
    }

    const dropTargetHandler = new DragTargetManager();
    dropTargetHandler.onComplete = (dragged, target) => {
        if (poll.move(dragged.dragId, target.dragId)) {
            history.push(poll.copy())
            updateButtons()
        }
    }

    function undo() {
        const newState = history.undo()
        if (newState !== null) {
            poll.setState(newState)
            voteGrid = poll.getLevels()
        }
        updateButtons()
    }

    function redo() {
        const newState = history.redo()
        if (newState !== null) {
            poll.setState(newState)
            voteGrid = poll.getLevels()
        }
        updateButtons()
    }

    type Disabled = "disabled" | ""
    let undoDisabled: Disabled = "disabled"
    let redoDisabled: Disabled = "disabled"

    function updateButtons() {
        undoDisabled = history.canUndo() ? "" : "disabled"
        redoDisabled = history.canRedo() ? "" : "disabled"
    }

</script>

<div class="container my-4">
    <div class="btn-group">
        <button type="button" class="btn btn-secondary" disabled={undoDisabled} on:click={undo}>Undo</button>
        <button type="button" class="btn btn-secondary" disabled={redoDisabled} on:click={redo}>Redo</button>
    </div>
    {#await promise}
        <div class="text-muted">
            Loading...
        </div>
    {:then _}
        {#each voteGrid as level, index}
            <VoteGridLevel level={level} dropTargetHandler={dropTargetHandler} resourcesApi={resourcesApi}/>
        {/each}
    {/await}
</div>

<style>
    .btn-group {
        margin-bottom: 1em;
    }
</style>