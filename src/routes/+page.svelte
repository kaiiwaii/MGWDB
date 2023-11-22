
<script lang="ts">
    import Popup from './SearchPopup.svelte';
    import GameList from './GameList.svelte';
    import {type Game} from '$lib/gameModel.js'
    import {onMount} from 'svelte';
    
    onMount(() => {
        //TODO:Fetch games from both apis and put them in gameList and addedGamesIds
    });

    let showSearchPopup: boolean = false;
    let gamesNotSaved: boolean = false;
    let searchTerm: string = "";

    let temporaryGames: Game[] = [];

    let addedGamesIds: number[] = [];
    let gameList: Game[] = [];

    const toggleSearchPopup = () => {
        showSearchPopup = !showSearchPopup;
    };

    function applyGames() {
        //TODO: send request with games to server
        gameList.push(...temporaryGames)
        temporaryGames.length = 0;
        gameList = gameList;
        
    }

</script>

<style>
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@500&display=swap');

    @tailwind base;
    @tailwind components;
    @tailwind utilities;

    #logo-text {
        font-family: Kanit;
        color: blueviolet;
        font-size: 50px;
        font-weight: 700;
    }
</style>

<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Navbar con Tailwind</title>
</head>
<body class="bg-gray-100">
    <nav class="bg-blue-500 p-4">
        <div class="container mx-auto flex items-center">
            <!-- Logo a la izquierda con margen -->
            <div class="mr-4">
                <img src="tu_logo.png" alt="Logo" class="h-8">
            </div>

            <!-- Barra de búsqueda en el centro con margen y padding -->
            <div class="flex-grow">
                <input type="search" placeholder="Buscar..." bind:value={searchTerm} class="px-4 py-2 w-1/2 mx-auto block rounded-md border border-gray-300 focus:outline-none focus:border-blue-700">
            </div>
            {#if gamesNotSaved}
            <div class="mr-4">
                <button on:click={applyGames} class="bg-red-500 text-white px-4 py-2 rounded-md z-10">Save games</button>
            </div>
            {/if}
            <!-- Botón "+ Add Game" con margen y padding -->
            <div class="mr-4">
                <button on:click={toggleSearchPopup} class="bg-green-500 text-white px-4 py-2 rounded-md z-10">+ Add Game</button>
            </div>

            <!-- Foto de perfil con dropdown -->
            <div class="relative">
                <img src="tu_foto_de_perfil.jpg" alt="Perfil" class="h-8 w-8 rounded-full cursor-pointer">
                <div class="absolute right-0 mt-2 w-48 bg-white border rounded-md shadow-lg hidden">
                    <a href="#" class="block px-4 py-2 text-gray-800 hover:bg-blue-500 hover:text-white">Perfil</a>
                    <a href="#" class="block px-4 py-2 text-gray-800 hover:bg-blue-500 hover:text-white">Ajustes de cuenta</a>
                    <a href="#" class="block px-4 py-2 text-gray-800 hover:bg-blue-500 hover:text-white">Cerrar sesión</a>
                </div>
            </div>
        </div>
    </nav>
    <Popup 
        bind:showPopup={showSearchPopup} 
        bind:gamesToAdd={temporaryGames}
        bind:addedGamesIds={addedGamesIds}
        bind:gamesNotSaved={gamesNotSaved}
    />
    <GameList {gameList} {temporaryGames} bind:searchTerm={searchTerm} />
</body>
</html>

