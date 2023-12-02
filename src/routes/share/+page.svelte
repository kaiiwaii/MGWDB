<script lang="ts">
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
        pageLoaded,
        ratingTemplate
    } from "./stores.js";

    export let games;

    let showProfileDropdown = false;
    const toggleProfileDropdown = () => {
        showProfileDropdown = !showProfileDropdown;
    };

    let loaded;

    async function loadAll() {
        let res = await fetch(`http://127.0.0.1:4321/mygames`, {
        credentials: "include",
        method: "GET"
    })
        if(res.status == 401) {
        goto("/login")
        return
        } else {
            let data = await res.json()
            games = data["games"]
            console.log(games)
            ratingTemplate.set(data["template"])
    }
        $gameList = games && games.length > 0 ? games : [];
    }

    onMount(() => loaded = loadAll());


</script>

<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>MGWDB</title>
    </head>
    {#await loaded}
    <h1>Loading...</h1>
    {:then}
    <body class="bg-white">
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
                <!-- Foto de perfil con dropdown -->
                <button
                    class="relative z-50 border-0"
                    on:click={toggleProfileDropdown}
                    on:click={toggleProfileDropdown}
                >
                    <img
                        src="/user-solid.svg"
                        alt="Perfil"
                        class="h-8 w-8 rounded-full cursor-pointer"
                    />
                    <div
                        class={`absolute right-0 w-48 bg-white border rounded-md shadow-lg', ${
                            showProfileDropdown ? "block" : "hidden"
                        }`}
                    >
                        <button
                            on:click={() => goto("/template")}
                            class="block border-0 mx-auto py-2 w-full text-gray-800 hover:bg-blue-600 hover:text-white"
                            >View review template</button
                        >
                    </div>
                </button>
            </div>
        </nav>
        <GameList />
    </body>
    {:catch error}
    {error}
    {/await}
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
