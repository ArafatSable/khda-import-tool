import json, io
def load(p): return json.load(io.open(p, encoding="utf-8"))
def save(p,c): io.open(p,"w",encoding="utf-8").write(json.dumps(c,indent=2,ensure_ascii=False))

# 1. drop the duplicate Health/Fitness entry the patch added (it was already mapped)
p="mappings/Student_Graduates_mapping.json"; c=load(p)
seen=False; out=[]
for f in c["fields"]:
    if f.get("raw_column")=="Grad_Health_Fitness_Certificate":
        if seen: continue
        seen=True
    out.append(f)
c["fields"]=out; save(p,c)

# 2. Employee Basic Details: KHDA v2 has no passportNumber on this dataset,
#    and the HEDB 2026 sheet no longer carries the column either.
p="mappings/Employee_Basic_Details_mapping.json"; c=load(p)
for f in c["fields"]:
    if f.get("raw_column")=="Enroll_Passport_Number":
        f["target_field"]=None; f["kind"]="unmapped"
        f["_note"]=("2026-11-02 KHDA fork: dropped. The KHDA v2 Employee - Basic Details API has no "
                    "passportNumber field and the HEDB 2026 sheet no longer lists the column. The "
                    "Passport_Number field stays on the Zoho form but is not imported or pushed.")
save(p,c)
print("fixed")
