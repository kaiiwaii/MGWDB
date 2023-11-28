<script lang="ts">
  import CodeMirror from "svelte-codemirror-editor";
import { json } from "@codemirror/lang-json";
  import { RatingSystem } from '$lib/rating/parser.js';
  import { onMount } from "svelte";
  import { reviewTemplate } from '../home/stores.js';
  import { get } from "svelte/store";

  let RSError = "";
  $: value = "";

    onMount(() => {
        let rt = get(reviewTemplate)
        if(rt != "") {
            value = rt
        } else {
            value = JSON.stringify({
                name: "MyRatingSystem",
                elements: {
                }
            }, null, "\t") + "\n".repeat(12)
        }
        
    })

    function validate() {
        RSError = "";
        try {
            let rs = new RatingSystem()
            //console.log(value)
            rs.parse(JSON.parse(value))
            //console.log(rs.elements);
            let groups = rs.check_global_weights()
            rs.check_local_weights(groups)
            console.log(rs.elements)
            fetch(`http://127.0.0.1:4321/addtemplate`, {
                method: "POST",
                body: JSON.stringify({template: value}),
                credentials: "include",
            });
        } catch (error) {
            if(error.message) {
                RSError = error.message
            } else {
                RSError = error
            }
        }
        
    }
</script>

<style>
    @tailwind base;
    @tailwind components;
    @tailwind utilities;
</style>

<div id="editor" class="flex flex-col items-center min-h-screen bg-gray-100 mt-10">
  <div class="text-center w-3/4">
    <h1 class="text-3xl font-bold mb-4">Review Template Editor</h1>
    <!-- <object class="mx-auto" data="/template_tutorial.pdf" width="80%" height="500rem">
      <p>Unable to display PDF file. <a href="/template_tutorial.pdf">Download</a> instead.</p>
    </object> -->
    <a class="mb-16" href="/template_tutorial.pdf"><b>See tutorial</b></a>
    <div class="w-3/5 mx-auto border border-black text-left">
      <CodeMirror
        bind:value
        lang={json()}
        class="w-full"
      />
    </div>

    <button class="mt-4 px-6 py-3 bg-blue-500 text-white rounded" on:click={validate}>
      Validate
    </button>

    {#if RSError.length != 0}
      <div class="mt-4 p-3 bg-red-500 text-white rounded">
        {RSError}
      </div>
    {/if}
  </div>
</div>
