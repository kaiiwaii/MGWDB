<script lang="ts">
    import GameList from "./GameList.svelte";
    import { onMount } from "svelte";
    import { page } from '$app/stores';

    import {
        gameList,
        librarySearchTerm,
        ratingTemplate,
        selectedSortType
    } from "./stores.js";

    import { SortType, SortOrder } from "$lib/gameModel.js";

    export let games;

    let darkMode;
    let sortDropdownVisible = false;

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
    <body class="flex justify-center items-center h-screen bg-gray-100 dark:bg-gray-800">
        <h1 class="text-5xl dark:text-white">[404] User not found</h1>
    </body>
    {:else if userNotPublic}
    <body class="flex justify-center items-center h-screen bg-gray-100 dark:bg-gray-800">
        <h1 class="dark:text-white text-5xl">[401] This user doesn't have a public profile</h1>
    </body>
    {:else}
    {#await loaded}
    <body class="flex justify-center items-center h-screen bg-gray-100 dark:bg-gray-800">
        <div class="animate-spin rounded-full h-16 w-16 border-t-5 border-blue-500 border-r-4 border-b-4 border-gray-300"></div>
      </body>
    {:then}
    <body class="bg-white dark:bg-[#263244] border-color-gray-800 max-h-screen h-full p-2 overflow-hidden">
        <nav class="dark:bg-[#1b1f29] bg-blue-700 p-4 m-0 rounded-md lg:m-2">
            <div class="container mx-auto flex flex-col md:flex-row items-center">
                <!-- Logo a la izquierda con margen -->
                <div class="mr-4 mb-4 md:mb-0">
                    <img src="/f_mghdblogo.svg" alt="Logo" class="h-12" />
                </div>

                <div class="flex-grow w-full md:w-2/5 mb-4 md:mb-0 flex items-center mx-auto justify-center relative">
                    <div class="w-4/6 flex relative">
                        <input
                            type="search"
                            placeholder="Search..."
                            bind:value={$librarySearchTerm}
                            class="px-4 py-2 w-full block rounded-md dark:bg-gray-600 focus:outline-red-400"
                        />
                        <div class="ml-1 relative">
                            <button on:click={() => sortDropdownVisible = !sortDropdownVisible}>
                                {#if darkMode}
                                    <img src="/sort_icon_dark.svg" class="h-7">
                                {:else} 
                                    <img src="/sort_icon_light.svg" class="h-7">
                                {/if}
                            </button>
                            {#if sortDropdownVisible}
                            <div class="absolute mt-2 z-50 left-0 dark:bg-gray-600 bg-white dark:text-light-50 p-2 rounded-md shadow-md">
                                <select bind:value={$selectedSortType.type} name="sort_type" class="mr-2 px-4 py-2 rounded-md text-lg mb-2 dark:bg-[#1b1f29] dark:text-white">
                                    <option value={SortType.Rating}>Rating</option>
                                    <option value={SortType.Name}>Name</option>
                                    <option value={SortType.Hours}>Hours</option>
                                </select>
                                <select bind:value={$selectedSortType.order} name="sort_order" class="px-4 py-2 rounded-md text-lg dark:bg-[#1b1f29] dark:text-white">
                                    <option value={SortOrder.Asc}>Ascending</option>
                                    <option value={SortOrder.Desc}>Descending</option>
                                </select>
                            </div>
                            {/if}
                        </div>
                    </div>
                    
                </div>

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