<script lang="ts">
    import {link} from "svelte-routing"
    import {PublicApi} from "../api"
    import type {VotingSession} from "../api"
    import {apiConfig} from "../network"
    import {makeLink} from "../network"
    import NoPolls from "./NoPolls.svelte"
    import {formatTime} from "./utils.js";

    const api = new PublicApi(apiConfig)

    async function fetchPolls(): Promise<Array<VotingSession>> {
        return await api.getVotingList()
    }

    let promise = fetchPolls()
</script>

<div>
    {#await promise}
        <div class="text-muted">
            Loading...
        </div>
    {:then polls}
        {#if polls.length > 0}
            <ul>
                {#each polls as poll}
                    <li class:text-muted={poll.closed}><a href={makeLink("/poll/" + poll.key)} use:link>{poll.name} ({poll.key})</a> {formatTime(poll.createdAt)}</li>
                {/each}
            </ul>
        {:else}
            <NoPolls />
        {/if}
    {/await}
</div>

<style>
    .text-muted a {
        color: color-mix(in srgb, var(--bs-link-color) 50%, gray);
    }
    .text-muted {
        font-style: italic;
    }
</style>