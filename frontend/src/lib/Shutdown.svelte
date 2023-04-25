<script lang="ts">
    import {apiConfig} from "../network"
    import {AdminApi} from "../api"

    const api = new AdminApi(apiConfig)

    async function shutdown() {
        console.log(await api.shutdown())
    }
</script>

<button type="button" class="btn btn-outline-danger" on:click={shutdown}>Shutdown backend</button>
