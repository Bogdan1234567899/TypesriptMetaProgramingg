

/*
   1) Conditional Types: IsString<T>
   true если T = string, иначе false
*/
export type IsString<T> = T extends string ? true : false;

type T1_1 = IsString<string>; // true
type T1_2 = IsString<number>; // false

const t1a: T1_1 = true;
const t1b: T1_2 = false;
// const t1c: T1_1 = false; // ошибка


/*
   2) Conditional + Union: OnlyNumbers<T>
   оставляет из union только number
 */
export type OnlyNumbers<T> = T extends number ? T : never;

type T2 = OnlyNumbers<string | number | boolean>; // number
const t2x: T2 = 123;
//const t2y: T2 = "hello"; // ошибка


/*
   3) infer: UnwrapPromise<T>
   если T = Promise<U> -> U, иначе T
 */
export type UnwrapPromise<T> = T extends Promise<infer U> ? U : T;

type T3_1 = UnwrapPromise<Promise<number>>; // number
type T3_2 = UnwrapPromise<string>; // string

const t3a: T3_1 = 10;
const t3b: T3_2 = "ok";
// const t3c: T3_1 = "10"; // ошибка


/*
   4) infer: ElementType<T>
   если T = U[] -> U, иначе T
*/
export type ElementType<T> = T extends (infer U)[] ? U : T;

type User4 = { id: number; name: string };
type T4 = ElementType<User4[]>; // User4

const t4u: T4 = { id: 1, name: "Ivan" };
// const t4u2: T4 = { id: 1 }; // ошибка


/*
   5) Mapped Types: Patch<T>
   делает все поля optional (как Partial)
*/
export type Patch<T> = {
    [K in keyof T]?: T[K];
};

type User5 = { id: number; name: string; email: string };
type User5Patch = Patch<User5>;

const p5a: User5Patch = {};
const p5b: User5Patch = { name: "Ivan" };
const p5c: User5Patch = { email: "a@b.com" };
// const p5d: User5Patch = { age: 10 }; // ошибка


/*
   6) PatchWithoutId<T>
   все поля optional, но id нельзя вообще
*/
export type PatchWithoutId<T> = {
    [K in Exclude<keyof T, "id">]?: T[K];
};

type User6 = { id: number; name: string; email: string };
type User6PatchNoId = PatchWithoutId<User6>;

const p6a: User6PatchNoId = {};
const p6b: User6PatchNoId = { name: "Ivan" };
const p6c: User6PatchNoId = { email: "a@b.com" };
// const p6d: User6PatchNoId = { id: 1 }; // ошибка


/*
   7) API контракт (простая версия)
   Api + EndpointKey = keyof Api
*/
export type User7 = { id: number; name: string; email: string };

export type Api = {
    "GET /users/:id": {
        params: { id: number };
        response: User7;
    };
    "POST /users": {
        body: { name: string; email: string };
        response: User7;
    };
};

export type EndpointKey = keyof Api;

type Keys7 = EndpointKey; // "GET /users/:id" | "POST /users"

const k7a: EndpointKey = "GET /users/:id";
const k7b: EndpointKey = "POST /users";



