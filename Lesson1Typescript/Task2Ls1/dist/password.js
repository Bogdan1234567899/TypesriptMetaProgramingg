"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.isStrongPassword = isStrongPassword;
function isStrongPassword(pwd) {
    const hasLen = pwd.length >= 8;
    const hasDigit = /\d/.test(pwd);
    const hasUpper = /[A-Z]/.test(pwd);
    return hasLen && hasDigit && hasUpper;
}
