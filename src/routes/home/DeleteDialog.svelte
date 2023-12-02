<script lang="ts">
  import { type selectedGame } from "$lib/gameModel.js";
  import { gameList, temporaryGames } from "./stores.js";
  import { onMount } from "svelte";

  onMount(() => {
    deleteDialogContainer = document.getElementById("delete_dialog");
  });

  let deleteDialogContainer;
  let isDeleting = false;

  export let showDeleteDialog: boolean;
  export let selected_game: selectedGame;

  $: {
    if (showDeleteDialog) {
      deleteDialogContainer.show();
    }
  }
  function closeDialog() {
    deleteDialogContainer.close();
    showDeleteDialog = false;
    isDeleting = false;
  }

  async function removeGame() {
    if (!isDeleting) {
      isDeleting = true;
      if (selected_game.saved) {
        const response = await fetch(
          `http://127.0.0.1:4321/deletegame?id=${selected_game.game.id}`,
          {
            method: "POST",
            credentials: "include",
          }
        );
        if (response.status != 200) {
          alert("Error deleting games");
          isDeleting = false;
          closeDialog();
          return;
        }
        $gameList.splice(selected_game.index, 1);
        $gameList = $gameList;
      } else {
        $temporaryGames.splice(selected_game.index, 1);
        $temporaryGames = $temporaryGames;
      }
      isDeleting = false;
      closeDialog();
    }
  }
</script>

<dialog
  id="delete_dialog"
  class="fixed inset-1/2 bg-white p-8 rounded-md shadow-lg z-50 transform -translate-x-1/2 -translate-y-1/2 lg:w-[30%] w-[80%]"
>
  <h1 class="text-xl font-bold mb-4">Do you want to delete the game?</h1>
  <button
    class="bg-gray-500 text-white px-4 py-2 rounded-md mr-2"
    on:click={closeDialog}>No</button
  >
  <button
    class="bg-red-500 text-white px-4 py-2 rounded-md"
    on:click={removeGame}>{isDeleting ? "Deleting..." : "Yes"}</button
  >
</dialog>
