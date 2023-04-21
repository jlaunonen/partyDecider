<script lang="ts">
    import {getBaseUrl} from "../network";

    async function rescan() {
        this.disabled = true
        try {
            const response = await fetch(getBaseUrl() + "/api/admin/rescan", {method: "POST"})
            const count = await response.text()
            alert(`Found ${count} games`)
        } catch (e) {
            alert(e)
        }
        this.disabled = false
    }
</script>

<div class="row my-4">
    <div class="col">
        <button class="btn btn-warning" on:click={rescan}>Rescan Steam collection</button>
    </div>
</div>
