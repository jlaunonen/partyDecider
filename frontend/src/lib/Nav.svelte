<script lang="ts">
    import "~bootstrap/dist/js/bootstrap.bundle.js"
    import {link} from "svelte-routing";
    import {makeLink} from "../network";

    function makeRelUrl(loc: Location): string {
        return loc.pathname + loc.search + loc.hash
    }

    let navDiv: HTMLElement = undefined
    export let current: Location = undefined

    $: if (navDiv !== undefined && current !== undefined) updateCurrentTarget(navDiv, makeRelUrl(current))

    function updateCurrentTarget(navDiv: HTMLElement, currentUrl: string) {
        navDiv.querySelectorAll(".nav-item > a").forEach((e: HTMLAnchorElement) => {
            // Get value from attribute to avoid getting full href, as currentUrl is only pathname and rest of it.
            const href = e.getAttribute("href")
            if (href === currentUrl) {
                e.classList.add("active")
                e.setAttribute("aria-current", "page")
            } else {
                e.classList.remove("active")
                e.removeAttribute("aria-current")
            }
        });
    }
</script>

<header>
    <nav class="navbar navbar-expand-md navbar-dark bg-dark">
        <div class="container">
            <span class="navbar-brand">Party Decider</span>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbar" aria-controls="navbar" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbar" bind:this={navDiv}>
                <ul class="navbar-nav me-auto mb-2 mb-md-0">
                    <li class="nav-item"><a class="nav-link" aria-current="page" href={makeLink("/")} use:link>Current polls</a></li>
                    <li class="nav-item"><a class="nav-link" href={makeLink("/default")} use:link>Default opinion</a></li>
                </ul>
                <ul class="navbar-nav mb-2 mb-md-0">
                    <li class="nav-item"><a class="nav-link" href={makeLink("/admin")} use:link>Admin</a></li>
                </ul>
            </div>
        </div>
    </nav>
</header>
