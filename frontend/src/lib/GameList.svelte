<script lang="ts">
    import {apiConfig} from "../network";
    import {AdminApi, ResourcesApi} from "../api";
    import type {App} from "../api";

    const api = new AdminApi(apiConfig);
    const resourcesApi = new ResourcesApi(apiConfig);

    async function fetchGames(): Promise<Array<App>> {
        return await api.getEnabled();
    }

    let promise = fetchGames();

    function updateGames() {
        promise = fetchGames();
    }

    function imageSrc(app: App): string {
        return resourcesApi.resIcon_Path({appId: app.steamId});
    }
</script>

<div class="card">
    <div class="card-header">
        Games from backend <button type="button" class="btn btn-link" on:click={updateGames}>Refresh</button>
    </div>
    {#await promise}
        <div class="card-body">…</div>
    {:then games}
        <ul id="games" class="list-group list-group-flush">
            {#each games as game}
                <li class="list-group-item"><img src={imageSrc(game)} alt="icon" /> {game.name}</li>
            {:else}
                <li class="list-group-item text-danger">No games</li>
            {/each}
        </ul>
    {:catch e}
        <div class="card-body">Error getting games: {e.message}</div>
    {/await}
</div>

<style>
    button {
        padding: 2px 4px 2px 4px;
        vertical-align: baseline;
    }
</style>
