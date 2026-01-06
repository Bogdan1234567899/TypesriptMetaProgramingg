export type Student = {
    name: string;
    grades: number[];
};

export function getMinGrade(grades: number[]): number {
    return Math.min(...grades);
}

export function getMaxGrade(grades: number[]): number {
    return Math.max(...grades);
}

export function getAverageGrade(grades: number[]): number {
    let sum: number = 0;

    for (const g of grades) {
        sum += g;
    }

    return sum / grades.length;
}
