export type Product = {
    title: string;
    price: number;
};

export function parseProduct(line: string): Product {
    const parts: string[] = line.split(" - ");
    const title: string = parts[0];
    const price: number = Number(parts[1]);

    return { title: title, price: price };
}

export function calcTotal(products: Product[]): number {
    let sum: number = 0;

    for (const p of products) {
        sum += p.price;
    }

    return sum;
}
