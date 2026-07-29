"""
Phase 2.3 - Problem Severity Scoring Model (quantified, reproducible)
Scores each identified problem on four weighted criteria and produces a ranked
priority list + chart. This turns Phase 2 from a narrative into a defensible,
computed prioritization - each score is traceable to Phase 1 evidence.

Scoring criteria (1-5 each), weighted:
  Evidence strength (25%) - how well Phase 1 proves the problem is real
  Impact severity   (30%) - how badly it harms park usability/experience
  User reach        (25%) - how many user groups / how much of the site it affects
  Urgency           (20%) - how time-critical / foundational it is to fix first
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(__file__), "..", "outputs")
os.makedirs(OUT, exist_ok=True)

WEIGHTS = {"Evidence": 0.25, "Impact": 0.30, "Reach": 0.25, "Urgency": 0.20}

# Each problem scored 1-5 per criterion, with the Phase 1 evidence basis noted.
problems = [
    {"id": "P1", "name": "Summer thermal discomfort (near-zero midday shade)",
     "Evidence": 5, "Impact": 5, "Reach": 5, "Urgency": 5,
     "basis": "Phase 1.05/1.06 computed: ~88° summer sun, <0.5m shadow at noon; affects whole site ~5 months/yr"},
    {"id": "P2", "name": "Undocumented / inadequate accessibility",
     "Evidence": 4, "Impact": 5, "Reach": 4, "Urgency": 4,
     "basis": "Phase 1.10: no verified universal-design features; brief mandates People of Determination access"},
    {"id": "P3", "name": "Shade inequity (canopy only on west side)",
     "Evidence": 4, "Impact": 3, "Reach": 4, "Urgency": 3,
     "basis": "Phase 1.02 image analysis + 1.11 SWOT: existing canopy concentrated west; east open/hot"},
    {"id": "P4", "name": "Missing commercial / service facilities",
     "Evidence": 3, "Impact": 3, "Reach": 4, "Urgency": 3,
     "basis": "Phase 1.03 + brief Section E: no kiosks/F&B; Manual benchmark ~15% leasable area unmet"},
    {"id": "P5", "name": "Weak legibility (arrival, wayfinding, lighting)",
     "Evidence": 3, "Impact": 3, "Reach": 3, "Urgency": 3,
     "basis": "Phase 1.03/1.10: single confirmed entrance, no signage/lighting data"},
    {"id": "P6", "name": "Severed metro/city connectivity across SZR",
     "Evidence": 4, "Impact": 2, "Reach": 3, "Urgency": 2,
     "basis": "Phase 1.08: ONPASSIVE metro across an 8-lane highway barrier; likely no safe crossing"},
    {"id": "P7", "name": "Irrigation-dependent landscape / water stress",
     "Evidence": 5, "Impact": 3, "Reach": 3, "Urgency": 3,
     "basis": "Phase 1.05: near-zero rainfall Jun-Sep; any planting is fully irrigation-dependent"},
    {"id": "P8", "name": "SZR-edge noise & air quality",
     "Evidence": 3, "Impact": 2, "Reach": 2, "Urgency": 2,
     "basis": "Phase 1.07: 8-lane arterial on east edge; no dB/air data but qualitatively significant"},
]

rows = []
for p in problems:
    weighted = sum(p[c] * WEIGHTS[c] for c in WEIGHTS)
    rows.append({**{k: p[k] for k in ["id","name","Evidence","Impact","Reach","Urgency"]},
                 "WeightedScore": round(weighted, 2), "basis": p["basis"]})

df = pd.DataFrame(rows).sort_values("WeightedScore", ascending=False).reset_index(drop=True)
df["Rank"] = df.index + 1
df["Priority"] = pd.cut(df["WeightedScore"], bins=[0,2.5,3.5,4.2,5],
                        labels=["LOW","MEDIUM","HIGH","CRITICAL"])

print("PHASE 2 - PROBLEM SEVERITY RANKING (computed):")
print(df[["Rank","id","name","WeightedScore","Priority"]].to_string(index=False))

df.to_csv(os.path.join(OUT, "problem_severity_scores.csv"), index=False)
with open(os.path.join(OUT, "problem_severity_scores.json"), "w") as f:
    json.dump(df.to_dict(orient="records"), f, indent=2, default=str)
print("\nSaved: problem_severity_scores.csv + .json")

# --- Chart: ranked weighted scores, colored by priority ---
color_map = {"CRITICAL": "#c1121f", "HIGH": "#e76f51", "MEDIUM": "#f4a261", "LOW": "#8ab17d"}
fig, ax = plt.subplots(figsize=(12, 7))
colors = [color_map[str(p)] for p in df["Priority"]]
bars = ax.barh([f"{r.id}: {r.name[:44]}" for r in df.itertuples()], df["WeightedScore"], color=colors)
for i, v in enumerate(df["WeightedScore"]):
    ax.text(v + 0.03, i, f"{v}", va="center", fontsize=9, fontweight="bold")
ax.set_xlabel("Weighted Severity Score (1–5)")
ax.set_xlim(0, 5.3)
ax.invert_yaxis()
ax.set_title("Al Safa 2 Park — Phase 2 Problem Severity Ranking\n"
             "(weighted: Evidence 25% · Impact 30% · Reach 25% · Urgency 20%)")
# legend
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=c, label=l) for l,c in color_map.items()], loc="lower right", title="Priority")
plt.tight_layout()
fig.savefig(os.path.join(OUT, "problem_severity_ranking.png"), dpi=160)
plt.close(fig)
print("Saved: problem_severity_ranking.png")

# --- Radar/heatmap of criteria scores per problem ---
fig, ax = plt.subplots(figsize=(10, 7))
crit = ["Evidence","Impact","Reach","Urgency"]
matrix = df[crit].values
im = ax.imshow(matrix, cmap="YlOrRd", aspect="auto", vmin=1, vmax=5)
ax.set_xticks(range(len(crit))); ax.set_xticklabels(crit)
ax.set_yticks(range(len(df))); ax.set_yticklabels([f"{r.id}" for r in df.itertuples()])
for i in range(len(df)):
    for j in range(len(crit)):
        ax.text(j, i, int(matrix[i,j]), ha="center", va="center",
                color="white" if matrix[i,j]>=4 else "black", fontweight="bold")
fig.colorbar(im, label="Score (1–5)")
ax.set_title("Al Safa 2 Park — Problem Scoring Matrix by Criterion")
plt.tight_layout()
fig.savefig(os.path.join(OUT, "problem_criteria_heatmap.png"), dpi=160)
plt.close(fig)
print("Saved: problem_criteria_heatmap.png")
