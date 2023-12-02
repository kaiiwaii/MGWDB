<script lang="ts">
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    // Import other dependencies as needed

    // Add your existing imports here
    let email = ""
    let username = ""
    let password = ""
    let code = ""
    // Existing functions and variables...

    // Add any additional functions or variables for signup functionality

    async function signUp() {
        let res = await fetch(`http://127.0.0.1/signup?username=${username}&password=${password}&email=${email}&code=${code}`)
        if(res.status != 200) {
            alert("Error signing up")
        } else {
            goto("/login")
        }
    }
</script>

<html lang="en">
    <!-- Head section remains the same -->

    <!-- Body section -->
    <body class="bg-white">
        <div class="container mx-auto mt-8">
            <div class="max-w-md mx-auto bg-white rounded-md p-8 shadow-md">
                <h2 class="text-2xl font-bold mb-4">Sign Up</h2>
        
                <!-- Update the form to bind email and password variables -->
                <form>
                    <div class="mb-4">
                        <label for="username" class="block text-sm font-medium text-gray-600">Username</label>
                        <input type="username" id="username" name="username" bind:value={username} class="mt-1 p-2 w-full border rounded-md" required />
                    </div>
                    <div class="mb-4">
                        <label for="code" class="block text-sm font-medium text-gray-600">Code</label>
                        <input type="code" id="code" name="code" bind:value={code} class="mt-1 p-2 w-full border rounded-md" required />
                    </div>
                    <!-- Email input field -->
                    <div class="mb-4">
                        <label for="email" class="block text-sm font-medium text-gray-600">Email</label>
                        <input type="email" id="email" name="email" bind:value={email} class="mt-1 p-2 w-full border rounded-md" required />
                    </div>
        
                    <!-- Password input field -->
                    <div class="mb-4">
                        <label for="password" class="block text-sm font-medium text-gray-600">Password</label>
                        <input type="password" id="password" name="password" bind:value={password} class="mt-1 p-2 w-full border rounded-md" required />
                    </div>
        
                    <!-- Add more form fields as needed -->
        
                    <button type="button" on:click={signUp} class="bg-blue-500 text-white px-4 py-2 rounded-md">
                        Sign Up
                    </button>
                </form>
            </div>
        </div>
    </body>
</html>

<style>
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
