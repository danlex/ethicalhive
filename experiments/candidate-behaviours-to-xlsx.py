"""Convert the candidate-behaviours markdown list into an Excel workbook.

Usage: python md_to_xlsx.py <input.md> <output.xlsx>
"""
import os
import json
from pathlib import Path
import re
import sys

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

src, out = sys.argv[1], sys.argv[2]
rows, groups, group = [], [], None
for line in open(src, encoding="utf-8"):
    m = re.match(r"^## ([A-Z]{1,2})\. (.+?) \(\d+\)", line)
    if m:
        group = m.group(2)
        groups.append(group)
        continue
    m = re.match(r"^\| (\d+) \|(.*)\|\s*$", line)
    if m and group:
        cells = [c.strip().replace("*", "") for c in m.group(2).split("|")]
        name, source, human, ai, nearest = cells[:5]
        n = int(m.group(1))
        rows.append([n, group, name, source, human, ai, nearest,
                     "Batch 8" if n > 422 else "Batch 7" if n > 305 else "Batch 6" if n > 190 else "Batch 5" if n > 180 else "Batch 4" if n > 169 else "Batch 3" if n > 145 else "Batch 2" if n > 100 else "Batch 1",
                     cells[5] if len(cells) > 5 else "From general knowledge"])
assert len(rows) == 541, len(rows)
review_path = os.path.join(os.path.dirname(src), "candidate-review-2026-11-06.tsv")
review = {}
if os.path.exists(review_path):
    for line in open(review_path, encoding="utf-8"):
        f = line.rstrip("\n").split("\t")
        if len(f) == 8:
            review[int(f[0])] = f
orig_path = os.path.join(os.path.dirname(src), "candidate-original-check-2026-11-07.tsv")
orig = {}
if os.path.exists(orig_path):
    for line in open(orig_path, encoding="utf-8"):
        f = line.rstrip("\n").split("\t")
        if len(f) == 8:
            orig[int(f[0])] = f

FONT = "Arial"
head_fill = PatternFill("solid", start_color="1F3864")
input_fill = PatternFill("solid", start_color="FFF2CC")
thin = Side(style="thin", color="BFBFBF")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

# Preserve the reviewer's three editable columns when refreshing generated data.
manual = {}
if Path(out).exists():
    previous = load_workbook(out, read_only=True, data_only=False)
    if "Behaviours" in previous.sheetnames:
        for values in previous["Behaviours"].iter_rows(min_row=2, values_only=True):
            if values[0] is not None:
                manual[values[0]] = list(values[9:12])
    previous.close()
correction_path = Path(src).resolve().parents[1] / "references/source-corrections-review-2026-11-07.json"
corrections = {}
if correction_path.exists():
    corrections = {r["bundle_candidate_id"]: r for r in json.loads(correction_path.read_text())["records"]}
wb = Workbook()
ws = wb.active
ws.title = "Behaviours"
headers = ["#", "Group", "Behaviour", "Source", "Human definition",
           "In an AI", "Nearest existing mode", "Batch", "Evidence",
           "Verification status", "Decision", "Notes",
           "Review: definition", "Review: source", "Review: AI parallel",
           "Review: duplicate of", "Review note",
           "Prior text search: term", "Prior text search: definition", "Work/edition searched", "Supplied quote", "Prior search caveat", "Current bibliography check", "Current definition check", "Correction evidence URLs", "Correction access and limits"]
widths = [5, 24, 30, 36, 48, 52, 28, 10, 40, 18, 16, 30, 14, 14, 14, 26, 50, 18, 16, 40, 50, 60, 30, 35, 60, 80]
ws.append(headers)
for i, (h, w) in enumerate(zip(headers, widths), start=1):
    c = ws.cell(row=1, column=i)
    c.font = Font(name=FONT, bold=True, color="FFFFFF")
    c.fill = head_fill
    c.alignment = Alignment(vertical="center", wrap_text=True)
    ws.column_dimensions[c.column_letter].width = w
for r in rows:
    v = review.get(r[0], [""] * 8)
    c = corrections.get(r[0])
    checks = ([c["bibliographic_review"]["status"], c["definition_review"]["status"],
               " ; ".join(c["bibliographic_review"]["evidence_urls"]),
               c["bibliographic_review"]["access_depth"] + " " + c["qualification"]] if c else [""] * 4)
    ws.append(r + manual.get(r[0], ["Unverified", "", ""]) +
              [v[2], v[3], v[5], v[6], v[7]] +
              [orig.get(r[0], [""] * 8)[k] for k in (4, 5, 2, 6, 7)] + checks)
