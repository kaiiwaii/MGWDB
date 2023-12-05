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
  let rating = selectedGame.rating;
  let hours = selectedGame.hours;
  let played_platform = selectedGame.played_platform;

  let rating_values = selectedGame.rating;
  let rating_score = selectedGame.score;

  const saveAndExit = () => {
    $showGamePopup = false;
  };
  let description_editor;


  onMount(() => {
      ClassicEditor
      .create( document.querySelector('#description_editor') , {
        
      })
      .then(newEditor => {
        newEditor.ui.view.editable.element.style.minHeight = '10rem';
        description_editor = newEditor;
        description_editor.setData(selectedGame.description || "")
        description_editor.enableReadOnlyMode( 'my-feature-id' );
      })
      .catch( error => {
          console.error( error );
      } );
      })

</script>

{#if $showGamePopup}
  <div class="fixed top-0 left-0 w-full h-full flex items-center justify-center z-20">
    <div class="absolute w-full h-full bg-black opacity-50"></div>
    <div class="relative z-10 p-4 bg-white dark:text-white dark:bg-gray-900 rounded-md shadow-md w-4/5 max-h-[90%] overflow-y-auto">
      <button class="top-0 right-5 text-white bg-blue-500 rounded-md p-2 sticky z-10" on:click={saveAndExit}>Exit</button>
      
      {#if selectedGame}
        <img src={`//images.igdb.com/igdb/image/upload/t_screenshot_big/${selectedGame.cover?.image_id}.jpg`} alt={selectedGame.name} class="mx-0 w-full object-cover h-[30vh] rounded-md" />
        <h2 class="text-xl font-semibold mt-4">{selectedGame.name}</h2>
        
        <label class="text-gray-500 dark:text-gray-200" for="description">Description:</label>
        <div id="description_editor" class="mt-2 max-h-[30%]"></div>
        
        <RatingComponent bind:ratingValues={rating_values} bind:ratingScore={rating_score}/>

        <div class="text-gray-500 dark:text-gray-200 mt-2">Hours Played: {hours}</div>

        <div class="text-gray-500 dark:text-gray-200 mt-2">Played Platform: {played_platform}</div>
        
        <p class="text-gray-500 dark:text-gray-200 mt-2">Release Date: {formatReleaseDate(selectedGame.first_release_date)}</p>
        <p class="text-gray-500 dark:text-gray-200">URL: {selectedGame.url}</p>
        <p class="text-gray-500 dark:text-gray-200">Platforms: {selectedGame.platforms?.map(p => p.abbreviation).join(', ')}</p>
        <p class="text-gray-500 dark:text-gray-200">Genres: {selectedGame.genres?.map(g => g.name).join(', ')}</p>
        <!-- Add other selectedGame details here -->
      {/if}
    </div>
  </div>
{/if}