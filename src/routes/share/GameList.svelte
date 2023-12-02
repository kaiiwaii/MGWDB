<!-- GamesList.svelte -->
<script lang="ts">
    import { type Game, type selectedGame} from '$lib/gameModel.js';
    import GamePopup from './GamePopup.svelte';
    import fuzzy from 'fuzzy';
    import {librarySearchTerm, gameList, temporaryGames, showGamePopup} from './stores.js'
    import ContextMenu, { Item, Divider, Settings } from "svelte-contextmenu";
    import Range from '$lib/Range.svelte';

    let gameCardScale = 50;

    let selected_game= {} as selectedGame;

    function show_game_popup(game: Game) {
        selected_game.game = game;
        $showGamePopup = true;
    }


    $: filteredGameList = fuzzy.filter($librarySearchTerm, $gameList, {extract: (g) => g.name || ""}).map(el => el.original)

  </script>

<style>
  :root {
  --ctx-menu-font-size: 1rem;
}
</style>


<div>
  {#if $gameList.length > 0 || $temporaryGames.length > 0}

<Range
  min={30}
  max={100}
  bind:value={gameCardScale}
/>

<div class="mt-4 flex flex-wrap justify-center z-0 bg-white">
  {#each filteredGameList as game, idx}
    <div class="m-4 cursor-pointer relative hover:scale-[1.15]" on:click={() => show_game_popup(game)}>
      <img src={`//images.igdb.com/igdb/image/upload/t_cover_big/${game.cover?.image_id}.jpg`} alt={game.name} class="object-cover rounded-md shadow-md z-0" style="height:{Math.trunc(374 * (gameCardScale/100))}px" />
      <h1 style="font-size:{Math.trunc(25 * (gameCardScale/100))}px; max-width:{Math.trunc(264 * (gameCardScale/100))}px"><b>{game.name}</b></h1>
    </div>
  {/each}

  {#if $showGamePopup}
      <GamePopup selectedGame={selected_game.game}/>
    {/if}
  </div>
{/if}
</div>

  
    