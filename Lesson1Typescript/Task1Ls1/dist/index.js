"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const temperature_1 = require("./temperature");
const cValues = [0, 20, 100, -10];
for (const c of cValues) {
    console.log(`${c}°C -> ${(0, temperature_1.celsiusToFahrenheit)(c)}°F`);
}
const fValues = [32, 68, 212];
for (const f of fValues) {
    console.log(`${f}°F -> ${(0, temperature_1.fahrenheitToCelsius)(f)}°C`);
}
