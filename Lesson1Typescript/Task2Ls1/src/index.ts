import { isStrongPassword } from "./password";

const passwords: string[] = ["zxcvb", "Metoprograming", ",metaprogram1", "zxcVBN34", "12345678A"];

for (const p of passwords) {
    console.log(p, "->", isStrongPassword(p));
}
