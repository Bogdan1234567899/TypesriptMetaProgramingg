import { celsiusToFahrenheit, fahrenheitToCelsius } from "./temperature";

const cValues: number[] = [0, 20, 100, -10];
for (const c of cValues) {
    console.log(`${c}°C -> ${celsiusToFahrenheit(c)}°F`);
}

const fValues: number[] = [32, 68, 212];
for (const f of fValues) {
    console.log(`${f}°F -> ${fahrenheitToCelsius(f)}°C`);
}
