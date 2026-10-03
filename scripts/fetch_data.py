import os, sys, csv, collections
import requests
url = os.environ.get("BUDGET_URL", "").strip()
dept_f = os.environ.get("DEPT_FIELD", "department")
amt_f = os.environ.get("AMOUNT_FIELD", "amount")
if not url:
    print("BUDGET_URL not set; keeping existing data/budget.csv")
    sys.exit(0)
resp = requests.get(url, params={"$limit": 50000}, timeout=60)
resp.raise_for_status()
rows = resp.json()
if not rows or dept_f not in rows[0] or amt_f not in rows[0]:
    print("ERROR: source format changed.")
    sys.exit(1)
totals = collections.defaultdict(float)
for r in rows:
    try:
        totals[str(r[dept_f]).strip()] += float(str(r[amt_f]).replace(",", "").replace("$", ""))
    except (ValueError, KeyError):
        continue
os.makedirs("data", exist_ok=True)
with open("data/budget.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["department", "amount"])
    for k, v in sorted(totals.items(), key=lambda kv: -kv[1]):
        w.writerow([k, round(v, 2)])
print("Wrote", len(totals), "departments")