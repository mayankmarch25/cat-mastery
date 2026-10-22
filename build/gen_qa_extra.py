# -*- coding: utf-8 -*-
"""
Generators for the chapters the earlier bank did not cover: Block V in full
(functions, inequalities, logarithms, quadratics), base systems, alligations,
coordinate geometry, and the First Things First calculation drills.

As in gen_qa.py, every answer is computed rather than authored.
"""
import random, math
from fractions import Fraction

R = random.Random(90210)
_seq = {'n': 0}


def fmt(x):
    if isinstance(x, Fraction):
        return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
    if isinstance(x, float):
        return str(int(round(x))) if abs(x - round(x)) < 1e-9 else f"{x:.2f}".rstrip('0').rstrip('.')
    return str(x)


def mk(topic, difficulty, question, correct, wrongs, explanation, how, stimulus=""):
    c = fmt(correct)
    seen, opts = {c}, []
    for w in wrongs:
        s = fmt(w)
        if s in seen:
            continue
        seen.add(s)
        opts.append(s)
    if len(opts) < 3:
        return None
    opts = opts[:3] + [c]
    R.shuffle(opts)
    _seq['n'] += 1
    return {"id": f"ORIG-QX-{_seq['n']:04d}", "section": "QA", "type": "MCQ", "topic": topic,
            "difficulty": difficulty, "sourceType": "ORIGINAL",
            "sourceLabel": "Original CAT-level practice (computed answer)", "sourceUrl": "",
            "year": None, "slot": None, "title": f"QA · {topic}", "stimulus": stimulus,
            "question": question, "options": opts, "answer": opts.index(c), "answerText": c,
            "explanation": explanation, "howToThink": how, "explanationStatus": "FULL"}


# ------------------------------------------------------------------ functions
def gen_functions(n):
    out = []
    for _ in range(n * 4):
        mode = R.choice(['compose', 'domain', 'parity', 'iterate', 'inverse'])
        if mode == 'compose':
            a, b = R.choice(range(2, 10)), R.choice([x for x in range(-9, 10) if x])
            c, d = R.choice(range(2, 8)), R.choice([x for x in range(-7, 8) if x])
            x = R.choice([v for v in range(-6, 8) if v])
            fg = a * (c * x + d) + b
            gf = c * (a * x + b) + d
            if fg == gf:
                continue
            sg = lambda v: f"+ {v}" if v >= 0 else f"- {abs(v)}"
            q = (f"If f(x) = {a}x {sg(b)} and g(x) = {c}x {sg(d)}, then f(g({x})) equals:")
            e = (f"g({x}) = {c}×{x} {sg(d)} = {c*x+d}. Then f({c*x+d}) = {a}×{c*x+d} {sg(b)} = {fg}.")
            h = "Work the inner function first. f(g(x)) and g(f(x)) are different, so read the order."
            out.append(mk("Functions", "Easy", q, fg, [gf, a * x + b, c * x + d], e, h))
        elif mode == 'domain':
            k = R.choice(range(2, 20))
            q = f"The domain of f(x) = 1/(x − {k}) is:"
            e = f"The denominator vanishes at x = {k}, so every real number except {k} is admissible."
            h = "Domain questions are denominator and square-root questions. Find what breaks, exclude it."
            out.append(mk("Functions", "Easy", q, f"All real x except x = {k}",
                          [f"All real x except x = {-k}", f"x > {k}", f"All real x"], e, h))
        elif mode == 'parity':
            kind = R.choice(['even', 'odd', 'neither'])
            expr, ans, why = {
                'even': (f"f(x) = {R.choice([2,3,5])}x² + {R.choice([1,4,7])}", "Even",
                         "Replacing x by −x leaves x² unchanged, so f(−x) = f(x)."),
                'odd': (f"f(x) = {R.choice([2,3,5])}x³ − {R.choice([2,6,8])}x", "Odd",
                        "Both terms are odd powers, so f(−x) = −f(x)."),
                'neither': (f"f(x) = {R.choice([2,3])}x² + {R.choice([3,5,7])}x", "Neither even nor odd",
                            "The square term is even and the linear term is odd, so neither identity holds."),
            }[kind]
            q = f"The function {expr} is:"
            e = why
            h = "Substitute −x and compare with f(x) and with −f(x). Only one comparison can hold."
            out.append(mk("Functions", "Medium", q, ans,
                          [x for x in ["Even", "Odd", "Neither even nor odd", "Even and odd"] if x != ans][:3],
                          e, h))
        elif mode == 'iterate':
            a = R.choice(range(2, 20))
            x = R.choice(range(2, 12))
            # f(x) = a - x is an involution
            q = f"If f(x) = {a} − x, then f(f(f({x}))) equals:"
            v1 = a - x
            v2 = a - v1
            v3 = a - v2
            e = (f"f({x}) = {v1}, f({v1}) = {v2}, f({v2}) = {v3}. The function undoes itself every two "
                 f"steps, so an odd number of applications behaves like one.")
            h = "Iterate two or three times and look for the repeat before computing further."
            out.append(mk("Functions", "Medium", q, v3, [x, v2, a], e, h))
        else:
            a, b = R.choice(range(2, 9)), R.choice([v for v in range(-9, 10) if v])
            y = R.choice(range(5, 60))
            inv = Fraction(y - b, a)
            if inv.denominator != 1:
                continue
            sg = lambda v: f"+ {v}" if v >= 0 else f"- {abs(v)}"
            q = f"If f(x) = {a}x {sg(b)}, the value of f⁻¹({y}) is:"
            e = f"Solve {a}x {sg(b)} = {y}, giving x = ({y} − {b})/{a} = {inv}."
            h = "The inverse answers 'what input produced this output'. Set f(x) equal to the value and solve."
            out.append(mk("Functions", "Medium", q, inv, [a * y + b, Fraction(y + b, a), y - b], e, h))
    return [x for x in out if x][:n]


