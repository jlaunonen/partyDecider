<script lang="ts">
    import VoteGrid from "./VoteGrid.svelte";
    import {eachToObject, joinToString, PairToString} from "./itertools";
    import {PublicApi} from "../api";
    import type {VotingItem} from "../api";
    import {apiConfig} from "../network";
    import {IS_DEVELOPMENT} from "./build";

    export let pollId: string

    /** Bound to VoteGrid - updated by it. */
    let ballot: Map<number, number>

    let saved = false

    const api = new PublicApi(apiConfig)

    async function submitBallot() {
        this.disabled = true

        try {
            // Convert ballot from number:number to object with string:number type.
            const strBallot = eachToObject(ballot, (v, k) => [k.toString(), v])

            await api.submitBallot({
                voteSessionKey: pollId,
                ballot: {
                    ballot: strBallot
                },
            })
            saved = true

            await getResults()
        } catch (e) {
            this.disabled = false
        }
    }

    let resultItems: Array<VotingItem>

    async function getResults() {
        const result = await api.getVotingResult({
            voteSessionKey: pollId
        })

        resultItems = result.items
    }

    getResults()
</script>

<h1>Current poll: {pollId}</h1>
<VoteGrid bind:ballot>
    <div slot="submit">
        {#if saved}
            <button type="button" class="btn btn-success" disabled>Saved</button>
        {:else}
            <button type="button" class="btn btn-primary" on:click={submitBallot}>Submit</button>
        {/if}
        {#if ballot && IS_DEVELOPMENT}
        From sub component: {joinToString(ballot, PairToString)}
        {/if}
    </div>
</VoteGrid>
{#if resultItems && resultItems.length}
<div>
    <h3>Results:</h3>
    <ul>
    {#each resultItems as item}
        <li>{item.name} : {item.score}</li>
    {/each}
    </ul>
</div>
{/if}
