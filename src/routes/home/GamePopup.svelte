<!-- GamePopup.svelte -->
<script lang="ts">
  import { type Game } from '$lib/gameModel.js';
  import {formatReleaseDate} from '$lib/utils.js'
  import { onMount } from 'svelte';
  import {showGamePopup, gameList, temporaryGames, gamesNotSaved} from './stores.js'
  import { DateInput } from 'date-picker-svelte';

  import RatingComponent from './RatingComponent.svelte';

  import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
  
  export let selectedGame: Game;
  console.log(selectedGame)

  let selectedCopy = Object.assign({}, selectedGame)

  //Why is this still needed
  let date_from = selectedCopy.date_range.from;
  let date_to = selectedCopy.date_range.to;

  const saveAndExit = () => {

    selectedCopy.description = description_editor.getData();
    selectedCopy.date_range = {from: date_from, to: date_to}
    console.log(selectedCopy.date_range)
    console.log(selectedGame.date_range)

    modifyGame();
    $showGamePopup = false;


  };
  let description_editor;

  function modifyGame() {

      let idx = $gameList.findIndex(g => g.id == selectedGame.id);
    console.log(JSON.stringify(selectedCopy), "\n", JSON.stringify(selectedGame));
      if(idx != -1) {
        let srating = selectedCopy.rating ? JSON.stringify(selectedCopy.rating, function replacer(key, value) {
          if (Array.isArray(value) && value.length === 0) {
            return { ...value }; // Converts empty array with string properties into a POJO
          }
          return value;
        }): "";
        if(typeof selectedGame.rating == "string") {
          selectedGame.rating = JSON.parse(selectedGame.rating);
        }
        if(JSON.stringify(selectedCopy) != JSON.stringify(selectedGame)) {

            $gameList.splice(idx, 1)
            $temporaryGames.push(selectedCopy);

            $gameList = $gameList;
            $temporaryGames = $temporaryGames;
            $gamesNotSaved = true;
          }

      } else {
        let idx = $temporaryGames.findIndex(g => g.id == selectedGame.id);
        
        if(idx != -1) {
          let srating = selectedCopy.rating ? JSON.stringify(selectedCopy.rating, function replacer(key, value) {
          if (Array.isArray(value) && value.length === 0) {
            return { ...value }; // Converts empty array with string properties into a POJO
          }
          return value;
        }) : "";

          if(JSON.stringify(selectedCopy) != JSON.stringify(selectedGame)) {

              $temporaryGames[idx] = selectedCopy;
              $gameList = $gameList;
              $temporaryGames = $temporaryGames;
            }
        }
  }      
  }
  onMount(() => {
    
      ClassicEditor
      .create( document.querySelector('#description_editor') , {
        
      })
      .then(newEditor => {
        newEditor.ui.view.editable.element.style.minHeight = '10rem';
        description_editor = newEditor;
        description_editor.setData(selectedGame.description || "")
      })
      .catch( error => {
          console.error( error );
      } );
      })

</script>

<style>
  :root {
    --date-picker-background: rgb(192, 192, 192);
  }
</style>

{#if $showGamePopup}
  <div class="fixed top-0 left-0 w-full h-full flex items-center justify-center z-20">
    <div class="absolute w-full h-full bg-black opacity-50"></div>
    <div class="relative z-10 p-4 bg-white dark:text-white dark:bg-gray-900 rounded-md shadow-md w-4/5 max-h-[90%] overflow-y-auto">
      <button class="top-0 mb-3 text-white bg-blue-500 rounded-md p-2 sticky z-10" on:click={saveAndExit}>Save and Exit</button>
      
      {#if selectedGame}
        <img src={`//images.igdb.com/igdb/image/upload/t_screenshot_big/${selectedGame.cover?.image_id}.jpg`} alt={selectedGame.name} class="mx-0 w-full object-cover h-[30vh] rounded-md" />
        <h2 class="text-xl font-semibold mt-4">{selectedGame.name}</h2>
        
        <label class="text-gray-500 dark:text-gray-200" for="description">Description:</label>
        <div id="description_editor" class="mt-2 max-h-[30%] --ck-color-base-background: #000"></div>
        
        <RatingComponent bind:ratingValues={selectedCopy.rating} bind:ratingScore={selectedCopy.score}/>

        <label class="text-gray-500 dark:text-gray-200 mt-2" for="hours">Hours Played:</label>
        <input type="number" id="hours" class="w-full rounded-md p-2 dark:bg-gray-900" bind:value={selectedCopy.hours} />

        <div class="flex flex-wrap items-center mt-2 pb-1">
          <label class="text-gray-500 dark:text-gray-200" for="date_from">Start Date:</label>
          <DateInput format="dd-MM-yyyy" bind:value={date_from} class="ml-2 dark:dp-dark" />
        
          <label class="text-gray-500 dark:text-gray-200 ml-2" for="date_to">End Date:</label>
          <DateInput format="dd-MM-yyyy" bind:value={date_to} class="ml-2" />
        </div>
      

        <label class="text-gray-500 mt-2 dark:text-gray-200" for="played_platform">Played Platform:</label>
        <select id="played_platform" class="w-full rounded-md p-2 dark:bg-dark-200" bind:value={selectedCopy.played_platform}>
          {#if selectedGame.platforms}
            {#each selectedGame.platforms?.map(p => p) as platform}
              <option value={platform.id}>
                {platform.abbreviation}
              </option>
            {/each}
          {:else}
          <option value={-1}>
            No data
          </option>
          {/if}        
        </select>
        
        <p class="text-gray-500 mt-2">Release Date: {formatReleaseDate(selectedGame.first_release_date)}</p>
        <p class="text-gray-500">URL: {selectedGame.url}</p>
        <p class="text-gray-500">Platforms: {selectedGame.platforms?.map(p => p.abbreviation).join(', ')}</p>
        <p class="text-gray-500">Genres: {selectedGame.genres?.map(g => g.name).join(', ')}</p>
        <!-- Add other selectedGame details here -->
      {/if}
    </div>
  </div>
{/if}