<script lang="ts">
    import Nav from "./lib/Nav.svelte";
    import { Router, Route} from "svelte-routing";
    import Admin from "./routes/Admin.svelte";
    import CurrentPoll from "./routes/CurrentPoll.svelte";

</script>

<Router>
    <Nav />
    <main class="container mt-4">
        <Route path="/" component={CurrentPoll} />
        <Route path="/admin" component={Admin} />
    </main>
</Router>

<style>
</style>
