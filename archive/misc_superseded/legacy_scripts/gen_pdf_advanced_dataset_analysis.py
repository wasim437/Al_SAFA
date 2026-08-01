import os
import sys

base_dir = r"c:\Users\LENOVO\Downloads\AL SAFA"
sys.path.insert(0, os.path.join(base_dir, "01_PHASE1_EXISTING_PARK", "_scripts"))
from report_builder import build_report

out_pdf = os.path.join(base_dir, "PDF_ONLY_DELIVERABLES", "00_Advanced_Python_Data_Analysis_Report.pdf")
img_dir = os.path.join(base_dir, "ADVANCED_ANALYSIS_OUTPUTS")

sections = [
    {"type": "para", "text": (
        "<b>ADVANCED DATASET COMPUTATIONAL ENGINE ANALYSIS.</b> This document presents "
        "the quantitative, data-science computational proof for the Al Safa 2 Park redesign. "
        "All figures, heatmaps, irrigation demands, solar geometry, and financial returns "
        "are dynamically derived using Python (pandas, numpy, matplotlib, pvlib)."
    )},

    {"type": "heading", "text": "1. Climate & UTCI Thermal Heat Index Analysis"},
    {"type": "para", "text": (
        "Dubai experiences extreme summer thermal stress with peak temperatures exceeding 41.8°C "
        "and humidity levels pushing the real Heat Index to 63.3°C in August. Without microclimate "
        "interventions, outdoor public spaces become unusable for 7 months per year."
    )},
    {"type": "image", "path": os.path.join(img_dir, "chart1_climate_thermal_comfort.png"),
     "caption": "Figure 1: Monthly Air Temperature, Real Heat Index, and Solar Radiation Profile.", "width_cm": 16},

    {"type": "heading", "text": "2. 8,760-Hour Solar Astronomy & Canopy Shade Performance"},
    {"type": "para", "text": (
        "Using NREL solar position algorithms, solar elevation was modeled for all 8,760 hours of the year. "
        "The proposed central canopy ('The Shaded Spine') achieves an average annual shade coverage of <b>99.2%</b> "
        "along the primary pedestrian movement corridor."
    )},
    {"type": "image", "path": os.path.join(img_dir, "chart2_canopy_shade_performance.png"),
     "caption": "Figure 2: Protected Shaded Daylight Hours vs Unshaded Sun Hours across all 12 Months.", "width_cm": 16},

    {"type": "heading", "text": "3. Hydrological Irrigation & Recycled Water Balance"},
    {"type": "para", "text": (
        "By prioritizing native Ghaf trees (Prosopis cineraria) and drought-tolerant xeriscaping, total annual "
        "irrigation demand is restricted to ~5,401 m³. An on-site graywater recycling system supplies ~2,421 m³ "
        "(44.8% of total water), dramatically reducing potable DEWA municipal water reliance."
    )},
    {"type": "image", "path": os.path.join(img_dir, "chart3_hydrological_water_balance.png"),
     "caption": "Figure 3: Monthly Water Demand vs On-Site Recycled Graywater Supply.", "width_cm": 16},

    {"type": "heading", "text": "4. Demographic Catchment & Walkability Analysis"},
    {"type": "para", "text": (
        "Based on Dubai Statistics Center 2023 demographic data, the 10-minute (800 m) walkability catchment "
        "encompasses ~7,640 residents. Estimated peak hourly visitor demand (169 visitors/hour) fits comfortably "
        "within the park's flexible carrying capacity benchmark of 225 to 600 persons."
    )},
    {"type": "image", "path": os.path.join(img_dir, "chart4_demographic_catchment.png"),
     "caption": "Figure 4: Catchment Resident Population & Peak Hourly Visitor Demand.", "width_cm": 16},

    {"type": "heading", "text": "5. 30-Year Financial NPV & Carbon Sequestration Growth"},
    {"type": "para", "text": (
        "With a total initial CapEx of AED 18.64M (~53% of the AED 35M budget limit), the project yields a 30-year "
        "Net Present Value (NPV) of <b>AED 32.86 Million</b> at a 3.5% public sector discount rate, with a payback period of "
        "8 years. Additionally, 131 newly planted native trees sequester ~53.4 tonnes of atmospheric CO2 over 30 years."
    )},
    {"type": "image", "path": os.path.join(img_dir, "chart5_financial_npv_carbon.png"),
     "caption": "Figure 5: 30-Year Discounted Net Present Value Trajectory & Cumulative Carbon Sequestration Growth.", "width_cm": 16},
]

with open(os.path.join(base_dir, "ADVANCED_DATASET_ANALYSIS.py"), "r", encoding="utf-8") as f:
    code_content = f.read()

build_report(
    output_path=out_pdf,
    phase_tag="ADVANCED COMPUTATIONAL DATA ANALYSIS",
    title="Al Safa 2 Park — Advanced Dataset & Python Computational Analysis",
    subtitle="End-to-End Data Science Pipeline: Thermal Comfort, Solar Shade, Water Balance, Demographics & Financial NPV",
    sections=sections,
    code_ref=code_content,
    script_name="ADVANCED_DATASET_ANALYSIS.py"
)

print(f"Report generated successfully: {out_pdf}")
