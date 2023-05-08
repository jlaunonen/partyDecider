<script lang="ts">
    import {apiConfig} from "../network"
    import {AdminApi} from "../api"

    const api = new AdminApi(apiConfig)

    async function rescan() {
        this.disabled = true
        try {
            const count = await api.rescanGames()
            alert(`Found ${count} games`)
        } catch (e) {
            alert(e)
        }
        this.disabled = false
    }
</script>

<div class="row my-4">
    <div class="col">
        <button type="button" class="btn btn-warning" on:click={rescan}>Rescan Steam collection</button>
    </div>
</div>
