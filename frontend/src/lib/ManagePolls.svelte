<script lang="ts">
    import "./extra.css"
    import {AdminApi, PublicApi} from "../api"
    import type {VotingSession} from "../api"
    import {apiConfig, makeLink} from "../network"
    import NoPolls from "./NoPolls.svelte"
    import {formatTime} from "./utils"

    const api = new PublicApi(apiConfig)
    const adminApi = new AdminApi(apiConfig)

    export let newSessionInfo: VotingSession = undefined

    interface VotingSessionSupplement {
        isNew: boolean
    }

    type _VotingSession = VotingSession & VotingSessionSupplement

    let list: Array<_VotingSession> = []

    async function getList() {
        list = (await api.getVotingList())
            .map((e) => (
                {...e, isNew: false}
            ))
    }

    function prependList(info: VotingSession) {
        if (info) {
            list.unshift({...info, isNew: true})
            list = list
        }
    }
    $: prependList(newSessionInfo)

    let loading: Promise<void> = getList()

    async function closePoll(this: HTMLButtonElement) {
        const key = this.getAttribute("data-key")
        const info = await adminApi.closeSession({
            voteSessionKey: key,
        })
        const listIndex = list.findIndex((e) => e.key === info.key)
        if (listIndex >= 0) {
            list[listIndex] = {...info, isNew: false}
        }
    }

    function removeNewClass(this: HTMLElement) {
        this.classList.remove("new-poll")
    }
</script>

<h3>Polls</h3>
{#await loading then _}
    {#if list.length > 0}
        <ul>
            {#each list as item}
                <li class={item.isNew ? "new-poll" : ""} on:animationend={removeNewClass}>
                    {#if item.closed}
                        <button class="btn btn-sm btn-outline-secondary" disabled>Closed</button>
                    {:else}
                        <button class="btn btn-sm btn-danger" on:click={closePoll} data-key={item.key}>Close</button>
                    {/if}
                    <a href={makeLink("/poll/" + item.key)}>
                        {item.name ?? item.key} (<span class="date">{formatTime(item.createdAt)}</span>)
                    </a>
                </li>
            {/each}
        </ul>
    {:else}
        <NoPolls/>
    {/if}
{/await}

<style>
    :global(.new-poll) {
        animation: new-fade 1s linear 1;
    }
    @keyframes new-fade {
        from {
            background-color: var(--my-success-light);
        }
        to {
            background-color: #fff0;
        }
    }
</style>
