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

    let darkMode;

    function toggleDarkMode() {

        darkMode = !darkMode
        
        if(darkMode) {
            document.documentElement.classList.add('dark')
        } else {
            document.documentElement.classList.remove('dark')
        }
            
        
    }

    let loaded;
    let userNotFound = false;
    let userNotPublic = false;
    const user = $page.url.searchParams.get('user')

    async function loadAll() {
        darkMode = window.matchMedia('(prefers-color-scheme: dark)').matches
        if(darkMode) {
            document.documentElement.classList.add('dark')
        } else {
            document.documentElement.classList.remove('dark')
        }
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
        background-image: linear-gradient(to right, #ff00cc, rgb(196, 106, 219) );
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

<main lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>MGWDB</title>
    </head>
    {#if userNotFound}
    <body class="flex justify-center items-center h-full bg-gray-100 dark:bg-gray-800">
        <h1 class="text-5xl dark:text-white">[404] User not found</h1>
    </body>
    {:else if userNotPublic}
    <body class="flex justify-center items-center h-screen bg-gray-100 dark:bg-gray-800">
        <h1 class="dark:text-white text-5xl">[401] This user doesn't have a public profile</h1>
    </body>
    {:else}
    {#await loaded}
    <body class="flex justify-center items-center h-full bg-gray-100 dark:bg-gray-800">
        <div class="animate-spin rounded-full h-16 w-16 border-t-5 border-blue-500 border-r-4 border-b-4 border-gray-300"></div>
      </body>
    {:then}
    <body class="bg-white dark:bg-gray-800 border-color-gray-800 max-h-screen h-full overflow-hidden p-2">
        <nav class="dark:bg-blue-800 bg-blue-500 p-4 m-0 rounded-md lg:m-2">
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
                <h1 class="text-4xl font-bold mr-4 mb-4 md:mb-0 relative inline-block">
                    <span class="animate-blink text-gradient text-shadow-md">
                        {user}'s library
                    </span>
                </h1>

                    <span class="dark:text-gray-400 text-white mr-2">🌞</span> <!-- Sun icon for light mode -->
                    <label class="switch inline-block relative w-10 h-4">
                        <input type="checkbox" checked={darkMode} on:change={toggleDarkMode} class="absolute opacity-0 h-0 w-0" />
                        <span class="dark:bg-blue-700 bg-gray-400 absolute cursor-pointer h-4 w-10 rounded-full -ml-1 transition-all duration-300"></span>
                        <span class="slider inline-block absolute cursor-pointer h-4 w-4 bg-white rounded-full -ml-2 transition-all duration-300 transform dark:translate-x-6 translate-x-0"></span>
                    </label>
                    <span class="dark:text-gray-400 text-white ml-2">🌙</span> <!-- Moon icon for dark mode -->
                </div>
        </nav>
        <GameList />
    </body>
    {:catch error}
        {error}
    {/await}
    {/if}
    </main>