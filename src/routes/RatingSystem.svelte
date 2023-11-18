<script lang="ts">
  import { RatingSystem, Group, Category, Setting } from '$lib/rating/parser.js';
  
  export let ratingSystem: RatingSystem;

  function formatWeight(weight: number): string {
    const formattedWeight = `${weight}%`;
    return formattedWeight;
  }

  let globalWeightError = false;
  let localWeightError = false;
  let localWeightErrorValue = '';

  function handleWeightChange() {
    try {
      globalWeightError = false;
      localWeightError = false;
      
      // Call check_global_weights and store the result in groups
      let groups = ratingSystem.check_global_weights();
      ratingSystem.check_local_weights(groups);
      
    } catch (error) {
      console.error('Weight check error:', error);

      if (error.name === "GlobalWeightError") {
        globalWeightError = true;
        localWeightError = false;
      } else if (error.name === "LocalWeightError") {
        globalWeightError = false;
        localWeightError = true;
        localWeightErrorValue = error.value;
      }
    }
}
</script>

<style>
  .rating-system {
    font-family: 'Arial', sans-serif;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    margin: 20px 0;
    transition: background-color 0.3s ease, border-color 0.3s ease;
    border-color: #ccc; /* Red border for global error */
  }

  .error-container {
    background-color: #ffcdd2; /* Light red color for error state */
  }

  .single_category, .group {
    margin-bottom: 20px;
  }

  .group-header,
  .category,
  .single_category,
  .setting {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
  }

  .weight-name,
  .slider,
  .checkbox {
    margin-right: 10px;
  }
</style>

<div class:error-container={globalWeightError} class="rating-system">
  {#if ratingSystem}
    <h1>{ratingSystem.name}</h1>

    {#each ratingSystem.elements as element (element.name)}
      {#if element && element instanceof Group}
        <div class="group">
          <h2 class="group-header">
            {element.name}
            <input style="margin-left: 2rem;"
              bind:value={element.weight}
              type="range"
              min="0"
              max="100"
              class="slider"
              on:input={() => handleWeightChange()}
            />
            <span>{formatWeight(element.weight)}</span>
          </h2>

          {#each element.categories as category (category.name)}
            <div class="category">
              <span class="category-name">{category.name}</span>
              <input
                bind:value={category.weight}
                type="range"
                min="0"
                max="100"
                class="slider"
                on:input={() => handleWeightChange()}
              />
              <span>{formatWeight(category.weight)}</span>
            </div>
          {/each}
        </div>
      {/if}

      {#if element && element instanceof Category}
        <div class="single_category">
          <h2 class="category-name">{element.name}</h2>
          <input
            bind:value={element.weight}
            type="range"
            min="0"
            max="100"
            class="slider"
            on:input={() => handleWeightChange()}
          />
          <span>{formatWeight(element.weight)}</span>
        </div>
      {/if}

      {#if element && element instanceof Setting}
        <div class="setting">
          <label>
            <input
              bind:checked={element.value}
              type="checkbox"
              class="checkbox"
              on:change={() => handleWeightChange()}
            />
            {element.name}
          </label>
        </div>
      {/if}
    {/each}
  {/if}
</div>

