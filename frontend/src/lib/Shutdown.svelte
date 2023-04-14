<script lang="ts">
    import {getBaseUrl} from "../network";

    async function shutdown() {
        console.log(await fetch(getBaseUrl() + "/api/admin/shutdown"));
    }
</script>

<button type="button" class="btn btn-outline-danger" on:click={shutdown}>Shutdown backend</button>
