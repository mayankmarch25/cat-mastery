"""
Repairs the extracted PYQ bank.

Three outcomes per record:
  KEEP      - answerable as stored (possibly after a structural repair)
  REPAIRED  - para-summary records where the paragraph had been dumped into
              the `question` field; paragraph moved to `stimulus`, standard
              CAT instruction restored as the stem
  QUARANTINE- the record cannot be answered from what was extracted
              (orphaned RC question with no passage, DILR question with no
              caselet, OCR-garbled options). These are written to a separate
              file and are NOT shipped in the live bank.

Nothing is invented. A record is never "fixed" by writing content for it.
"""
import json, re, os, collections

SRC = "build/source/raw-pyq.js"
OUT_CLEAN = "data/pyq-bank.js"
OUT_QUAR = "data/pyq-quarantine.json"

PARA_SUMMARY_STEM = ("The passage given above is followed by four alternate summaries. "
                     "Choose the option that best captures the essence of the passage.")

# question refers to context that is not present in the record
NEEDS_CONTEXT = re.compile(
    r'\b(the passage|according to the passage|the author of the passage|the paragraph above|'
    r'the following table|the following graph|the following chart|the above data|the given data|'
    r'the figure above|the table below|the graph below)\b', re.I)

# generic stems that only make sense attached to a caselet
GENERIC_STEM = re.compile(
    r'^(which (one )?of the following is (true|false|correct)|what is the value|how many|'
    r'which of these|what was the|who (is|was)|in which)\b', re.I)

# OCR damage signatures in option text
def ocr_garbled(opt: str) -> bool:
    s = opt.strip()
    if not s:
        return True
    letters = sum(c.isalnum() for c in s)
    if letters == 0:
        return True
    # stray quote marks mid-token, or heavy punctuation noise
    noise = sum(1 for c in s if c in '"\\|~^`')
    if noise >= 2:
        return True
    if len(s) > 3 and noise / len(s) > 0.08:
        return True
    # tokens like 'p2 2 "Tif - r'
    if re.search(r'"\s*[A-Za-z]{2,4}\s', s):
        return True
    return False


def load(path):
    s = open(path, encoding='utf-8').read()
    s = s[s.index('['):].rstrip().rstrip(';')
    return json.loads(s)


def is_para_summary(rec):
    opts = rec.get('options') or []
    if len(opts) != 4:
        return False
    if rec.get('stimulus'):
        return False
    q = rec['question']
    if len(q) < 350:
        return False
    avg = sum(len(o) for o in opts) / len(opts)
    return avg > 70


def norm_opt(t):
    """Normalises an option for comparison: collapses whitespace and strips
    the stray ' S' / 'S' token the PDF extractor appended to some options."""
    t = re.sub(r'\s+', ' ', str(t)).strip()
    t = re.sub(r'\s+S$', '', t)
    return t.strip().lower()


def reconcile_answer(rec):
    """The source bank stores both an answer index and an answer string, and in
    many records they disagree. The string comes from the published key, so it
    wins. Returns (fixed_record, status)."""
    opts = rec.get('options') or []
    at = str(rec.get('answerText', '')).strip()
    if rec.get('type') != 'MCQ' or not opts or not at:
        return rec, 'untouched'
    idx = rec.get('answer')
    if isinstance(idx, int) and 0 <= idx < len(opts) and norm_opt(opts[idx]) == norm_opt(at):
        return rec, 'already_consistent'
    hits = [i for i, o in enumerate(opts) if norm_opt(o) == norm_opt(at)]
    if len(hits) != 1 and len(norm_opt(at)) >= 12:
        # the extractor truncated many answer strings mid-sentence, so an exact
        # match fails on records whose key is otherwise perfectly usable
        na = norm_opt(at)
        hits = [i for i, o in enumerate(opts)
                if norm_opt(o).startswith(na) or na.startswith(norm_opt(o))]
    if len(hits) == 1:
        out = dict(rec)
        out['answer'] = hits[0]
        out['answerText'] = opts[hits[0]]
        out['answerFix'] = 'index_corrected_from_key'
        return out, 'corrected'
    return rec, 'conflict'


