"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getMinGrade = getMinGrade;
exports.getMaxGrade = getMaxGrade;
exports.getAverageGrade = getAverageGrade;
function getMinGrade(grades) {
    return Math.min(...grades);
}
function getMaxGrade(grades) {
    return Math.max(...grades);
}
function getAverageGrade(grades) {
    let sum = 0;
    for (const g of grades) {
        sum += g;
    }
    return sum / grades.length;
}
