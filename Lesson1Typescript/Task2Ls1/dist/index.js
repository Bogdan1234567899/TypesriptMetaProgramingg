"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const password_1 = require("./password");
const passwords = ["zxcvb", "Metoprograming", ",metaprogram1", "zxcVBN34", "12345678A"];
for (const p of passwords) {
    console.log(p, "->", (0, password_1.isStrongPassword)(p));
}
