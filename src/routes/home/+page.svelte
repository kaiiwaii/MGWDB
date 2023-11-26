<script lang="ts">
    import Popup from "./SearchPopup.svelte";
    import GameList from "./GameList.svelte";
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";

    import {
        gameList,
        gamesNotSaved,
        isSavingGames,
        librarySearchTerm,
        showSearchPopup,
        temporaryGames,
    } from "./stores.js";

    export let data;

    const toggleSearchPopup = () => {
        $showSearchPopup = !$showSearchPopup;
    };
    let showProfileDropdown = false;
    const toggleProfileDropdown = () => {
        showProfileDropdown = !showProfileDropdown;
    };

    onMount(() => {
        $gameList = data.games && data.games.length > 0 ? data.games : [];
    });

    function logOut() {
        document.cookie =
            "token" +
            "=; Path=/; Domain=127.0.0.1 ; SameSite=None; Expires=Thu, 01 Jan 1970 00:00:01 GMT;";
        goto("/login");
    }

    function applyGames() {
        // Disable the "Add Game" button and show loading spinner
        $isSavingGames = true;

        // TODO: send request with games to server
        // Simulating an asynchronous operation with a timeout

        try {
            fetch(`http://127.0.0.1:4321/addgames`, {
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

<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>MGWDB</title>
    </head>
    <body class="bg-gray-100">
        <nav class="bg-blue-500 p-4">
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
                        placeholder="Buscar..."
                        bind:value={$librarySearchTerm}
                        class="px-4 py-2 w-full lg:max-w-[50%] mx-auto block rounded-md border border-gray-300 focus:outline-none focus:border-blue-700"
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
                                class="bg-red-500 text-white px-4 py-2 rounded-md z-10"
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
                                : 'bg-green-500 text-white'} px-4 py-2 rounded-md z-10"
                        >
                            Add Game
                        </button>
                    </div>
                </div>

                <!-- Foto de perfil con dropdown -->
                <button
                    class="relative"
                    on:click={toggleProfileDropdown}
                    on:click={toggleProfileDropdown}
                >
                    <img
                        src="/user-solid.svg"
                        alt="Perfil"
                        class="h-8 w-8 rounded-full cursor-pointer"
                    />
                    <div
                        class={`absolute right-0 mt-2 w-48 bg-white border rounded-md shadow-lg', ${
                            showProfileDropdown ? "block" : "hidden"
                        }`}
                    >
                        <button
                            on:click={() => goto("/template")}
                            class="block px-4 py-2 text-gray-800 hover:bg-blue-500 hover:text-white"
                            >Edit review template</button
                        >
                        <button
                            on:click={logOut}
                            class="block px-4 py-2 text-gray-800 hover:bg-blue-500 hover:text-white"
                            >Log out</button
                        >
                    </div>
                </button>
            </div>
        </nav>
        <Popup />
        <GameList />
    </body>
</html>

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
