# -*- coding: utf-8 -*-
"""
Assembles the final shipping bank.

Order of operations:
  1. load the repaired PYQ bank (produced by repair_pyq.py)
  2. deduplicate the legacy practice bank and flag its answers as unverified
  3. add the generated QA and DILR banks (answers computed, so verified)
  4. add the written VARC bank (answers authored with explanations)
  5. validate every record structurally and drop anything that fails
  6. write data files plus an integrity report the UI reads
"""
import json, os, sys, collections, re
sys.path.insert(0, os.path.dirname(__file__))
import gen_qa, gen_dilr, gen_varc, gen_qa_extra, gen_qa_lod3, quant_track

OUT = "data"


def load_js(path):
    s = open(path, encoding='utf-8').read()
    s = s[s.index('['):].rstrip().rstrip(';')
    return json.loads(s)


# ----------------------------------------------------- quant syllabus tagging
# Topic strings vary across the three source banks, so they are normalised onto
# the chapter spine in quant_track.py before tagging.
TOPIC_ALIASES = {
    "Algebra": "Equations", "Averages": "Averages and Mixtures",
    "Mixtures": "Averages and Mixtures", "Time Speed Distance": "Time, Speed & Distance",
    "Time and Work": "Time & Work", "Exponents": "Logarithms & Indices",
    "Logarithms": "Logarithms & Indices", "Logarithm and Surds": "Logarithms & Indices",
    "Compound Interest": "Simple & Compound Interest",
    "Simple Interest": "Simple & Compound Interest", "Interest": "Simple & Compound Interest",
    "Profit and Loss": "Profit & Loss", "Profit, Loss & Discount": "Profit & Loss",
    "Ratio": "Ratio, Proportion & Variation",
    "Sequence & Series": "Progressions",
    "Permutations and Combinations": "Permutation & Combination",
    "Arithmetic / Algebra": "Equations",
}
CHAPTER_IDX = quant_track.chapter_index()
LOD_BY_DIFFICULTY = {"Easy": 1, "Medium": 2, "Hard": 3, "Actual CAT": 2}


def tag_syllabus(r):
    """Attaches block, chapter and level-of-difficulty to a QA record."""
    if r["section"] != "QA":
        r["lod"] = LOD_BY_DIFFICULTY.get(r.get("difficulty"), 2)
        return r
    topic = TOPIC_ALIASES.get(r["topic"], r["topic"])
    hit = CHAPTER_IDX.get(topic)
    if hit:
        r["block"], r["chapter"], r["chapterNo"], r["chapterName"] = hit
    r["normalTopic"] = topic
    r["lod"] = LOD_BY_DIFFICULTY.get(r.get("difficulty"), 2)
    return r


# ------------------------------------------------------------------ validate
def validate(r):
    """Returns a reason string if the record is unusable, else None."""
    for f in ("id", "section", "type", "topic", "question"):
        if not str(r.get(f, "")).strip():
            return f"missing_{f}"
    if r["section"] not in ("QA", "DILR", "VARC"):
        return "bad_section"
    if r["type"] in ("RC", "LR", "DI"):
        r["type"] = "MCQ"
    if r["type"] == "MCQ":
        opts = r.get("options") or []
        if len(opts) < 4:
            return "too_few_options"
        if len({str(o).strip().lower() for o in opts}) != len(opts):
            return "duplicate_options"
        if any(not str(o).strip() for o in opts):
            return "empty_option"
        a = r.get("answer")
        if not isinstance(a, int) or not (0 <= a < len(opts)):
            return "bad_answer_index"
        if str(r.get("answerText", "")).strip() and str(r["answerText"]).strip() != str(opts[a]).strip():
            return "answertext_mismatch"
    elif r["type"] == "TITA":
        if not str(r.get("answerText", "")).strip():
            return "tita_missing_answer"
    else:
        return "bad_type"
    if len(str(r["question"]).strip()) < 10:
        return "question_too_short"
    return None


