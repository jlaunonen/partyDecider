import format from "date-fns/format"
import parseISO from "date-fns/parseISO"

export function formatTime(dateTime: string): string {
    return format(parseISO(dateTime), "PPpp")
}
