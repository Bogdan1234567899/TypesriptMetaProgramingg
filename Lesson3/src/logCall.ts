export function LogCall(
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
): void {
    const original = descriptor.value;

    descriptor.value = function (...args: any[]) {
        console.log("[LOG] method:", propertyKey);
        console.log("[LOG] args:", args);
        return original.apply(this, args);
    };
}