def norm(r):
    """Fills the fields the app and the schema expect."""
    r.setdefault("stimulus", "")
    r.setdefault("sourceUrl", "")
    r.setdefault("year", None)
    r.setdefault("slot", None)
    r.setdefault("howToThink", "")
    r.setdefault("explanation", "")
    r.setdefault("explanationStatus", "FULL")
    r.setdefault("title", f"{r['section']} · {r['topic']}")
    r["verifiedAnswer"] = bool(r.get("verifiedAnswer", False))
    return r


def main():
    os.makedirs(OUT, exist_ok=True)
    report = {"droppedByValidation": collections.Counter()}

    # 1. repaired PYQ ------------------------------------------------------
    pyq = load_js(f"{OUT}/pyq-bank.js")
    for r in pyq:
        r["verifiedAnswer"] = True          # answer key comes from the source paper
        r["answerSource"] = "source answer key"

    # 2. legacy practice, deduplicated -------------------------------------
    legacy = load_js("build/source/legacy-practice.js") + load_js("build/source/legacy-starter.js")
    seen, legacy_clean = set(), []
    dupes = 0
    for r in legacy:
        key = (str(r.get("stimulus", "")).strip(),
               r["question"].strip(),
               tuple(str(o).strip() for o in (r.get("options") or [])))
        if key in seen:
            dupes += 1
            continue
        seen.add(key)
        r = dict(r)
        r["verifiedAnswer"] = False
        r["answerSource"] = "authored, not independently verified"
        r["sourceLabel"] = (r.get("sourceLabel") or "Practice") + " · answer not independently verified"
        legacy_clean.append(r)
    report["legacyInput"] = len(legacy)
    report["legacyDuplicatesRemoved"] = dupes

    # 3 + 4. generated and written ----------------------------------------
    qa = gen_qa.build() + gen_qa_extra.build() + gen_qa_lod3.build()
    dilr = gen_dilr.build(320)
    varc = gen_varc.build()
    for r in qa + dilr:
        r["verifiedAnswer"] = True
        r["answerSource"] = "computed at build time"
    for r in varc:
        r["verifiedAnswer"] = True
        r["answerSource"] = "authored with full explanation"

    # 5. validate ----------------------------------------------------------
    def clean(batch, label):
        ok = []
        for r in batch:
            r = norm(r)
            why = validate(r)
            if why:
                report["droppedByValidation"][f"{label}:{why}"] += 1
                continue
            ok.append(r)
        return ok

    pyq = [tag_syllabus(r) for r in pyq]
    legacy_clean = [tag_syllabus(r) for r in legacy_clean]
    qa = [tag_syllabus(r) for r in qa]
    dilr = [tag_syllabus(r) for r in dilr]
    varc = [tag_syllabus(r) for r in varc]

    pyq = clean(pyq, "pyq")
    legacy_clean = clean(legacy_clean, "legacy")
    original = clean(qa + dilr + varc, "original")

    # global id uniqueness
    used = set()
    for r in pyq + original + legacy_clean:
        base = r["id"]
        i = 1
        while r["id"] in used:
            i += 1
            r["id"] = f"{base}-{i}"
        used.add(r["id"])

    # cross-bank duplicate stems (PYQ first, so a real paper question wins)
    stems = set()
    pyq_dedup = []
    for r in pyq:
        k = (str(r.get("stimulus", ""))[:200].strip(), r["question"].strip())
        if k in stems:
            report["droppedByValidation"]["pyq_internal_duplicate"] += 1
            continue
        stems.add(k)
        pyq_dedup.append(r)
    pyq = pyq_dedup
    final_practice = []
    for r in original + legacy_clean:
        k = (str(r.get("stimulus", ""))[:200].strip(), r["question"].strip())
        if k in stems:
            report["droppedByValidation"]["cross_bank_duplicate"] += 1
            continue
        stems.add(k)
        final_practice.append(r)

    # 6. write -------------------------------------------------------------
    with open(f"{OUT}/pyq-bank.js", "w", encoding="utf-8") as f:
        f.write("window.PYQ_BANK = " + json.dumps(pyq, ensure_ascii=False) + ";\n")
    with open(f"{OUT}/practice-bank.js", "w", encoding="utf-8") as f:
        f.write("window.PRACTICE_BANK = " + json.dumps(final_practice, ensure_ascii=False) + ";\n")
    with open(f"{OUT}/questions.js", "w", encoding="utf-8") as f:
        f.write("window.STARTER_BANK = [];\n")

    allq = pyq + final_practice
    quar = json.load(open(f"{OUT}/pyq-quarantine.json", encoding="utf-8"))

    def by(key, batch=allq):
        return dict(collections.Counter(r[key] for r in batch))

    # quant syllabus file consumed by the Quant Track page
    qa_all = [r for r in allq if r["section"] == "QA"]
    chapter_counts = {}
    for r in qa_all:
        ch = r.get("chapter")
        if not ch:
            continue
        d = chapter_counts.setdefault(ch, {"total": 0, "1": 0, "2": 0, "3": 0})
        d["total"] += 1
        d[str(r.get("lod", 2))] += 1
    track = dict(quant_track.TRACK)
    track["counts"] = chapter_counts
    with open(f"{OUT}/quant-track.js", "w", encoding="utf-8") as f:
        f.write("window.QUANT_TRACK = " + json.dumps(track, ensure_ascii=False) + ";\n")

    integrity_extra = {
        "qaTagged": len([r for r in qa_all if r.get("chapter")]),
        "qaUntagged": len([r for r in qa_all if not r.get("chapter")]),
        "chaptersWithQuestions": len(chapter_counts),
        "chaptersTotal": len(quant_track.all_chapters()),
        "byLod": dict(collections.Counter(str(r.get("lod")) for r in qa_all)),
    }

    integrity = {
        "generatedOn": "build",
        "totals": {
            "shipped": len(allq),
            "pyq": len(pyq),
            "original": len([r for r in final_practice if r["sourceType"] == "ORIGINAL"
                             and r.get("answerSource") in ("computed at build time",
                                                           "authored with full explanation")]),
            "legacyUnverified": len([r for r in final_practice
                                     if r.get("answerSource") == "authored, not independently verified"]),
            "uniqueStems": len({r["question"].strip() for r in allq}),
            "verifiedAnswers": len([r for r in allq if r["verifiedAnswer"]]),
            "quarantined": len(quar),
        },
        "bySection": by("section"),
        "sectionUnique": {s: len({r["question"].strip() for r in allq if r["section"] == s})
                          for s in ("QA", "DILR", "VARC")},
        "pyqByYear": dict(sorted(collections.Counter(r["year"] for r in pyq).items(),
                                 key=lambda t: (t[0] is None, t[0]))),
        "quarantineReasons": dict(collections.Counter(q["quarantineReason"] for q in quar)),
        "explanationStatus": by("explanationStatus"),
        "legacyDuplicatesRemoved": dupes,
        "droppedByValidation": dict(report["droppedByValidation"]),
        "quant": integrity_extra,
        "distinctStimuli": {
            s: len({r["stimulus"][:200] for r in allq if r["section"] == s and r.get("stimulus")})
            for s in ("VARC", "DILR")
        },
    }
    with open(f"{OUT}/integrity.js", "w", encoding="utf-8") as f:
        f.write("window.BANK_INTEGRITY = " + json.dumps(integrity, ensure_ascii=False, indent=1) + ";\n")
    with open(f"{OUT}/integrity.json", "w", encoding="utf-8") as f:
        json.dump(integrity, f, ensure_ascii=False, indent=1)

    print(json.dumps(integrity, indent=1))


if __name__ == "__main__":
    main()
