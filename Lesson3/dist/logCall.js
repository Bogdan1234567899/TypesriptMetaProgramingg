"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.LogCall = LogCall;
function LogCall(target, propertyKey, descriptor) {
    const original = descriptor.value;
    descriptor.value = function (...args) {
        console.log("[LOG] method:", propertyKey);
        console.log("[LOG] args:", args);
        return original.apply(this, args);
    };
}
