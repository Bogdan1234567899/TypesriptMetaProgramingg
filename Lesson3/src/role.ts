const rolesStorage: WeakMap<object, Map<string, string[]>> = new WeakMap();

export function Role(roleName: string) {
    return function (target: any, propertyKey: string): void {
        let methodsMap = rolesStorage.get(target);

        if (!methodsMap) {
            methodsMap = new Map<string, string[]>();
            rolesStorage.set(target, methodsMap);
        }

        const currentRoles = methodsMap.get(propertyKey) || [];
        currentRoles.push(roleName);
        methodsMap.set(propertyKey, currentRoles);
    };
}

export function getRoles(target: any, methodName: string): string[] {
    const methodsMap = rolesStorage.get(target);
    if (!methodsMap) return [];
    return methodsMap.get(methodName) || [];
}
