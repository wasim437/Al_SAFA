import zipfile, pathlib

root = pathlib.Path("c:/Users/LENOVO/Downloads/AL SAFA")
upload_dir = root / "UPLOAD_THESE_12_FILES"

pdf_12 = upload_dir / "12_One-minute_Concept_Animation.pdf"
video = upload_dir / "Falaj_Al_Safa_Concept_Film_60s_4K.mp4"

assert pdf_12.exists(), "12_One-minute_Concept_Animation.pdf missing"
assert video.exists(), "Falaj_Al_Safa_Concept_Film_60s_4K.mp4 missing"

zip_path = root / "SLOT_12_VIDEO_AND_PDF.zip"

print(f"Creating {zip_path.name} with video and 12th PDF...")

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    z.write(pdf_12, arcname=pdf_12.name)
    z.write(video, arcname=video.name)
    print(f"  + {pdf_12.name} ({pdf_12.stat().st_size / (1024*1024):.1f} MB)")
    print(f"  + {video.name} ({video.stat().st_size / (1024*1024):.1f} MB)")

zip_mb = zip_path.stat().st_size / (1024 * 1024)
print(f"\nSUCCESS: Created {zip_path.name} ({zip_mb:.1f} MB total)")
