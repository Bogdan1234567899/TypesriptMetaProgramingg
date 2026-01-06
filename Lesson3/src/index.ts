import { LogCall } from "./logCall";
import { Role, getRoles } from "./role";
import { JsonProperty, getJsonName } from "./jsonProperty";
import { analyzeModels } from "./analyzeModels";
import { analyzeImports } from "./analyzeImports";
import * as path from "path";

//Task 1 
class Calculator {
    @LogCall
    add(a: number, b: number): number {
        return a + b;
    }

    sub(a: number, b: number): number {
        return a - b;
    }
}

const calc = new Calculator();
console.log("add result:", calc.add(2, 3));

//Task 2
class DocumentController {
    @Role("admin")
    create(): void {}

    @Role("user")
    read(): void {}

    @Role("admin")
    delete(): void {}
}

console.log("Roles for create:", getRoles(DocumentController.prototype, "create"));
console.log("Roles for read:", getRoles(DocumentController.prototype, "read"));
console.log("Roles for delete:", getRoles(DocumentController.prototype, "delete"));

//Task 3
class UserDto {
    @JsonProperty("user_name")
    name!: string;

    @JsonProperty("user_age")
    age!: number;
}

console.log("Json name for name:", getJsonName(UserDto.prototype, "name"));
console.log("Json name for age:", getJsonName(UserDto.prototype, "age"));

//Task 4
const modelsPath = path.join(__dirname, "../src/models.ts");
console.log("\n=== Analyze models.ts ===");
analyzeModels(modelsPath);

//Task 5 demo
const importsPath = path.join(__dirname, "../src/importsSample.ts");
console.log("\n=== Analyze importsSample.ts ===");
analyzeImports(importsPath);