# --------------------------------------------------------------- inequalities
def gen_inequalities(n):
    out = []
    for _ in range(n * 4):
        mode = R.choice(['linear', 'modulus', 'amgm', 'quadratic', 'intervals'])
        if mode == 'linear':
            a = R.choice([-7, -5, -4, -3, -2])
            b = R.choice([6, 9, 12, 15, 20])
            bound = Fraction(b, a)
            q = f"Solve for x: {a}x > {b}."
            e = (f"Dividing by {a}, which is negative, reverses the inequality, giving x < {bound}.")
            h = "Dividing by a negative flips the sign. This single rule causes most errors in the chapter."
            out.append(mk("Inequalities", "Easy", q, f"x < {bound}",
                          [f"x > {bound}", f"x > {-bound}", f"x < {-bound}"], e, h))
        elif mode == 'modulus':
            a, b = R.choice([2, 3, 5, 6, 8]), R.choice([2, 3, 4, 5, 7])
            q = f"The solution set of |x − {a}| < {b} is:"
            e = f"The inequality says x lies within {b} of {a}, so {a-b} < x < {a+b}."
            h = "|x − a| < b is a band around a. |x − a| > b is the two rays outside it."
            out.append(mk("Inequalities", "Easy", q, f"{a-b} < x < {a+b}",
                          [f"x < {a-b} or x > {a+b}", f"{-a-b} < x < {-a+b}", f"0 < x < {a+b}"], e, h))
        elif mode == 'amgm':
            k = R.choice([4, 9, 16, 25, 36, 49, 64, 100])
            m = 2 * int(math.isqrt(k))
            q = f"For x > 0, the minimum value of x + {k}/x is:"
            e = (f"By AM ≥ GM, x + {k}/x ≥ 2√({k}) = {m}, with equality when x = √{k} = {int(math.isqrt(k))}.")
            h = "A sum of a term and its reciprocal multiple is an AM-GM question. Equality fixes the value of x."
            out.append(mk("Inequalities", "Medium", q, m, [k, m + 2, int(math.isqrt(k))], e, h))
        elif mode == 'quadratic':
            r1, r2 = sorted(R.sample([-6, -4, -3, -2, 1, 2, 3, 5, 7], 2))
            b, c = -(r1 + r2), r1 * r2
            sg = lambda v: f"+ {v}" if v >= 0 else f"- {abs(v)}"
            q = f"The solution of x² {sg(b)}x {sg(c)} < 0 is:"
            e = (f"The expression factorises as (x − {r1})(x − {r2}), so it is negative strictly "
                 f"between the roots: {r1} < x < {r2}.")
            h = "A quadratic with positive leading coefficient is negative only between its roots."
            out.append(mk("Inequalities", "Medium", q, f"{r1} < x < {r2}",
                          [f"x < {r1} or x > {r2}", f"x > {r2}", f"{r2} < x < {r1}"], e, h))
        else:
            lo, hi = R.choice([1, 2, 3]), R.choice([9, 11, 14, 17, 20])
            cnt = hi - lo - 1
            q = f"How many integers x satisfy {lo} < x < {hi}?"
            e = f"The integers run from {lo+1} to {hi-1}, giving {hi-1} − {lo+1} + 1 = {cnt} values."
            h = "Strict inequalities exclude both endpoints. Count the endpoints of the integer range, not the bounds."
            out.append(mk("Inequalities", "Easy", q, cnt, [cnt + 1, cnt + 2, cnt - 1], e, h))
    return [x for x in out if x][:n]


