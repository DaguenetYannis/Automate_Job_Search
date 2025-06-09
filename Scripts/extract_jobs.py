import os
import json
from ctransformers import AutoModelForCausalLM
import gspread
from oauth2client.service_account import ServiceAccountCredentials

FIELDS = [
    "Entreprise", "Poste", "Compétences", "Domaine", "Source", "Lieu",
    "Date", "Salaire", "Statut", "Lien", "Commentaires", "Contact Recruteur", "Contact Employé"
]

PROMPT_TEMPLATE = """You are an assistant that extracts structured data from job descriptions.

Please extract the following fields:

Entreprise:
Poste:
Compétences:
Domaine:
Source:
Lieu:
Date:
Salaire:
Statut:
Lien:
Commentaires:
Contact Recruteur:
Contact Employé:

If a field is missing in the job description, leave it blank.
Respond only with the fields listed, in the format shown.

Here is the job description:
---
{job_description}
---
"""

def load_processed_jobs(log_path="processed_jobs.json"):
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            return set(json.load(f))
    return set()

def save_processed_jobs(processed, log_path="processed_jobs.json"):
    with open(log_path, "w") as f:
        json.dump(sorted(list(processed)), f, indent=2)

def truncate_text(text, max_tokens=500):
    words = text.split()
    truncated = []
    token_count = 0

    for word in words:
        token_count += max(1, len(word) // 4)  # Estimation : 1 token ~ 4 caractères
        if token_count > max_tokens:
            break
        truncated.append(word)

    return " ".join(truncated)

def extract_and_append_jobs(
    gguf_path: str,
    txt_folder: str,
    credentials_path: str,
    spreadsheet_name: str = "Job Tracker - Yannis",
    sheet_name: str = "Jobs"
):
    print("⏳ Loading Mistral model...")
    model = AutoModelForCausalLM.from_pretrained(
        gguf_path,
        model_type="mistral",
        context_length=4096,
        max_new_tokens=1024
    )
    print(f"✅ Mistral model loaded.")
    print(f"🧾 Context length: {model.config.context_length}")
    print(f"🆕 Max new tokens: {model.config.max_new_tokens}")

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    client = gspread.authorize(creds)
    sheet = client.open(spreadsheet_name).worksheet(sheet_name)

    log_path = "processed_jobs.json"
    processed_jobs = load_processed_jobs(log_path)

    for filename in os.listdir(txt_folder):
        if not filename.endswith(".txt"):
            continue
        if filename in processed_jobs:
            print(f"⏭️ Skipping already processed file: {filename}")
            continue

        path = os.path.join(txt_folder, filename)
        with open(path, "r", encoding="utf-8") as f:
            job_text = f.read()

        job_text = truncate_text(job_text, max_tokens=480)
        prompt = PROMPT_TEMPLATE.format(job_description=job_text)

        print(f"🤖 Extracting: {filename}")
        response = model(prompt)
        lines = response.splitlines()

        row = []
        for field in FIELDS:
            value = ""
            for line in lines:
                if line.lower().startswith(field.lower() + ":"):
                    value = line.split(":", 1)[1].strip()
                    break
            row.append(value)

        sheet.append_row(row)
        print(f"✅ Added to sheet: {filename}")

        processed_jobs.add(filename)
        save_processed_jobs(processed_jobs, log_path)

    print("🏁 All jobs processed.")
