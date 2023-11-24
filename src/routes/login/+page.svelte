<script lang="ts">
    import {goto} from '$app/navigation';

    let email = "";
    let password = "";
    let error = "";

  
    async function handleLogin() {
        let res = await fetch(`http://127.0.0.1:4321/login?email=${email}&password=${password}`, {
            method: "GET",
            credentials: "include",
            headers: {
                "Access-Control-Allow-Origin": "http://127.0.0.1:4321"
            }
        })
        let data = await res.json()
        if(res.status != 200) {
            error = data["error"]
        } else {
            goto("/home")
            
        }     
    
    };
</script>
  
<style>
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@500&display=swap');

    @tailwind base;
    @tailwind components;
    @tailwind utilities;

    body {
        font-family: Kanit, sans-serif;
    }
</style>

<html>
    <body>
        <div class="min-h-screen flex items-center justify-center bg-gray-100">
            <div class="w-full max-w-md p-8 bg-white rounded-lg shadow-md">
                <h1 class="text-3xl font-bold mb-6 text-center">Log In</h1>
                {#if error}
                <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4" role="alert">
                    <p>{error}</p>
                </div>
                {/if}
                <form>
                <div class="mb-4">
                    <label for="email" class="block text-gray-600">Email:</label>
                    <input type="text" id="email" bind:value={email} class="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500">
                </div>
                <div class="mb-6">
                    <label for="password" class="block text-gray-600">Password:</label>
                    <input type="password" id="password" bind:value={password} class="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500">
                </div>
                <div class="flex justify-center">
                    <button type="button" on:click={handleLogin} class="bg-blue-500 text-white px-6 py-3 rounded-full hover:bg-blue-600 transition duration-300">
                    Log In
                    </button>
                </div>
                </form>
            </div>
            </div>
    </body>
</html>
  