# ---------------------------------------------------------------- logarithms
def gen_logarithms(n):
    out = []
    for _ in range(n * 4):
        mode = R.choice(['evaluate', 'collapse', 'basechange', 'equation', 'identity'])
        if mode == 'evaluate':
            b = R.choice([2, 3, 5, 6, 7, 10, 11, 12])
            k = R.choice([2, 3, 4, 5, 6])
            q = f"The value of log₍{b}₎({b**k}) is:"
            e = f"{b}^{k} = {b**k}, so the logarithm is {k}."
            h = "Ask what power of the base gives the argument. That is the whole definition."
            out.append(mk("Logarithms & Indices", "Easy", q, k, [b * k, b ** k, k + 1], e, h))
        elif mode == 'collapse':
            a, b = R.choice(range(2, 13)), R.choice(range(3, 30))
            q = f"log {a} + log {b} − log {a} equals:"
            e = f"The first and third terms cancel, leaving log {b}."
            h = "Products become sums and quotients become differences. Cancel before computing."
            out.append(mk("Logarithms & Indices", "Easy", q, f"log {b}",
                          [f"log {a*b}", f"log {a+b}", f"log {Fraction(b,a)}"], e, h))
        elif mode == 'basechange':
            b = R.choice([2, 3, 5, 6, 7, 10])
            k = R.choice([2, 3, 4, 5])
            val = Fraction(1, k)
            q = f"log₍{b**k}₎({b}) equals:"
            e = (f"Write {b**k} as {b}^{k}. Then log₍{b}^{k}₎({b}) = 1/{k} = {val}.")
            h = "When base and argument are powers of the same number, the log is the ratio of the exponents."
            out.append(mk("Logarithms & Indices", "Medium", q, val, [k, b, Fraction(k, 1)], e, h))
        elif mode == 'equation':
            b = R.choice([2, 3, 5, 6, 7, 10])
            k = R.choice([2, 3, 4, 5])
            shift = R.choice(range(1, 12))
            x = b ** k - shift
            q = f"If log₍{b}₎(x + {shift}) = {k}, then x equals:"
            e = f"x + {shift} = {b}^{k} = {b**k}, so x = {b**k} − {shift} = {x}."
            h = "Convert to exponential form immediately, then solve the ordinary equation."
            out.append(mk("Logarithms & Indices", "Easy", q, x, [b ** k, k - shift, x + 2 * shift], e, h))
        else:
            a = R.choice(range(2, 40))
            q = f"The value of log₍{a}₎(b) × log₍b₎({a}), for any valid b, is:"
            e = f"By the base-change rule the two logarithms are reciprocals, so the product is 1."
            h = "log_b a and log_a b are reciprocals. Spot the pair before computing anything."
            out.append(mk("Logarithms & Indices", "Medium", q, 1, [0, a, f"log {a}"], e, h))
    return [x for x in out if x][:n]


