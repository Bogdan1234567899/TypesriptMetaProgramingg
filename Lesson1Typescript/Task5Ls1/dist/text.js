"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.normalizeSentence = normalizeSentence;
exports.countWords = countWords;
function normalizeSentence(text) {
    const trimmed = text.trim();
    const lower = trimmed.toLowerCase();
    const oneSpace = lower.replace(/\s+/g, " ");
    return oneSpace;
}
function countWords(text) {
    const n = normalizeSentence(text);
    if (n === "")
        return 0;
    const parts = n.split(" ");
    return parts.length;
}
