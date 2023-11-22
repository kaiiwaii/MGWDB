<!-- GamesList.svelte -->
<script lang="ts">
    import { type Game } from '$lib/gameModel.js';
    import GamePopup from './GamePopup.svelte';
    import levenshtein from 'js-levenshtein';
    
    export let searchTerm: string = '';
    export let gameList: Game[] = [];
    export let temporaryGames: Game[] = [];
    export let show_game_popup: boolean = false;

    let selectedGame: Game;

    function showGamePopup(game: Game) {
        selectedGame = game;
        show_game_popup = true;
    }

    $: filteredGameList = gameList.map(game => {
        if(levenshtein(searchTerm, game.name) <= 3) {
            return game
        }
    });

    $: filteredTemporaryGames = temporaryGames.map(game => {
        if(levenshtein(searchTerm, game.name) <= 3) {
            return game
        }
    });

  </script>
  
  <div class="mt-4 flex flex-wrap justify-center z-0">
    {#each filteredGameList as game (game.id)}
      <div class="m-4 cursor-pointer relative" on:click={() => showGamePopup(game)}>
        <img src={game.cover.url} alt={game.name} class="h-32 w-32 object-cover rounded-md shadow-md" />
      </div>
    {/each}
  
    {#each filteredTemporaryGames as game (game.id)}
      <div class="m-4 cursor-pointer relative" on:click={() => showGamePopup(game)}>
        <img src={game.cover.url} alt={game.name} class="h-32 w-32 object-cover rounded-md shadow-md" />
        <!-- Display 'NOT APPLIED' for games in temporaryGames -->
        {#if temporaryGames.find(tempGame => tempGame.id === game.id)}
          <div class="absolute inset-0 flex items-center justify-center">
            <span class="text-red-500 font-semibold">NOT APPLIED</span>
          </div>
        {/if}
      </div>
    {/each}
  
    {#if show_game_popup}
      <GamePopup bind:visible={show_game_popup} bind:gameList={gameList} game={selectedGame}/>
    {/if}
  </div>
  
  <style>
    /* Add your styling here */
  </style>