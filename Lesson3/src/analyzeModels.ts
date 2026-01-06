import * as ts from "typescript";
import { readFileSync } from "fs";

export function analyzeModels(filePath: string): void {
    const sourceText: string = readFileSync(filePath, "utf-8");

    const sourceFile = ts.createSourceFile(
        filePath,
        sourceText,
        ts.ScriptTarget.Latest,
        true
    );

    function visit(node: ts.Node): void {
        if (ts.isInterfaceDeclaration(node)) {
            const interfaceName: string = node.name.text;
            const fields: string[] = [];

            for (const member of node.members) {
                if (ts.isPropertySignature(member) && member.name) {
                    fields.push(member.name.getText());
                }
            }

            console.log(`Interface: ${interfaceName}`);
            console.log("Fields:", fields);
            console.log("----");
        }

        ts.forEachChild(node, visit);
    }

    visit(sourceFile);
}
