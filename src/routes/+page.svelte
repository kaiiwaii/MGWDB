<script lang="ts" context="module">
    export interface AppProps {
        showPopup: boolean;
    }
</script>

<script lang="ts">
    import Popup from './SearchPopup.svelte';

    export let showPopup: boolean;
    const togglePopup = () => {
        console.log("togglePopup")
        showPopup = !showPopup;
    };

</script>

<style>
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@500&display=swap');

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

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Navbar con Tailwind</title>
</head>
<body class="bg-gray-100">
    <nav class="bg-blue-500 p-4">
        <div class="container mx-auto flex items-center">
            <!-- Logo a la izquierda con margen -->
            <div class="mr-4">
                <img src="tu_logo.png" alt="Logo" class="h-8">
            </div>

            <!-- Barra de búsqueda en el centro con margen y padding -->
            <div class="flex-grow">
                <input type="search" placeholder="Buscar..." class="px-4 py-2 w-1/2 mx-auto block rounded-md border border-gray-300 focus:outline-none focus:border-blue-700">
            </div>

            <!-- Botón "+ Add Game" con margen y padding -->
            <div class="mr-4">
                <button on:click={togglePopup} class="bg-green-500 text-white px-4 py-2 rounded-md">+ Add Game</button>
            </div>

            <!-- Foto de perfil con dropdown -->
            <div class="relative">
                <img src="tu_foto_de_perfil.jpg" alt="Perfil" class="h-8 w-8 rounded-full cursor-pointer">
                <div class="absolute right-0 mt-2 w-48 bg-white border rounded-md shadow-lg hidden">
                    <a href="#" class="block px-4 py-2 text-gray-800 hover:bg-blue-500 hover:text-white">Perfil</a>
                    <a href="#" class="block px-4 py-2 text-gray-800 hover:bg-blue-500 hover:text-white">Ajustes de cuenta</a>
                    <a href="#" class="block px-4 py-2 text-gray-800 hover:bg-blue-500 hover:text-white">Cerrar sesión</a>
                </div>
            </div>
        </div>
    </nav>
    <Popup bind:showPopup={showPopup} />
</body>
</html>

