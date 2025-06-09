import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Authentification
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("API/credentials.json", scope)
client = gspread.authorize(creds)

# Ouvre ton Google Sheet existant
spreadsheet = client.open("Job Tracker - Yannis")
sheet = spreadsheet.worksheet("Compétences/Skills")

# Liste des compétences
skills = [
    "Analyse de données statistiques", "Analyse des données", "Modélisation statistique",
    "Visualisation de données", "Modélisation économique", "Data wrangling", "Économétrie",
    "Data analytics", "Programmation statistique", "Machine Learning Operations (MLOps)",
    "Sciences économiques", "Microéconomie", "Macroéconomie", "Techniques d’étude",
    "Analyse du cycle de vie (ACV)", "Google BigQuery", "Google Apps Script", "DataGrip", "R",
    "Python", "Bases de données", "Google Sheets", "CRM (Gestion de la relation client)",
    "Rédaction académique", "Rédaction de rapport", "Rédaction de brèves", "Synthèse d’informations",
    "Rédaction", "Communication d’entreprise", "Insight client", "Position Papers", "Communication",
    "Réseaux sociaux", "Édition audio", "Développement durable", "Connaissances en économie du climat",
    "Connaissances en transition bas-carbone", "Sens de l’organisation", "Travail d’équipe",
    "Leadership", "Gestion d’équipe", "Compétences analytiques", "Relation client", "Savoir-être",
    "Autonomie", "Anglais", "Français"
]

# Formatage pour mise en colonne F
skills_data = [[skill] for skill in skills]

# Titre + données
sheet.update("G1", [["Compétences individuelles"]])
sheet.update("G2", skills_data)

print("✅ Compétences ajoutées dans la colonne G du Google Sheet.")
