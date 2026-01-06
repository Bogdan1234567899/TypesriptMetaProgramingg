"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const arrays_1 = require("./arrays");
const nums = [3, -1, 4, 0, 10, -5];
console.log("nums:", nums);
console.log("sumPositive:", (0, arrays_1.sumPositive)(nums));
console.log("filterEven:", (0, arrays_1.filterEven)(nums));
