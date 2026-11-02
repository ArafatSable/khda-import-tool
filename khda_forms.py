"""
khda_forms.py
Registry of the KHDA forms this app can build an import-ready sheet for.
Shared by app_streamlit.py and app_cli.py.

Target application: "Zoho To KHDA" (link name zoho-to-khda), development
environment. Forked from cheds-import-tool on 2026-11-02 for the first seven
datasets due to KHDA on 5 Nov 2026.

Each entry: display name -> mapping config JSON path (relative to this folder).
"""

FORMS = {
    "1. Applicants - Basic Details":      "mappings/Applicants_Basic_Details_mapping.json",
    "2. Graduates":                       "mappings/Student_Graduates_mapping.json",
    "3. Employee - Basic Details":        "mappings/Employee_Basic_Details_mapping.json",
    "4. Employee - Workload":             "mappings/Employee_Workload_mapping.json",
    "5. Graduate Licensure":              "mappings/Graduate_Licensure_mapping.json",
    "6. Institute - Employers":           "mappings/Institute_Employers_mapping.json",
    "7. Institute - Academic Programs":   "mappings/Institute_Academic_Program_mapping.json",
}

# Forms with no verified KHDA push workflow yet. All seven are pending until
# KHDA issues the client credentials and the transport layer is in place.
UNVERIFIED_NO_WORKFLOW = set(FORMS.keys())

OUT_OF_SCOPE = {
    "Real-time datasets (15)",
    "The other 24 semester/annual datasets",
}
