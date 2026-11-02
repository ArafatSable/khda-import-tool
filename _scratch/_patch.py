# -*- coding: utf-8 -*-
import json, io, collections

KHDA = "2026-11-02 KHDA fork: added for the KHDA University API v2 migration. Target field created in the Zoho To KHDA development environment on 2026-11-02."
GUESS = " RAW COLUMN NAME IS A GUESS -- the HEDB 2026 'Institute - Academic Programs' sheet has no 'Database Field Name' column, so the export header could not be confirmed. Verify against a real KHDA export before relying on this."

def load(p):
    return json.load(io.open(p, encoding="utf-8"))

def save(p, c):
    io.open(p, "w", encoding="utf-8").write(json.dumps(c, indent=2, ensure_ascii=False))

def add(cfg, **kw):
    note = kw.pop("note", "")
    e = {"raw_column": kw.pop("raw"), "target_field": kw.pop("target"), "kind": kw.pop("kind")}
    e.update(kw)
    e["_note"] = (note + " " + KHDA).strip()
    cfg["fields"].append(e)

# ---------- 1. Graduates ----------
p = "mappings/Student_Graduates_mapping.json"; c = load(p)
add(c, raw="Grad_Al_Ethbara", target="Al_Ethbara", kind="plain",
    note="Passport stamp number, UAE nationals only. Imported exactly as provided.")
add(c, raw="Grad_Marital_Status_Code", target="Marital_Status", kind="map",
    value_map={"S": "S - Single", "M": "M - Married", "D": "D - Divorced",
               "W": "W - Widowed", "U": "U - Undeclared/unknown"},
    note="Picklist stores 'CODE - Description', so the push can take the code with .subString(0,1).")
add(c, raw="Grad_Area_of_Specialization", target="Area_of_Specialization", kind="lookup",
    lookup_direction="code_to_name", hedb_sheet="Area of Specialization",
    note="KHDA requires this to equal the FIRST TWO DIGITS of Grad_Major_CIP -- worth a pre-import check.")
add(c, raw="Grad_Mode_of_Study", target="Mode_of_Study", kind="map",
    value_map={"FT": "FT - Full time", "PT": "PT - Part time"})
add(c, raw="Grad_Master_Thesis_Title", target="Master_Thesis_Title", kind="plain",
    note="Use 'NT' for professional programs with no thesis requirement.")
add(c, raw="Grad_PhD_Dissertation_Title", target="PhD_Dissertation_Title", kind="plain")
add(c, raw="Grad_Student_Major", target="Graduate_Major_Text", kind="plain",
    note="'Foundation' for pre-college students, 'Undeclared' where no major is known.")
add(c, raw="Grad_Major_CIP", target="Graduate_Major_CIP", kind="plain",
    note="CIP code from the program master; 99.9999 when the code is not listed.")
add(c, raw="Grad_LC", target="Licensure_Certificate_Completed", kind="map",
    value_map={"C": "C - Professional certificate or licensure completed",
               "M": "M - Microcredential completed", "B": "B - Both", "N": "N - Neither"},
    note="C, M or B oblige a matching row on Graduates-Licensures / Microcredential-Graduates.")
add(c, raw="Grad_Workplacement", target="Work_Placement_Completed", kind="yesno",
    note="Only placements formally recognised by the institution and in the approved study plan.")
add(c, raw="Grad_Health_Fitness_Certificate", target=None, kind="unmapped",
    note="Present on the HEDB sheet but absent from the KHDA v2 Graduates API field list. Not imported; confirm with KHDA.")
save(p, c)

# ---------- 2. Employee - Basic Details ----------
p = "mappings/Employee_Basic_Details_mapping.json"; c = load(p)
add(c, raw="Emp_Last_Promotion_Date", target="Last_Promotion_Date", kind="date",
    note="Most recent promotion within the institution, YYYY-MM-DD.")
# v35 picklist corrections
for f in c["fields"]:
    if f.get("target_field") == "Position_Title" and isinstance(f.get("value_map"), dict):
        vm = f["value_map"]
        for k, v in list(vm.items()):
            if v == "Career advisor":
                vm[k] = "Career advisor/Counselor"
            elif v == "Head of department":
                vm[k] = "Academic Department Chairs/Head"
        f["_note"] = (f.get("_note", "") +
            " 2026-11-02: two labels re-pointed to the v35 picklist text "
            "(Career advisor -> Career advisor/Counselor, Head of department -> "
            "Academic Department Chairs/Head). The picklist also gained Adjunct Faculty, "
            "Part-time Professor/Associate Professor/Assistant Professor, "
            "Provost/Chief Academic Officer and Associate Provost -- their CHEDS codes are "
            "not yet known, so rows carrying those codes will be flagged as unresolved.").strip()
save(p, c)

# ---------- 3. Employee - Workload ----------
p = "mappings/Employee_Workload_mapping.json"; c = load(p)
add(c, raw="Load_Full_Part_Time", target="Full_or_Part_Time", kind="map",
    value_map={"FT": "FT - Employed on a full-time contract",
               "PT": "PT - Employed on a part-time contract"})
