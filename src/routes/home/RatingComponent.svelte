<script>
  import { onMount } from 'svelte';
  import {RatingSystem, Group, Category, Setting} from '$lib/rating/parser.js'
  import Range from '$lib/Range.svelte';

  let ratingSystem = new RatingSystem();
  let items = [];
  export let ratingScore = 0;

  let example = {
    "name": "MyRatingSystem",
    "elements": {
        "Art": {
            "weight": 40,
            "categories": {
                "Graphics": 40,
                "Animations": 40,
                "Other": 20
            }
        },
        
        "Characters": 20,

        "Music": {
            "weight": 40,
            "categories": {
                "Soundtrack": 80,
                "Effects": 20
            }
        }
    }
};

  onMount(() => {
    ratingSystem.parse(example);
    items = ratingSystem.elements;
    console.log(items)
    if(!ratingValues) {
      ratingValues = [[]]
    }
  });

  function getScoreValues(index, subindex) {
    try {
      return ratingValues[index][subindex]
    } catch {
      return 0
    }
  }

  export let ratingValues = [];

  function computeWeight(value, weight, index, subindex) {

    ratingScore = 0;
    try {
      ratingValues[index][subindex] = value * weight
    } catch {
      ratingValues[index] = []
      ratingValues[index][subindex] = value * weight
    }

    ratingValues.forEach(v => {
      v.forEach(sv => ratingScore+=sv)
    })
    console.log(ratingValues)
    
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

<main class="pt-6 bg-white mx-auto text-center">
  <h1 class="text-blue-600 text-2xl mb-4 mx-auto font-bold text-[3rem] pb-2">{Math.round(ratingScore)}</h1>
  {#each items as item, idx}
    <div id="element_container" class="w-full lg:w-[60%] mb-6 border-[3px] p-2 mx-auto">
      <h2 class="text-gray-800 text-lg mb-2 text-left">{item.name} ({item.weight}%)</h2>

      {#if isGroup(item)}
        {#each item.categories as subItem, sidx}
          <div class="flex items-center mb-4 w-full">
            <h1 class="text-gray-800 text-md mr-2">{subItem.name} ({subItem.weight}%)</h1>
            <div class="flex items-center w-[100%] lg:w-[60%]">
              <Range
                min={0}
                max={100}
                value={getScoreValues(idx, sidx)}
                on:change={(v) => computeWeight(v.detail.value, (item.weight / 100) * (subItem.weight / 100), idx, sidx)}
              />
            </div>
          </div>
        {/each}
      {:else if isCategory(item)}
        <div class="flex items-center mb-4">
          <div class="flex items-center w-[100%] lg:w-[40%]">
            <Range
              min={0}
              max={100}
              value={getScoreValues(idx, 0)}
              on:change={(v) => computeWeight(v.detail.value, item.weight / 100, idx, 0)}
            />
          </div>
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




