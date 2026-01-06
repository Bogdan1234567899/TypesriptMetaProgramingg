import { countWords, normalizeSentence } from "./text";

const s: string = "   Праздник к Нам   приходит    ";

console.log("original:", JSON.stringify(s));
console.log("normalized:", JSON.stringify(normalizeSentence(s)));
console.log("words:", countWords(s));
