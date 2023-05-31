<script lang="ts">
    import type {VotingItem} from "../api";

    export let items: Array<VotingItem> = []

    function resultMax(items: Array<VotingItem>): number {
        return items.reduce((prev, current) => {
            return Math.max(prev, current.score)
        }, 0)
    }

    let max = resultMax(items)
</script>

<table class="table">
    <tbody>
        {#each items as item}
            {@const percent = item.score * 100 / max}
            <tr class={(item.score > 0 && item.score === max) ? "table-success" : ""}>
                <td>{item.name}</td>
                <td>
                    <div class="progress">
                        <div class="progress-bar" style:width={`${percent}%`}>
                            {#if percent >= 50}
                                {item.score}
                            {/if}
                        </div>
                        <div class="progress-out">
                            {#if percent < 50}
                                {item.score}
                            {/if}
                        </div>
                    </div>
                </td>
            </tr>
        {/each}
    </tbody>
</table>

<style>
    td {
        width: 50%;
    }
    .progress-out {
        flex-grow: 1;
        text-align: center;
    }
</style>
