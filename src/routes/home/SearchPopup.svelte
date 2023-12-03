
<script lang="ts">
    import {formatReleaseDate} from '$lib/utils.js'
    import { type Game } from '$lib/gameModel.js';
    import {showSearchPopup, gamesNotSaved, temporaryGames, gameList} from './stores.js';

    let searchTerm = '';

    let games_to_add_length = 0;
    const VITE_API_URL = import.meta.env.VITE_API_URL;

    let searchResults: Game[] = [];
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

    function closePopup() {
        $showSearchPopup = false;
        searchResults = [];
        searchTerm = "";
        games_to_add_length = 0;
    }


    const fetchData = async () => {
        try {

            if(!isSearching) {
                isSearching = true;
                const response = await fetch(`${VITE_API_URL}/api/searchgames?search=${searchTerm}`, {
                method: 'GET',
                credentials: "include"
                });

                const data = await response.json();
                searchResults = data;
            }
        } catch (error) {
            console.error('Error fetching data from IGDB API', error);
            isSearching = false;
        } finally {
            isSearching = false;
        }
    };

    const debouncedSearch = debounce(fetchData, 300);

</script>

{#if $showSearchPopup}
  <div class="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50 z-50">
    <div class="bg-white p-4 rounded shadow-lg md:w-1/2">
      <!-- Search bar at the top center -->
      <div class="flex mb-4">
        <input
          type="search"
          placeholder="Search..."
          bind:value={searchTerm}
          on:input={debouncedSearch}
          class="w-full p-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
        />
        <button on:click={fetchData} class="ml-2 px-4 py-2 bg-blue-500 text-white rounded">
          Search
        </button>
      </div>

      <!-- List of results with images on the left and data on the right -->
      <ul class="overflow-y-auto max-h-96">
        {#each searchResults as result}
          <li class="flex items-center mb-4">
            <!-- Image on the left -->
            <img
              src={`//images.igdb.com/igdb/image/upload/t_cover_big/${result.cover?.image_id}.jpg`}
              alt={result.name}
              class="w-16 h-16 object-cover mr-4 rounded"
            />

            <!-- Data on the right -->
            <div>
              <p class="font-bold">{result.name}</p>
              <p>Genres: {result.genres?.map(g => g.name).join(', ')}</p>
              <p>Release Date: {formatReleaseDate(result.first_release_date)}</p>
              <p>Platforms: {result.platforms?.map(p => p.abbreviation).join(", ")}</p>
              <p>
                <a href={result.url} target="_blank" rel="noopener noreferrer">
                  More Info
                </a>
              </p>

              <button
                on:click={() => {
                  $temporaryGames.push(result);
                  $temporaryGames = $temporaryGames;
                  games_to_add_length++;
                }}
                class="{$temporaryGames.some(g=>g.id === result.id) || $gameList.some(g=>g.id === result.id) ? 'mt-2 bg-gray-500 text-white cursor-not-allowed px-4 py-2 rounded-full' : 'mt-2 bg-green-500 text-white px-4 py-2 rounded-full'}"
                disabled="{$temporaryGames.some(g=>g.id === result.id) || $gameList.some(g=>g.id === result.id)}"
              >
                {$temporaryGames.some(g=>g.id === result.id) || $gameList.some(g=>g.id === result.id) ? 'Game Added' : 'Add Game'}
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

      <button on:click={() => {if(games_to_add_length>0){$gamesNotSaved=true}closePopup()}} class="mt-4 bg-blue-500 text-white px-4 py-2 rounded-full">
        {games_to_add_length > 0 ? 'Add selected games and close' : 'Close'}
      </button>
    </div>
  </div>
{/if}
