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
                elements: {}
            }, null, "\t")
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




<div id="editor" class="flex flex-col items-center justify-center min-h-screen bg-gray-100">
    <div class="text-center">
      <h1 class="text-2xl font-bold mb-4">JSON Editor</h1>
      <object class="mx-auto" data="/template_tutorial.pdf" width="75%" height="400rem">
        <p>Unable to display PDF file. <a href="/template_tutorial.pdf">Download</a> instead.</p>
      </object>
      <div class="w-3/5 mx-auto">
        <CodeMirror
          bind:value
          lang={json()}
          styles={{
            "&": {
              "width": "60%", // Set width to 100% to fill the container
              "border": "1px solid black",
              "margin": "auto"
            }
          }}
        />
      </div>
  
      <button
        class="mt-4 px-4 py-2 bg-blue-500 text-white rounded"
        on:click={validate}
      >
        Validate
      </button>
  
      {#if RSError.length != 0}
        <div class="mt-4 p-2 bg-red-500 text-white rounded">
          {RSError}
        </div>
      {/if}
    </div>
  </div>