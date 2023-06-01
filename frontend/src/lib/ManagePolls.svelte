<script lang="ts">
    import {AdminApi, PublicApi} from "../api"
    import {apiConfig} from "../network"
    import NoPolls from "./NoPolls.svelte"
    import {formatTime} from "./utils"

    const api = new PublicApi(apiConfig)
    const adminApi = new AdminApi(apiConfig)

    let getList = api.getVotingList()

    async function closePoll(this: HTMLButtonElement) {
        const key = this.getAttribute("data-key")
        await adminApi.closeSession({
            voteSessionKey: key,
        })
        getList = api.getVotingList()
    }
</script>

<h3>Polls</h3>
{#await getList then list}
    {#if list.length > 0}
        <ul>
            {#each list as item}
                <li>
                    {#if item.closed}
                        <button class="btn btn-sm btn-outline-secondary" disabled>Closed</button>
                    {:else}
                        <button class="btn btn-sm btn-danger" on:click={closePoll} data-key={item.key}>Close</button>
                    {/if}
                    {item.name ?? item.key} (<span class="date">{formatTime(item.createdAt)}</span>)
                </li>
            {/each}
        </ul>
    {:else}
        <NoPolls/>
    {/if}
{/await}
