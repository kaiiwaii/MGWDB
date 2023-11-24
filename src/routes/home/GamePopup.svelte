<!-- GamePopup.svelte -->
<script lang="ts">
    import { type Game } from '$lib/gameModel.js';
    import {formatReleaseDate} from '$lib/utils.js'
  
    export let visible: boolean = false;
    export let game: Game;
    export let gameList: Game[];


    const saveAndExit = () => {
      // Call the save function
      modifyGame(game);
      visible = false;
    };

    function modifyGame(game: Game) {
        //find game in gameList
        let idx = gameList.findIndex(g => g.id == game.id);
        //update game
        gameList[idx] = game;
        //update gameList
        gameList = gameList;
    }

  </script>
  
  {#if visible}
    <div class="fixed top-0 left-0 w-full h-full flex items-center justify-center">
      <div class="absolute w-full h-full bg-black opacity-50"></div>
      <div class="relative z-10 p-4 bg-white rounded-md shadow-md w-4/5 max-h-[45rem] overflow-y-auto">
        <button class="absolute top-2 right-2 text-gray-500" on:click={saveAndExit}>Save and Exit</button>
        {#if game}
          <img src={`//images.igdb.com/igdb/image/upload/t_cover_big/${game.cover?.image_id}.jpg`} alt={game.name} class="mx-auto h-64 object-cover rounded-md" />
          <h2 class="text-xl font-semibold mt-4">{game.name}</h2>
          
          <label for="description" class="text-gray-500">Description:</label>
          <textarea id="description" class="w-full rounded-md p-2 mt-2" bind:value={game.description}></textarea>
          
          <label for="review" class="text-gray-500 mt-2">Review:</label>
          <textarea id="review" class="w-full rounded-md p-2" bind:value={game.review}></textarea>
  
          <label for="hours" class="text-gray-500 mt-2">Hours Played:</label>
          <input type="text" id="hours" class="w-full rounded-md p-2" bind:value={game.hours} />
  
          <label for="played_platform" class="text-gray-500 mt-2">Played Platform:</label>
          <textarea id="played_platform" class="w-full rounded-md p-2" bind:value={game.played_platform}></textarea>
          
          <p class="text-gray-500 mt-2">Release Date: {formatReleaseDate(game.first_release_date)}</p>
          <p class="text-gray-500">URL: {game.url}</p>
          <p class="text-gray-500">Platforms: {game.platforms?.map(p => p.abbreviation).join(', ')}</p>
          <p class="text-gray-500">Genres: {game.genres?.map(g => g.name).join(', ')}</p>
          <!-- Add other game details here -->
        {/if}
      </div>
    </div>
  {/if}
  
  <style>
    /* Add your styling here */
  </style>