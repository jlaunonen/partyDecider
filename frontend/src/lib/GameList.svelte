<script lang="ts">
    import {apiConfig} from "../network";
    import {AdminApi, ResourcesApi} from "../api";
    import type {App} from "../api";

    /** Is this component displayed in admin site? */
    export let asAdmin = false

    const api = new AdminApi(apiConfig);
    const resourcesApi = new ResourcesApi(apiConfig);

    class AppInfo {
        constructor(
            readonly id: number,
            readonly name: string,
            readonly steamId: number,
            readonly iconUrl: string,
            readonly enabled: boolean,
        ) {
        }
    }

    let allAppInfos: Array<AppInfo> = []

    async function fetchGames(): Promise<Array<AppInfo>> {
        const allApps = await api.getAll()
        allApps.sort((a, b) => a.name > b.name ? 1 : a.name < b.name ? -1 : 0);

        const enabledArray = await api.getEnabled()
        const enabledIdSet = new Set<number>(
            enabledArray.map((e) => e.id)
        )

        allAppInfos = allApps.map((e) => new AppInfo(
            e.id,
            e.name,
            e.steamId,
            imageSrc(e),
            enabledIdSet.has(e.id),
        ))
        return allAppInfos
    }

    let promise: Promise<Array<AppInfo>> = fetchGames();

    function updateGames() {
        promise = fetchGames();
    }

    function imageSrc(app: App): string {
        return resourcesApi.resIcon_Path({appId: app.id, asAdmin: asAdmin});
    }

    function toggle(this: HTMLElement, _: PointerEvent) {
        const id = this.getAttribute("data-target")
        if (id) {
            const cb = document.getElementById(id) as HTMLInputElement
            cb.checked = !cb.checked
        }
    }

    function noBubble(e: Event) {
        // Stop event from bubbling and toggle() to be called, causing the checkbox to be toggled twice.
        e.stopPropagation()
    }

    async function updateByOnlyEnabled(only: boolean): Promise<Array<AppInfo>> {
        return allAppInfos.filter((e) => !only || e.enabled)
    }

    function onOnlyEnabled(this: HTMLInputElement) {
        promise = updateByOnlyEnabled(this.checked)
    }
</script>

<div class="card">
    <div class="card-header">
        <div>
            Games from backend <button type="button" class="btn btn-link" on:click={updateGames}>Refresh</button>
        </div>
        <div class="form-check">
            <input class="form-check-input" type="checkbox" value="" id="onlyEnabled" on:change={onOnlyEnabled}/>
            <label for="onlyEnabled">Show only enabled games</label>
        </div>
    </div>
    {#await promise}
        <div class="card-body">…</div>
    {:then games}
        <ul id="games" class="list-group list-group-flush">
            {#each games as game}<!-- type: AppInfo -->
                {@const id = "enable-" + game.id}
                <!-- This on:click is only to help mouse usage. The control used by keyboard is the input below. -->
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <li class="list-group-item" data-target={id} on:click={toggle}>
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="" checked={game.enabled} id={id} on:click={noBubble} />
                        <label for={id}>
                            <img src={game.iconUrl} alt="icon"/> {game.name}
                        </label>
                    </div>
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
        background-color: #19875440;
    }
</style>
