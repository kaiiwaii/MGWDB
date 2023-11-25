<!-- GamesList.svelte -->
<script lang="ts">
    import { type Game } from '$lib/gameModel.js';
    import GamePopup from './GamePopup.svelte';
    import fuzzy from 'fuzzy';

    
    export let searchTerm: string = '';
    export let gameList: Game[] = [];
    export let temporaryGames: Game[] = [];
    export let show_game_popup: boolean = false;

    let selectedGame: Game;

    function showGamePopup(game: Game) {
        selectedGame = game;
        show_game_popup = true;
    }
    console.log(gameList)
    console.log(temporaryGames)


    $: filteredGameList = fuzzy.filter(searchTerm, gameList, {extract: function(g) {return g.name}}).map(el => el.original)

    $: filteredTemporaryGames = fuzzy.filter(searchTerm, temporaryGames, {extract: function(g) {return g.name}}).map(el => el.original)

    $:console.log(`GL: ${JSON.stringify(filteredGameList)}  //  TL: ${JSON.stringify(filteredTemporaryGames)}`)
  </script>


{#if gameList.length > 0 || temporaryGames.length > 0}
<div class="mt-4 flex flex-wrap justify-center z-0">
  {#each filteredGameList as game}
    <div class="m-4 cursor-pointer relative" on:click={() => showGamePopup(game)}>
      <img src={`//images.igdb.com/igdb/image/upload/t_cover_big/${game.cover?.image_id}.jpg`} alt={game.name} class="h-32 w-32 object-cover rounded-md shadow-md" />
    </div>
  {/each}

  {#each filteredTemporaryGames as game}
    <div class="m-4 cursor-pointer relative" on:click={() => showGamePopup(game)}>
        <img src={`//images.igdb.com/igdb/image/upload/t_cover_big/${game.cover?.image_id}.jpg`} alt={game.name} class="h-32 w-32 object-cover rounded-md shadow-md" />
        <div class="absolute inset-0 flex items-center justify-center">
            <div class="bg-red-500 p-1 rounded-full absolute top-2 left-2 cursor-pointer">
                <span class="text-white rounded-full p-1" style="background-color: inherit;">ⓘ</span>
                <!-- <div class="hidden bg-white p-1 group-hover:block text-yellow-500 absolute top-8 left-0 rounded-full">
                    <span>Not Saved</span>
                </div> -->
            </div>
        </div>
    </div>
  {/each}
  {#if show_game_popup}
      <GamePopup bind:visible={show_game_popup} bind:temporaryGames={temporaryGames} bind:gameList={gameList} game={selectedGame}/>
    {/if}
  </div>
{/if}

  
    