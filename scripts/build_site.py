import csv, datetime, html, os
SOURCE_NAME = os.environ.get("SOURCE_NAME") or "SAMPLE DATA - replace with the real County of San Diego dataset"
SOURCE_URL = os.environ.get("BUDGET_PAGE_URL") or "https://data.sandiegocounty.gov"
with open("data/budget.csv", newline="", encoding="utf-8") as f:
    rows = [(r["department"], float(r["amount"])) for r in csv.DictReader(f)]
rows.sort(key=lambda r: -r[1])
top = rows[:12]
mx = max(a for _, a in top) or 1
def money(x): return "${:,.0f}".format(x)
bars = []
for i, (name, amt) in enumerate(top):
    y = i * 28 + 4
    w = int(420 * amt / mx)
    bars.append('<text class="lbl" x="0" y="%d">%s</text>' % (y + 14, html.escape(name[:28])) +
        '<rect class="bar" x="210" y="%d" width="%d" height="18"/>' % (y, w) +
        '<text class="lbl" x="%d" y="%d">%s</text>' % (214 + w, y + 14, money(amt)))
svg = '<svg class="chart" viewBox="0 0 760 %d" role="img" aria-label="Budget by department">%s</svg>' % (len(top) * 28 + 8, "".join(bars))
trs = "".join('<tr><td>%s</td><td class="num">%s</td></tr>' % (html.escape(n), money(a)) for n, a in rows)
today = datetime.date.today().isoformat()
page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="referrer" content="no-referrer">
<title>Budget by department - San Diego County Transparency</title>
<link rel="stylesheet" href="style.css"></head><body>
<header><strong>San Diego County Transparency</strong>
<nav><a href="index.html">Home</a><a href="budget.html">Budget</a><a href="methodology.html">Methodology</a><a href="corrections.html">Corrections</a><a href="disclaimer.html">Disclaimer</a></nav></header>
<main>
<h1>County budget by department</h1>
{svg}
<table><thead><tr><th>Department</th><th class="num">Amount</th></tr></thead><tbody>{trs}</tbody></table>
<p class="note">Source: {html.escape(SOURCE_NAME)} (<a href="{html.escape(SOURCE_URL)}">link</a>). Last updated: {today}.</p>
</main>
<footer>Independent public-interest project. Not affiliated with any government. Read-only: this site collects no data.</footer>
</body></html>"""
with open("site/budget.html", "w", encoding="utf-8") as f:
    f.write(page)
print("Built site/budget.html")