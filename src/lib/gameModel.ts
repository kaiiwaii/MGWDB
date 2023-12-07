export class Game {
  id: number;
  name?: string;
  cover?: { image_id: string };
  platforms?: { id: number; abbreviation: string }[];
  genres?: { name: string }[];
  first_release_date?: number;
  url?: string;

  rating: string;
  score: number;
  description: string;
  hours: number;
  played_platform: number;
  date_range: {from: Date, to: Date};

  constructor(obj) {
    this.id = obj.id;
    this.name = obj.name;
    this.cover = obj.cover;
    this.platforms = obj.platforms;
    this.genres = obj.genres;
    this.first_release_date = obj.first_release_date;
    this.url = obj.url;
    
    this.rating = obj.rating || {};
    this.score = obj.score || 0;
    this.description = obj.description || "";
    this.hours = obj.hours || 0;
    this.played_platform = obj.played_platform || 0;

    if(!obj.date_range) {
      this.date_range = {from: new Date(), to: new Date()};
    } else if(typeof obj.date_range.from == "string" || typeof obj.date_range.to == "string") {
      this.date_range = {from: new Date(obj.date_range.from), to: new Date(obj.date_range.to)}
    } else {
      this.date_range = obj.date_range
    }
  }
  
}

export interface selectedGame {
  game?: Game;
  index?: number;
  saved?: boolean;
}


export enum SortType {
  Rating = 0,
  Hours = 1,
  Name = 2
}
export enum SortOrder {
  Asc = 0,
  Desc = 1
}

export class Sort {
  type: SortType;
  order: SortOrder;
  
  constructor(type?: SortType, order?: SortOrder) {
    this.type = type || SortType.Rating;
    this.order = order || SortOrder.Desc
  }
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
