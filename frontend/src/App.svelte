<script lang="ts">
    import Nav from "./lib/Nav.svelte";
    import {Router, Route} from "svelte-routing";
    import Admin from "./routes/Admin.svelte";
    import CurrentPoll from "./routes/Poll.svelte";
    import PollList from "./routes/PollList.svelte";

</script>

<Router>
    <Nav />
    <main class="container mt-4">
        <Route path="/" component={PollList} />
        <Route path="/poll/:pollId" component={CurrentPoll} />
        <Route path="/admin" component={Admin} />
    </main>
</Router>

<style>
</style>
