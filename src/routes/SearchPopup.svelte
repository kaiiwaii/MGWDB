<script lang="ts">
    import { onMount } from 'svelte';
    export let showPopup: boolean;
    let searchResults: GameResult[] = [];
    let searchTerm = '';


    interface GameResult {
        name: string;
    }

    const IGDB_CLIENT_ID = 'orhhwm21vn308qugaiup8lqxmzhp2g';
    const IGDB_TOKEN = "yu3rak2poca82ga71382ftbtk134kr";
    const fetchData = async () => {
        try {
            const response = await fetch("https://api.igdb.com/v4/games", {
                method: 'POST',
                headers: {
                    "Access-Control-Allow-Origin": "https://api.igdb.com",
                    'Client-ID': IGDB_CLIENT_ID,
                    'Authorization': `Bearer ${IGDB_TOKEN}`,
                },
                body: JSON.stringify({
                    query: `fields name; search ${searchTerm}`,
                    // Add other query parameters
                }),
            });

            const data = await response.json();
            searchResults = data;
        } catch (error) {
            console.error('Error fetching data from IGDB API', error);
        }
    };

    const handleSearch = () => {
        fetchData();
    };

    onMount(() => {
        // Optional: Fetch data on component mount if needed
    });
</script>

{#if showPopup}
    <div class="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50">
        <div class="bg-white p-4 rounded shadow-lg w-1/2">
            <!-- Search bar at the top center -->
            <input
                type="search"
                placeholder="Search..."
                bind:value={searchTerm}
                on:input={handleSearch}
                class="w-full p-2 mb-4 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
            >

            <!-- Search button -->
            <button on:click={handleSearch} class="bg-blue-500 text-white px-4 py-2 rounded-full mb-4">Search</button>

            <!-- List of results -->
            <ul>
                {#each searchResults as result}
                    <li>{result.name}</li>
                {/each}
            </ul>

            <button on:click={() => showPopup = false} class="mt-4 bg-blue-500 text-white px-4 py-2 rounded-full">Close</button>
        </div>
    </div>
{/if}