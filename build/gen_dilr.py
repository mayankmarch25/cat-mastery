"""
Generates original DILR sets.

Each set is a caselet plus 4 questions that share one stimulus, matching the
way the app groups questions. Data interpretation answers are computed from
the generated table. Arrangement puzzles are brute-force verified to have
exactly one valid solution before the set is emitted, so no puzzle ships
under-determined.
"""
import random, itertools
from fractions import Fraction

R = random.Random(777111)
_seq = {'n': 0}

PRODUCTS = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]
REGIONS = ["North", "South", "East", "West"]
NAMES = ["Arun", "Bela", "Chitra", "Dev", "Esha", "Farid", "Gita", "Hari",
         "Ira", "Jatin", "Kiran", "Lata", "Manoj", "Nisha", "Omar", "Priya"]
CITIES = ["Pune", "Kochi", "Indore", "Surat", "Nagpur", "Jaipur", "Bhopal"]


def mk(topic, difficulty, stimulus, question, correct, wrongs, explanation, how, title):
    c = str(correct)
    seen = {c}
    opts = []
    for w in wrongs:
        s = str(w)
        if s in seen:
            continue
        seen.add(s)
        opts.append(s)
    if len(opts) < 3:
        return None
    opts = opts[:3] + [c]
    R.shuffle(opts)
    _seq['n'] += 1
    return {
        "id": f"ORIG-DILR-{_seq['n']:04d}",
        "section": "DILR",
        "type": "MCQ",
        "topic": topic,
        "difficulty": difficulty,
        "sourceType": "ORIGINAL",
        "sourceLabel": "Original CAT-level practice (computed answer)",
        "sourceUrl": "",
        "year": None,
        "slot": None,
        "title": title,
        "stimulus": stimulus,
        "question": question,
        "options": opts,
        "answer": opts.index(c),
        "answerText": c,
        "explanation": explanation,
        "howToThink": how,
        "explanationStatus": "FULL",
    }


def table_text(headers, rows):
    out = [" | ".join(headers)]
    for r in rows:
        out.append(" | ".join(str(x) for x in r))
    return "\n".join(out)


# ---------------------------------------------------------------- table DI
def set_sales_table(idx):
    years = [2021, 2022, 2023, 2024]
    prods = R.sample(PRODUCTS, 4)
    data = {p: [R.randrange(40, 320, 5) for _ in years] for p in prods}
    headers = ["Product"] + [str(y) for y in years]
    rows = [[p] + data[p] for p in prods]
    stim = (f"The table below shows the revenue (in Rs crore) of four products of a company "
            f"over four years.\n\n{table_text(headers, rows)}")
    title = f"DI · Revenue table {idx}"
    qs = []

    # Q1 total for a year
    yi = R.randrange(4)
    tot = sum(data[p][yi] for p in prods)
    qs.append(mk("Table based DI", "Easy", stim,
                 f"What is the total revenue of all four products in {years[yi]} (Rs crore)?",
                 tot, [tot + R.randrange(10, 60), tot - R.randrange(10, 60), round(tot / 4)],
                 f"Adding the {years[yi]} column: " + " + ".join(str(data[p][yi]) for p in prods) + f" = {tot}.",
                 "Column totals first. Most DI sets reuse the same totals across questions.", title))

    # Q2 percentage growth for a product
    p = R.choice(prods)
    a, b = data[p][0], data[p][-1]
    growth = round((b - a) * 100 / a, 1)
    qs.append(mk("Table based DI", "Medium", stim,
                 f"The percentage change in the revenue of {p} from {years[0]} to {years[-1]} is closest to:",
                 f"{growth}%", [f"{round((b-a)*100/b,1)}%", f"{b-a}%", f"{round(b*100/a,1)}%"],
                 f"Change = {b} − {a} = {b-a}. As a percentage of the {years[0]} value, "
                 f"({b-a})/{a} × 100 = {growth}%.",
                 "The base year is the denominator. Reading it off the wrong year is the standard trap.", title))

    # Q3 highest contributor in a year
    yj = R.randrange(4)
    best = max(prods, key=lambda x: data[x][yj])
    share = round(data[best][yj] * 100 / sum(data[x][yj] for x in prods), 1)
    qs.append(mk("Table based DI", "Medium", stim,
                 f"In {years[yj]}, which product had the highest share of total revenue, and what was that share?",
                 f"{best}, {share}%",
                 [f"{best}, {round(share+4.5,1)}%",
                  f"{R.choice([x for x in prods if x != best])}, {share}%",
                  f"{best}, {round(share-6.2,1)}%"],
                 f"{best} recorded {data[best][yj]} out of {sum(data[x][yj] for x in prods)} in {years[yj]}, "
                 f"which is {share}%.",
                 "Identify the maximum by inspection, then compute only that one share.", title))

    # Q4 ratio
    p1, p2 = R.sample(prods, 2)
    yk = R.randrange(4)
    fr = Fraction(data[p1][yk], data[p2][yk])
    qs.append(mk("Table based DI", "Medium", stim,
                 f"In {years[yk]}, the ratio of the revenue of {p1} to that of {p2} is:",
                 f"{fr.numerator} : {fr.denominator}",
                 [f"{fr.denominator} : {fr.numerator}",
                  f"{data[p1][yk]} : {data[p2][yk] + 5}",
                  f"{fr.numerator + 1} : {fr.denominator}"],
                 f"Ratio = {data[p1][yk]} : {data[p2][yk]}, which reduces to "
                 f"{fr.numerator} : {fr.denominator}.",
                 "Always reduce before matching against options.", title))
    return [q for q in qs if q]


