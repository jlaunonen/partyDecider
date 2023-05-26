<script lang="ts">

    import {AdminApi} from "../api";
    import {apiConfig} from "../network";

    const api = new AdminApi(apiConfig)

    let formName: string
    let formDuration = 0

    async function submit(e: Event) {
        e.preventDefault()
        const newSession = await api.addVotingSession({
            newVotingSession: {
                duration: formDuration,
                name: formName,
            }
        })

        alert(`New session created: ${newSession.name} (${newSession.key})`)
    }
</script>

<form class="mb-5" on:submit={submit}>
    <div class="mb-3">
        <label for="poll-name" class="form-label">Poll name (optional)</label>
        <input type="text" class="form-control" id="poll-name" maxlength="100" bind:value={formName}/>
    </div>
    <div class="mb-3">
        <label for="poll-duration" class="form-label">Poll duration in seconds; 0 for infinite</label>
        <input type="number" class="form-control" id="poll-duration" step="30" min="0" bind:value={formDuration} />
    </div>

    <button type="submit" class="btn btn-primary">Create</button>
</form>
