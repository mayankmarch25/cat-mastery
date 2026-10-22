# CAT Mastery (v7)

A static CAT practice and analytics app that runs on GitHub Pages with no backend.

v6 was a repair of v5's question bank. v7 adds the book-aligned Quant Track and
a rebuilt interface. The app itself was working; the question bank was not.
v5 reported 2,000 questions, of which a large share were exact duplicates, orphaned
from their passages, or carried an answer index that disagreed with the published key.
Everything below is the state after that repair, and every number here is produced by
the build rather than typed in.

---

## Bank at a glance

| | Count |
|---|---|
| Questions shipped | 3,079 |
| Answers verified | 2,581 |
| Answers carried over, not independently verified | 498 |
| Real CAT PYQs retained | 343 |
| Original practice (computed or authored) | 2,238 |
| Removed as unanswerable or conflicting | 306 |

By section: QA 2,511 · DILR 382 · VARC 186.

Quant is tagged to the syllabus: 2,510 of 2,511 QA questions
carry a block and chapter, across all 23 chapters. By level of difficulty:
LOD I 1,049 · LOD II 1,087 · LOD III 375.

"Verified" means one of three things: the answer was computed at build time from the
numbers in the question, it came from a published answer key that matches the stored
options, or it was authored together with a full worked explanation.

The live counts are rendered in the **Bank integrity** panel on the Random Test page.
They are read from `data/integrity.js`, which the build regenerates.

---

## Quant Track

A seventh view that organises quant the way Arun Sharma's *How to Prepare for
Quantitative Aptitude for CAT* (8th edition, McGraw Hill 2018) organises it, so the
book and the app can be worked side by side.

**On copyright.** The book is copyrighted and its copyright page prohibits
reproduction. Nothing from it is reproduced here. What the app mirrors is the
syllabus organisation: seven parts (First Things First plus Blocks I to VI),
nineteen numbered chapters in the book's order, and the LOD I / II / III difficulty
convention. Every chapter carries a page reference so you read the book itself for
the theory. All teaching notes and all questions in this app are original.

Each chapter gives you:

- **What matters in this chapter.** The concepts and formulas, written as working rules.
- **Where marks are lost.** The specific errors that chapter produces under time.
- **A speed target.** What "fluent" looks like for that chapter.
- **LOD I / II / III drills** pulled from the tagged bank, 15 questions per drill.

First Things First is treated as a calculation drill rather than a three-level
ladder, because speed work has no difficulty ladder. Its four chapters hold 240
timed mental-calculation items at roughly four seconds each.

Chapter accuracy is computed from your own completed attempts and shown against each
chapter. The dashboard's syllabus strip aggregates that into block-level progress.

---

## What was fixed

**1. Duplicate padding removed.**
The v5 practice bank held 1,267 records built from 423 distinct questions. 567 were
byte-identical copies, including VARC, where 300 questions were generated off just
6 passages. All exact duplicates have been removed.

**2. Answer-key conflicts caught.**
187 extracted PYQs stored an answer index that pointed at a different option from the
one named in the answer text. In v5 the app marked the index as correct, so a student
answering correctly could be scored wrong. 119 of these were recoverable, because the
answer text was a truncated prefix of exactly one option, and the index has been
corrected from the key. The remaining 152 could not be resolved and were removed.

**3. Orphaned questions removed.**
59 VARC questions referred to a passage that did not survive extraction. 80 DILR
questions were generic stems ("Which of the following is true?") with no caselet.
These are unanswerable, so they are no longer shipped. They sit in
`data/pyq-quarantine.json` with a reason recorded against each one, so nothing was
silently discarded and the extraction can be redone later.

**4. Fabricated explanations avoided.**
501 PYQs had no worked solution in the source, only a key. Writing solutions for them
would have meant inventing derivations. Instead, 235 surviving records are labelled
`KEY_ONLY` and display an "answer key only" badge in review, stating plainly that the
source carried a key and no solution.

**5. QA and DILR rebuilt with computed answers.**
859 new QA questions were generated across 17 topics, with every answer computed from
the question's own parameters, so correctness is structural rather than a matter of
trust. Distractors come from realistic error patterns (wrong percentage base, forgetting
to subtract, swapping rate and time) rather than random numbers. 320 new DILR questions
were built as caselet sets; every arrangement puzzle is brute-force checked to have
exactly one valid solution before it ships.

