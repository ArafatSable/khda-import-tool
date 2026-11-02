# khda-import-tool

Converts HEDB 2026 Excel exports into import-ready sheets for the **Zoho To KHDA**
Creator application (`zoho-to-khda`), for the seven datasets due to KHDA on
5 November 2026.

Forked from `cheds-import-tool` on 2026-11-02. The conversion engine
(`khda_import_tool.py`) is unchanged; what differs is the form registry and the
seven mapping files, which target the KHDA app's fields rather than the CHEDS app's.

## Datasets covered

| # | Dataset | Mapping | Active fields |
|---|---------|---------|---------------|
| 1 | Applicants - Basic Details | `Applicants_Basic_Details_mapping.json` | 8 |
| 2 | Graduates | `Student_Graduates_mapping.json` | 37 |
| 3 | Employee - Basic Details | `Employee_Basic_Details_mapping.json` | 31 |
| 4 | Employee - Workload | `Employee_Workload_mapping.json` | 28 |
| 5 | Graduate Licensure | `Graduate_Licensure_mapping.json` | 15 |
| 6 | Institute - Employers | `Institute_Employers_mapping.json` | 11 |
| 7 | Institute - Academic Programs | `Institute_Academic_Program_mapping.json` | 54 |

## Run it

```
setup.bat          # once -- creates the venv and installs requirements
run_web_app.bat    # Streamlit UI
run_cli.bat        # command line
```

You need the HEDB dictionary workbook (`HEDB_.xlsx`) alongside, same as the
CHEDS tool -- it supplies the code/name reference lists for every lookup.

## What changed from the CHEDS version

**31 new target fields.** Created in the Zoho To KHDA development environment on
2026-11-02 and mapped here:

- Graduates -- `Al_Ethbara`, `Marital_Status`, `Area_of_Specialization`,
  `Mode_of_Study`, `Master_Thesis_Title`, `PhD_Dissertation_Title`,
  `Graduate_Major_Text`, `Graduate_Major_CIP`, `Licensure_Certificate_Completed`,
  `Work_Placement_Completed`
- Employee - Basic Details -- `Last_Promotion_Date`
- Employee - Workload -- `Full_or_Part_Time`, `Credits_Delivered`,
  `Total_Credited_Students`, `Total_Non_Credited_Students`
- Graduate Licensure -- `Graduate_Level`, `Graduate_Degree`, `Licensing_Body_Website`
- Institute - Academic Programs -- `Degree`, `Area_of_Specialization`,
  `First_Enroll_Year`, `Major_CIP`, `Initial_Accreditation_Date`,
  `Number_of_Students_Enrolled`, `Number_of_Faculty_FT`, `Number_of_Faculty_PT`,
  `Coordinator_Email`, `Coordinator_Mobile`, `STEM_Indicator`,
  `CAA_Accreditation_Status`, `Distance_Learning`

**Nine picklists store `CODE - Description`.** For example `S - Single`,
`FT - Full time`, `Y - Accredited by CAA`. The value maps here produce that exact
text. On the push side this means `.subString(0,1)` or `.subString(0,2)` yields the
KHDA code directly -- no `Dropdown_Fields` function is needed for any of the nine.

**`Position_Title` re-pointed to the v35 picklist.** `Career advisor` became
`Career advisor/Counselor` and `Head of department` became
`Academic Department Chairs/Head`.

**Two fields dropped.** `Enroll_Passport_Number` on Employee - Basic Details and
`Licensure_Type` on Graduate Licensure -- neither exists in KHDA v2. The Zoho
fields remain on the forms; they are simply no longer imported.

**`institutionName` is not mapped anywhere.** KHDA wants it on 29 of its 31
datasets, but it is a constant for SIUD and belongs in the Deluge payload
alongside the hardcoded `institutionCode` 141 -- not as a column in every import
sheet.

## Open items -- read before relying on output

1. **Institute - Academic Programs raw column names are unverified.** That sheet in
   the HEDB 2026 dictionary has no "Database Field Name" column, so the 13 new
   `Prog_*` headers were inferred from the naming pattern of the existing 43. Every
   one carries a `RAW COLUMN NAME IS A GUESS` note. Check them against a real KHDA
   export before a production run -- a wrong header silently resolves to MISSING and
   the column is simply not converted.
2. **Four new Position Title codes are unknown.** The v35 picklist gained
   `Adjunct Faculty`, `Part-time Professor/Associate Professor/Assistant Professor`,
   `Provost/Chief Academic Officer` and `Associate Provost`. Their CHEDS codes are
   not in the dictionary's Staff Position sheet, so rows carrying them will be
   flagged unresolved rather than converted.
3. **`Area_of_Specialization` must match the first two digits of the CIP code.**
   KHDA validates this on both Graduates (`Grad_Major_CIP`) and Academic Programs.
   The tool does not check it yet.
4. **`Grad_Health_Fitness_Certificate`** is on the HEDB sheet but absent from the
   KHDA v2 Graduates field list. Left unmapped pending confirmation.
5. **No push workflow exists yet.** All seven forms are listed in
   `UNVERIFIED_NO_WORKFLOW` until KHDA issues client credentials and the
   `KHDA_Get_Token` / `KHDA_Post` transport layer is in place.

## Layout

```
khda_import_tool.py   conversion engine (unchanged from the CHEDS tool)
khda_forms.py         the seven-dataset registry
app_streamlit.py      web UI
app_cli.py            command line
mappings/             one JSON per dataset
_scratch/             build scripts, not part of the tool
```