add(c, raw="Load_Credits_Delivered", target="Credits_Delivered", kind="plain",
    note="Total credits delivered by the faculty member; excludes non-credit courses.")
add(c, raw="Load_Total_Credited_Students", target="Total_Credited_Students", kind="plain",
    note="Students counted once per class they are registered in.")
add(c, raw="Load_Total_Non_Credited_Students", target="Total_Non_Credited_Students", kind="plain")
save(p, c)

# ---------- 4. Graduate Licensure ----------
p = "mappings/Graduate_Licensure_mapping.json"; c = load(p)
LEVELS = [("FN","Foundation"),("RM","Remedial program (pre Masters)"),("FR","Freshman"),
          ("SP","Sophomore"),("JR","Junior"),("SR","Senior"),("M1","Masters Year 1"),
          ("M2","Masters Year 2"),("M3","Masters Year 3"),
          ("D1","Doctorate 1: Not advanced to candidacy"),("D2","Doctorate 2: Advanced to candidacy"),
          ("PD","Post-doctorate"),("PF","Professional Education"),("CR","Certificate/Credential"),
          ("DP","Diploma"),("HD","Higher Diploma"),("P1","Phase A"),("P2","Phase B"),
          ("P3","Medical residency and training"),("PG","Post graduate diploma"),("MC","Microcredential")]
add(c, raw="GLC_Student_Level", target="Graduate_Level", kind="map",
    value_map=collections.OrderedDict((k, k + " - " + v) for k, v in LEVELS),
    note="Student Level list. Picklist stores 'CODE - Description'.")
add(c, raw="GLC_Student_Degree", target="Graduate_Degree", kind="lookup",
    lookup_direction="code_to_name", hedb_sheet="Degree or Program Level")
add(c, raw="GLC_Org_website", target="Licensing_Body_Website", kind="plain",
    note="Website of the licence/certificate issuing organisation.")
for f in c["fields"]:
    if f.get("target_field") == "Licensure_Type":
        f["target_field"] = None; f["kind"] = "unmapped"
        f["_note"] = ("KHDA v2 has no licensureType field -- it asks for licensureStatus instead. "
                      "Left on the form but no longer imported. " + KHDA)
save(p, c)

# ---------- 5. Institute - Academic Programs ----------
p = "mappings/Institute_Academic_Program_mapping.json"; c = load(p)
add(c, raw="Prog_Degree", target="Degree", kind="lookup",
    lookup_direction="code_to_name", hedb_sheet="Degree or Program Level", note=GUESS)
add(c, raw="Prog_Area_Of_Specialization", target="Area_of_Specialization", kind="lookup",
    lookup_direction="code_to_name", hedb_sheet="Area of Specialization", note=GUESS)
add(c, raw="Prog_First_Enroll_Year", target="First_Enroll_Year", kind="lookup",
    lookup_direction="code_to_name", hedb_sheet="Academic Year", note=GUESS)
add(c, raw="Prog_Major_CIP", target="Major_CIP", kind="plain", note=GUESS)
add(c, raw="Prog_Initial_Accreditation_Date", target="Initial_Accreditation_Date", kind="date", note=GUESS)
add(c, raw="Prog_Number_Of_Students_Enroll", target="Number_of_Students_Enrolled", kind="plain", note=GUESS)
add(c, raw="Prog_Number_Of_Faculty_FT", target="Number_of_Faculty_FT", kind="plain", note=GUESS)
add(c, raw="Prog_Number_Of_Faculty_PT", target="Number_of_Faculty_PT", kind="plain", note=GUESS)
add(c, raw="Prog_Coordinator_Email", target="Coordinator_Email", kind="plain", note=GUESS)
add(c, raw="Prog_Coordinator_Mobile", target="Coordinator_Mobile", kind="phone", note=GUESS)
add(c, raw="Prog_Stem_Indicator", target="STEM_Indicator", kind="map",
    value_map={"Y": "Y - Program falls under STEM", "N": "N - Program does not fall under STEM"}, note=GUESS)
add(c, raw="Prog_CAA_Accreditation_Status", target="CAA_Accreditation_Status", kind="map",
    value_map={"Y": "Y - Accredited by CAA", "N": "N - Not accredited by CAA"}, note=GUESS)
add(c, raw="Prog_Distance_Learning", target="Distance_Learning", kind="map",
    value_map={"Y": "Y - Entire program can be completed online",
               "N": "N - Physical presence on campus required"}, note=GUESS)
save(p, c)

print("patched")
for p in ["mappings/Applicants_Basic_Details_mapping.json","mappings/Student_Graduates_mapping.json",
          "mappings/Employee_Basic_Details_mapping.json","mappings/Employee_Workload_mapping.json",
          "mappings/Graduate_Licensure_mapping.json","mappings/Institute_Employers_mapping.json",
          "mappings/Institute_Academic_Program_mapping.json"]:
    c = load(p)
    act = [f for f in c["fields"] if f.get("kind") != "unmapped"]
    print("  %-55s %3d active / %3d total" % (p.split("/")[-1], len(act), len(c["fields"])))