# -------------------------------------------------------------- base systems
def gen_base(n):
    out = []
    for _ in range(n * 4):
        mode = R.choice(['to_dec', 'from_dec', 'addition'])
        base = R.choice([2, 3, 4, 5, 6, 7, 8, 9])
        if mode == 'to_dec':
            digits = [R.randrange(1, base)] + [R.randrange(0, base) for _ in range(R.choice([2, 3]))]
            val = 0
            for d in digits:
                val = val * base + d
            s = "".join(str(d) for d in digits)
            q = f"The base-{base} number {s} expressed in base 10 is:"
            e = (f"Evaluate the positional expansion: " +
                 " + ".join(f"{d}×{base}^{len(digits)-1-i}" for i, d in enumerate(digits)) + f" = {val}.")
            h = "A number in base b is a polynomial in b. Converting to decimal is evaluating it."
            out.append(mk("Base Systems", "Medium", q, val, [val + base, val - 1, int(s)], e, h))
        elif mode == 'from_dec':
            val = R.randrange(20, 400)
            t, digs = val, []
            while t:
                digs.append(t % base)
                t //= base
            s = "".join(str(d) for d in reversed(digs))
            q = f"The decimal number {val} written in base {base} is:"
            e = (f"Divide repeatedly by {base} and read the remainders upward, giving {s}.")
            h = "Repeated division by the base; the remainders read bottom to top."
            out.append(mk("Base Systems", "Medium", q, s, [s + "0", str(int(s) + 1), s[::-1]], e, h))
        else:
            x, y = R.randrange(5, 60), R.randrange(5, 60)
            def tob(v, b):
                if v == 0:
                    return "0"
                d = []
                while v:
                    d.append(str(v % b))
                    v //= b
                return "".join(reversed(d))
            q = f"In base {base}, the sum of {tob(x,base)} and {tob(y,base)} is:"
            e = (f"In decimal the numbers are {x} and {y}, summing to {x+y}, which is "
                 f"{tob(x+y,base)} in base {base}.")
            h = "Convert to decimal, add, convert back. Direct addition in base is error-prone under time."
            out.append(mk("Base Systems", "Hard", q, tob(x + y, base),
                          [str(int(tob(x, base)) + int(tob(y, base))), tob(x + y, base) + "0",
                           tob(abs(x - y), base)], e, h))
    return [x for x in out if x][:n]


