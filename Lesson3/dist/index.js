"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
const logCall_1 = require("./logCall");
const role_1 = require("./role");
const jsonProperty_1 = require("./jsonProperty");
const analyzeModels_1 = require("./analyzeModels");
const analyzeImports_1 = require("./analyzeImports");
const path = __importStar(require("path"));
//Task 1 
class Calculator {
    add(a, b) {
        return a + b;
    }
    sub(a, b) {
        return a - b;
    }
}
__decorate([
    logCall_1.LogCall
], Calculator.prototype, "add", null);
const calc = new Calculator();
console.log("add result:", calc.add(2, 3));
//Task 2
class DocumentController {
    create() { }
    read() { }
    delete() { }
}
__decorate([
    (0, role_1.Role)("admin")
], DocumentController.prototype, "create", null);
__decorate([
    (0, role_1.Role)("user")
], DocumentController.prototype, "read", null);
__decorate([
    (0, role_1.Role)("admin")
], DocumentController.prototype, "delete", null);
console.log("Roles for create:", (0, role_1.getRoles)(DocumentController.prototype, "create"));
console.log("Roles for read:", (0, role_1.getRoles)(DocumentController.prototype, "read"));
console.log("Roles for delete:", (0, role_1.getRoles)(DocumentController.prototype, "delete"));
//Task 3
class UserDto {
}
__decorate([
    (0, jsonProperty_1.JsonProperty)("user_name")
], UserDto.prototype, "name", void 0);
__decorate([
    (0, jsonProperty_1.JsonProperty)("user_age")
], UserDto.prototype, "age", void 0);
console.log("Json name for name:", (0, jsonProperty_1.getJsonName)(UserDto.prototype, "name"));
console.log("Json name for age:", (0, jsonProperty_1.getJsonName)(UserDto.prototype, "age"));
//Task 4
const modelsPath = path.join(__dirname, "../src/models.ts");
console.log("\n=== Analyze models.ts ===");
(0, analyzeModels_1.analyzeModels)(modelsPath);
//Task 5 demo
const importsPath = path.join(__dirname, "../src/importsSample.ts");
console.log("\n=== Analyze importsSample.ts ===");
(0, analyzeImports_1.analyzeImports)(importsPath);
