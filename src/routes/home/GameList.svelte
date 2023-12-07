<!-- GamesList.svelte -->
<script lang="ts">
    import { type Game, type selectedGame, SortType, SortOrder} from '$lib/gameModel.js';
    import GamePopup from './GamePopup.svelte';
    import fuzzy from 'fuzzy';
    import {librarySearchTerm, gameList, temporaryGames, showGamePopup, selectedSortType} from './stores.js'
    import ContextMenu, { Item, Divider, Settings } from "svelte-contextmenu";
    import Range from '$lib/Range.svelte';
    import DeleteDialog from './DeleteDialog.svelte';

    let ctxMenu: ContextMenu;
    let showDeleteDialog = false;
    let gameCardScale = 50;

    let selected_game= {} as selectedGame;

    function show_game_popup(game: Game) {
        selected_game.game = game;
        $showGamePopup = true;
    }

    $: filteredGameList = $gameList.length > 0 ? [...fuzzy.filter($librarySearchTerm, $gameList, {extract: (g) => g.name}).map(el => el.original)].sort((a, b) => {
      if($selectedSortType.type == SortType.Rating) {
        if($selectedSortType.order == SortOrder.Desc) {
          return b.score - a.score
        } else {
          return a.score - b.score
        }
        
      } else if ($selectedSortType.type == SortType.Name) {
        if($selectedSortType.order == SortOrder.Desc) {
          return a.name.localeCompare(b.name)
        } else {
          return b.name.localeCompare(a.name)
        }
      } else {
        if($selectedSortType.order == SortOrder.Desc) {
          return b.hours - a.hours
        } else {
          return a.hours - b.hours
        }
      }
    }) : [];

    $: filteredTemporaryGames = [...fuzzy.filter($librarySearchTerm, $temporaryGames, {extract: function(g) {return g.name}}).map(el => el.original)].sort((a, b) => b.score - a.score);

  </script>

<style>
  :root {
  --ctx-menu-font-size: 1rem;
}
</style>


<div>
  {#if $gameList.length > 0 || $temporaryGames.length > 0}

<DeleteDialog bind:showDeleteDialog {selected_game}/>
<div class="w-full mb-4 z-0">
  <Range
  min={30}
  max={100}
  bind:value={gameCardScale}
/>
</div>


<ContextMenu bind:this={ctxMenu}>
  <Item on:click={() => {showDeleteDialog = true; console.log(showDeleteDialog)}}>Remove game</Item>
  <!-- <Divider /> -->
</ContextMenu>

<div class="mt-4 flex flex-wrap content-start justify-center z-1 bg-white dark:bg-[#263244] overflow-y-auto h-screen pb-80 lg:pb-40">
  {#each filteredGameList as game, idx}
    <div class="m-2 cursor-pointer relative hover:scale-[1.15] z-1" style="height:{Math.round(374 * (gameCardScale/100))}px" on:contextmenu={(e)=> {
      //OnMount sometimes doesn't work

      selected_game.game = game;
      selected_game.index = idx
      selected_game.saved = true;
      ctxMenu.show(e)
      }} on:click={() => show_game_popup(game)}>
      <ContextMenu />
      <img src={`//images.igdb.com/igdb/image/upload/t_cover_big/${game.cover?.image_id}.jpg`} alt={game.name} class="object-cover rounded-md shadow-2xl z-0"  style="height:{Math.round(374 * (gameCardScale/100))}px" />
      <!-- <h1 style="font-size:{Math.trunc(25 * (gameCardScale/100))}px; max-width:{Math.trunc(264 * (gameCardScale/100))}px"><b>{game.name}</b></h1> -->
    </div>
  {/each}

  {#each filteredTemporaryGames as game, idx}
    <div class="m-2 cursor-pointer relative hover:scale-[1.15]" on:contextmenu={(e)=> {
      selected_game.game = game;
      selected_game.index = idx
      selected_game.saved = false;
      ctxMenu.show(e)
    }} on:click={() => show_game_popup(game)}>
      <ContextMenu />
        <img src={`//images.igdb.com/igdb/image/upload/t_cover_big/${game.cover?.image_id}.jpg`} alt={game.name} class="object-cover rounded-md shadow-md z-0" style="height:{Math.trunc(374 * (gameCardScale/100))}px"/>
        <div class="absolute inset-0 flex items-center justify-center">
            <div class="bg-red-500 p-1 rounded-full absolute top-2 left-2 cursor-pointer">
                <span class="text-white rounded-full p-1" style="background-color: inherit;">ⓘ</span>
            </div>
        </div>
    </div>
  {/each}
  {#if $showGamePopup}
      <GamePopup selectedGame={selected_game.game}/>
    {/if}
  </div>
{/if}
</div>

  
    