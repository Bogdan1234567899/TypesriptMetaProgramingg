import { addContact, findContactByName, listContacts } from "./contacts";

addContact("Mike", "111-111");
addContact("Walte", "222-222");
addContact("Bohdan", "333-333");

console.log("Find Mike:", findContactByName("Mike"));

console.log("All contacts:");
listContacts();
