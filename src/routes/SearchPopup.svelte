
<script lang="ts">
    import { onMount, afterUpdate } from 'svelte';
    import { format } from 'date-fns';

    export let showPopup: boolean;
    let searchTerm = '';

    let games_to_add: number[] = [];
    $: addedGames = [...games_to_add];
    let games_to_add_length = 0;

    interface GameResult {
        id: number,
        name: string;
        cover: {url: string};
        genres: string[];
        first_release_date: number;
        platforms: string[];
        url: string;
    }

    let searchResults: GameResult[] = [];
    let isSearching = false;
    let isAddingGames = false; // Track the state of adding games

    function debounce<T extends (...args: any[]) => any>(func: T, delay: number) {
        let timer: number;
        return function (...args: Parameters<T>) {
            clearTimeout(timer);
            timer = setTimeout(() => {
                func.apply(this, args);
            }, delay);
        } as T;
    }

    function formatReleaseDate(timestamp: number): string {
        return format(new Date(timestamp * 1000), 'MM/dd/yyyy');
    }

    const TEST_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwidGltZXN0YW1wIjoxNzAwNTg0MTg0LjkwNzgwMjh9.oRpCFHhXYZilNAKhorb2RbWl_7BKrmHxTC9J3mInCJM"; // Replace with your actual token

    async function addGames() {
        try {
            isAddingGames = true; // Set the flag to indicate adding games
            // Simulate an artificial delay (replace this with actual logic)
            await new Promise(resolve => setTimeout(resolve, 5000));
        } finally {
            isAddingGames = false; // Reset the flag after the asynchronous operation is complete
        }
    }

    const fetchData = async () => {
        try {
            isSearching = true;
            const response = await fetch(`http://127.0.0.1:4321/api/games?token=${TEST_TOKEN}&search=${searchTerm}`, {
                method: 'GET',
                headers: {"Access-Control-Allow-Origin": "*"}
            });

            const data = await response.json();
            searchResults = data;
        } catch (error) {
            console.error('Error fetching data from IGDB API', error);
        } finally {
            isSearching = false;
        }
    };

    const debouncedSearch = debounce(fetchData, 300);

    onMount(() => {
        // Optional: Fetch data on component mount if needed
    });
</script>

{#if showPopup}
  <div class="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50">
    <div class="bg-white p-4 rounded shadow-lg w-1/2">
      <!-- Search bar at the top center -->
      <div class="flex mb-4">
        <input
          type="search"
          placeholder="Search..."
          bind:value={searchTerm}
          on:input={debouncedSearch}
          class="w-full p-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
        >
        <button on:click={fetchData} class="ml-2 px-4 py-2 bg-blue-500 text-white rounded">
          Search
        </button>
      </div>

      <!-- List of results with images on the left and data on the right -->
      <ul class="overflow-y-auto max-h-64">
        {#each searchResults as result}
          <li class="flex items-center mb-4">
            <!-- Image on the left -->
            <img src={result.cover.url} alt={result.name} class="w-16 h-16 object-cover mr-4 rounded">

            <!-- Data on the right -->
            <div>
              <p class="font-bold">{result.name}</p>
              <p>Genres: {result.genres.join(', ')}</p>
              <p>Release Date: {formatReleaseDate(result.first_release_date)}</p>
              <p>Platforms: {result.platforms.join(', ')}</p>
              <p><a href={result.url} target="_blank" rel="noopener noreferrer">More Info</a></p>

              
              <button
                    on:click={() => {
                        //TODO: react on added
                        games_to_add.push(result.id);
                        games_to_add_length++;
                        
                    }}
                    class="{addedGames.includes(result.id) ? 'mt-2 bg-gray-500 text-white cursor-not-allowed px-4 py-2 rounded-full' : 'mt-2 bg-green-500 text-white px-4 py-2 rounded-full'}"
                    disabled="{addedGames.includes(result.id)}"
                    >
                    {addedGames.includes(result.id) ? 'Game Added' : 'Add Game'}
                </button>

            </div>
          </li>
        {/each}
      </ul>

      {#if isSearching && searchTerm !== ''}
        <div class="flex items-center justify-center mt-4">
          <!-- Spinner for loading or searching -->
          <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-blue-500 border-r-2 border-b-2 border-gray-300"></div>
          <span class="ml-2">{isSearching ? 'Searching...' : 'Adding selected games...'}</span>
        </div>
      {/if}

      {#if isAddingGames}
        <div class="flex items-center justify-center mt-4">
          <!-- Loading spinner for adding games -->
          <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-blue-500 border-r-2 border-b-2 border-gray-300"></div>
          <span class="ml-2">Adding selected games...</span>
        </div>
      {/if}

      <button on:click={async () => {
        if (!isSearching && games_to_add.length === 0) {
          showPopup = false;
          searchResults = [];
          games_to_add = [];
          games_to_add_length = 0;
        } else if (games_to_add.length > 0) {
          await addGames();
          showPopup = false;
          searchResults = [];
          games_to_add = [];
          games_to_add_length = 0;
        }
      }} class="mt-4 bg-blue-500 text-white px-4 py-2 rounded-full">
        {isSearching || games_to_add_length > 0 ? 'Add Selected Games' : 'Close'}
      </button>
    </div>
  </div>
{/if}
