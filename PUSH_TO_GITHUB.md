# Publishing this repository

Everything is committed and ready. This machine had **no network connection to
github.com** when the work was done (`Test-NetConnection github.com -Port 443`
returned `False`), so the push itself is the one step left to you.

Two commits are waiting:

```
8d134d2  Keep personal contact details out of the public repository
e65dbd7  Rebuild as a reproducible data-analysis and ML project
```

433 tracked files. Run `git log --stat` to see exactly what will be published
before you push anything.

---

## Option A — GitHub CLI (easiest)

Install once, from PowerShell:

```powershell
winget install --id GitHub.cli
```

Then, from the project folder:

```powershell
cd "c:\Users\LENOVO\Downloads\AL SAFA"
gh auth login                      # choose GitHub.com → HTTPS → login with a browser
gh repo create al-safa-2-park-ai --public --source=. --remote=origin --push
```

That creates the repository and pushes in one command.

---

## Option B — Plain git (no extra install)

1. Create an empty repository on GitHub named **`al-safa-2-park-ai`**.
   Do **not** let GitHub add a README, .gitignore or licence — this repo already
   has them and an initialised remote will cause a conflict.

2. Then:

```powershell
cd "c:\Users\LENOVO\Downloads\AL SAFA"
git remote add origin https://github.com/wasimmisaw437/al-safa-2-park-ai.git
git push -u origin main
```

Git Credential Manager will open a browser for authentication the first time.

---

## Turn on the website

The site lives in `docs/`. After the first push:

**Settings → Pages → Build and deployment**
- Source: **Deploy from a branch**
- Branch: **`main`**, folder: **`/docs`** → **Save**

It goes live in a minute or two at:

**https://wasimmisaw437.github.io/al-safa-2-park-ai/**

---

## Check the username first

Every link in `README.md`, `docs/index.html` and `src/config.py` assumes the
GitHub username **`wasimmisaw437`** — taken from the email on your submission
form. Your Hugging Face account is `wasimmisaw`, so it is worth confirming which
one your GitHub account actually uses.

If it differs, change it in **one place** and rebuild:

```powershell
# edit GITHUB_USER in src/config.py, then:
python tools/build_site.py
```

`README.md` has the username written out in its links, so search and replace
there too if it changes.

---

## What is deliberately not published

| Item | Why |
|---|---|
| `00_BRIEF/UPLODED DOCUMENT DETAILS.txt` | Contains your name, email and mobile number. Gitignored — stays on your disk only. |
| `__pycache__/`, `.ipynb_checkpoints/` | Build artefacts. |

Everything else **is** published on purpose, including `data/`, `figures/` and
`models/`. The point of the repository is that a juror can see the inputs, the
outputs and the model metrics without running anything.

The Dubai Municipality source documents in `00_BRIEF/` (brief, parks
manual, DWG, master plan) are competition materials that were distributed to all
entrants. If you would rather not republish them, add this to `.gitignore` before
pushing:

```
00_BRIEF/
```

then `git rm -r --cached 00_BRIEF` and commit.

---

## After it is live

Add the URL to the **AI Methodology Report** (submission slot 06), on the first
page:

> *The complete analysis — data, code, models and tests — is published at
> `github.com/wasimmisaw437/al-safa-2-park-ai` and runs end to end with
> `python run_analysis.py`.*

Most entries cannot offer a juror that. It costs one line.
