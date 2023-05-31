<script lang="ts">
    import VoteGridLevel from "./VoteGridLevel.svelte"
    import {DragTargetManager} from "./dragLib"
    import {Poll} from "./models"
    import type {SourceHandlers} from "./dragLib"
    import type {Level} from "./models"
    import type {PollProps} from "./models"

    import {apiConfig} from "../network"
    import {PublicApi, ResourcesApi} from "../api"
    import {EditHistory} from "./editHistory"
    import {joinToString, PairToString} from "./itertools.js";
    import {IS_DEVELOPMENT} from "./build.js";

    const api = new PublicApi(apiConfig)
    const resourcesApi = new ResourcesApi(apiConfig)

    let poll: Poll
    let voteGrid: Array<Level> = []
    const history = new EditHistory<PollProps>()

    if (IS_DEVELOPMENT) {
        history.listener = () => console.log("History:", history.toString())
    }

    async function fetchGames(): Promise<void> {
        const enabled = await api.getApps();
        poll = new Poll(enabled)
        voteGrid = poll.getLevels()
        // Push initial state.
        history.replaceWith(poll.copy())
        updateButtons()
    }

    let promise = fetchGames();

    export let ballot: Map<number, number> = new Map()

    const sourceHandlers: SourceHandlers = {
        onEnd: () => {
            voteGrid = poll.getLevels()
            ballot = poll.getBallot()
        }
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

    let undoDisabled = true
    let redoDisabled = true

    function updateButtons() {
        undoDisabled = !history.canUndo()
        redoDisabled = !history.canRedo()
    }

    function collapse() {
        if (poll.collapseEmpty()) {
            history.push(poll.copy())
            voteGrid = poll.getLevels()
            updateButtons()
        }
    }

</script>

<div class="container my-4">
    <div class="btn-group" role="group">
        <button type="button" class="btn btn-secondary" disabled={undoDisabled} on:click={undo}>Undo</button>
        <button type="button" class="btn btn-secondary" disabled={redoDisabled} on:click={redo}>Redo</button>
    </div>
    <div class="btn-group" role="group">
        <button type="button" class="btn btn-outline-secondary" on:click={collapse}>Collapse empty</button>
    </div>
    {#await promise}
        <div class="text-muted">
            Loading...
        </div>
    {:then _}
        {#each voteGrid as level}
            <VoteGridLevel level={level} dropTargetHandler={dropTargetHandler} sourceHandlers={sourceHandlers} resourcesApi={resourcesApi} />
        {/each}
    {/await}
    {#if poll && IS_DEVELOPMENT}
        <!-- voteGrid referred only to make this reactive on that -->
        <!--suppress CommaExpressionJS -->
        <div>Ballot: {voteGrid, joinToString(poll.getBallot(), PairToString)}</div>
    {/if}
    <slot name="submit" />
</div>

<style>
    .btn-group {
        margin-bottom: 1em;
    }
</style>