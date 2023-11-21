<script lang="ts">
    import { onMount } from 'svelte';
    import { format } from 'date-fns';

    export let showPopup: boolean;
    let searchTerm = '';

    interface GameResult {
        name: string;
        cover: {url: string}; // Assuming cover is a URL
        genres: string[];
        first_release_date: number; // Unix timestamp
        platforms: string[];
        url: string;
    }

    let searchResults: GameResult[] = [];
    let isSearching = false;

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

    const TEST_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwidGltZXN0YW1wIjoxNzAwNTg0MTg0LjkwNzgwMjh9.oRpCFHhXYZilNAKhorb2RbWl_7BKrmHxTC9J3mInCJM";


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
            </div>
          </li>
        {/each}
      </ul>

      {#if isSearching && searchTerm !== ''}
        <div class="flex items-center justify-center mt-4">
          <!-- Spinner for loading -->
          <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-blue-500 border-r-2 border-b-2 border-gray-300"></div>
          <span class="ml-2">Searching...</span>
        </div>
      {/if}

      <button on:click={() => showPopup = false} class="mt-4 bg-blue-500 text-white px-4 py-2 rounded-full">Close</button>
    </div>
  </div>
{/if}