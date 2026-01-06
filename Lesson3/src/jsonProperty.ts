const jsonNames: WeakMap<object, Map<string, string>> = new WeakMap();

export function JsonProperty(name: string) {
    return function (target: any, propertyKey: string): void {
        let map = jsonNames.get(target);

        if (!map) {
            map = new Map<string, string>();
            jsonNames.set(target, map);
        }

        map.set(propertyKey, name);
    };
}

export function getJsonName(target: any, propertyKey: string): string | undefined {
    const map = jsonNames.get(target);
    return map?.get(propertyKey);
}
