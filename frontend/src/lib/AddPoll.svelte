<script lang="ts">

    import {AdminApi} from "../api";
    import {apiConfig} from "../network";

    const api = new AdminApi(apiConfig)

    let formName: HTMLInputElement
    let formDuration: HTMLInputElement

    async function submit(e: Event) {
        e.preventDefault()

        const duration = Number.parseInt(formDuration.value)

        const newSession = await api.addVotingSession({
            newVotingSession: {
                duration: duration,
                name: formName.value,
            }
        })

        alert(`New session created: ${newSession.name} (${newSession.key})`)
    }
</script>

<form class="mb-5" on:submit={submit}>
    <div class="mb-3">
        <label for="poll-name" class="form-label">Poll name (optional)</label>
        <input type="text" class="form-control" id="poll-name" maxlength="100" bind:this={formName}/>
    </div>
    <div class="mb-3">
        <label for="poll-duration" class="form-label">Poll duration in seconds; 0 for infinite</label>
        <input type="number" class="form-control" id="poll-duration" step="30" min="0" value="0" bind:this={formDuration}/>
    </div>

    <button type="submit" class="btn btn-primary">Create</button>
</form>
