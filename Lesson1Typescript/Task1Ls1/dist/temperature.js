"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.celsiusToFahrenheit = celsiusToFahrenheit;
exports.fahrenheitToCelsius = fahrenheitToCelsius;
function celsiusToFahrenheit(c) {
    return (c * 9) / 5 + 32;
}
function fahrenheitToCelsius(f) {
    return ((f - 32) * 5) / 9;
}
