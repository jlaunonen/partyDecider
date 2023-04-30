<script lang="ts">
    import {ItemInfo, Level} from "./models";
    import VoteGridLevel from "./VoteGridLevel.svelte";

    const dragStuff = () => {

        let dragSrcEl;

        function handleDragStart(e) {
            this.style.opacity = '0.4';
            console.log(e);
            dragSrcEl = this;
            e.dataTransfer.effectAllowed = "move";
            e.dataTransfer.setData("text/html", this.innerHTML);
        }

        function handleDragEnd(e) {
            this.style.opacity = '1';
            console.log(e);
            items.forEach(function (item) {
                item.classList.remove('over');
            });
        }

        function handleDragOver(e) {
            e.preventDefault();
            return false;
        }

        function handleDragEnter(e) {
            this.classList.add('over');
        }

        function handleDragLeave(e) {
            this.classList.remove('over');
        }

        function handleDrop(e) {
            console.log(e);
            e.stopPropagation();

            if (dragSrcEl !== this) {
                dragSrcEl.innerHTML = this.innerHTML;
                this.innerHTML = e.dataTransfer.getData("text/html");
            }
            return false;
        }


        let items = document.querySelectorAll('.container .box');
        items.forEach(function (item) {
            item.addEventListener('dragstart', handleDragStart);
            item.addEventListener('dragend', handleDragEnd);
            item.addEventListener('dragover', handleDragOver);
            item.addEventListener('dragenter', handleDragEnter);
            item.addEventListener('dragleave', handleDragLeave);
            item.addEventListener("drop", handleDrop);
        });

        return {}
    };

    const voteGrid: Array<Level> = [
        new Level("1.", [
            new ItemInfo("Portal 2"),
            new ItemInfo("Portal 2"),
            new ItemInfo("Portal 2"),
            new ItemInfo("Portal 2"),
            new ItemInfo("Portal 2"),
            new ItemInfo("Portal 2"),
            new ItemInfo("Portal 2"),
            new ItemInfo("Portal 2"),
            new ItemInfo("Portal 2"),
        ]),
        new Level("2.", [
            new ItemInfo("Portal 2"),
        ]),
        new Level("3.", [
            new ItemInfo("Portal 2"),
            new ItemInfo("Portal 2"),
        ]),
        new Level("4."),
        new Level("no vote", [
            new ItemInfo("Portal 2"),
        ]),
    ];
</script>


<div class="container">
    {#each voteGrid as level}
        <VoteGridLevel name={level.name} items={level.items}/>
    {/each}
</div>
<div class="container" use:dragStuff>
    <div draggable="true" class="box">A</div>
    <div draggable="true" class="box">B</div>
    <div draggable="true" class="box">C</div>
</div>


<style>
    .container {
        counter-reset: itemindex;
    }

    .box:before {
        content: counter(itemindex) ": ";
    }

    .box {
        counter-increment: itemindex;
        border: 3px solid #666;
        border-radius: .5em;
        padding: 10px;
        cursor: move;
    }

    .box:global(.over) {
        border: 3px dotted #666;
    }
</style>
