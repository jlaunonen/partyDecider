<script lang="ts">
    import Nav from "./lib/Nav.svelte";
    import {Router, Route} from "svelte-routing";
    import Admin from "./routes/Admin.svelte";
    import Poll from "./routes/Poll.svelte";
    import PollList from "./routes/PollList.svelte";

</script>

<Router let:location>
    <Nav current={location} />
    <main class="container mt-4">
        <Route path="/" component={PollList} />
        <Route path="/poll/:pollId" component={Poll} />
        <Route path="/admin" component={Admin} />
    </main>
</Router>

<style>
</style>
