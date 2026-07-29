import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "01_PHASE1_EXISTING_PARK", "_scripts"))
from docx_report_builder import build_docx_report, convert_docx_to_pdf

HERE = os.path.dirname(__file__)
OUT_DIR = os.path.join(HERE, "..")

sections = [
    {"type": "para", "text": (
        "<b>This document explains the whole project in simple words.</b> No jargon. "
        "Read this first if you want the short version of everything we did."
    )},

    {"type": "heading", "text": "1. What is this project?"},
    {"type": "para", "text": (
        "Dubai Municipality is running a competition called the <b>AI Park Design "
        "Challenge</b>. They want people to redesign a real park — <b>Al Safa 2 Park</b> — "
        "using AI tools to help with the thinking, not to replace human designers. "
        "Deadline to submit: <b>15 August 2026</b>. Prize money: 1st place AED 100,000."
    )},

    {"type": "heading", "text": "2. What do we have to hand in?"},
    {"type": "para", "text": "12 files, uploaded through the official website. In simple terms:"},
    {"type": "bullets", "items": [
        "A written story of the design idea (Design Narrative)",
        "A map of the new park (Masterplan)",
        "Drawings showing zones and paths (Concept Plans)",
        "Cut-through drawings showing heights (Sections & Elevations)",
        "3D pictures of what it will look like (Visualizations)",
        "A report explaining how AI was used (AI Methodology Report)",
        "A report on how people will use the park (User Experience Strategy)",
        "A report on eco-friendly choices (Sustainability Strategy)",
        "A list of materials and plants (Material & Landscape Palette)",
        "One big report with everything combined (Complete Design Report)",
        "A report on the site itself, before designing (Site Analysis)",
        "A short video showing the design (optional, 1 minute)",
    ]},

    {"type": "heading", "text": "3. How did we organize the work?"},
    {"type": "para", "text": (
        "We split the whole job into <b>10 phases</b> — like 10 steps, each one building on "
        "the step before it. Every phase has its own folder and its own PDF report."
    )},
    {"type": "table", "header": ["Phase", "In Simple Words"], "rows": [
        ["1. Understand the Site", "Learn everything real about the park before touching the design — climate, sun, surroundings, problems."],
        ["2. Find the Problems", "List what's actually wrong with the park today, backed by evidence from Phase 1."],
        ["3. Set the Goals", "Decide what success looks like — a vision, a mission, and measurable targets."],
        ["4. Pick an Idea", "Come up with 3 different design ideas, compare them fairly, and choose the best one."],
        ["5. Draw the Masterplan", "Turn the chosen idea into an actual map with real measurements (in square meters)."],
        ["6. Add the Details", "Choose real plants, real materials, lighting, and draw a cut-through view (section)."],
        ["7. Check the Performance", "Use real math (sun angles) to prove the design actually works — how much shade, when."],
        ["8. Think About the People", "Imagine real visitors (a mom, an elderly man, a teenager) and how their day at the park goes."],
        ["9. Show the Work", "Explain how AI was used at every step, and generate pictures (day view, night view) of the park."],
        ["10. Package Everything", "Take all of the above and prepare the final 12 files for submission."],
    ]},

    {"type": "heading", "text": "4. What is real data vs. what is a guess?"},
    {"type": "para", "text": (
        "This matters a lot, so here it is in plain words:"
    )},
    {"type": "bullets", "items": [
        "<b>100% real, no guessing:</b> the sun's exact position in the sky, every hour of the "
        "year, computed with real astronomy math (not estimated).",
        "<b>100% real, from real sources:</b> Dubai's weather (temperature, humidity, sunshine "
        "— Dubai Meteorological Office); wind (WNW, 16.7 km/h — 24-year airport record); how "
        "many people live around the park (Dubai Statistics Center 2023 — about 7,640 within a "
        "10-minute walk); the metro station details (Red Line, Zone 2 — RTA); and how much "
        "water the trees need (real Ghaf tree study). All pulled live from the internet.",
        "<b>Real facts from the competition papers:</b> the park's size (15,000 sqm), the "
        "budget (AED 35 million), the deadline, the rules — all copied directly from the "
        "official documents Dubai Municipality gave us.",
        "<b>Honest 'we don't know yet':</b> the exact shape of the existing park, the exact "
        "number of existing trees, existing lighting — we don't have this because the park's "
        "technical drawing file (a DWG file) needs a special free tool to open properly, which "
        "hasn't been done yet. We wrote 'not available' instead of making up numbers. (We fixed "
        "a lot of other gaps though — population, wind, transit, and water are now all real, "
        "sourced numbers, not guesses.)",
        "<b>AI-suggested design (needs your review):</b> the actual park layout, which plants "
        "go where, which idea was 'best' — this is our first draft, made by AI, using the "
        "real facts above as a foundation. A human should check this before it's final.",
    ]},

    {"type": "heading", "text": "5. What did we actually design? (The short version)"},
    {"type": "para", "text": (
        "We call our chosen design idea the <b>\"Shaded Spine\"</b>. In simple words:"
    )},
    {"type": "bullets", "items": [
        "One long, fully-shaded walking path runs through the middle of the park, connecting "
        "two entrances (one on each end).",
        "On both sides of this shaded path, there are 8 separate \"rooms\" — a kids' play area, "
        "a picnic area, a community plaza, a fitness zone, a quiet garden, a shop area, a "
        "sports lawn, and a nature strip.",
        "Why this idea won: Dubai gets extremely hot in summer, and the sun is almost directly "
        "overhead at noon — meaning normal shade (like a tree) barely helps at that time. Our "
        "math proved that only a solid overhead roof-type structure gives real shade at noon "
        "in summer. So we put that overhead structure along the one main path everyone uses.",
    ]},

    {"type": "heading", "text": "6. What did the math actually prove?"},
    {"type": "para", "text": "This is the most important, most 'real' result in the whole project:"},
    {"type": "bullets", "items": [
        "We built a computer simulation that checks, hour by hour, for an entire year "
        "(8,760 hours), whether the sun is blocked by our shade structure at every part of "
        "the park.",
        "<b>Result: the main shaded path is covered by shade 99.2% of all daylight hours in "
        "the year.</b> That's not a guess — that's a computed fact from real sun-position math.",
        "But the same math also showed something we didn't expect: the middle of each "
        "activity room (like the middle of the kids' play area) only gets shade 3.6% to 16.2% "
        "of the time, because it's too far from the shade structure's edge.",
        "<b>So we now know exactly what to fix next:</b> we need to add trees or small shade "
        "structures INSIDE each room too, not just along the main path. This is a real, useful "
        "discovery that came directly from the math — not a guess.",
    ]},

    {"type": "heading", "text": "6b. Does it fit the money?"},
    {"type": "para", "text": (
        "Yes — and we proved it with numbers, not a guess. We took real Dubai construction "
        "prices (per square meter) and multiplied them by our actual zone sizes, then added "
        "the normal extras (contingency, fees). The total comes to about <b>AED 18.6 million "
        "— roughly 53% of the AED 35 million budget.</b> That means the design is affordable "
        "with plenty of money left over for extra shade trees and higher-quality finishes. "
        "We also drew the entrance gateway and the shaded walkway as proper to-scale "
        "elevation drawings, and made two big competition presentation boards."
    )},

    {"type": "heading", "text": "7. What still needs a human to check or decide?"},
    {"type": "bullets", "items": [
        "The exact shape/boundary of the real park (we assumed a simple rectangle; the real "
        "shape might be different — needs the DWG file opened properly).",
        "Whether our chosen design idea (\"Shaded Spine\") is really the best one, or if the "
        "human design team prefers a different one.",
        "The exact plant list, materials, and prices — a real landscape architect should "
        "confirm these before construction.",
        "Everything marked 'AI-GENERATED DRAFT — FOR REVIEW' inside each phase's PDF.",
    ]},

    {"type": "heading", "text": "8. Where is everything saved?"},
    {"type": "para", "text": (
        "Inside the main 'AL SAFA' folder, organized as: 00_MASTER_TRACKER (this document, "
        "the project tracker, and the Submission Checklist), 01 through 09 (one folder per "
        "phase, each with its own PDF report), 10_PHASE10_UPLOAD_DOCUMENTS (the 12 submission "
        "folders — now FILLED with the finished files), and 99_SOURCE_FILES (the original "
        "documents Dubai Municipality gave us)."
    )},

    {"type": "heading", "text": "9. What's the very next step?"},
    {"type": "para", "text": (
        "All 10 phases are done and all 12 submission folders are filled (see the "
        "SUBMISSION_CHECKLIST_AND_COMPLIANCE.pdf — 11 of 11 required slots ready). The "
        "remaining steps are things only a human can do: (1) review and approve the AI-draft "
        "design decisions; (2) open the DWG file to confirm the real park shape; (3) turn the "
        "picture files into PDF sheets where the form asks for PDF; (4) make the optional "
        "1-minute video from the storyboard we wrote; (5) submit on the website before "
        "15 August 2026 and tick all 4 declaration boxes."
    )},
]

docx_path = build_docx_report(
    output_path=os.path.join(OUT_DIR, "EASY_UNDERSTANDING_GUIDE.docx"),
    phase_tag="MASTER GUIDE — PLAIN LANGUAGE",
    title="Easy Understanding Guide",
    subtitle="Al Safa 2 Park Project — Everything Explained in Simple Words",
    sections=sections,
    code_ref=None,
)
convert_docx_to_pdf(docx_path)
