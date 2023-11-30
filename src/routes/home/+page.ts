import {type Game} from "$lib/gameModel.js"
import { goto } from "$app/navigation";


export const ssr = false;

export const load = async ({fetch}) => {

    let res = await fetch(`http://127.0.0.1:4321/mygames`, {
        credentials: "include",
        method: "GET"
    })
    if(res.status == 401) {
        goto("/login")
        return
    } else {
        let games: Game[] = await res.json()
        return {games}
    }
    
}