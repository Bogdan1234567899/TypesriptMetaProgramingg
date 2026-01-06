"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const products_1 = require("./products");
const lines = ["Milk - 42.5", "Bread - 25", "Caло - 30"];
const products = [];
for (const line of lines) {
    products.push((0, products_1.parseProduct)(line));
}
console.log("products:", products);
console.log("total:", (0, products_1.calcTotal)(products));
