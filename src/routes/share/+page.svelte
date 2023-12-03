<script lang="ts">
    import GameList from "./GameList.svelte";
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import { page } from '$app/stores';

    import {
        gameList,
        librarySearchTerm,
        ratingTemplate
    } from "./stores.js";

    export let games;

    let showProfileDropdown = false;
    const toggleProfileDropdown = () => {
        showProfileDropdown = !showProfileDropdown;
    };

    let loaded;
    let userNotFound = false;
    let userNotPublic = false;
    const user = $page.url.searchParams.get('user')

    async function loadAll() {
        let res = await fetch(`${import.meta.env.VITE_API_URL}/user/${user}`, {
        credentials: "include",
        method: "GET"
    })
        if(res.status == 401) {
            userNotPublic = true
        } else if (res.status == 404) {
            userNotFound = true
        } else {
            let data = await res.json()
            games = data["games"]
            console.log(games)
            ratingTemplate.set(data["template"])
    }
        $gameList = games && games.length > 0 ? games : [];
    }

    onMount(() =>{
        if(user) {
            loaded = loadAll()
        } else {
            userNotFound = true
        }
    });


</script>

<style>
    .text-gradient {
        background-clip: text;
        color: transparent;
        display: inline-block;
        font-size: inherit;
        font-weight: inherit;
        margin: 0;
        background-image: linear-gradient(to right, #ff00cc, #3333cc);
    }

    .animate-blink {
        animation: blink 3s ease-in-out infinite; /* Adjust the duration as needed */
    }

    @keyframes blink {
        0%, 50%, 100% {
            opacity: 1.25;
            scale: 1;
        }
        25%, 75% {
            opacity: 0.7;
            scale: 1.05;
        }
    }

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

<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>MGWDB</title>
    </head>
    {#if userNotFound}
        <h1>User not found</h1>
    {:else if userNotPublic}
        <h1>This user doesn't have a public profile</h1>
    {:else}
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
                            placeholder="Search..."
                            bind:value={$librarySearchTerm}
                            class="px-4 py-2 w-full lg:max-w-[50%] mx-auto block rounded-md border border-gray-300 focus:outline-none focus:border-blue-700"
                        />
                    </div>
                    <h1 class="text-4xl font-bold mb-6 relative inline-block">
                        <span class="animate-blink text-gradient text-shadow-md">
                            {user}'s library
                        </span>
                    </h1>
                    <!-- <button
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
                    </button> -->
                </div>
            </nav>
            <GameList />
        </body>
    {:catch error}
        {error}
    {/await}
    {/if}
</html>