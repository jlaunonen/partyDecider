<script>
    import VoteGrid from "../lib/VoteGrid.svelte";

    // Set by svelte-routing.
    // svelte-ignore unused-export-let
    export let location
</script>

<h1>Current poll</h1>
<VoteGrid />
