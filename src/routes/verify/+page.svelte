<script lang="ts">
    import { page } from '$app/stores'
    const token = $page.url.searchParams.get('token')

    async function verify() {
        if (token) {
            let res = await fetch(`${import.meta.env.VITE_API_URL}/verify/${token}`, {method: "POST"})
            if(res.status != 200) {
                throw {
                    message: "Error while verifying"
                }
            } 
        } else {
            throw {
                message: "Token not found"
            }
        }
    }
</script>

<main>
    {#await verify()}
    <body class="flex justify-center items-center h-screen bg-gray-100 dark:bg-gray-800">
        <div class="animate-spin rounded-full h-16 w-16 border-t-5 border-blue-500 border-r-4 border-b-4 border-gray-300"></div>
      </body>
    {:then}
    <body class="flex justify-center items-center h-screen bg-gray-100 dark:bg-gray-800">
        <a href="https://mghdb.com/login">Verification successful, you can now proceed to the login page</a>
      </body>
    {:catch error}
    <body class="flex justify-center items-center h-screen bg-gray-100 dark:bg-gray-800">
        <div>{error.message}</div>
      </body>
    {/await}
</main>