# ------------------------------------------------------------- caselet DI
def set_caselet(idx):
    total = R.randrange(400, 1201, 20)
    pa = R.choice([30, 35, 40, 45])
    pb = R.choice([25, 30, 20])
    a = total * pa // 100
    b = total * pb // 100
    c = total - a - b
    fa = R.choice([40, 50, 60])
    female_a = a * fa // 100
    stim = (f"A training centre enrolled {total} candidates across three programmes: Analytics, "
            f"Operations and Finance. {pa}% joined Analytics and {pb}% joined Operations, with the "
            f"rest joining Finance. Among the Analytics candidates, {fa}% were women. "
            f"Overall, {R.choice([45, 50, 55])}% of all candidates cleared the final assessment.")
    title = f"DI · Enrolment caselet {idx}"
    qs = []
    qs.append(mk("Reasoning based DI", "Easy", stim,
                 "How many candidates joined the Finance programme?",
                 c, [a, b, total - a], 
                 f"Finance = {total} − {a} − {b} = {c}.",
                 "Convert every percentage to a head count once, at the start.", title))
    qs.append(mk("Reasoning based DI", "Medium", stim,
                 "How many women joined the Analytics programme?",
                 female_a, [a - female_a, total * fa // 100, female_a * 2],
                 f"Analytics had {a} candidates, of whom {fa}% were women: {female_a}.",
                 "Percentages inside a subgroup apply to the subgroup, never to the grand total.", title))
    ratio = Fraction(a, c)
    qs.append(mk("Reasoning based DI", "Medium", stim,
                 "The ratio of Analytics candidates to Finance candidates is:",
                 f"{ratio.numerator} : {ratio.denominator}",
                 [f"{ratio.denominator} : {ratio.numerator}", f"{pa} : {pb}", f"{a} : {b}"],
                 f"Ratio = {a} : {c} = {ratio.numerator} : {ratio.denominator}.",
                 "Reduce using the HCF before comparing with options.", title))
    diff = a - b
    qs.append(mk("Reasoning based DI", "Easy", stim,
                 "By how many candidates does Analytics enrolment exceed Operations enrolment?",
                 diff, [b - c, abs(c - b), diff + 10],
                 f"{a} − {b} = {diff}.",
                 "Simple differences are free marks in a DI set. Take them first.", title))
    return [q for q in qs if q]


# ---------------------------------------------------- linear arrangement
def set_linear(idx):
    for _ in range(80):
        people = R.sample(NAMES, 5)
        perm = people[:]
        R.shuffle(perm)
        clues, texts = [], []

        i, j = R.sample(range(5), 2)
        if abs(i - j) != 1:
            continue
        left, right = (perm[i], perm[j]) if i < j else (perm[j], perm[i])
        clues.append(lambda p, l=left, r=right: p.index(l) + 1 == p.index(r))
        texts.append(f"{left} sits immediately to the left of {right}.")

        endp = perm[R.choice([0, 4])]
        clues.append(lambda p, e=endp: p.index(e) in (0, 4))
        texts.append(f"{endp} sits at one of the two ends.")

        mid = perm[2]
        clues.append(lambda p, m=mid: p.index(m) == 2)
        texts.append(f"{mid} sits exactly in the middle.")

        x, y = R.sample(people, 2)
        gap = abs(perm.index(x) - perm.index(y))
        clues.append(lambda p, a=x, b=y, g=gap: abs(p.index(a) - p.index(b)) == g)
        texts.append(f"There are exactly {gap - 1} people seated between {x} and {y}.")

        sols = [list(p) for p in itertools.permutations(people) if all(c(list(p)) for c in clues)]
        if len(sols) != 1:
            continue
        sol = sols[0]
        stim = ("Five friends " + ", ".join(sorted(people)) +
                " sit in a row of five chairs facing north, numbered 1 to 5 from the left.\n" +
                "\n".join("• " + t for t in texts))
        title = f"Arrangement set {idx}"
        pos = R.randrange(5)
        qs = []
        qs.append(mk("Arrangement & Puzzles", "Medium", stim,
                     f"Who sits in seat number {pos + 1}?",
                     sol[pos], [p for p in people if p != sol[pos]][:3],
                     f"The only arrangement satisfying all four conditions is "
                     f"{' – '.join(sol)}, so seat {pos+1} is {sol[pos]}.",
                     "Start from the most restrictive clue, usually the fixed middle or end position.", title))
        who = sol[R.randrange(5)]
        wi = sol.index(who)
        nb = sorted([sol[k] for k in (wi - 1, wi + 1) if 0 <= k <= 4])
        qs.append(mk("Arrangement & Puzzles", "Medium", stim,
                     f"Who is seated adjacent to {who}?",
                     " and ".join(nb) if len(nb) > 1 else nb[0],
                     [" and ".join(sorted(R.sample([p for p in people if p != who], 2))) for _ in range(3)],
                     f"In the unique arrangement {' – '.join(sol)}, {who} is next to "
                     f"{' and '.join(nb)}.",
                     "Fix the full line once, then read every subsequent question off it.", title))
        qs.append(mk("Arrangement & Puzzles", "Easy", stim,
                     "Who occupies seat number 1?",
                     sol[0], [p for p in people if p != sol[0]][:3],
                     f"The unique arrangement is {' – '.join(sol)}.",
                     "End positions are usually pinned first. Work inward from them.", title))
        far = sol[4]
        qs.append(mk("Arrangement & Puzzles", "Medium", stim,
                     f"How many people sit between {sol[0]} and {far}?",
                     3, [2, 4, 1],
                     f"They occupy the two ends of the row, so three people sit between them.",
                     "Count gaps, not seats. Between positions 1 and 5 there are exactly three people.", title))
        return [q for q in qs if q]
    return []


# ------------------------------------------------------- tournament table
def set_tournament(idx):
    teams = R.sample(CITIES, 4)
    results = {}
    pts = {t: 0 for t in teams}
    gf = {t: 0 for t in teams}
    for a, b in itertools.combinations(teams, 2):
        x, y = R.randrange(0, 4), R.randrange(0, 4)
        results[(a, b)] = (x, y)
        gf[a] += x
        gf[b] += y
        if x > y:
            pts[a] += 3
        elif y > x:
            pts[b] += 3
        else:
            pts[a] += 1
            pts[b] += 1
    lines = [f"{a} {x} - {y} {b}" for (a, b), (x, y) in results.items()]
    stim = ("Four teams played a single round-robin tournament, so every team played every other "
            "team exactly once. A win is worth 3 points, a draw 1 point and a loss 0 points. "
            "The results were:\n" + "\n".join("• " + l for l in lines))
    title = f"Tournament set {idx}"
    top = max(teams, key=lambda t: (pts[t], gf[t]))
    qs = []
    qs.append(mk("Reasoning based DI", "Medium", stim,
                 f"How many points did {teams[0]} finish with?",
                 pts[teams[0]], [pts[teams[0]] + 1, pts[teams[0]] + 3,
                                 max(0, pts[teams[0]] - 2)],
                 f"{teams[0]} ended on {pts[teams[0]]} points from its three matches.",
                 "Build the points table once before reading any question.", title))
    qs.append(mk("Reasoning based DI", "Medium", stim,
                 "Which team topped the table on points (goal difference breaking any tie)?",
                 top, [t for t in teams if t != top][:3],
                 f"Points were " + ", ".join(f"{t}: {pts[t]}" for t in teams) + f", so {top} finished on top.",
                 "Tabulate, then sort. Do not try to track the leader while reading the results.", title))
    tg = sum(gf.values())
    qs.append(mk("Reasoning based DI", "Easy", stim,
                 "What was the total number of goals scored in the tournament?",
                 tg, [tg + 2, tg - 3, tg * 2],
                 f"Adding all six scorelines gives {tg} goals.",
                 "Six matches in a four-team round robin. Confirm the match count before adding.", title))
    draws = sum(1 for (x, y) in results.values() if x == y)
    qs.append(mk("Reasoning based DI", "Easy", stim,
                 "How many matches ended in a draw?",
                 draws, [draws + 1, draws + 2, max(0, draws - 1)],
                 f"{draws} of the six matches finished level.",
                 "Scan the scorelines for equal pairs. This is a one-pass question.", title))
    return [q for q in qs if q]


# ------------------------------------------------------------- venn / survey
def set_venn(idx):
    only_a, only_b, only_c = R.randrange(20, 61), R.randrange(15, 51), R.randrange(10, 41)
    ab, bc, ca, abc = R.randrange(5, 21), R.randrange(4, 18), R.randrange(3, 16), R.randrange(2, 12)
    none = R.randrange(0, 26)
    total = only_a + only_b + only_c + ab + bc + ca + abc + none
    stim = (f"A survey of {total} commuters recorded the modes of transport used in a week. "
            f"{only_a} used only the metro, {only_b} only the bus and {only_c} only an auto. "
            f"{ab} used exactly the metro and the bus, {bc} exactly the bus and an auto, and "
            f"{ca} exactly an auto and the metro. {abc} used all three, and {none} used none of them.")
    title = f"Venn survey set {idx}"
    metro = only_a + ab + ca + abc
    qs = []
    qs.append(mk("Venn Diagrams", "Medium", stim,
                 "How many commuters used the metro at any point during the week?",
                 metro, [only_a, metro - abc, metro + none],
                 f"Metro users = {only_a} + {ab} + {ca} + {abc} = {metro}.",
                 "'At any point' means the full circle, so add every region that touches it.", title))
    exactly_two = ab + bc + ca
    qs.append(mk("Venn Diagrams", "Medium", stim,
                 "How many commuters used exactly two of the three modes?",
                 exactly_two, [exactly_two + abc, ab + bc + ca + abc, abc],
                 f"Exactly two = {ab} + {bc} + {ca} = {exactly_two}. The {abc} who used all three are excluded.",
                 "'Exactly two' excludes the triple overlap. 'At least two' includes it.", title))
    atleast_one = total - none
    qs.append(mk("Venn Diagrams", "Easy", stim,
                 "How many commuters used at least one of the three modes?",
                 atleast_one, [total, atleast_one - abc, none],
                 f"{total} − {none} = {atleast_one}.",
                 "Subtract the 'none' group from the total. That is usually the first line of working.", title))
    qs.append(mk("Venn Diagrams", "Medium", stim,
                 "How many commuters used the bus but not the metro?",
                 only_b + bc, [only_b, only_b + ab, only_b + bc + abc],
                 f"Bus but not metro = only bus ({only_b}) + bus and auto only ({bc}) = {only_b + bc}.",
                 "Shade the target region on the diagram first, then add only the regions inside it.", title))
    return [q for q in qs if q]


BUILDERS = [set_sales_table, set_caselet, set_linear, set_tournament, set_venn]


def build(target=300):
    out, seen = [], set()
    idx = 0
    while len(out) < target and idx < 400:
        idx += 1
        fn = BUILDERS[idx % len(BUILDERS)]
        for rec in fn(idx):
            key = (rec['stimulus'][:120], rec['question'])
            if key in seen:
                continue
            seen.add(key)
            out.append(rec)
    out = out[:target]
    for i, r in enumerate(out, 1):
        r['id'] = f"ORIG-DILR-{i:04d}"
    return out


if __name__ == '__main__':
    import json, collections
    qs = build()
    print("generated:", len(qs), "| unique sets:", len({q['stimulus'][:120] for q in qs}))
    print(dict(collections.Counter(q['topic'] for q in qs)))
