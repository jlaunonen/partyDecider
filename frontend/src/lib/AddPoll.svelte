<script lang="ts">

    import {AdminApi} from "../api"
    import type {VotingSession} from "../api"
    import {apiConfig} from "../network"
    import {BaseSubmitHandler} from "./utils"

    const api = new AdminApi(apiConfig)

    let formName: string
    let formDuration = 0

    export let newSessionInfo: VotingSession = undefined

    const submitHandler = new class extends BaseSubmitHandler {
        protected async doSubmit() {
            newSessionInfo = await api.addVotingSession({
                newVotingSession: {
                    duration: formDuration,
                    name: formName,
                }
            })
        }

        onSuccess() {
            formName = ""
            formDuration = 0
        }
    }

</script>

<h3>Add new poll</h3>
<form on:submit={(e) => submitHandler.submit(e)}>
    <div class="mb-3">
        <label for="poll-name" class="form-label">Poll name (optional)</label>
        <input type="text" class="form-control" id="poll-name" maxlength="100" bind:value={formName}/>
    </div>
    <div class="mb-3">
        <label for="poll-duration" class="form-label">Poll duration in seconds; 0 for infinite</label>
        <input type="number" class="form-control" id="poll-duration" step="30" min="0" bind:value={formDuration} />
    </div>

    <button type="submit" class="btn btn-primary" bind:this={submitHandler.submitBtn}>Create</button>
</form>
