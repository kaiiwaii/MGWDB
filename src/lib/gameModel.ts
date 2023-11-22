export interface Game {
    id:  number;
    name: string;
    cover: {url: string};
    platforms: number[];
    genres: string[];
    first_release_date: number;
    url: string;

    review: string;
    description: string;
    hours: number;
    played_platform: [number, number];
}
// export interface GameResult {
//     id: number,
//     name: string;
//     cover: {url: string};
//     genres: string[];
//     first_release_date: number;
//     platforms: string[];
//     url: string;
// }
