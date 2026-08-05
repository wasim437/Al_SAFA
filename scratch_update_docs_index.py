from pathlib import Path

p = Path("docs/index.html")
t = p.read_text(encoding="utf-8")

old_topbar = '<button class="icon-btn" id="printBtn" aria-label="Print full report" title="Print the whole portal">⎙</button>'
new_topbar = '<a href="concept_film_hero.html" style="background:#B03A48; color:#ffffff; padding:6px 14px; border-radius:6px; font-weight:700; text-decoration:none; font-size:12px; display:inline-flex; align-items:center; gap:6px; margin-left:8px;" target="_blank">▶ 60s 4K Film</a>\n    ' + old_topbar

old_overview = '<div class="page-head">'
new_overview = """<div style="background: linear-gradient(135deg, #1f2430, #0f131a); border: 1px solid #2e3646; border-left: 4px solid #f59e0b; border-radius: 8px; padding: 16px 20px; margin-bottom: 24px; display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap;">
    <div>
        <div style="font-weight: 700; font-size: 16px; color: #f59e0b; margin-bottom: 4px;">▶ 60-Second Concept Animation Film (4K)</div>
        <div style="font-size: 13px; color: #9ca3af;">Drawn entirely from project data — no photographs. Solar model &amp; heat index 56.8 °C → 48.7 °C.</div>
    </div>
    <a href="concept_film_hero.html" style="background: #f59e0b; color: #07070a; padding: 10px 20px; border-radius: 6px; font-weight: 700; text-decoration: none; font-size: 14px; white-space: nowrap;">Play 4K Concept Film →</a>
</div>
<div class="page-head">"""

assert old_topbar in t, "old_topbar not found"
assert old_overview in t, "old_overview not found"

t = t.replace(old_topbar, new_topbar, 1)
t = t.replace(old_overview, new_overview, 1)
p.write_text(t, encoding="utf-8")
print("Updated docs/index.html with direct film link & hero banner!")
