"""
Master rebuild: regenerates every phase PDF + the Phase 10 package, in order.
Run this after any change to report_builder.py or any analysis script.
"""
import subprocess, os, sys

BASE = os.path.join(os.path.dirname(__file__), "..", "..")

# (script dir, script file) in dependency order
jobs = [
    ("01_PHASE1_EXISTING_PARK/_scripts", "gen_pdf_01_regional.py"),
    ("01_PHASE1_EXISTING_PARK/_scripts", "gen_pdf_02_urban_context.py"),
    ("01_PHASE1_EXISTING_PARK/_scripts", "gen_pdf_03_existing_park.py"),
    ("01_PHASE1_EXISTING_PARK/_scripts", "gen_pdf_04_gis.py"),
    ("01_PHASE1_EXISTING_PARK/_scripts", "gen_pdf_05_climate.py"),
    ("01_PHASE1_EXISTING_PARK/_scripts", "gen_pdf_06_shadow.py"),
    ("01_PHASE1_EXISTING_PARK/_scripts", "gen_pdf_07_environmental.py"),
    ("01_PHASE1_EXISTING_PARK/_scripts", "gen_pdf_08_transportation.py"),
    ("01_PHASE1_EXISTING_PARK/_scripts", "gen_pdf_09_human.py"),
    ("01_PHASE1_EXISTING_PARK/_scripts", "gen_pdf_10_accessibility.py"),
    ("01_PHASE1_EXISTING_PARK/_scripts", "gen_pdf_11_swot.py"),
    ("01_PHASE1_EXISTING_PARK/_scripts", "gen_pdf_12_ai_analysis.py"),
    ("01_PHASE1_EXISTING_PARK/_scripts", "gen_pdf_13_catchment.py"),
    ("01_PHASE1_EXISTING_PARK/_scripts", "gen_pdf_00_knowledge_base.py"),
    ("02_PHASE2_PROBLEM_DEFINITION/_scripts", "gen_pdf_phase2.py"),
    ("03_PHASE3_OPPORTUNITY_AND_OBJECTIVES/_scripts", "gen_pdf_phase3.py"),
    ("04_PHASE4_CONCEPT_DEVELOPMENT/_scripts", "gen_pdf_phase4.py"),
    ("05_PHASE5_MASTERPLAN_DEVELOPMENT/_scripts", "gen_pdf_phase5.py"),
    ("06_PHASE6_DETAILED_DESIGN/_scripts", "gen_pdf_phase6.py"),
    ("07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/_scripts", "gen_pdf_phase7.py"),
    ("08_PHASE8_USER_EXPERIENCE_AND_ACTIVATION/_scripts", "gen_pdf_phase8.py"),
    ("09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION/_scripts", "gen_pdf_phase9.py"),
    ("00_MASTER_TRACKER/_scripts", "gen_pdf_easy_understanding.py"),
    ("00_MASTER_TRACKER/_scripts", "gen_pdf_roadmap.py"),
    ("10_PHASE10_UPLOAD_DOCUMENTS/_scripts", "01_compile_submission.py"),
    ("10_PHASE10_UPLOAD_DOCUMENTS/_scripts", "02_complete_design_report.py"),
    ("10_PHASE10_UPLOAD_DOCUMENTS/_scripts", "03_animation_storyboard.py"),
    ("10_PHASE10_UPLOAD_DOCUMENTS/_scripts", "04_submission_checklist.py"),
]

ok, fail = 0, 0
for d, f in jobs:
    script = os.path.join(BASE, d, f)
    if not os.path.exists(script):
        print(f"  SKIP (missing): {d}/{f}")
        continue
    r = subprocess.run([sys.executable, f], cwd=os.path.join(BASE, d),
                       capture_output=True, text=True)
    if r.returncode == 0:
        ok += 1
        print(f"  OK   {d}/{f}")
    else:
        fail += 1
        print(f"  FAIL {d}/{f}")
        print("       " + (r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "unknown error"))

print(f"\nDONE: {ok} ok, {fail} failed")
