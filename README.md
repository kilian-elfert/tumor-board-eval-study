# Tumor Board Evaluation

A Flask web application for a clinical study evaluating LLM-generated tumor board case summaries and problem statements. Medical experts rate AI- vs. human-written texts on completeness, correctness, and clinical relevance across multiple melanoma cases.

---

## Overview

After login, evaluators run through a fixed sequence:

1. **Consent** form, **demographic** questionnaire, and a **study procedure** page.
2. A **case dashboard** ("Patientenakte") landing page lists all cases with progress per evaluator.

For each case the evaluator then steps through:

0. **Patient dashboard** — interactive anatomical body map, basic data, staging,
   molecular pathology, lab values, imaging diagnostics, therapies, and a
   clinical timeline. Per-modality imaging reports are linked from here.
1. **Information relevance.** Rate the clinical relevance of a fixed set of
   information items (`INFO_ITEMS` in `app.py`).
2. **Case summary (Zusammenfassung).** Evaluate the human-written and the
   LLM-generated version side by side across information content, false
   information, correctness, completeness, conciseness, post-editing effort,
   origin guess, and overall preference.
3. **Problem statement (Fragestellung).** Evaluate both versions on focus,
   guideline conformity, specificity, post-editing effort, origin guess,
   and preference.
4. **Final per-case questions** — case complexity rating and an optional
   free-text comment.

Which version appears as "A" or "B" is randomised per participant and
independently for the Zusammenfassung and the Fragestellung block, to prevent
order bias. Progress is persisted after every step in
`responses/responses_<username>.json`, so an interrupted session can be
resumed at the exact same step.

### Demo pages

Every rating step has its own demo, plus two for the patient dashboard: the
relevance rating (`case_relevance`) and a tour of the record itself
(`case_record`: tabs, body map, original imaging reports and texts). Each demo
stands alone for its page — there is no overview and no previous/next
navigation between demos. It
opens as click-through slides (Weiter/Zurück, dots, arrow keys, Esc) in a modal
dialog on top of the current page (`/demo/<step_key>/folien`,
`templates/demo_slides.html`, loaded in an iframe; modal markup and script in
`templates/demo/_slides_modal.html`). Each slide shows one chapter next to a
mock-up of the rating UI — built from the real widget classes and a fictional
melanoma case — alternating between *Bedienung* (how to use the UI) and
*Hintergrund* (why the rating is collected this way); a final slide summarises
the takeaways. The entry point is the task card at the top of each rating step:
the one-line task (`alert` in `RATING_STEPS`) next to the **▶ Demo ansehen**
button, the **Demo ansehen** cards in the relevance intro dialog and sidebar,
and **▶ Demo: Patientenakte** next to the record tabs (all openers share one
modal; `data-slides-src` selects another demo).
The play button / cards are highlighted until the user has opened that demo
(tracked per user in `localStorage`). The demo URL carries the current page as
`?back=<path>` (same-site paths only), used when the slides are opened outside
the modal. They target desktop/laptop screens only.
Content lives in `demo_content.py`; each page's chapter *i* drives scene *i* of
`templates/demo/stage_<stage>.html` (scene attributes are documented in
`templates/demo/_macros.html`). The two patient-record demos share the page
mock-up `templates/demo/_dash_page.html`.

---

## Project Structure

