<script lang="ts">
    import Popup from "./SearchPopup.svelte";
    import GameList from "./GameList.svelte";
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";

    const VITE_API_URL= import.meta.env.VITE_API_URL
    import {
        gameList,
        gamesNotSaved,
        isSavingGames,
        librarySearchTerm,
        showSearchPopup,
        temporaryGames,
        ratingTemplate
    } from "./stores.js";
    import { Game } from "$lib/gameModel.js";

    export let games = [];

    const toggleSearchPopup = () => {
        $showSearchPopup = !$showSearchPopup;
    };
    let showProfileDropdown = false;
    const toggleProfileDropdown = () => {
        showProfileDropdown = !showProfileDropdown;
    };

    let loaded;

    async function loadAll() {
        let res = await fetch(`${import.meta.env.VITE_API_URL}/mygames`, {
        credentials: "include",
        method: "GET"
    })
        if(res.status == 401) {
        goto("/login")
        return
        } else {
            let data = await res.json()
            console.log(data["games"])
            for(let game of data["games"]) {
                console.log(game)
                games.push(new Game(game));
            }    
            ratingTemplate.set(data["template"])
    }
        $gameList = games && games.length > 0 ? games : [];
    }

    onMount(() => loaded = loadAll());

    function logOut() {
        document.cookie =
            "token" +
            "=; Path=/; Domain=mghdb.com ; SameSite=None; Expires=Thu, 01 Jan 1970 00:00:01 GMT;";
        goto("/login");
    }

    function applyGames() {

        $isSavingGames = true;
        try {
            fetch(`${VITE_API_URL}/addgames`, {
                method: "POST",
                body: JSON.stringify($temporaryGames),
                credentials: "include",
            });
            $gameList.push(...$temporaryGames);
            $gameList = $gameList;
            $temporaryGames.length = 0;
            $gamesNotSaved = false;
            $isSavingGames = false;
        } catch (error) {
            console.log(error);
            alert("Error saving games");
            $isSavingGames = false;
        }
    }
</script>

<svelte:head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>MGWDB</title>
</svelte:head>


<main class="h-screen dark:bg-gray-800 bg-white m-0">
    {#await loaded}
    <body class="flex justify-center items-center h-screen bg-gray-100 dark:bg-gray-800">
        <div class="animate-spin rounded-full h-16 w-16 border-t-5 border-blue-500 border-r-4 border-b-4 border-gray-300"></div>
      </body>
    {:then}
    <body class="bg-white dark:bg-gray-800 border-color-gray-800 h-screen p-2">
        <nav class="dark:bg-blue-800 bg-blue-500 p-4 m-2 rounded-full">
            <div
                class="container mx-auto flex flex-col md:flex-row items-center"
            >
                <!-- Logo a la izquierda con margen -->
                <div class="mr-4 mb-4 md:mb-0">
                    <img src="tu_logo.png" alt="Logo" class="h-8" />
                </div>

                <!-- Barra de búsqueda en el centro con margen y padding -->
                <div class="flex-grow w-full md:w-1/2 md:mr-4 mb-4 md:mb-0">
                    <input
                        type="search"
                        placeholder="Search..."
                        bind:value={$librarySearchTerm}
                        class="px-4 py-2 w-full lg:max-w-[50%] mx-auto block rounded-md border dark:bg-gray-500 border-gray-300 focus:outline-none focus:border-blue-700"
                    />
                </div>

                <!-- Botones en una fila con espacio entre ellos -->
                <div class="flex mb-4 md:mb-0 md:ml-4">
                    {#if $gamesNotSaved}
                        <div
                            class="{$isSavingGames
                                ? 'opacity-50 cursor-not-allowed'
                                : ''} mr-4"
                        >
                            <button
                                on:click={applyGames}
                                disabled={$isSavingGames}
                                class="bg-red-500 dark:bg-red-800 text-white px-4 py-2 rounded-md z-10"
                            >
                                {$isSavingGames ? "Saving..." : "Save games"}
                            </button>
                        </div>
                    {/if}

                    <!-- Botón "+ Add Game" con margen y padding -->
                    <div class="mr-4">
                        <button
                            on:click={toggleSearchPopup}
                            disabled={$isSavingGames}
                            class="{$isSavingGames
                                ? 'bg-gray-500 cursor-not-allowed'
                                : 'bg-green-500 dark:bg-green-800 text-white'} px-4 py-2 rounded-md z-10"
                        >
                            Add Game
                        </button>
                    </div>
                </div>

                <!-- Foto de perfil con dropdown -->
                <button
                    class="relative z-20 border-0"
                    on:click={toggleProfileDropdown}
                >
                <img src="/user-solid.svg"
                        alt="Perfil"
                        class="h-8 w-8 rounded-full cursor-pointer"
                    />
                    <div
                        class={`absolute right-0 w-48 dark:bg-gray-600 border rounded-md shadow-lg', ${
                            showProfileDropdown ? "block" : "hidden"
                        }`}
                    >
                        <button
                            on:click={() => goto("/template")}
                            class="block border-0 mx-auto py-2 w-full dark:text-black  text-gray-800 hover:bg-blue-600 hover:text-white"
                            >Edit review template</button
                        >
                        <button
                            on:click={logOut}
                            class="block mx-auto w-full py-2 dark:text-black  text-gray-800 hover:bg-blue-600 hover:text-white"
                            >Log out</button
                        >
                    </div>
                </button>
            </div>
        </nav>
        <Popup />
        <GameList />
    </body>
    {:catch error}
    {error}
    {/await}
</main>

<style>
    @import url("https://fonts.googleapis.com/css2?family=Kanit:wght@500&display=swap");

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
