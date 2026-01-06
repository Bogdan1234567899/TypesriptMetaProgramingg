"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const contacts_1 = require("./contacts");
(0, contacts_1.addContact)("Mike", "111-111");
(0, contacts_1.addContact)("Walte", "222-222");
(0, contacts_1.addContact)("Bohdan", "333-333");
console.log("Find Mike:", (0, contacts_1.findContactByName)("Mike"));
console.log("All contacts:");
(0, contacts_1.listContacts)();