last = len(rows) + 1
for row in ws.iter_rows(min_row=2, max_row=last):
    for c in row:
        c.font = Font(name=FONT, size=10)
        c.alignment = Alignment(vertical="top", wrap_text=True)
        c.border = border
    row[2].font = Font(name=FONT, size=10, bold=True)
    for c in row[9:12]:
        c.fill = input_fill
ws.freeze_panes = "D2"
ws.auto_filter.ref = f"A1:Z{last}"

dv_status = DataValidation(type="list", allow_blank=True,
                           formula1='"Unverified,Search-checked,Source checked,LLM paper found,Rejected"')
dv_dec = DataValidation(type="list", allow_blank=True,
                        formula1='"New mode,Synonym,Drop,Undecided"')
ws.add_data_validation(dv_status)
ws.add_data_validation(dv_dec)
dv_status.add(f"J2:J{last}")
dv_dec.add(f"K2:K{last}")

s = wb.create_sheet("Summary")
s["A1"] = f"{len(rows)} candidate AI behaviours from psychology and psychotherapy"
s["A1"].font = Font(name=FONT, bold=True, size=13)
s["A3"], s["B3"], s["C3"], s["D3"], s["E3"], s["F3"], s["G3"] = "Group", "Behaviours", "Close to an existing mode", "Batches 2 to 8 (search-checked)", "Source checked", "Duplicate per review", "Historical reported term hits"
for col in "ABCDEFG":
    s[f"{col}3"].font = Font(name=FONT, bold=True, color="FFFFFF")
    s[f"{col}3"].fill = head_fill
rng = f"Behaviours!$B$2:$B${last}"
for i, g in enumerate(groups, start=4):
    s[f"A{i}"] = g
    s[f"B{i}"] = f'=COUNTIF({rng},A{i})'
    s[f"C{i}"] = f'=COUNTIFS({rng},A{i},Behaviours!$G$2:$G${last},"?*")'
    s[f"D{i}"] = f'=COUNTIFS({rng},A{i},Behaviours!$H$2:$H${last},"<>Batch 1")'
    s[f"E{i}"] = f'=COUNTIFS({rng},A{i},Behaviours!$J$2:$J${last},"Source checked")'
    s[f"F{i}"] = f'=COUNTIFS({rng},A{i},Behaviours!$P$2:$P${last},"?*")'
    s[f"G{i}"] = f'=COUNTIFS({rng},A{i},Behaviours!$R$2:$R${last},"FOUND")'
tot = 4 + len(groups)
s[f"A{tot}"] = "Total"
for col in "BCDEFG":
    s[f"{col}{tot}"] = f"=SUM({col}4:{col}{tot - 1})"
for row in s.iter_rows(min_row=4, max_row=tot):
    for c in row:
        c.font = Font(name=FONT, bold=(c.row == tot))
        c.border = border
n = tot + 2
notes = [
    "How to use: the yellow columns on the Behaviours sheet (Verification status, Decision, Notes) are for you to fill in; pick values from the drop-downs.",
    "Example: set Verification status to 'Source checked' once the attribution is confirmed in the book or paper, and Decision to 'Synonym' if it duplicates the Nearest existing mode.",
    "Scope: research working records, not new catalogue admissions. The supplied review and text-search reports do not establish an independent audit or full-book reading. The rest of the bundle has not been re-audited.",
    "Current corrections: see references/source-corrections-review-2026-11-07.json. Bibliography, definition support and empirical AI evidence are separate. All AI examples remain untested proposals.",
    "Historical text-search results refer to the listed work and edition, which may differ from the corrected source. DIFFERS refers to the pre-correction definition. Unsuccessful searches do not prove absence.",
    "Deduplication: supplied overlap fields are historical leads. Many names already occur in the current 434-record catalogue; an empty overlap cell does not establish novelty. Bundle numbers are not website Reference IDs.",
    "Regeneration preserves Verification status, Decision and Notes by local research ID. Generated review columns are refreshed from source records.",
    "Source file: experiments/candidate-behaviours-2026-11-06.md (danlex/ethicalhive).",
]
for i, t in enumerate(notes):
    c = s.cell(row=n + i, column=1, value=t)
    c.font = Font(name=FONT, size=10, italic=(i >= 2))
s.column_dimensions["A"].width = 44
for col in "BCDEFG":
    s.column_dimensions[col].width = 22
wb.move_sheet("Summary", offset=-1)
wb.active = 0
wb.save(out)
print(f"wrote {len(rows)} rows, {len(groups)} groups -> {out}")
