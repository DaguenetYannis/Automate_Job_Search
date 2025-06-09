from convert_rtf_to_txt import convert_rtf_folder
from extract_jobs import extract_and_append_jobs

convert_rtf_folder("Jobs_database/rtf", "Jobs_database/txt")

job_list = extract_and_append_jobs(
    gguf_path="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    txt_folder="Jobs_database/txt",
    credentials_path="API/credentialsGoogleSheet.json"
)

from update_contacts import update_contacts_from_sheet

update_contacts_from_sheet(
    credentials_path="API/credentialsGoogleSheet.json",
    spreadsheet_name="Job Tracker - Yannis",
    sheet_name="Jobs"
)