**6. VARC rewritten rather than multiplied.**
14 original RC passages with 56 questions, plus 12 para-jumbles, 12 para-summaries and
10 odd-one-out items, each with an explanation and a "how to think" line. VARC now runs
on 93 distinct stimuli instead of 6.

**7. Daily practice no longer repeats.**
v5 reshuffled the pool with a date seed, so questions recurred at random. The rotation
now advances through the bank. VARC and DILR sets are kept intact rather than split
across days.

Non-repeating days available from the current bank:

| Section | Days before the rotation restarts |
|---|---|
| QA | 308 |
| DILR | 63 |
| VARC | 31 |

VARC is the binding constraint, and that is the honest position. Adding passages to
`build/varc_passages_a.py` or `_b.py` and rebuilding is the way to extend it. The
earlier claim of five years of distinct daily practice was never supportable: at 15
questions a day it needs 27,375 question-appearances, and no bank of this size
delivers that.

---

## Publication and copyright

CAT papers are the intellectual property of the IIMs. Extracting them for your own
study is one thing; republishing them on a public website is another.

`data/config.js` carries a switch:

```js
includePYQ: true   // PYQ bank loaded, Past Papers page active
includePYQ: false  // original practice only, site ships nothing extracted
```

Recommended: keep `true` if the repository is **private**, set `false` if it is
**public**. With it off, the site still has 1,767 original questions and every feature
except the Past Papers page.

---

## Rebuilding the bank

The shipped `data/*.js` files are build output. To change them:

```bash
python3 build/repair_pyq.py    # cleans the raw PYQ bank, writes the quarantine file
python3 build/assemble.py      # dedupes, generates, validates, writes data/ + integrity
```

`build/assemble.py` applies a validation gate to every record. A question is dropped if
it has fewer than four options, duplicate options, an answer index out of range, an
answer text that contradicts the indexed option, or a stem under ten characters. The
drop counts appear in `data/integrity.json`.

To add questions by hand, use the JSON importer in the app, or extend the generators:

| File | What it produces |
|---|---|
| `build/gen_qa.py` | QA, answers computed from parameters |
| `build/gen_dilr.py` | DILR caselets, puzzles verified unique |
| `build/varc_passages_a.py`, `_b.py` | RC passages and questions |
| `build/varc_verbal.py` | para-jumbles, summaries, odd-one-out |

---

## Features

Daily VARC, DILR and QA sets with a 20-minute timer and CAT scoring (+3 / −1, no
negative on TITA). Results with correct, wrong, skipped, accuracy and time. Per-question
explanation and a "how to think" line. Calendar history, streaks, section accuracy,
topic-level weakness analysis, error log, attempt history. Random test builder at 25 /
50 / 75 / 100 questions with section and source filters. Geometry learning path with 18
modules. Exam Intelligence weightage hub. JSON export and import for progress and for
new questions.

## Storage

Progress and any imported questions live in `localStorage`, so they stay on the device.
Use **Export progress** regularly. Multi-device sync, shared leaderboards and real
percentile ranks need a backend such as Supabase or Firebase, which a static GitHub
Pages site cannot provide.

## Files

```
index.html
.nojekyll
README.md
HOSTING.md
assets/   styles.css, theme.css, app.js
data/     config.js, integrity.js, quant-track.js, pyq-bank.js,
          practice-bank.js, questions.js, weightage.js,
          pyq-coverage.json, pyq-quarantine.json, integrity.json,
          question-schema.json, source-map.json, sample-import.json
build/    repair_pyq.py, assemble.py, quant_track.py, gen_qa.py,
          gen_qa_extra.py, gen_qa_lod3.py, gen_dilr.py, gen_varc.py,
          varc_passages_a.py, varc_passages_b.py, varc_verbal.py,
          source/ (the raw banks the build reads from)
```

## Design

The interface uses a slate and teal instrument palette rather than a document
palette, with IBM Plex Sans for data and Newsreader for headings. Numerals are set
in tabular figures throughout, since the subject is arithmetic and columns of
numbers should align. The dashboard leads with the syllabus strip, because the
question a student actually has each morning is how much of the course is left,
not what their streak is.
