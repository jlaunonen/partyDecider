<script lang="ts">
    import VoteGrid from "./VoteGrid.svelte";
    import {eachToObject, joinToString, objectToMap, PairToString} from "./itertools";
    import {PublicApi} from "../api";
    import type {VotingItem} from "../api";
    import {apiConfig} from "../network";
    import {IS_DEVELOPMENT} from "./build";
    import PollResultTable from "./PollResultTable.svelte";

    export let pollId: string

    /** Bound to VoteGrid - updated by it. */
    let ballot: Map<number, number>
    /** Bound to VoteGrid - consumed by it. */
    let populate: Map<number, number>

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

    /** See also VotingSessionResult */
    interface Result {
        name?: string
        items?: Array<VotingItem>
        responses: number
        closed: boolean
        hasVoted?: boolean
    }

    let result: Result

    async function getResults() {
        const vr = await api.getVotingResult({
            voteSessionKey: pollId
        })
        if (vr.ballot) {
            populate = objectToMap(vr.ballot, (v, k) => [
                Number.parseInt(k), v
            ])
        }
        result = vr
    }

    getResults()

    function statusName(result: Result): string {
        const values: Array<string> = []
        if (result.hasVoted) {
            values.push("saved")
        } else {
            values.push("unsaved")
        }
        if (result.closed) {
            values.push("closed")
        }
        return values.join(", ")
    }
</script>

<h1>Current poll: {result?.name ?? pollId}</h1>
{#if result}
    <p class="lead">{statusName(result)}</p>
    {#if !result.closed || result.hasVoted}
        <VoteGrid bind:ballot bind:populate disabled={result.closed}>
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
    {/if}
    {#if result.closed || result.hasVoted}
        <div>
            <h3>Results:</h3>
            <div>{result.responses} responses</div>
            {#if result.items}
                <PollResultTable items={result.items} />
            {/if}
        </div>
    {/if}
{/if}
