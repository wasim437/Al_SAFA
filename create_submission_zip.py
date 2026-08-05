import zipfile, os, pathlib

root = pathlib.Path("c:/Users/LENOVO/Downloads/AL SAFA")
upload_dir = root / "UPLOAD_THESE_12_FILES"
zip_path = root / "AL_SAFA_2_PARK_SUBMISSION_PACK.zip"

files_to_zip = sorted(list(upload_dir.glob("*.pdf")) + list(upload_dir.glob("*.mp4")))

print(f"Packaging {len(files_to_zip)} files into {zip_path.name}...")

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for f in files_to_zip:
        z.write(f, arcname=f.name)
        mb = f.stat().st_size / (1024 * 1024)
        print(f"  + {f.name} ({mb:.1f} MB)")

zip_mb = zip_path.stat().st_size / (1024 * 1024)
print(f"\nSUCCESS: Created {zip_path.name} ({zip_mb:.1f} MB total)")
