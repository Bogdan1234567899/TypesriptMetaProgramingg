export function sumPositive(nums: number[]): number {
    let sum: number = 0;

    for (const n of nums) {
        if (n > 0) sum += n;
    }

    return sum;
}

export function filterEven(nums: number[]): number[] {
    const res: number[] = [];

    for (const n of nums) {
        if (n % 2 === 0) res.push(n);
    }

    return res;
}