# --------------------------------------------------------------- alligations
def gen_alligation(n):
    out = []
    for _ in range(n * 4):
        mode = R.choice(['ratio', 'replacement', 'concentration'])
        if mode == 'ratio':
            c1, c2 = R.choice([12, 15, 18, 20, 24]), R.choice([36, 40, 45, 48, 60])
            if c1 >= c2:
                continue
            mean = R.choice([v for v in range(c1 + 2, c2, 2)])
            fr = Fraction(c2 - mean, mean - c1)
            q = (f"In what ratio must a liquid costing Rs {c1} per litre be mixed with one costing "
                 f"Rs {c2} per litre to obtain a mixture worth Rs {mean} per litre?")
            e = (f"Cross differences give ({c2} − {mean}) : ({mean} − {c1}) = {c2-mean} : {mean-c1} "
                 f"= {fr.numerator} : {fr.denominator}.")
            h = "Alligation is a cross difference from the mean. Cheaper on the left, dearer on the right, always."
            out.append(mk("Alligations", "Easy", q, f"{fr.numerator} : {fr.denominator}",
                          [f"{fr.denominator} : {fr.numerator}", f"{c1} : {c2}", f"{mean} : {c2}"], e, h))
        elif mode == 'replacement':
            V = R.choice([40, 50, 60, 80, 100])
            x = R.choice([5, 10, 20])
            k = R.choice([2, 3])
            if x >= V:
                continue
            rem = Fraction(V - x, V) ** k * V
            q = (f"A vessel holds {V} litres of pure milk. {x} litres are removed and replaced with "
                 f"water, and this operation is performed {k} times in all. The milk remaining is:")
            e = (f"After each operation the milk is multiplied by (1 − {x}/{V}). After {k} operations "
                 f"the milk is {V} × ({V-x}/{V})^{k} = {rem} litres.")
            h = "Repeated replacement is a geometric decay. Compute the surviving fraction, then multiply by the volume."
            out.append(mk("Alligations", "Hard", q, f"{rem} litres",
                          [f"{V - k*x} litres", f"{Fraction(V-x,V)*V} litres",
                 f"{Fraction((V-x)**k, V**(k-1))} litres", f"{V-x} litres"], e, h))
        else:
            tot = R.choice([40, 60, 80, 100])
            p = R.choice([20, 25, 30, 40])
            add = R.choice([10, 20, 25])
            acid = tot * p / 100
            newp = Fraction(int(acid) * 100, tot + add)
            q = (f"A {tot}-litre solution is {p}% acid. If {add} litres of water are added, the acid "
                 f"concentration becomes:")
            e = (f"Acid stays at {int(acid)} litres while the volume rises to {tot+add}, so the "
                 f"concentration is {int(acid)}/{tot+add} = {newp}%.")
            h = "Adding water changes the denominator only. Track the solute, which does not move."
            out.append(mk("Alligations", "Medium", q, f"{newp}%",
                          [f"{p}%", f"{Fraction(p,2)}%", f"{Fraction(int(acid)*100,tot+2*add)}%",
                 f"{Fraction(int(acid)*100,add)}%"], e, h))
    return [x for x in out if x][:n]


