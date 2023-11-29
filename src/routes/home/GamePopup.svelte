<!-- GamePopup.svelte -->
<script lang="ts">
  import { type Game } from '$lib/gameModel.js';
  import {formatReleaseDate} from '$lib/utils.js'
  import { onMount } from 'svelte';
  import {showGamePopup, gameList, temporaryGames, gamesNotSaved} from './stores.js'    

  import RatingComponent from './RatingComponent.svelte';

  import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
  
  export let selectedGame: Game;

  //There's no need to have this many variables, but it's to avoid updating selectedGame (it's bound somehow?)
  let description = selectedGame.description;
  let review = selectedGame.review;
  let hours = selectedGame.hours;
  let played_platform = selectedGame.played_platform;
  //TODO:
  let review_values = selectedGame.review;
  let review_score = selectedGame.score;

  const saveAndExit = () => {
    // Call the save function
    console.log(played_platform)
    description = description_editor.getData();
    console.log(description)
    modifyGame();
    $showGamePopup = false;
  };
  let description_editor;

  function modifyGame() {

      let idx = $gameList.findIndex(g => g.id == selectedGame.id);
      if(idx != -1) {
        if(selectedGame.description != description || 
          selectedGame.review != review ||
          selectedGame.hours != hours ||
          selectedGame.played_platform != played_platform) {
            
            $gameList.splice(idx, 1)
            //hell itself
            let edited_game = selectedGame;
              edited_game.description = description
              edited_game.review = review
              edited_game.hours = hours
              edited_game.played_platform = played_platform

            $temporaryGames.push(edited_game);
            $gameList = $gameList;
            $temporaryGames = $temporaryGames;
            $gamesNotSaved = true
          }

      } else {
        let idx = $temporaryGames.findIndex(g => g.id == selectedGame.id);
        
        if(idx != -1) {
          if(selectedGame.description != description || 
            selectedGame.review != review ||
            selectedGame.hours != hours ||
            selectedGame.played_platform != played_platform) {
              //Hades himself fears this
              let edited_game = selectedGame;
              edited_game.description = description
              edited_game.review = review
              edited_game.hours = hours
              edited_game.played_platform = played_platform

              $temporaryGames[idx] = edited_game
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
        description_editor.setData(selectedGame.description)
      })
      .catch( error => {
          console.error( error );
      } );
      })

</script>

{#if $showGamePopup}
  <div class="fixed top-0 left-0 w-full h-full flex items-center justify-center">
    <div class="absolute w-full h-full bg-black opacity-50"></div>
    <div class="relative z-10 p-4 bg-white rounded-md shadow-md w-4/5 max-h-[45rem] overflow-y-auto">
      <button class="absolute top-2 right-2 text-gray-500" on:click={saveAndExit}>Save and Exit</button>
      
      {#if selectedGame}
        <img src={`//images.igdb.com/igdb/image/upload/t_screenshot_huge/${selectedGame.cover?.image_id}.jpg`} alt={selectedGame.name} class="mx-auto object-contain rounded-md" />
        <h2 class="text-xl font-semibold mt-4">{selectedGame.name}</h2>
        
        <label class="text-gray-500" for="description">Description:</label>
        <div id="description_editor" class="mt-2 max-h-[30%]"></div>
        
        <RatingComponent bind:ratingValues={review_values} bind:ratingScore={review_score}/>

        <label class="text-gray-500 mt-2" for="hours">Hours Played:</label>
        <input type="number" id="hours" class="w-full rounded-md p-2" bind:value={hours} />

        <label class="text-gray-500 mt-2" for="played_platform">Played Platform:</label>
        <select id="played_platform" class="w-full rounded-md p-2" bind:value={played_platform}>
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