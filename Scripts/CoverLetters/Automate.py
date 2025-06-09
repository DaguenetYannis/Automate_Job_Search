import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# --- CONFIGURATION ---
SCOPES = ['https://www.googleapis.com/auth/documents']
CREDENTIALS_PATH = "API/credentialsGoogleDocs.json"
SKILLS_FILES = {
    "en": "Messages/CL_Skills_en.json",
    "fr": "Messages/CL_Skills_fr.json"
}

TEMPLATES = {
    "en": {
        "opening": "Dear Hiring Team,\n\nI am writing to express my interest in the position of [POSITION], as advertised. With a background in economics, data analysis, and project management, I am confident in my ability to contribute meaningfully to your team.",
        "closing": "Thank you for considering my application. I would be glad to further discuss how my experience and motivation align with your goals.\n\nSincerely,\nYannis Daguenet"
    },
    "fr": {
        "opening": "Madame, Monsieur,\n\nJe me permets de vous adresser ma candidature pour le poste de [POSTE]. Titulaire d’un double cursus en économie et affaires européennes, je souhaite mettre mes compétences analytiques et ma rigueur au service de votre équipe.",
        "closing": "Je vous remercie de l’attention portée à ma candidature, et reste à votre disposition pour un entretien.\n\nCordialement,\nYannis Daguenet"
    }
}

# --- Authentification Google Docs ---
def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
    creds = flow.run_local_server(port=0)
    return build('docs', 'v1', credentials=creds)

# --- Chargement des paragraphes depuis JSON ---
def load_paragraphs(language):
    filepath = SKILLS_FILES.get(language)
    if not filepath:
        print("❌ Invalid language. Please choose 'en' or 'fr'.")
        exit()
    with open(filepath, encoding='utf-8') as f:
        return json.load(f)

# --- Sélection interactive des compétences ---
def choose_skills(paragraphs):
    print("\n📌 Available skills:")
    for i, item in enumerate(paragraphs):
        print(f"{i + 1}. {item['Skill']}")

    selected = input("\n✏️ Enter the numbers of the skills you want to include (comma-separated): ")
    selected_indices = [int(i.strip()) - 1 for i in selected.split(",") if i.strip().isdigit()]

    print("\n✅ Skills selected:")
    for i in selected_indices:
        if 0 <= i < len(paragraphs):
            print(f" - {paragraphs[i]['Skill']}")

    return [paragraphs[i]["Paragraph"] for i in selected_indices if 0 <= i < len(paragraphs) and paragraphs[i]["Paragraph"].strip()]

# --- Création du Google Docs avec insertion des textes ---
def create_doc(service, title, opening, paragraphs, closing):
    doc = service.documents().create(body={'title': title}).execute()
    doc_id = doc['documentId']

    full_blocks = [opening] + paragraphs + [closing]
    requests = []

    for block in reversed(full_blocks):  # On insère à l'index 1, donc on inverse l'ordre
        requests.append({
            'insertText': {
                'location': {'index': 1},
                'text': block.strip() + '\n\n'
            }
        })

    service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
    print(f"\n✅ Document created: https://docs.google.com/document/d/{doc_id}")

# --- MAIN ---
if __name__ == "__main__":
    lang = input("🌍 Choose language (en/fr): ").strip().lower()
    if lang not in SKILLS_FILES:
        print("❌ Invalid language. Exiting.")
        exit()

    position = input("📌 Enter the job title: ").strip()
    opening = TEMPLATES[lang]["opening"].replace("[POSITION]" if lang == "en" else "[POSTE]", position)
    closing = TEMPLATES[lang]["closing"]

    service = authenticate()
    paragraphs_data = load_paragraphs(lang)
    selected_paragraphs = choose_skills(paragraphs_data)

    if not selected_paragraphs:
        print("⚠️ No paragraphs selected. Exiting.")
        exit()

    doc_title = f"Cover Letter - {position}"
    create_doc(service, doc_title, opening, selected_paragraphs, closing)