# --------------------------------------------------------- coordinate geometry
def gen_coordinate(n):
    out = []
    for _ in range(n * 4):
        mode = R.choice(['midpoint', 'slope', 'collinear', 'area', 'section', 'circle'])
        x1, y1 = R.randrange(-9, 10), R.randrange(-9, 10)
        x2, y2 = R.randrange(-9, 10), R.randrange(-9, 10)
        if (x1, y1) == (x2, y2):
            continue
        if mode == 'midpoint':
            mx, my = Fraction(x1 + x2, 2), Fraction(y1 + y2, 2)
            q = f"The midpoint of the segment joining ({x1}, {y1}) and ({x2}, {y2}) is:"
            e = f"Average the coordinates: (({x1}+{x2})/2, ({y1}+{y2})/2) = ({mx}, {my})."
            h = "Midpoint averages; section divides. Check which the question asked."
            out.append(mk("Coordinate Geometry", "Easy", q, f"({mx}, {my})",
                          [f"({x1+x2}, {y1+y2})", f"({my}, {mx})",
                           f"({Fraction(x1-x2,2)}, {Fraction(y1-y2,2)})"], e, h))
        elif mode == 'slope':
            if x1 == x2:
                continue
            m = Fraction(y2 - y1, x2 - x1)
            q = f"The slope of the line through ({x1}, {y1}) and ({x2}, {y2}) is:"
            e = f"Slope = ({y2} − {y1})/({x2} − {x1}) = {m}."
            h = "Rise over run, in that order. Reversing it is the standard slip."
            out.append(mk("Coordinate Geometry", "Easy", q, m,
                          [Fraction(x2 - x1, y2 - y1) if y2 != y1 else m + 1, -m, m + 1], e, h))
        elif mode == 'collinear':
            k = R.choice([2, 3])
            x3, y3 = x1 + k * (x2 - x1), y1 + k * (y2 - y1)
            area = abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2
            q = (f"Are the points ({x1}, {y1}), ({x2}, {y2}) and ({x3}, {y3}) collinear?")
            e = (f"The triangle they form has area {int(area)}, and zero area means the points lie "
                 f"on one line.")
            h = "Collinearity is a zero-area test. One determinant settles it."
            out.append(mk("Coordinate Geometry", "Medium", q, "Yes, they are collinear",
                          ["No, they form a triangle", "Only two of them coincide",
                           "They form a right triangle"], e, h))
        elif mode == 'area':
            x3, y3 = R.randrange(-9, 10), R.randrange(-9, 10)
            ar = Fraction(abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)), 2)
            if ar == 0:
                continue
            q = (f"The area of the triangle with vertices ({x1}, {y1}), ({x2}, {y2}) and "
                 f"({x3}, {y3}) is:")
            e = (f"Using ½|x₁(y₂−y₃) + x₂(y₃−y₁) + x₃(y₁−y₂)|, the area is {ar} square units.")
            h = "Take the absolute value last. A negative result only means the vertices were listed clockwise."
            out.append(mk("Coordinate Geometry", "Medium", q, f"{ar} sq units",
                          [f"{ar*2} sq units", f"{Fraction(ar,2)} sq units", f"{ar+1} sq units"], e, h))
        elif mode == 'section':
            m_, n_ = R.choice([1, 2, 3]), R.choice([1, 2, 3, 4])
            px = Fraction(m_ * x2 + n_ * x1, m_ + n_)
            py = Fraction(m_ * y2 + n_ * y1, m_ + n_)
            q = (f"The point dividing the segment from ({x1}, {y1}) to ({x2}, {y2}) internally in "
                 f"the ratio {m_} : {n_} is:")
            e = (f"Section formula: (({m_}×{x2} + {n_}×{x1})/{m_+n_}, ({m_}×{y2} + {n_}×{y1})/{m_+n_}) "
                 f"= ({px}, {py}).")
            h = "The far point pairs with the first ratio term. Swapping them is the common error."
            out.append(mk("Coordinate Geometry", "Medium", q, f"({px}, {py})",
                          [f"({py}, {px})", f"({Fraction(x1+x2,2)}, {Fraction(y1+y2,2)})",
                           f"({Fraction(n_*x2+m_*x1,m_+n_)}, {Fraction(n_*y2+m_*y1,m_+n_)})"], e, h))
        else:
            h_, k_, r_ = R.randrange(-6, 7), R.randrange(-6, 7), R.choice([2, 3, 4, 5, 6])
            sg = lambda v: f"+ {abs(v)}" if v < 0 else (f"- {v}" if v > 0 else "")
            q = (f"The centre and radius of the circle (x {sg(h_)})² + (y {sg(k_)})² = {r_*r_} are:")
            e = f"Comparing with (x−h)² + (y−k)² = r², the centre is ({h_}, {k_}) and the radius is {r_}."
            h = "Read the centre with the signs flipped from what appears inside the brackets."
            out.append(mk("Coordinate Geometry", "Easy", q, f"Centre ({h_}, {k_}), radius {r_}",
                          [f"Centre ({-h_}, {-k_}), radius {r_}", f"Centre ({h_}, {k_}), radius {r_*r_}",
                           f"Centre ({k_}, {h_}), radius {r_}"], e, h))
    return [x for x in out if x][:n]


