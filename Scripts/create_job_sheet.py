import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# Authentification
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("API/credentials.json", scope)
client = gspread.authorize(creds)

# Création du Google Sheet
spreadsheet = client.create("Job Tracker - Yannis")
spreadsheet.share('yannisdaguenet@gmail.com', perm_type='user', role='writer')

### 1. Sheet Compétences/Skills
skills_data = [
    ["Compétence", "Détail / Technologie", "Exemple Projet", "Postes Visés"],                                               
    ["Économétrie", "DiD, Panel, Modèles gravitationnels", "Étude Eurozone, GVC", "Economist, Policy Analyst"],            
    ["Machine Learning", "Random Forest, Regressions", "Projet prédiction socio-éco", "Data Scientist Junior"],             
    ["Automation", "Google Apps Script", "Greenly – automatisation workflow", "Climate Data Engineer"],                     
    ["Carbon Accounting", "SBTi, Scope 3, FLAG", "Greenly – analyse des achats, fret, ventes", "ESG Analyst"],              
    ["SQL / BigQuery", "Data pipeline, requêtes", "Greenly", "Data Analyst, Data Engineer"],                                
    ["Communication analytique", "Rédaction de KB, vulgarisation", "Bases internes SBTi chez Greenly", "Knowledge Analyst"] 
]

sheet1 = spreadsheet.get_worksheet(0)
sheet1.update_title("Compétences/Skills")
sheet1.update("A1", skills_data)

### 2. Sheet Jobs
jobs_headers = [
    ["Entreprise", "Poste", "Domaine", "Source", "Date", "Statut", "Lien", "Commentaires", "Contact Recruteur", "Contact Employé"]
]
spreadsheet.add_worksheet(title="Jobs", rows="100", cols="20")
sheet2 = spreadsheet.worksheet("Jobs")
sheet2.update("A1", jobs_headers)

print("✅ Fichier Google Sheets créé avec succès !")