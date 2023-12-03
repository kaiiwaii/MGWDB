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

  let selectedCopy = {... selectedGame};

  const saveAndExit = () => {
    // Call the save function
    selectedCopy.description = description_editor.getData();
    modifyGame();
    $showGamePopup = false;

  };
  let description_editor;

  function modifyGame() {

      let idx = $gameList.findIndex(g => g.id == selectedGame.id);

      if(idx != -1) {
        let srating = selectedCopy.rating ? JSON.stringify(selectedCopy.rating, function replacer(key, value) {
          if (Array.isArray(value) && value.length === 0) {
            return { ...value }; // Converts empty array with string properties into a POJO
          }
          return value;
        }): "";

        console.log(JSON.stringify(selectedGame))
        console.log(JSON.stringify(selectedCopy))
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
        console.log(srating)
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

{#if $showGamePopup}
  <div class="fixed top-0 left-0 w-full h-full flex items-center justify-center">
    <div class="absolute w-full h-full bg-black opacity-50"></div>
    <div class="relative z-10 p-4 bg-white rounded-md shadow-md w-4/5 max-h-[90%] overflow-y-auto">
      <button class="top-0 right-5 text-white bg-blue-500 rounded-md p-2 sticky z-10" on:click={saveAndExit}>Save and Exit</button>
      
      {#if selectedGame}
        <img src={`//images.igdb.com/igdb/image/upload/t_screenshot_big/${selectedGame.cover?.image_id}.jpg`} alt={selectedGame.name} class="mx-0 w-full object-cover h-[30vh] rounded-md" />
        <h2 class="text-xl font-semibold mt-4">{selectedGame.name}</h2>
        
        <label class="text-gray-500" for="description">Description:</label>
        <div id="description_editor" class="mt-2 max-h-[30%]"></div>
        
        <RatingComponent bind:ratingValues={selectedCopy.rating} bind:ratingScore={selectedCopy.score}/>

        <label class="text-gray-500 mt-2" for="hours">Hours Played:</label>
        <input type="number" id="hours" class="w-full rounded-md p-2" bind:value={selectedCopy.hours} />
        <DateInput format="dd-MM-yyyy" bind:value={selectedCopy.date_range.from} />
        <DateInput format="dd-MM-yyyy" bind:value={selectedCopy.date_range.to} />
        

        <label class="text-gray-500 mt-2" for="played_platform">Played Platform:</label>
        <select id="played_platform" class="w-full rounded-md p-2" bind:value={selectedCopy.played_platform}>
          {#each selectedGame.platforms?.map(p => p) as platform}
			    <option value={platform.id}>
				    {platform.abbreviation}
			    </option>
		{/each}        
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