<script lang="ts">
    import {link} from "svelte-routing";
    import {PublicApi} from "../api"
    import type {VotingSession} from "../api";
    import {apiConfig} from "../network";
    import {makeLink} from "../network";

    const api = new PublicApi(apiConfig)

    async function fetchPolls(): Promise<Array<VotingSession>> {
        return await api.getVotingList();
    }

    let promise = fetchPolls()
</script>

<div>
    {#await promise}
        <div class="text-muted">
            Loading...
        </div>
    {:then polls}
        <ul>
            {#each polls as poll}
                <li><a href={makeLink("/poll/" + poll.key)} use:link>{poll.name} ({poll.key})</a></li>
            {/each}
        </ul>
        <div></div>
    {/await}
</div>
