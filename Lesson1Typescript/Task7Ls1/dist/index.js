"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const student_1 = require("./student");
const students = [
    { name: "Bohdan", grades: [12, 11, 10, 12, 9] },
    { name: "Sasha", grades: [7, 8, 6, 9] }
];
for (const s of students) {
    console.log("Name:", s.name);
    console.log("Grades:", s.grades);
    console.log("Min:", (0, student_1.getMinGrade)(s.grades));
    console.log("Max:", (0, student_1.getMaxGrade)(s.grades));
    console.log("Average:", (0, student_1.getAverageGrade)(s.grades));
    console.log("-----");
}
