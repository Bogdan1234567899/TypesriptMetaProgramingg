"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Role = Role;
exports.getRoles = getRoles;
const rolesStorage = new WeakMap();
function Role(roleName) {
    return function (target, propertyKey) {
        let methodsMap = rolesStorage.get(target);
        if (!methodsMap) {
            methodsMap = new Map();
            rolesStorage.set(target, methodsMap);
        }
        const currentRoles = methodsMap.get(propertyKey) || [];
        currentRoles.push(roleName);
        methodsMap.set(propertyKey, currentRoles);
    };
}
function getRoles(target, methodName) {
    const methodsMap = rolesStorage.get(target);
    if (!methodsMap)
        return [];
    return methodsMap.get(methodName) || [];
}
