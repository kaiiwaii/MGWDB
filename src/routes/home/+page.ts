import {type Game} from "$lib/gameModel.js"

export const load = async ({fetch}) => {
    let res = await fetch(`http://127.0.0.1:4321/mygames`, {
        credentials: "include",
        method: "GET"
    })
    let games: Game[] = await res.json()
    return {games}
}