<script lang="ts">
  import { RatingSystem, Group, Category, Setting } from '$lib/rating/parser.js';
  
  export let ratingSystem: RatingSystem;

  function formatWeight(weight: number): string {
    const formattedWeight = `${weight}%`;
    return formattedWeight;
  }

  let weightCheckError = false;

  function handleWeightChange() {
    try {
      ratingSystem.check_weights();
      weightCheckError = false;
    } catch (error) {
      console.error('Weight check error:', error);
      weightCheckError = true;
      // Handle the error as needed
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
    transition: background-color 0.3s ease;
  }

  .error-container {
    background-color: #ffcdd2; /* Light red color for error state */
  }

  .group {
    margin-bottom: 15px;
  }

  .category {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
  }

  .category-name {
    flex: 1;
    margin-right: 10px;
  }

  .slider {
    width: 200px;
    margin-right: 10px;
  }
</style>

<div class:error-container={weightCheckError} class="rating-system">
  {#if ratingSystem}
    <h1>{ratingSystem.name}</h1>

    {#each ratingSystem.elements as element (element.name)}
      {#if element && element instanceof Group}
        <div class="group">
          <h2>{element.name}</h2>
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
        <div class="category">
          <span class="category-name">{element.name}</span>
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
    {/each}
  {/if}
</div>
