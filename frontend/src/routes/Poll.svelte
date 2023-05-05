<script>
    import Poll from "../lib/Poll.svelte";

    // Set by svelte-routing.
    // svelte-ignore unused-export-let
    export let location

    // Parameter from link
    export let pollId
</script>

<Poll pollId={pollId} />
