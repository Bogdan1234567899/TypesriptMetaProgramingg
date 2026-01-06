"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.addContact = addContact;
exports.findContactByName = findContactByName;
exports.listContacts = listContacts;
const contacts = [];
let nextId = 1;
function addContact(name, phone) {
    const c = { id: nextId, name: name, phone: phone };
    nextId = nextId + 1;
    contacts.push(c);
    return c;
}
function findContactByName(name) {
    for (const c of contacts) {
        if (c.name === name)
            return c;
    }
    return null;
}
function listContacts() {
    for (const c of contacts) {
        console.log(c.id, c.name, c.phone);
    }
}
