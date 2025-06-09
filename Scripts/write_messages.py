import json
from pathlib import Path

TEMPLATE_PATH = Path("Messages/template.txt")
CONTACTS_PATH = Path("Messages/contacts.json")
OUTPUT_DIR = Path("Messages/output")

def load_template():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()

def load_contacts():
    with open(CONTACTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_messages(template, contacts):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for contact in contacts:
        message = template.format(**contact)
        name_slug = contact["Name"].replace(" ", "_").lower()
        filename = OUTPUT_DIR / f"message_to_{name_slug}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(message)
        print(f"✅ Created: {filename}")

if __name__ == "__main__":
    template = load_template()
    contacts = load_contacts()
    generate_messages(template, contacts)
