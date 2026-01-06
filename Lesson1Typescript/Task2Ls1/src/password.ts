export function isStrongPassword(pwd: string): boolean {
    const hasLen: boolean = pwd.length >= 8;
    const hasDigit: boolean = /\d/.test(pwd);
    const hasUpper: boolean = /[A-Z]/.test(pwd);

    return hasLen && hasDigit && hasUpper;
}
