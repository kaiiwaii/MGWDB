import { format } from 'date-fns';

export function formatReleaseDate(timestamp: number | null): string {
    let t = timestamp ? format(new Date(timestamp * 1000), 'dd/MM/yyyy') : "No data";
    return t;
}