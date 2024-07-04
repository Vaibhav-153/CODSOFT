import tkinter as tk
from tkinter import messagebox
import json
import re

class Contact:
    def __init__(self, name, phone, email, address):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address

    def to_dict(self):
        return {
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'], data['phone'], data['email'], data['address'])

class ContactManager:
    def __init__(self, filename='contacts.json'):
        self.contacts = []
        self.filename = filename
        self.load_contacts()

    def add_contact(self, contact):
        self.contacts.append(contact)
        self.save_contacts()

    def delete_contact(self, index):
        if 0 <= index < len(self.contacts):
            del self.contacts[index]
            self.save_contacts()
            return True
        return False

    def update_contact(self, index, contact):
        if 0 <= index < len(self.contacts):
            self.contacts[index] = contact
            self.save_contacts()
            return True
        return False

    def search_contacts(self, query):
        result = [contact for contact in self.contacts if query.lower() in contact.name.lower() or query in contact.phone]
        return result

    def save_contacts(self):
        with open(self.filename, 'w') as f:
            json.dump([contact.to_dict() for contact in self.contacts], f)

    def load_contacts(self):
        try:
            with open(self.filename, 'r') as f:
                contacts_data = json.load(f)
                self.contacts = [Contact.from_dict(contact) for contact in contacts_data]
        except FileNotFoundError:
            self.contacts = []

class ContactApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")
        self.contact_manager = ContactManager()
        self.selected_contact_index = None

        self.create_widgets()
        self.refresh_contact_list()

    def create_widgets(self):
        self.name_label = tk.Label(self.root, text="Name")
        self.name_label.grid(row=0, column=0, padx=10, pady=10)
        self.name_entry = tk.Entry(self.root, width=30)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.phone_label = tk.Label(self.root, text="Phone")
        self.phone_label.grid(row=1, column=0, padx=10, pady=10)
        self.phone_entry = tk.Entry(self.root, width=30)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=10)

        self.email_label = tk.Label(self.root, text="Email")
        self.email_label.grid(row=2, column=0, padx=10, pady=10)
        self.email_entry = tk.Entry(self.root, width=30)
        self.email_entry.grid(row=2, column=1, padx=10, pady=10)

        self.address_label = tk.Label(self.root, text="Address")
        self.address_label.grid(row=3, column=0, padx=10, pady=10)
        self.address_entry = tk.Entry(self.root, width=30)
        self.address_entry.grid(row=3, column=1, padx=10, pady=10)

        self.add_button = tk.Button(self.root, text="Add Contact", command=self.add_contact)
        self.add_button.grid(row=4, column=0, padx=10, pady=10)

        self.update_button = tk.Button(self.root, text="Update Contact", command=self.update_contact)
        self.update_button.grid(row=4, column=1, padx=10, pady=10)

        self.delete_button = tk.Button(self.root, text="Delete Contact", command=self.delete_contact)
        self.delete_button.grid(row=4, column=2, padx=10, pady=10)

        self.search_label = tk.Label(self.root, text="Search")
        self.search_label.grid(row=5, column=0, padx=10, pady=10)
        self.search_entry = tk.Entry(self.root, width=30)
        self.search_entry.grid(row=5, column=1, padx=10, pady=10)

        self.search_button = tk.Button(self.root, text="Search", command=self.search_contact)
        self.search_button.grid(row=5, column=2, padx=10, pady=10)

        self.contact_listbox = tk.Listbox(self.root, height=10, width=50)
        self.contact_listbox.grid(row=6, column=0, columnspan=3, padx=10, pady=10)
        self.contact_listbox.bind('<<ListboxSelect>>', self.on_contact_select)

    def add_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()

        if name and phone and email and address:
            if not self.validate_phone(phone):
                messagebox.showwarning("Warning", "Please enter a valid 10-digit phone number")
                return
            if not self.validate_email(email):
                messagebox.showwarning("Warning", "Please enter a valid email address")
                return
            contact = Contact(name, phone, email, address)
            self.contact_manager.add_contact(contact)
            self.refresh_contact_list()
            self.clear_entries()
        else:
            messagebox.showwarning("Warning", "Please fill in all fields")

    def update_contact(self):
        if self.selected_contact_index is not None:
            name = self.name_entry.get().strip()
            phone = self.phone_entry.get().strip()
            email = self.email_entry.get().strip()
            address = self.address_entry.get().strip()

            if name and phone and email and address:
                if not self.validate_phone(phone):
                    messagebox.showwarning("Warning", "Please enter a valid 10-digit phone number")
                    return
                if not self.validate_email(email):
                    messagebox.showwarning("Warning", "Please enter a valid email address")
                    return
                contact = Contact(name, phone, email, address)
                if self.contact_manager.update_contact(self.selected_contact_index, contact):
                    self.refresh_contact_list()
                    self.clear_entries()
                    self.selected_contact_index = None
                else:
                    messagebox.showerror("Error", "Failed to update contact")
            else:
                messagebox.showwarning("Warning", "Please fill in all fields")
        else:
            messagebox.showwarning("Warning", "Please select a contact to update")

    def delete_contact(self):
        if self.selected_contact_index is not None:
            if self.contact_manager.delete_contact(self.selected_contact_index):
                self.refresh_contact_list()
                self.clear_entries()
                self.selected_contact_index = None
            else:
                messagebox.showerror("Error", "Failed to delete contact")
        else:
            messagebox.showwarning("Warning", "Please select a contact to delete")

    def search_contact(self):
        query = self.search_entry.get().strip()
        if query:
            result = self.contact_manager.search_contacts(query)
            self.display_contacts(result)
        else:
            messagebox.showwarning("Warning", "Please enter a search query")

    def on_contact_select(self, event):
        try:
            index = self.contact_listbox.curselection()[0]
            self.selected_contact_index = index
            contact = self.contact_manager.contacts[index]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, contact.name)
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, contact.phone)
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, contact.email)
            self.address_entry.delete(0, tk.END)
            self.address_entry.insert(0, contact.address)
        except IndexError:
            pass

    def refresh_contact_list(self):
        self.display_contacts(self.contact_manager.contacts)

    def display_contacts(self, contacts):
        self.contact_listbox.delete(0, tk.END)
        for contact in contacts:
            self.contact_listbox.insert(tk.END, f"{contact.name} - {contact.phone}")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)

    def validate_phone(self, phone):
        # Validate phone numbers to be exactly 10 digits
        return phone.isdigit() and len(phone) == 10

    def validate_email(self, email):
        # Simple regex for validating email addresses
        email_regex = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
        return email_regex.match(email) is not None

def main():
    root = tk.Tk()
    app = ContactApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