```
app.py                     Main Flask application (routes, logic, data loading)
demo_content.py            Texts for the per-step demos (/demo/<step_key>/folien)
setup_users.py             Create user accounts — interactive prompts or
                           batch from a comma-separated file
                           (roles: evaluator / annotator / admin)
pyproject.toml              Project metadata and dependencies (source of truth)
requirements.txt           Minimal pip fallback (prefer uv + pyproject.toml)
users.json                 Hashed credentials for all evaluator accounts
.env                       Local environment variables — not committed
                           (SECRET_KEY, NTFY_URL, DATA_ROOT)

texts_human/
  zusammenfassung/         Human-written case summaries (one .txt per case_id)
  fragestellung/           Human-written problem formulations

texts_llm/
  zusammenfassung/         LLM-generated case summaries
  fragestellung/           LLM-generated problem formulations

dashboard_data/            Structured patient dashboards: <case_id>_dashboard.json.
                           Rendered as the "Patientenakte" before each
                           evaluation.

annotations/               Per-case researcher annotations: <case_id>.json
                           (status of each info item per text version:
                           enthalten / nicht_enthalten / falsch, plus the
                           corresponding text spans). Drives the false-info
                           highlighting and the missing/false/irrelevant
                           item lists shown on the Korrektheit,
                           Vollständigkeit, Prägnanz, and
                           Falschinformationen rating steps.

guideline/                 S3-Leitlinie PDF shown during the guideline-conformity step

responses/                 Per-evaluator response files: responses_<username>.json

exports/                   Auto-generated per-user exports (written on submission of
                           the final questions):
                             ratings_<user>.csv          Per-rating long-format CSV
                             ratings_<user>.json         Per-rating JSON records
                             integrity_items_<user>.csv  Per-info-item integrity /
                                                         false-info / missing-info
                             responses_raw_<user>.json   Verbatim copy of
                                                         responses_<user>.json

templates/                 Jinja2 HTML templates
  base.html                Base layout (navigation, stepper)
  _body_map.html           Reusable body map component (anatomical overview)
  case_dashboard.html      Patient dashboard shown before evaluation steps
  login.html               Login page
  consent.html             Informed consent
  demographics.html        Demographic questionnaire
  study_info.html          Study procedure overview
  intro.html               Welcome / start page
  dashboard.html           Per-user case-progress overview
  evaluate.html            Main rating step template
  demo_slides.html         Demo slides per step (shown in a modal via demo/_slides_modal.html)
  demo/                    Demo stage partials (stage_*.html) and shared _macros.html
  final_questions.html     Final per-case questions
  complete.html            Case completion confirmation
  end.html                 Study completion page
  error.html               Error display

static/
  style.css                Application stylesheet
  dashboard.css            Dashboard-specific styles (body map, charts, timeline)
  demo_tour.css            Styles for the demo slides
  demo_tour.js             Demo engine (scenes, cursor, slide navigation)
  body_map_echelon.png             Male body map image
  body_map_echelon_female.png      Female body map image
  body_map.jpg, certificate.jpg, signature.png,
  pdf-icon.png, wispermed.{png,svg}, Wispermed_Logo_de.png   UI assets
```

### External data root

Large case-source artefacts live outside the repo, under
`$DATA_ROOT/$SOURCES_SUBDIR/` (by default `…/Data/sources/`). Files are named by
`case_id`, a 64-char SHA-256 stem of the source protocol:

```
<case_id>.pdf                       Original protocol PDF (not served by app.py)
<case_id>.txt                       Plain-text dump of the protocol
<case_id>_lab.txt                   Lab values (chronological)
<case_id>_verlaufsdoku.jsonl        Clinical course timeline (one JSON per line)
<case_id>_<modality>/...            Imaging reports (PDF + .txt) per modality,
                                    e.g. <case_id>_ct/, <case_id>_pet_ct/
```

`app.py` serves protocols and imaging directly from this directory. If
`DATA_ROOT` is unset, it falls back to in-repo `original_documents/` and
`imaging/` folders (legacy, not present in the current checkout).

---

## Setup

