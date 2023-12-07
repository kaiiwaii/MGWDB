import { writable } from "svelte/store";
import { type Game, Sort} from "$lib/gameModel.js";

export const showSearchPopup = writable(false);
export const showGamePopup = writable(false);

export const gamesNotSaved = writable(false);
export const isSavingGames = writable(false);

export const librarySearchTerm = writable("");

export const temporaryGames = writable([] as Game[]);

export const gameList = writable([] as Game[]);

export const ratingTemplate = writable("");

export const pageLoaded = writable(false);

export const selectedSortType = writable(new Sort())
