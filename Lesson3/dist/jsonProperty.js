"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.JsonProperty = JsonProperty;
exports.getJsonName = getJsonName;
const jsonNames = new WeakMap();
function JsonProperty(name) {
    return function (target, propertyKey) {
        let map = jsonNames.get(target);
        if (!map) {
            map = new Map();
            jsonNames.set(target, map);
        }
        map.set(propertyKey, name);
    };
}
function getJsonName(target, propertyKey) {
    const map = jsonNames.get(target);
    return map === null || map === void 0 ? void 0 : map.get(propertyKey);
}
