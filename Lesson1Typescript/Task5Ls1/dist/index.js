"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const text_1 = require("./text");
const s = "   Праздник к Нам   приходит    ";
console.log("original:", JSON.stringify(s));
console.log("normalized:", JSON.stringify((0, text_1.normalizeSentence)(s)));
console.log("words:", (0, text_1.countWords)(s));
