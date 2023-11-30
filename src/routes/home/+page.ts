import {type Game} from "$lib/gameModel.js"
import { goto } from "$app/navigation";
import { ratingTemplate } from "./stores.js";


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
        let data = await res.json()
        let games: Game[] = data["games"]
        ratingTemplate.set(data["template"])
        return {games}
    }
    
}