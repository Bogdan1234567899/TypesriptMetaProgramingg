"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.sumPositive = sumPositive;
exports.filterEven = filterEven;
function sumPositive(nums) {
    let sum = 0;
    for (const n of nums) {
        if (n > 0)
            sum += n;
    }
    return sum;
}
function filterEven(nums) {
    const res = [];
    for (const n of nums) {
        if (n % 2 === 0)
            res.push(n);
    }
    return res;
}
