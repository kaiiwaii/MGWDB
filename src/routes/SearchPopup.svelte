<script lang="ts">
    import { onMount } from 'svelte';
    export let showPopup: boolean;
    let searchResults = [];

    // Dummy API endpoint and key, replace with actual values
    const IGDB_API_ENDPOINT = 'YOUR_IGDB_API_ENDPOINT';
    const IGDB_API_KEY = 'YOUR_IGDB_API_KEY';

    const fetchData = async () => {
        try {
            const response = await fetch(IGDB_API_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'user-key': IGDB_API_KEY,
                },
                body: JSON.stringify({
                    // Add your query parameters
                }),
            });

            const data = await response.json();
            searchResults = data;
        } catch (error) {
            console.error('Error fetching data from IGDB API', error);
        }
    };

    onMount(() => {
        fetchData();
    });
</script>

{#if showPopup}
    <div class="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50">
        <div class="bg-white p-4 rounded shadow-lg w-1/2">
            <!-- Search bar at the top center -->
            <input type="text" placeholder="Search..." class="w-full p-2 mb-4 border border-gray-300 rounded focus:outline-none focus:border-blue-500">

            <!-- List of 3 results -->
            <ul>
                {#each searchResults as result (result.id)}
                    <li>{result.name}</li>
                {/each}
            </ul>

            <button on:click={() => showPopup = false} class="mt-4 bg-blue-500 text-white px-4 py-2 rounded-full">Close</button>
        </div>
    </div>
{/if}
