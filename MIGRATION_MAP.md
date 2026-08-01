# Migration map

Where everything went when the project was restructured into a repository layout. **Nothing was deleted** — every path below was moved, not removed.

Run `python tools/restructure.py --dry-run` to see the rules that produced this.

| Was | Is now | Contents |
|---|---|---|
| `10_PHASE10_UPLOAD_DOCUMENTS/10.2_Required_Files` | `submission` | 52 items |
| `_FINAL_DELIVERABLES/01_All_Phase_Reports` | `reports/pdf` | 9 items |
| `_FINAL_DELIVERABLES/01_All_Phase_Reports_EDITABLE_DOCX` | `reports/editable_docx` | 9 items |
| `_FINAL_DELIVERABLES/02_Key_Visuals` | `design/visuals` | 20 items |
| `_FINAL_DELIVERABLES/03_Submission_Package` | `reports/submission_package` | 2 items |
| `_FINAL_DELIVERABLES/EASY_UNDERSTANDING_GUIDE.pdf` | `reports/EASY_UNDERSTANDING_GUIDE.pdf` | 1 items |
| `_FINAL_DELIVERABLES/EASY_UNDERSTANDING_GUIDE.docx` | `reports/EASY_UNDERSTANDING_GUIDE.docx` | 1 items |
| `_FINAL_DELIVERABLES/PROJECT_METHODOLOGY_ROADMAP.pdf` | `reports/PROJECT_METHODOLOGY_ROADMAP.pdf` | 1 items |
| `_FINAL_DELIVERABLES/PROJECT_METHODOLOGY_ROADMAP.docx` | `reports/PROJECT_METHODOLOGY_ROADMAP.docx` | 1 items |
| `_FINAL_DELIVERABLES/AL_SAFA_2_PARK_MASTER_ALL_IN_ONE.pdf` | `reports/AL_SAFA_2_PARK_MASTER_ALL_IN_ONE.pdf` | 1 items |
| `09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION/9.7_Renderings` | `design/renders` | 14 items |
| `09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION/9.9_Presentation_Graphics` | `design/boards` | 2 items |
| `99_SOURCE_FILES` | `archive/source_files` | 8 items |
| `_PORTAL` | `archive/misc_superseded/portal/_PORTAL` | 10 items |
| `index.html` | `archive/misc_superseded/portal/index.html` | 1 items |
| `00_MASTER_TRACKER` | `archive/phases/00_MASTER_TRACKER` | 14 items |
| `01_PHASE1_EXISTING_PARK` | `archive/phases/01_PHASE1_EXISTING_PARK` | 141 items |
| `02_PHASE2_PROBLEM_DEFINITION` | `archive/phases/02_PHASE2_PROBLEM_DEFINITION` | 18 items |
| `03_PHASE3_OPPORTUNITY_AND_OBJECTIVES` | `archive/phases/03_PHASE3_OPPORTUNITY_AND_OBJECTIVES` | 12 items |
| `04_PHASE4_CONCEPT_DEVELOPMENT` | `archive/phases/04_PHASE4_CONCEPT_DEVELOPMENT` | 13 items |
| `05_PHASE5_MASTERPLAN_DEVELOPMENT` | `archive/phases/05_PHASE5_MASTERPLAN_DEVELOPMENT` | 25 items |
| `06_PHASE6_DETAILED_DESIGN` | `archive/phases/06_PHASE6_DETAILED_DESIGN` | 30 items |
| `07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY` | `archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY` | 51 items |
| `08_PHASE8_USER_EXPERIENCE_AND_ACTIVATION` | `archive/phases/08_PHASE8_USER_EXPERIENCE_AND_ACTIVATION` | 16 items |
| `09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION` | `archive/phases/09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION` | 24 items |
| `10_PHASE10_UPLOAD_DOCUMENTS` | `archive/phases/10_PHASE10_UPLOAD_DOCUMENTS` | 14 items |
| `_FINAL_DELIVERABLES` | `archive/misc_superseded/final_deliverables` | 1 items |
| `PDF_ONLY_DELIVERABLES` | `archive/misc_superseded/pdf_only_deliverables` | 16 items (2 survive after dedup) |
| `ADVANCED_ANALYSIS_OUTPUTS` | `archive/misc_superseded/legacy_outputs` | 11 items |
| `ADVANCED_DATASET_ANALYSIS.py` | `archive/misc_superseded/legacy_scripts/ADVANCED_DATASET_ANALYSIS.py` | 1 items |
| `gen_pdf_advanced_dataset_analysis.py` | `archive/misc_superseded/legacy_scripts/gen_pdf_advanced_dataset_analysis.py` | 1 items |
| `gen_pdf_winning_competition_package.py` | `archive/misc_superseded/legacy_scripts/gen_pdf_winning_competition_package.py` | 1 items |
| `START_HERE.md` | `archive/misc_superseded/START_HERE_superseded.md` | 1 items |

**Later consolidated** (see the cleanup commits): `_FINAL_DELIVERABLES`,
`PDF_ONLY_DELIVERABLES`, `ADVANCED_ANALYSIS_OUTPUTS`, `archive/legacy_scripts`,
`archive/superseded_site`, `archive/portal` and `START_HERE_superseded.md` were
folded into one `archive/misc_superseded/` folder — none of them were still
referenced by name from any other part of the pipeline, unlike
`archive/phases/`, `archive/source_files/`, `archive/withdrawn_visuals/` and
`archive/weak_renders/`, which stayed put because tools and docs point at them
by path.