# ----------------------------------------------------- calculation drills (FTF)
def gen_ftf(n):
    per = max(1, n // 4)
    adds, mults, pcts, sqs = [], [], [], []

    for _ in range(per * 3):                                   # additions
        nums = [R.randrange(120, 900) for _ in range(4)]
        tot = sum(nums)
        q = f"Add mentally: {' + '.join(str(x) for x in nums)}"
        e = (f"Work left to right in pairs: {nums[0]}+{nums[1]} = {nums[0]+nums[1]}, "
             f"{nums[2]}+{nums[3]} = {nums[2]+nums[3]}, total {tot}.")
        h = "Add left to right and in pairs. Carrying across four numbers at once is where errors enter."
        adds.append(mk("Speed Addition", "Easy", q, tot, [tot + 10, tot - 9, tot + 100], e, h))

    for _ in range(per * 3):                                   # multiplications
        a, b = R.randrange(88, 112), R.randrange(88, 112)
        if a == b:
            continue
        p = a * b
        q = f"Compute mentally: {a} × {b}"
        e = (f"Both numbers sit near 100. Deviations are {a-100} and {b-100}: "
             f"({a} {'+' if b-100>=0 else '-'} {abs(b-100)}) = {a+b-100}, and "
             f"({a-100})×({b-100}) = {(a-100)*(b-100)}, giving {p}.")
        h = "Numbers near a base multiply by the deviation method. Cross-add, then multiply the deviations."
        mults.append(mk("Speed Multiplication", "Medium", q, p, [p + 100, p - 100, p + 10], e, h))

    for _ in range(per * 3):                                   # percentages / division
        num, den = R.randrange(3, 40), R.choice([8, 10, 12, 16, 20, 25, 40, 50])
        if num >= den:
            continue
        pct = round(num * 100 / den, 2)
        q = f"Express {num}/{den} as a percentage."
        e = f"{num}/{den} = {num}×100/{den} = {pct}%."
        h = "Keep the fraction-to-percentage table to sixteenths in recall. Most of these are a lookup."
        pcts.append(mk("Percentage Calculations", "Easy", q, f"{pct}%",
                      [f"{round(den*100/num,2)}%", f"{num*den}%", f"{round(pct+5,2)}%"], e, h))

    for _ in range(per * 3):                                   # squares and cubes
        if R.random() < 0.6:
            k = R.randrange(21, 100)
            v = k * k
            q = f"Compute mentally: {k}²"
            if k % 10 == 5:
                e = f"For a number ending in 5, take {k//10}×{k//10+1} = {(k//10)*(k//10+1)} then append 25, giving {v}."
            else:
                near = round(k / 10) * 10
                e = (f"Use (a±b)² about {near}: {near}² = {near*near}, adjust by "
                     f"2×{near}×{k-near} = {2*near*(k-near)} and {k-near}² = {(k-near)**2}, giving {v}.")
            h = "Anchor on the nearest multiple of ten and correct. Numbers ending in 5 have their own one-step rule."
            sqs.append(mk("Squares and Cubes", "Easy", q, v, [v + 100, v - 100, v + 2 * k], e, h))
        else:
            k = R.randrange(6, 20)
            v = k ** 3
            q = f"Compute mentally: {k}³"
            e = f"{k}² = {k*k}, and {k*k} × {k} = {v}."
            h = "Cubes to 15 should be recall. Beyond that, square first and multiply once."
            sqs.append(mk("Squares and Cubes", "Easy", q, v, [k * k, v + k, v - k], e, h))

    def take(lst):
        seen, keep = set(), []
        for r in lst:
            if not r or r['question'] in seen:
                continue
            seen.add(r['question'])
            keep.append(r)
        return keep[:per]
    return take(adds) + take(mults) + take(pcts) + take(sqs)


PLAN = [(gen_functions, 120), (gen_inequalities, 110), (gen_logarithms, 110),
        (gen_base, 55), (gen_alligation, 70), (gen_coordinate, 110), (gen_ftf, 240)]


def build():
    out, seen = [], set()
    for fn, cnt in PLAN:
        for rec in fn(cnt):
            k = rec['question'].strip()
            if k in seen:
                continue
            seen.add(k)
            out.append(rec)
    for i, r in enumerate(out, 1):
        r['id'] = f"ORIG-QX-{i:04d}"
    return out


if __name__ == '__main__':
    import collections
    qs = build()
    print("generated:", len(qs))
    print(dict(collections.Counter(q['topic'] for q in qs)))
