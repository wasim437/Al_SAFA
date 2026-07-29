"""
Phase 10 - Final Competition Package Compilation
Maps every deliverable produced across Phases 1-9 into the 12 official upload
folders (from the real submission form in UPLODED DOCUMENT DETAILS.txt), copies
the files, and produces a compliance checklist against the competition brief.
"""

import os
import shutil
import json

BASE = os.path.join(os.path.dirname(__file__), "..", "..")
REQ = os.path.join(os.path.dirname(__file__), "..", "10.2_Required_Files")

# --- The 12 required uploads (exact names from the real submission form) ---
# Each maps to: (source files to copy in, from which phases)
def p(*parts):
    return os.path.join(BASE, *parts)

mapping = {
    "01_Design_Narrative_Concept": [
        p("03_PHASE3_OPPORTUNITY_AND_OBJECTIVES", "Phase3_Opportunity_and_Objectives_Report.pdf"),
        p("04_PHASE4_CONCEPT_DEVELOPMENT", "Phase4_Concept_Development_Report.pdf"),
    ],
    "02_Preliminary_Design_Masterplan": [
        p("05_PHASE5_MASTERPLAN_DEVELOPMENT", "Phase5_Masterplan_Development_Report.pdf"),
        p("05_PHASE5_MASTERPLAN_DEVELOPMENT", "outputs", "masterplan_diagram.png"),
    ],
    "03_Concept_Plans_Spatial_Diagrams": [
        p("04_PHASE4_CONCEPT_DEVELOPMENT", "Phase4_Concept_Development_Report.pdf"),
        p("05_PHASE5_MASTERPLAN_DEVELOPMENT", "outputs", "masterplan_diagram.png"),
        p("05_PHASE5_MASTERPLAN_DEVELOPMENT", "outputs", "circulation_diagram.png"),
    ],
    "04_Key_Sections_Elevations": [
        p("06_PHASE6_DETAILED_DESIGN", "Phase6_Detailed_Design_Report.pdf"),
        p("06_PHASE6_DETAILED_DESIGN", "outputs", "section_shaded_spine.png"),
        p("06_PHASE6_DETAILED_DESIGN", "outputs", "elevation_entrance_gateway.png"),
        p("06_PHASE6_DETAILED_DESIGN", "outputs", "elevation_shaded_spine_long.png"),
    ],
    "05_3D_Spatial_Visualizations": [
        p("09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION", "outputs", "masterplan_aerial_golden_hour.jpg"),
        p("09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION", "outputs", "spine_corridor_interior.jpg"),
        p("09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION", "outputs", "thermal_comfort_heatmap.jpg"),
        p("09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION", "outputs", "aerial_day_view_1784970538631.jpg"),
        p("09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION", "outputs", "eyelevel_spine_1784970552956.jpg"),
        p("09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION", "outputs", "night_plaza_render_1784970565232.jpg"),
        p("09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION", "9.9_Presentation_Graphics", "presentation_board_1_concept.png"),
        p("09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION", "9.9_Presentation_Graphics", "presentation_board_2_evidence.png"),
    ],
    "06_AI_Methodology_Report": [
        p("09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION", "Phase9_AI_Workflow_and_Visualization_Report.pdf"),
        p("01_PHASE1_EXISTING_PARK", "12_AI_Analysis", "outputs", "Phase1.12_AI_Analysis_Report.pdf"),
    ],
    "07_User_Experience_Activation_Strategy": [
        p("08_PHASE8_USER_EXPERIENCE_AND_ACTIVATION", "Phase8_User_Experience_and_Activation_Report.pdf"),
    ],
    "08_Sustainability_Concept_Strategy": [
        p("07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY", "Phase7_Performance_and_Sustainability_Report.pdf"),
    ],
    "09_Material_Landscape_Palette": [
        p("06_PHASE6_DETAILED_DESIGN", "Phase6_Detailed_Design_Report.pdf"),
        p("06_PHASE6_DETAILED_DESIGN", "outputs", "planting_plan.png"),
    ],
    "10_Complete_Design_Report": [
        p("_FINAL_DELIVERABLES", "03_Submission_Package", "Al_Safa_2_Park_Complete_Design_Report.pdf"),
    ],
    "11_Site_Analysis_Human_Centric_Research": [
        p("01_PHASE1_EXISTING_PARK", "00_EXISTING_CONDITIONS_KNOWLEDGE_BASE.pdf"),
        p("01_PHASE1_EXISTING_PARK", "13_Catchment_Demand_Analysis", "outputs", "Phase1.13_Catchment_Demand_Analysis_Report.pdf"),
        p("02_PHASE2_PROBLEM_DEFINITION", "Phase2_Problem_Definition_Report.pdf"),
    ],
    "12_Concept_Animation_Video": [
        p("10_PHASE10_UPLOAD_DOCUMENTS", "10.2_Required_Files", "12_Concept_Animation_Video", "Concept_Animation_Storyboard.pdf"),
    ],
}

log = {"copied": [], "missing_source": [], "empty_slots": []}

for folder, sources in mapping.items():
    dest = os.path.join(REQ, folder)
    os.makedirs(dest, exist_ok=True)
    if not sources:
        log["empty_slots"].append(folder)
        continue
    for src in sources:
        if os.path.exists(src):
            target = os.path.join(dest, os.path.basename(src))
            if os.path.abspath(src) != os.path.abspath(target):
                shutil.copy2(src, target)
            log["copied"].append(f"{folder} <- {os.path.basename(src)}")
        else:
            log["missing_source"].append(f"{folder}: MISSING {src}")

print("COPIED:")
for c in log["copied"]:
    print("  +", c)
print("\nEMPTY SLOTS (need separate build/manual input):")
for e in log["empty_slots"]:
    print("  -", e)
if log["missing_source"]:
    print("\nMISSING SOURCES:")
    for m in log["missing_source"]:
        print("  !", m)

with open(os.path.join(os.path.dirname(__file__), "..", "compilation_log.json"), "w") as f:
    json.dump(log, f, indent=2)
print("\nSaved: compilation_log.json")
