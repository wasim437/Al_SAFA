import os
from pypdf import PdfWriter

base_dir = r"c:\Users\LENOVO\Downloads\AL SAFA"
final_dir = os.path.join(base_dir, "_FINAL_DELIVERABLES")

pdf_files = [
    os.path.join(final_dir, "EASY_UNDERSTANDING_GUIDE.pdf"),
    os.path.join(final_dir, "PROJECT_METHODOLOGY_ROADMAP.pdf"),
    os.path.join(final_dir, "03_Submission_Package", "Al_Safa_2_Park_Complete_Design_Report.pdf"),
    os.path.join(final_dir, "01_All_Phase_Reports", "Phase1_Knowledge_Base.pdf"),
    os.path.join(final_dir, "01_All_Phase_Reports", "Phase2_Problem_Definition_Report.pdf"),
    os.path.join(final_dir, "01_All_Phase_Reports", "Phase3_Opportunity_and_Objectives_Report.pdf"),
    os.path.join(final_dir, "01_All_Phase_Reports", "Phase4_Concept_Development_Report.pdf"),
    os.path.join(final_dir, "01_All_Phase_Reports", "Phase5_Masterplan_Development_Report.pdf"),
    os.path.join(final_dir, "01_All_Phase_Reports", "Phase6_Detailed_Design_Report.pdf"),
    os.path.join(final_dir, "01_All_Phase_Reports", "Phase7_Performance_and_Sustainability_Report.pdf"),
    os.path.join(final_dir, "01_All_Phase_Reports", "Phase8_User_Experience_and_Activation_Report.pdf"),
    os.path.join(final_dir, "01_All_Phase_Reports", "Phase9_AI_Workflow_and_Visualization_Report.pdf"),
]

merger = PdfWriter()

for pdf in pdf_files:
    if os.path.exists(pdf):
        print(f"Adding: {os.path.basename(pdf)}")
        merger.append(pdf)
    else:
        print(f"Warning: File not found: {pdf}")

output_path = os.path.join(final_dir, "AL_SAFA_2_PARK_MASTER_ALL_IN_ONE.pdf")
with open(output_path, "wb") as f_out:
    merger.write(f_out)

print(f"Successfully generated single merged PDF: {output_path}")
