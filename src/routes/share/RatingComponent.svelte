<script lang="ts">
  import { onMount } from 'svelte';
  import {RatingSystem, Group, Category, Setting} from '$lib/rating/parser.js'
  import Range from '$lib/Range.svelte';
  import {ratingTemplate} from './stores.js'

  let ratingSystem = new RatingSystem();
  let invalidSystem: bool = false;
  let items = [];

  export let ratingScore = 0;

  onMount(() => {

    if($ratingTemplate == null || Object.keys($ratingTemplate).length == 0) {

      invalidSystem = true;
      return

    } else {
      ratingSystem.parse(JSON.parse($ratingTemplate));
      items = ratingSystem.elements;
      
      ratingScore=0;
      if(typeof ratingValues == "string") {    
        ratingValues = JSON.parse(ratingValues)
      }
      getAllValues(ratingValues).forEach(sv => ratingScore+=sv)      
    }
  });

  function getScoreValues(key, subkey) {
    try {
      if(subkey) {
        return ratingValues[key][subkey]
      } else {
        return ratingValues[key] || 0
      }
    } catch {
      return 0
    }
  }

  export let ratingValues;

  function computeWeight(value, weight, key, subkey) {
    ratingScore = 0;
    try {
      if(subkey) {
        //ratingValues[key] = {}
        ratingValues[key][subkey]=Math.round(value * weight)
        console.log(ratingValues)
      } else {
        ratingValues[key] = Math.round(value * weight)
      }
    } catch {
      ratingValues[key] = []
      ratingValues[key][subkey] = Math.round(value * weight)
    }

    getAllValues(ratingValues).forEach(sv => ratingScore+=sv)
    
  }

  function getAllValues(obj) {
  let values = [];

  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      const value = obj[key];

      if (typeof value === 'object' && value !== null) {
        // If the value is an object (including subdicts), recursively call the function
        values = values.concat(getAllValues(value));
      } else {
        // Otherwise, add the value to the array
        values.push(value);
      }
    }
  }

  return values;
}

  function isGroup(item) {
    return item instanceof Group;
  }

  function isCategory(item) {
    return item instanceof Category;
  }

  function isSetting(item) {
    return item instanceof Setting;
  }
</script>

{#if !invalidSystem}
<main class="pt-6 bg-white mx-auto text-center dark:bg-gray-900">
  <h1 class="text-blue-600 text-2xl mb-4 mx-auto font-bold text-[3rem] pb-2">{Math.round(ratingScore)}</h1>
  {#each items as item}
    <div id="element_container" class="w-full lg:w-[60%] mb-6 border-[3px] p-2 mx-auto">
      <h2 class="text-gray-800 dark:text-gray-100 text-lg mb-2 text-left">{item.name} ({item.weight}%)</h2>

      {#if isGroup(item)}
        {#each item.categories as subitem}
          <div class="flex items-center mb-4 w-full text-gray-800 dark:text-gray-100">
            <h1 class="text-md mr-2">{subitem.name} ({subitem.weight}%)</h1>
            <div style="pointer-events: none;" class="flex items-center w-[100%] lg:w-[60%]">
              <Range
                min={0}
                max={100}
                value={Math.round(getScoreValues(item.name, subitem.name) / ((item.weight/100) * (subitem.weight/100)))}
                on:change={(v) => computeWeight(v.detail.value, (item.weight / 100) * (subitem.weight / 100), item.name, subitem.name)}
              />
            </div>
            <span>{Math.round(getScoreValues(item.name, subitem.name) / ((item.weight/100) * (subitem.weight/100)))}</span>
          </div>
        {/each}
      {:else if isCategory(item)}
        <div class="flex items-center mb-4 dark:text-gray-100">
          <div style="pointer-events: none;" class="flex items-center w-[100%] lg:w-[40%]">
            <Range
              min={0}
              max={100}
              value={getScoreValues(item.name, null) / (item.weight/100)}
              on:change={(v) => computeWeight(v.detail.value, item.weight / 100, item.name, 0)}
            />
          </div>
          <span>{getScoreValues(item.name, null) / (item.weight/100)}</span>
        </div>
      {:else if isSetting(item)}
        <div class="flex items-center mb-4">
          <label class="flex items-center">
            <input type="checkbox" bind:checked={item.value} class="mr-2" />
            <span class="text-gray-800">{item.name}</span>
          </label>
        </div>
{/if}
    </div>
  {/each}
</main>
{:else}
<h1 class="text-xl mb-4 mx-auto font-bold text-[3rem] p-5">Please configure your rating system to add scores</h1>
{/if}