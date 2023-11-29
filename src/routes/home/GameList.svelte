<!-- GamesList.svelte -->
<script lang="ts">
    import { type Game } from '$lib/gameModel.js';
    import GamePopup from './GamePopup.svelte';
    import fuzzy from 'fuzzy';
    import {librarySearchTerm, gameList, temporaryGames, showGamePopup} from './stores.js'

    let selectedGame: Game;
    $: console.log($gameList);
    $: console.log($temporaryGames);

    function show_game_popup(game: Game) {
        selectedGame = game;
        $showGamePopup = true;
    }


    $: filteredGameList = fuzzy.filter($librarySearchTerm, $gameList, {extract: function(g) {return g.name}}).map(el => el.original)

    $: filteredTemporaryGames = fuzzy.filter($librarySearchTerm, $temporaryGames, {extract: function(g) {return g.name}}).map(el => el.original)

  </script>


{#if $gameList.length > 0 || $temporaryGames.length > 0}
<div class="mt-4 flex flex-wrap justify-center z-0 bg-white">
  {#each filteredGameList as game}
    <div class="m-4 cursor-pointer relative" on:click={() => show_game_popup(game)}>
      <img src={`//images.igdb.com/igdb/image/upload/t_cover_big/${game.cover?.image_id}.jpg`} alt={game.name} class="object-cover h-[187px] rounded-md shadow-md" />
    </div>
  {/each}

  {#each filteredTemporaryGames as game}
    <div class="m-4 cursor-pointer relative" on:click={() => show_game_popup(game)}>
        <img src={`//images.igdb.com/igdb/image/upload/t_cover_big/${game.cover?.image_id}.jpg`} alt={game.name} class="object-cover h-[187px] rounded-md shadow-md" />
        <div class="absolute inset-0 flex items-center justify-center">
            <div class="bg-red-500 p-1 rounded-full absolute top-2 left-2 cursor-pointer">
                <span class="text-white rounded-full p-1" style="background-color: inherit;">ⓘ</span>
            </div>
        </div>
    </div>
  {/each}
  {#if $showGamePopup}
      <GamePopup {selectedGame}/>
    {/if}
  </div>
{/if}

  
    