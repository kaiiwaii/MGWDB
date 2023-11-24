export interface Game {
    id: number;
    name: string;
    cover: { image_id: string } | null;
    platforms: {abbreviation: string}[] | null;
    genres: {name: string}[] | null;
    first_release_date: number | null;
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
