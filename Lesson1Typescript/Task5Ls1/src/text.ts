export function normalizeSentence(text: string): string {
    const trimmed: string = text.trim();
    const lower: string = trimmed.toLowerCase();
    const oneSpace: string = lower.replace(/\s+/g, " ");
    return oneSpace;
}

export function countWords(text: string): number {
    const n: string = normalizeSentence(text);

    if (n === "") return 0;

    const parts: string[] = n.split(" ");
    return parts.length;
}
