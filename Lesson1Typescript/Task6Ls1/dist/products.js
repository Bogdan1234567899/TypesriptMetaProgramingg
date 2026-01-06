"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.parseProduct = parseProduct;
exports.calcTotal = calcTotal;
function parseProduct(line) {
    const parts = line.split(" - ");
    const title = parts[0];
    const price = Number(parts[1]);
    return { title: title, price: price };
}
function calcTotal(products) {
    let sum = 0;
    for (const p of products) {
        sum += p.price;
    }
    return sum;
}
