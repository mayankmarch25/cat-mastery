# -*- coding: utf-8 -*-
"""Assembles the original VARC bank from written passages and verbal items."""
import random, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from varc_passages_a import PASSAGES_A
from varc_passages_b import PASSAGES_B
from varc_verbal import JUMBLES, SUMMARIES, ODD_ONE_OUT

R = random.Random(31415)
_n = {'i': 0}


def rec(topic, difficulty, title, stimulus, question, options, answer_idx, exp, how):
    _n['i'] += 1
    return {
        "id": f"ORIG-VARC-{_n['i']:04d}",
        "section": "VARC",
        "type": "MCQ",
        "topic": topic,
        "difficulty": difficulty,
        "sourceType": "ORIGINAL",
        "sourceLabel": "Original CAT-level practice",
        "sourceUrl": "",
        "year": None,
        "slot": None,
        "title": title,
        "stimulus": stimulus,
        "question": question,
        "options": options,
        "answer": answer_idx,
        "answerText": options[answer_idx],
        "explanation": exp,
        "howToThink": how,
        "explanationStatus": "FULL",
    }


def build_rc():
    out = []
    for p in PASSAGES_A + PASSAGES_B:
        for q in p["questions"]:
            opts = [q["correct"]] + list(q["wrong"])
            R.shuffle(opts)
            out.append(rec(p["topic"], p["difficulty"], f"RC · {p['title']}",
                           p["text"], q["q"], opts, opts.index(q["correct"]),
                           q["exp"], q["how"]))
    return out


def build_jumbles():
    out = []
    perms = ["1234", "1324", "1342", "1432", "2134", "2314", "2341", "2143",
             "3124", "3142", "3412", "4123", "4312", "2413", "1243", "3214"]
    for j in JUMBLES:
        correct = j["order"]
        pool = [p for p in perms if p != correct]
        R.shuffle(pool)
        opts = [correct] + pool[:3]
        R.shuffle(opts)
        stim = ("The four sentences below, labelled 1 to 4, have been placed in random order. "
                "Arrange them to form a coherent paragraph.\n\n" +
                "\n".join(f"{i+1}. {s}" for i, s in enumerate(j["sents"])))
        out.append(rec("Para Jumbles", "Medium", "Verbal · Para jumble", stim,
                       "What is the correct order of the sentences?",
                       opts, opts.index(correct), j["exp"],
                       "Find the opening sentence first, then look for pairs that cannot be separated, "
                       "such as a pronoun and its referent or a claim and its 'therefore'."))
    return out


def build_summaries():
    out = []
    for s in SUMMARIES:
        opts = [s["correct"]] + list(s["wrong"])
        R.shuffle(opts)
        out.append(rec("Para Summary", "Hard", "Verbal · Para summary", s["para"],
                       "Choose the option that best captures the essence of the passage.",
                       opts, opts.index(s["correct"]), s["exp"],
                       "Reject options that add a recommendation the passage never made, and reject "
                       "options that capture only one half of a two-part argument."))
    return out


def build_odd():
    out = []
    for o in ODD_ONE_OUT:
        stim = ("Five sentences are given below, labelled 1 to 4. Four of them form a coherent "
                "paragraph. Identify the sentence that does not belong.\n\n" +
                "\n".join(f"{i+1}. {s}" for i, s in enumerate(o["sents"])))
        opts = ["1", "2", "3", "4"]
        out.append(rec("Odd Sentence Out", "Medium", "Verbal · Odd one out", stim,
                       "Which sentence does not belong to the paragraph?",
                       opts, o["odd"] - 1, o["exp"],
                       "The odd sentence is usually true and topically related but plays no role in "
                       "the argument the others are building. Test each for necessity, not relevance."))
    return out


def build():
    out = build_rc() + build_jumbles() + build_summaries() + build_odd()
    for i, r in enumerate(out, 1):
        r['id'] = f"ORIG-VARC-{i:04d}"
    return out


if __name__ == '__main__':
    import json, collections
    qs = build()
    print("generated:", len(qs))
    print(dict(collections.Counter(q['topic'] for q in qs)))
    print("unique passages:", len({q['stimulus'][:80] for q in qs}))