**Requirements:** Python ≥ 3.14, [uv](https://docs.astral.sh/uv/)

```bash
# Install dependencies
uv sync

# Create accounts — interactive prompts
uv run setup_users.py

# ...or batch from a comma-separated file (one "username, role, password" per line)
uv run setup_users.py accounts.txt
```

`setup_users.py` creates user accounts and writes hashed credentials to
`users.json`. Run it **without arguments** to be prompted for each username,
password, and role, or pass a **comma-separated file** with one
`username, role, password` per line (empty role → `evaluator`; blank lines and
lines starting with `#` are ignored).

> ⚠️ A batch file holds **plaintext passwords** — it is excluded via
> `.gitignore` (`accounts.txt`); keep it out of git and delete it after use.

| Role | Access |
|------|--------|
| `evaluator` (default) | Study rating flow |
| `annotator` | Annotation interface for marking spans as `enthalten` / `falsch` / `nicht_enthalten` |
| `admin` | Admin dashboard + export access |

---

## Running the App

```bash
uv run app.py
```

The app starts on `http://localhost:5001` (debug mode is on by default; disable
before exposing the app publicly).

### Environment variables

Loaded from `.env` (via `python-dotenv`) or the process environment:

| Variable | Purpose |
|----------|---------|
| `SECRET_KEY` | Flask session signing key. **Set this in production** — the built-in fallback is insecure. |
| `NTFY_URL`   | Optional [ntfy.sh](https://ntfy.sh) topic URL for push notifications when an evaluator starts a case. No-op if unset. |
| `DATA_ROOT`, `SOURCES_SUBDIR`, `OUTPUTS_SUBDIR`, `CSV_FILENAME` | External data paths. `app.py` serves protocols and imaging reports (`<case_id>_<modality>/`) from `$DATA_ROOT/$SOURCES_SUBDIR/`. |

```bash
SECRET_KEY=your-secret-key uv run app.py
```

---

## Data Flow

1. **Case discovery.** At startup `app.py` scans `texts_human/`, `texts_llm/`,
   `dashboard_data/`, and the configured sources directory and assembles the
   union of `case_id` stems (64-char SHA-256 hashes) found there.
2. **Texts.** Human and LLM versions of the case summary and problem statement
   are read from `texts_human/<kind>/<case_id>.txt` and
   `texts_llm/<kind>/<case_id>.txt`.
3. **Patient dashboards.** `dashboard_data/<case_id>_dashboard.json` is loaded
   per case and rendered as the "Patientenakte" (basic data, body map with
   metastases, therapies, lab values, imaging, comorbidities, staging,
   molecular pathology). Lab values, imaging entries, metastases and therapies
   are sorted chronologically at load time.
4. **Annotations.** `annotations/<case_id>.json` holds the researcher
   verdict for each information item per text version (`enthalten`,
   `nicht_enthalten`, `falsch`) plus the matching text spans. These drive
   the inline `falsch` highlighting on the Falschinformationen and
   Korrektheit steps and the displayed item lists on the Korrektheit,
   Vollständigkeit, and Prägnanz steps. Without this file those steps
   show no highlights/lists but still function.
4. **Imaging reports.** PDF and free-text reports are served on demand from
   `<case_id>_<modality>/` under the sources directory via `/api/imaging-pdf`
   and `/api/imaging-txt`.
5. **Guideline.** The S3-Leitlinie PDF in `guideline/` is served to evaluators
   during the guideline-conformity step.
6. **Responses.** Per-user state is persisted to
   `responses/responses_<username>.json` after every step.
7. **Exports.** When the final questions are submitted, four files are
   written to `exports/` for the calling user. Admins can download the
   complete study data at any time via `/export` (link "Export (ZIP)" in the
   navigation bar): a ZIP with `ratings.csv`, `integrity_items.csv`,
   `ratings.json` and `responses_raw/<user>.json` for all participants.
   The route is admin-only: the data covers all participants and reveals
   the human/LLM assignment of versions A/B.
8. **Notifications.** If `NTFY_URL` is set, a push notification is sent the
   first time an evaluator opens a case dashboard.

---

## Dependencies

Declared in `pyproject.toml` (use `uv sync`):

| Package | Purpose |
|---------|---------|
| `flask >= 3.0` | Web framework |
| `werkzeug >= 3.0` | Password hashing, request utilities |
| `python-dotenv >= 1.0` | Loads `.env` at startup |

`requirements.txt` is a minimal pip fallback and may lag behind
`pyproject.toml`; prefer `uv sync`.


---

## Sharing the project with a collaborator

Code lives in git; **patient data and credentials must never enter git**.
Already excluded by `.gitignore`: `.env`, `responses/`, `dashboard_data/`,
`texts_human/`, `texts_llm/`, `original_documents/`, `highlight_mappings.json`,
`annotations/`, `users.json`, `assignments.json`, `accounts.txt`, `exports/`.

### What goes via git

The full repo (code, templates, static assets, `pyproject.toml`,
`requirements.txt`, this README, the public S3 guideline text, and
`.env.example`).

Before pushing:

1. Rotate any secrets that ever sat in `.env` and remove them from history if
   needed (`git log --all -- .env` / `git filter-repo`).
2. Confirm no patient files were ever committed:
   ```powershell
   git log --all --full-history -- dashboard_data texts_human texts_llm responses users.json highlight_mappings.json annotations
   ```


### Internal file sharing

Two bundles need to be transferred separately:

**Bundle A — app data (belongs *inside* the cloned repo)**

These folders/files live next to `app.py` and are read directly by the Flask
app. After cloning the repo, place each item at the path on the right (paths
are relative to the repo root):

| In the file-share bundle  | Place at (relative to repo root) | Required? |
|---------------------------|----------------------------------|-----------|
| `dashboard_data/`         | `./dashboard_data/`              | yes       |
| `texts_human/`            | `./texts_human/`                 | yes       |
| `texts_llm/`              | `./texts_llm/`                   | yes       |
| `annotations/`            | `./annotations/`                 | optional (drives `falsch` highlights and the item lists on Korrektheit / Vollständigkeit / Prägnanz / Falschinformationen; without it those steps show no highlights or lists) |
| `highlight_mappings.json` | `./highlight_mappings.json`      | optional (without it the Falschinformationen step falls back to bold headers) |

After unpacking, the repo root should look like:

```
tumor_board_eval/
├── app.py
├── dashboard_data/                 ← from file-share
│   ├── 1119efbd…_dashboard.json
│   └── …
├── texts_human/
│   ├── fragestellung/              ← from file-share
│   └── zusammenfassung/            ← from file-share
├── texts_llm/
│   ├── fragestellung/              ← from file-share
│   └── zusammenfassung/            ← from file-share
├── annotations/                    ← optional, from file-share
│   ├── 1119efbd….json
│   └── …
└── highlight_mappings.json         ← optional, from file-share
```

**Bundle B — raw source data / CSV (lives *outside* the repo)**

This is the larger sensitive dataset. Pick any local folder (e.g.
`C:\Users\<yourfolder>\Data`) and unpack the bundle so the layout is:

```
<DATA_ROOT>/
├── sampled_cases.csv
└── sources/
    ├── <case_id_1>/
    │   ├── *.pdf
    │   └── …
    └── <case_id_2>/
        └── …
```

Then set `DATA_ROOT` in `.env` to the **absolute path** of `<DATA_ROOT>` —
that is the parent of `sources/`, *not* `sources/` itself. Keep the defaults
`SOURCES_SUBDIR=sources` and `CSV_FILENAME=sampled_cases.csv` unless the
bundle uses different names.

### Setup steps for the collaborator

```powershell
git clone <repo-url>
cd tumor_board_eval
uv sync

# 1. Configure environment
Copy-Item .env.example .env
#   - set SECRET_KEY (e.g. python -c "import secrets; print(secrets.token_urlsafe(48))")
#   - set DATA_ROOT to the absolute path of the folder that contains
#     sources/ and sampled_cases.csv (Bundle B)

# 2. Unpack Bundle A into the repo root so dashboard_data/, texts_human/,
#    texts_llm/, annotations/ (and optional highlight_mappings.json) sit
#    next to app.py.

# 3. Unpack Bundle B at <DATA_ROOT> so <DATA_ROOT>\sources\ and
#    <DATA_ROOT>\sampled_cases.csv exist.

# 4. Create local evaluator account(s) — interactive, or batch from a file
#    (uv run setup_users.py accounts.txt)
uv run setup_users.py

# 5. Run
uv run app.py  
```
