import { getAverageGrade, getMaxGrade, getMinGrade, type Student } from "./student";

const students: Student[] = [
    { name: "Bohdan", grades: [12, 11, 10, 12, 9] },
    { name: "Sasha", grades: [7, 8, 6, 9] }
];

for (const s of students) {
    console.log("Name:", s.name);
    console.log("Grades:", s.grades);
    console.log("Min:", getMinGrade(s.grades));
    console.log("Max:", getMaxGrade(s.grades));
    console.log("Average:", getAverageGrade(s.grades));
    console.log("-----");
}
