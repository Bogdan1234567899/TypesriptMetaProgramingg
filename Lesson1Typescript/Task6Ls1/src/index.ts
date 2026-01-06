import { calcTotal, parseProduct, type Product } from "./products";

const lines: string[] = ["Milk - 42.5", "Bread - 25", "Caло - 30"];

const products: Product[] = [];
for (const line of lines) {
    products.push(parseProduct(line));
}

console.log("products:", products);
console.log("total:", calcTotal(products));
