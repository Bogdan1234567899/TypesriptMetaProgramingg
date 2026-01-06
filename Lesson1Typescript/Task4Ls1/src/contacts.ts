export type Contact = {
    id: number;
    name: string;
    phone: string;
};

const contacts: Contact[] = [];
let nextId: number = 1;

export function addContact(name: string, phone: string): Contact {
    const c: Contact = { id: nextId, name: name, phone: phone };
    nextId = nextId + 1;

    contacts.push(c);
    return c;
}

export function findContactByName(name: string): Contact | null {
    for (const c of contacts) {
        if (c.name === name) return c;
    }
    return null;
}

export function listContacts(): void {
    for (const c of contacts) {
        console.log(c.id, c.name, c.phone);
    }
}