def classify(rec):
    opts = rec.get('options') or []
    typ = rec.get('type')
    sec = rec['section']

    # structural: MCQ must carry four usable options
    if typ == 'MCQ':
        if len(opts) < 4:
            return 'QUARANTINE', 'mcq_missing_options'
        if any(ocr_garbled(o) for o in opts):
            return 'QUARANTINE', 'ocr_garbled_options'
        a = rec.get('answer')
        if not isinstance(a, int) or not (0 <= a < len(opts)):
            return 'QUARANTINE', 'invalid_answer_index'
    if typ == 'TITA' and not str(rec.get('answerText', '')).strip():
        return 'QUARANTINE', 'tita_missing_answer'

    if is_para_summary(rec):
        return 'REPAIR', 'para_summary_split'

    if not rec.get('stimulus'):
        q = rec['question']
        if sec == 'DILR':
            # a DILR question without its caselet is not answerable, and the
            # stems are almost always generic
            if len(q) < 400 or GENERIC_STEM.search(q.strip()) or NEEDS_CONTEXT.search(q):
                return 'QUARANTINE', 'dilr_caselet_missing'
        if sec == 'VARC':
            if NEEDS_CONTEXT.search(q):
                return 'QUARANTINE', 'rc_passage_missing'
            if len(q) < 160:
                return 'QUARANTINE', 'rc_passage_missing'
        if sec == 'QA' and NEEDS_CONTEXT.search(q):
            return 'QUARANTINE', 'qa_context_missing'

    return 'KEEP', 'ok'


def repair(rec):
    out = dict(rec)
    out['stimulus'] = rec['question'].strip()
    out['question'] = PARA_SUMMARY_STEM
    out['topic'] = 'Para Summary'
    out['repaired'] = 'passage_moved_to_stimulus'
    return out


def main():
    os.makedirs('data', exist_ok=True)
    recs = load(SRC)
    keep, quar = [], []
    reasons = collections.Counter()

    for r in recs:
        r, status = reconcile_answer(r)
        reasons['answer_' + status] += 1
        if status == 'conflict':
            q = dict(r)
            q['quarantineReason'] = 'answer_key_conflict'
            quar.append(q)
            continue
        verdict, why = classify(r)
        reasons[why] += 1
        if verdict == 'QUARANTINE':
            q = dict(r)
            q['quarantineReason'] = why
            quar.append(q)
        elif verdict == 'REPAIR':
            keep.append(repair(r))
        else:
            keep.append(r)

    # explanation integrity: stub explanations get an explicit, honest label
    stub = re.compile(r'^\s*Source answer key', re.I)
    for r in keep:
        exp = (r.get('explanation') or '').strip()
        if stub.match(exp) or len(exp) < 40:
            r['explanationStatus'] = 'KEY_ONLY'
            r['explanation'] = (
                f"Verified answer: {r.get('answerText') or (r.get('options') or [''])[r.get('answer', 0)]}. "
                "The source document for this paper carries the answer key but no worked solution, "
                "so no step-by-step derivation is shown here rather than one being invented."
            )
        else:
            r['explanationStatus'] = 'FULL'

    with open(OUT_CLEAN, 'w', encoding='utf-8') as f:
        f.write('window.PYQ_BANK = ' + json.dumps(keep, ensure_ascii=False) + ';\n')
    with open(OUT_QUAR, 'w', encoding='utf-8') as f:
        json.dump(quar, f, ensure_ascii=False, indent=1)

    print(f"input {len(recs)} | kept {len(keep)} | quarantined {len(quar)}")
    print("reasons:", dict(reasons))
    print("kept by section:", dict(collections.Counter(r['section'] for r in keep)))
    print("kept by year:", dict(sorted(collections.Counter(r['year'] for r in keep).items())))
    print("explanation status:", dict(collections.Counter(r['explanationStatus'] for r in keep)))


if __name__ == '__main__':
    main()
