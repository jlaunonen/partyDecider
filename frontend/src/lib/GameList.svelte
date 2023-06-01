<script lang="ts">
    import "./extra.css"
    import {apiConfig} from "../network"
    import {AdminApi, ResourcesApi} from "../api"
    import type {App} from "../api"

    /** Is this component displayed in admin site? */
    export let asAdmin = false

    const api = new AdminApi(apiConfig)
    const resourcesApi = new ResourcesApi(apiConfig)

    interface AppSupplement {
        iconUrl: string
    }
    type AppInfo = App & AppSupplement

    let allAppInfos: Array<AppInfo> = []

    async function fetchGames(): Promise<Array<AppInfo>> {
        const allApps = await api.getAll()
        allApps.sort((a, b) => a.name > b.name ? 1 : a.name < b.name ? -1 : 0)

        allAppInfos = allApps.map((e) => ({
            ...e,
            iconUrl: imageSrc(e),
        }))
        return allAppInfos
    }

    let promise: Promise<Array<AppInfo>> = fetchGames();

    function updateGames() {
        promise = fetchGames();
    }

    function imageSrc(app: App): string {
        return resourcesApi.resIcon_Path({appId: app.id, asAdmin: asAdmin})
    }

    async function updateByOnlyEnabled(only: boolean): Promise<Array<AppInfo>> {
        return allAppInfos.filter((e) => !only || e.enabled)
    }

    function onOnlyEnabled(this: HTMLInputElement) {
        promise = updateByOnlyEnabled(this.checked)
    }
</script>

<h3>Enabled apps <small><button type="button" class="btn btn-link" on:click={updateGames}>Refresh</button></small></h3>
<div class="card">
    <div class="card-header">
        <div class="form-check">
            <input class="form-check-input" type="checkbox" value="" id="onlyEnabled" on:change={onOnlyEnabled}/>
            <label for="onlyEnabled">Show only enabled apps</label>
        </div>
    </div>
    {#await promise}
        <div class="card-body">…</div>
    {:then games}
        <ul id="games" class="list-group list-group-flush">
            {#each games as game}<!-- type: AppInfo -->
                <li class="list-group-item">
                    <label class="form-check">
                        <input class="form-check-input" type="checkbox" value="" checked={game.enabled} id={"enable-" + game.id} />
                        <img src={game.iconUrl} alt="icon"/> {game.name}
                    </label>
                </li>
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
    .list-group-item:has(input:checked) {
        background-color: var(--my-success-light);
    }

    /*
    Bootstrap expects checkbox label to be next to input:checkbox, but we wrap whole row/li
    with <label> to make the row clickable and easier to use with mouse.
    These values try to mimic the original
    <li.list-group-item> <div.form-check> <input.form-check-input/> <label>..</label> </div> </li>
    layout.
    */
    li.list-group-item {
        padding: 0;
    }
    li.list-group-item label {
        padding: var(--bs-list-group-item-padding-y) var(--bs-list-group-item-padding-x);
    }
    li.list-group-item label input.form-check-input {
        margin-left: 0;
        margin-right: 0.5em;
    }
</style>
