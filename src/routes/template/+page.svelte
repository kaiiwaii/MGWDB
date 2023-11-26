<script lang="ts">
  import { JSONEditor, Mode } from 'svelte-jsoneditor';
  import { RatingSystem } from '$lib/rating/parser.js';

  let jsonError = false;
  let content = {
    text: JSON.stringify({
        name: "MyRatingSystem",
        elements: {}
    }, null, "\t") // can be used to pass a stringified JSON document instead
  }
  function handleChange(updatedContent, previousContent, { contentErrors, patchResult }) {
    // content is an object { json: JSONValue } | { text: string }
    if(contentErrors) {
        return
    }
    console.log(updatedContent.text)
    let json = JSON.parse(updatedContent.text);
    let rs = new RatingSystem();
    try {
        rs.parse(json)
        console.log(rs.elements)
    } catch (error) {
        console.log(error)
    }
  }
</script>

<div>
  <JSONEditor bind:content 
    statusBar={false} 
    navigationBar={false} 
    mainMenuBar={false}
    onError={() => {return}}
    mode={Mode.text}
    onChange={handleChange}

  />
</div>