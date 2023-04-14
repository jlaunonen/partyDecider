<script lang="ts">
    import {getBaseUrl} from "../network";

    async function fetchGames() {
        const result = await fetch(getBaseUrl() + "/api/admin/enabled")
        if (result.ok) {
            const data: Array<any> = await result.json();
            const newGames: Array<string> = []
            for (let index in data) {
                let game = data[index];
                newGames.push(game.name);
            }
            return newGames;
        } else {
            throw new Error(result.statusText);
        }
    }

    let promise = fetchGames();

    function updateGames() {
        promise = fetchGames();
    }
</script>

<div class="card">
    <div class="card-header">
        Games from backend <a type="button" href="javascript:void(0)" on:click={updateGames}>Refresh</a>
    </div>
    {#await promise}
        <div class="card-body">…</div>
    {:then games}
        <ul id="games" class="list-group list-group-flush">
            {#each games as game}
                <li class="list-group-item">{game}</li>
            {:else}
                <li class="list-group-item text-danger">No games</li>
            {/each}
        </ul>
    {:catch e}
        <div class="card-body">Error getting games: {e.message}</div>
    {/await}
</div>
