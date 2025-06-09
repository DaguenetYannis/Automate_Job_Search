import json
from pathlib import Path
import gspread
from oauth2client.service_account import ServiceAccountCredentials

CONTACTS_PATH = Path("Messages/contacts.json")

def update_contacts_from_sheet(
    credentials_path="API/credentials.json",
    spreadsheet_name="Job Tracker - Yannis",
    sheet_name="Jobs"
):
    # Connect to Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    client = gspread.authorize(creds)
    sheet = client.open(spreadsheet_name).worksheet(sheet_name)

    # Load existing contacts
    contacts = []
    if CONTACTS_PATH.exists():
        try:
            with open(CONTACTS_PATH, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    contacts = json.loads(content)
        except json.JSONDecodeError:
            print("⚠️ contacts.json exists but contains invalid JSON. Resetting it.")

    # Convert to a dict for easy replacement: { company_name: name }
    contact_map = {c["Company_Name"]: c["Name"] for c in contacts}

    # Parse new entries from the sheet
    records = sheet.get_all_records()
    added_or_updated = 0

    for row in records:
        name = row.get("Contact Recruteur", "").strip()
        company = row.get("Entreprise", "").strip()

        if not name or not company:
            continue

        if contact_map.get(company) != name:
            contact_map[company] = name
            added_or_updated += 1

    # Rebuild contacts list from final map
    contacts = [{"Name": name, "Company_Name": company} for company, name in contact_map.items()]

    # Save result
    CONTACTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONTACTS_PATH, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=4, ensure_ascii=False)

    print(f"✅ Updated contacts.json with {added_or_updated} new or modified contact(s) ({len(contacts)} total).")
