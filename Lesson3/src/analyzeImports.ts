import * as ts from "typescript";
import { readFileSync } from "fs";

export function analyzeImports(filePath: string): void {
    const text: string = readFileSync(filePath, "utf-8");

    const sourceFile = ts.createSourceFile(
        filePath,
        text,
        ts.ScriptTarget.Latest,
        true
    );

    for (const st of sourceFile.statements) {
        if (ts.isImportDeclaration(st)) {
            const fromModule: string = (st.moduleSpecifier as ts.StringLiteral).text;

            const names: string[] = [];
            const clause = st.importClause;

            if (clause?.name) {
                names.push(clause.name.text); // default import
            }

            const bindings = clause?.namedBindings;
            if (bindings && ts.isNamedImports(bindings)) {
                for (const el of bindings.elements) {
                    names.push(el.name.text);
                }
            }

            console.log("From:", fromModule);
            console.log("Imports:", names);
            console.log("----");
        }
    }
}
