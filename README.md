# CAT Mastery — GitHub Pages package

A static CAT daily-practice and analytics app designed to run on GitHub Pages.

## Included

- Daily VARC, DILR and QA sections
- 20-minute timer
- CAT-style +3 / -1 scoring
- Results page with correct / wrong / skipped / accuracy / time
- Question-by-question explanation + "How to think"
- Calendar history
- Streak, total attempts, overall accuracy
- Section accuracy
- Topic-level weakness analysis
- Error log
- Attempt history
- JSON export/import for progress backup
- JSON question-bank importer
- 2012–2025 paper-bank structure
- Source/provenance fields for each question
- 50 starter original CAT-style questions

## Important content note

The package is deliberately **not** filled with thousands of copied questions from free coaching websites. Free-to-view does not necessarily mean free-to-republish.

Recommended approach:

1. Use verified CAT PYQs where you have a legitimate source and are comfortable republishing.
2. Keep `sourceType`, `sourceLabel`, year, slot and source URL with every question.
3. Mark 2012–2016 as `RECONSTRUCTED` unless independently verified.
4. For coaching/free websites such as 2IIM or Cracku, link to the original source unless the content's reuse terms permit republication.
5. Build the large 5-year bank mainly with original CAT-standard practice questions plus verified PYQs.

## Folder structure

```text
cat-mastery/
├── index.html
├── .nojekyll
├── README.md
├── HOSTING.md
├── data/
│   ├── questions.js
│   ├── question-schema.json
│   └── sample-import.json
└── assets/
    ├── styles.css
    └── app.js
```

## Five-year readiness

The **engine** supports a five-year calendar and deterministic daily selection. To have genuinely different questions every day for five years, you need a large enough question bank.

At 15 questions/day:
- 365 × 5 × 15 = 27,375 question appearances.

Actual CAT PYQs alone cannot supply that many unique questions. Use a mix of:
- verified CAT PYQs,
- clearly-labelled reconstructed older questions,
- licensed/permitted external practice,
- original CAT-level practice.

Imported JSON questions are saved to the browser and become available immediately.

## Local testing

Because this site is plain HTML/CSS/JavaScript, you can open `index.html` directly. For the closest GitHub Pages behaviour, run any simple static file server.

## Data storage

This version stores:
- progress in `localStorage`
- imported question bank in `localStorage`

That means data stays on the browser/device. Use **Export progress** regularly.

For genuine multi-device sync, shared leaderboards, ranks and participant percentiles, connect the frontend to a backend such as Supabase or Firebase. Those are not included in this zero-backend package.


## Exam Intelligence / Topic Weightage Hub

The package now includes an **Exam Intelligence** page. It combines:
- exam → section → year filtering
- historical topic/question counts
- a relative-weight bar
- a priority list
- questions in the local bank tagged to that topic
- your own accuracy for the topic
- one-click topic drills

CAT 2020–2022 counts are preloaded from the user-provided Careers360 year-wise chapter-weightage PDF. XAT, SNAP, NMAT and CMAT are present as source-safe placeholders and intentionally remain empty until verified source data is added.

## Real PYQ test center (v4)

This package includes **683 scored PYQ records extracted from the uploaded answer-bearing CAT PDFs**.

The Past CAT Papers page now supports:
- year → slot → section selection
- full extracted section, 10-question, or 5-question attempt
- CAT MCQ and TITA scoring
- timer
- post-exam answer review
- source answer key for extracted records
- detailed source solution text where the uploaded PDF contains it (especially CAT 2022)

Coverage is intentionally shown per year. Some uploaded PDFs are index/link ebooks rather than the underlying full paper, so the UI labels those years as partial instead of inventing questions or answers. See `data/pyq-coverage.json`.


## v5 additions
- 2,000 total usable questions in the bundled bank
- Real PYQs remain separately labelled from original practice
- Random Test Builder: 25 / 50 / 75 / 100 questions
- Source filter: PYQ only / Practice only / mixed
- Section filter: VARC / DILR / QA / all
- Geometry Learning Path with 18 modules and progress tracking
- 25-question geometry practice launch

### Question-count integrity
The site does **not** relabel generated practice as PYQ. `sourceType=PYQ` is reserved for extracted CAT previous-year questions.
