# -*- coding: utf-8 -*-
"""
Level of Difficulty III questions: multi-step problems that combine two or more
concepts from a chapter, matching the role LOD III plays in the book's
structure. Answers are computed, as everywhere else in this bank.
"""
import random, math
from fractions import Fraction

R = random.Random(606042)
_seq = {'n': 0}


def fmt(x):
    if isinstance(x, Fraction):
        return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
    return str(x)


def mk(topic, question, correct, wrongs, explanation, how):
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
    return {"id": f"ORIG-L3-{_seq['n']:04d}", "section": "QA", "type": "MCQ", "topic": topic,
            "difficulty": "Hard", "sourceType": "ORIGINAL",
            "sourceLabel": "Original CAT-level practice (computed answer)", "sourceUrl": "",
            "year": None, "slot": None, "title": f"QA · {topic}", "stimulus": "",
            "question": question, "options": opts, "answer": opts.index(c), "answerText": c,
            "explanation": explanation, "howToThink": how, "explanationStatus": "FULL"}


def numbers(n):
    out = []
    for _ in range(n * 4):
        mode = R.choice(['rem_big', 'lcm_rem', 'factors_sum', 'zeros'])
        if mode == 'rem_big':
            a, p, m = R.choice([13, 17, 19, 23, 29, 31]), R.choice([101, 143, 202, 257]), R.choice([7, 11, 13, 17])
            v = pow(a, p, m)
            out.append(mk("Number Systems",
                f"Find the remainder when {a}^{p} is divided by {m}.", v,
                [(v + 1) % m, (v + 2) % m, (v + m - 1) % m],
                f"Reduce the base: {a} ≡ {a%m} (mod {m}). The powers of {a%m} modulo {m} repeat with a "
                f"short cycle, and reducing the exponent {p} within that cycle leaves {v}.",
                "Reduce the base first, find the cycle length of its powers, then reduce the exponent modulo that length."))
        elif mode == 'lcm_rem':
            ds = R.sample([4, 5, 6, 7, 8, 9, 11], 3)
            r = R.choice([1, 2, 3])
            L = ds[0]
            for d in ds[1:]:
                L = L * d // math.gcd(L, d)
            v = L + r
            out.append(mk("Number Systems",
                f"What is the smallest number greater than {r} which leaves a remainder of {r} when "
                f"divided by each of {ds[0]}, {ds[1]} and {ds[2]}?", v,
                [L, L - r, L * 2 + r],
                f"A number leaving the same remainder {r} with each divisor is LCM × k + {r}. "
                f"LCM({ds[0]}, {ds[1]}, {ds[2]}) = {L}, so the smallest such number beyond {r} is {L} + {r} = {v}.",
                "Equal remainders across several divisors always point at the LCM plus that remainder."))
        elif mode == 'factors_sum':
            x = R.choice([72, 96, 120, 144, 180, 196, 216, 240, 360])
            divs = [d for d in range(1, x + 1) if x % d == 0]
            s = sum(divs)
            odd = len([d for d in divs if d % 2])
            out.append(mk("Number Systems",
                f"How many odd factors does {x} have, and what is the sum of all its factors?",
                f"{odd} odd factors, sum {s}",
                [f"{odd+1} odd factors, sum {s}", f"{odd} odd factors, sum {s-x}",
                 f"{len(divs)} odd factors, sum {s}"],
                f"{x} has {len(divs)} factors in all, of which {odd} are odd, and they sum to {s}. "
                f"Odd factors come from the odd part of the prime factorisation alone.",
                "Split the factorisation into its power of 2 and its odd part. The odd part alone generates the odd factors."))
        else:
            k = R.choice([60, 75, 100, 125, 150, 200])
            z, p5 = 0, 5
            while p5 <= k:
                z += k // p5
                p5 *= 5
            out.append(mk("Number Systems",
                f"How many consecutive zeros does {k}! end in?", z,
                [z + 1, z - 2, k // 5],
                f"Count the factors of 5: " + " + ".join(f"[{k}/{5**i}]" for i in range(1, 5) if 5**i <= k) +
                f" = {z}. The factors of 2 are always in surplus, so the 5s decide.",
                "Only the count of 5s matters. Include higher powers of 5, which contribute more than one each."))
    return [x for x in out if x][:n]


def arithmetic(n):
    out = []
    for _ in range(n * 4):
        mode = R.choice(['two_disc', 'work_leave', 'meet', 'mix_two'])
        if mode == 'two_disc':
            mp = R.choice([1200, 1500, 1800, 2400, 3000])
            d1, d2 = R.choice([10, 15, 20]), R.choice([5, 10, 12])
            sp = Fraction(mp * (100 - d1) * (100 - d2), 10000)
            single = Fraction((mp - sp) * 100, mp)
            out.append(mk("Profit & Loss",
                f"An item marked at Rs {mp} is sold after two successive discounts of {d1}% and {d2}%. "
                f"The single discount equivalent to these two is:",
                f"{single}%", [f"{d1+d2}%", f"{Fraction(d1*d2,100)}%", f"{d1+d2+1}%"],
                f"Selling price = {mp} × {100-d1}/100 × {100-d2}/100 = Rs {sp}. The total reduction is "
                f"{mp} − {sp} = {mp-sp}, which is {single}% of {mp}.",
                "Successive discounts multiply. The equivalent single discount is always less than their sum."))
        elif mode == 'work_leave':
            a, b, c = R.sample([10, 12, 15, 18, 20, 24, 30], 3)
            d = R.choice([2, 3, 4])
            ra, rb, rc = Fraction(1, a), Fraction(1, b), Fraction(1, c)
            done = (ra + rb + rc) * d
            if done >= 1:
                continue
            rem = (1 - done) / (rb + rc)
            out.append(mk("Time & Work",
                f"A, B and C can finish a job alone in {a}, {b} and {c} days. All three start together, "
                f"but A leaves after {d} days. In how many more days do B and C finish the job?",
                f"{rem} days", [f"{Fraction(b*c,b+c)} days", f"{b-d} days", f"{done*b} days"],
                f"In {d} days the three complete {d}(1/{a} + 1/{b} + 1/{c}) = {done}. The remaining "
                f"{1-done} is cleared by B and C at a combined rate of {rb+rc} per day, needing {rem} more days.",
                "Track the fraction completed, then divide what is left by the rate of whoever remains."))
        elif mode == 'meet':
            d_ = R.choice([180, 240, 300, 360, 420])
            u, v = R.choice([30, 40, 45, 50]), R.choice([55, 60, 70, 80])
            t = Fraction(d_, u + v)
            pos = u * t
            out.append(mk("Time, Speed & Distance",
                f"Two cars start simultaneously towards each other from towns {d_} km apart, at {u} km/h "
                f"and {v} km/h. How far from the first town do they meet?",
                f"{pos} km", [f"{Fraction(d_,2)} km", f"{v*t} km", f"{Fraction(d_*u,v)} km"],
                f"Closing speed = {u} + {v} = {u+v} km/h, so they meet after {d_}/{u+v} = {t} hours. "
                f"The first car has covered {u} × {t} = {pos} km.",
                "Opposite directions add speeds. Find the meeting time first, then the distance for whichever car is asked."))
        else:
            c1, c2 = R.choice([20, 24, 30]), R.choice([45, 50, 60])
            q1, q2 = R.choice([8, 10, 12]), R.choice([15, 18, 20])
            profit = R.choice([10, 20, 25])
            cost = Fraction(c1 * q1 + c2 * q2, q1 + q2)
            sp = cost * (100 + profit) / 100
            out.append(mk("Averages and Mixtures",
                f"{q1} kg of a variety costing Rs {c1} per kg is mixed with {q2} kg costing Rs {c2} per kg. "
                f"At what price per kg must the mixture be sold to earn a profit of {profit}%?",
                f"Rs {sp}", [f"Rs {cost}", f"Rs {Fraction(c1+c2,2)}", f"Rs {cost*2}"],
                f"Mixture cost = ({q1}×{c1} + {q2}×{c2})/({q1}+{q2}) = Rs {cost} per kg. Adding {profit}% "
                f"gives {cost} × {100+profit}/100 = Rs {sp}.",
                "Find the weighted cost of the mixture first. Only then apply the profit margin."))
    return [x for x in out if x][:n]


def algebra(n):
    out = []
    for _ in range(n * 4):
        mode = R.choice(['cubes', 'maxmin', 'log_eq', 'ineq_range'])
        if mode == 'cubes':
            a = R.choice([1, 2])
            b = R.choice([-14, -11, -9, -7, 7, 10, 13])
            c = R.choice([-20, -12, 6, 15, 18])
            s = Fraction(-b, a)
            p = Fraction(c, a)
            v = s ** 3 - 3 * p * s
            out.append(mk("Equations",
                f"If α and β are the roots of {a}x² + ({b})x + ({c}) = 0, the value of α³ + β³ is:",
                v, [s ** 3, s ** 3 - p, s * p],
                f"α + β = {s} and αβ = {p}. Then α³ + β³ = (α+β)³ − 3αβ(α+β) = {s}³ − 3({p})({s}) = {v}.",
                "Build symmetric expressions from the sum and product. Never solve for the roots themselves."))
        elif mode == 'maxmin':
            a = R.choice([1, 2, 3])
            h = R.choice([-5, -3, -2, 2, 4, 6])
            k = R.choice([-12, -6, 3, 9, 15])
            b, c = -2 * a * h, a * h * h + k
            sg = lambda v: f"+ {v}" if v >= 0 else f"- {abs(v)}"
            out.append(mk("Equations",
                f"The minimum value of {a}x² {sg(b)}x {sg(c)} is:", k,
                [h, -k, k + a],
                f"The vertex sits at x = −b/2a = {h}, and substituting gives {k}. Since the leading "
                f"coefficient {a} is positive, this is a minimum.",
                "Complete the square or use x = −b/2a. The sign of a decides whether it is a maximum or a minimum."))
        elif mode == 'log_eq':
            b = R.choice([2, 3, 5])
            m = R.choice([2, 3, 4])
            n_ = R.choice([2, 3, 5, 6])
            val = b ** m * n_
            out.append(mk("Logarithms & Indices",
                f"If log₍{b}₎x − log₍{b}₎{n_} = {m}, then x equals:", val,
                [b ** m, b ** m + n_, Fraction(b ** m, n_)],
                f"The difference of logarithms is the logarithm of the quotient, so log₍{b}₎(x/{n_}) = {m}, "
                f"giving x/{n_} = {b}^{m} = {b**m} and x = {val}.",
                "Collapse the logarithms into one before converting to exponential form."))
        else:
            a = R.choice([2, 3, 4])
            b = R.choice([5, 7, 9, 11])
            c = R.choice([13, 17, 21, 25])
            lo = Fraction(b - c, a) if a else 0
            lo = Fraction(-(c - b), a)
            hi = Fraction(c + b, a)
            cnt = len([x for x in range(-60, 121) if lo < x < hi])
            out.append(mk("Inequalities",
                f"How many integers x satisfy |{a}x − {b}| < {c}?", cnt,
                [cnt + 1, cnt - 1, cnt + 2],
                f"The inequality unfolds to {-c} < {a}x − {b} < {c}, so {lo} < x < {hi}. "
                f"The integers strictly inside that interval number {cnt}.",
                "Unfold the modulus into a double inequality, solve for x, then count integers strictly inside."))
    return [x for x in out if x][:n]


def counting(n):
    out = []
    for _ in range(n * 4):
        mode = R.choice(['together', 'atleast', 'distribute', 'committee'])
        if mode == 'together':
            tot = R.choice([5, 6, 7, 8])
            grp = R.choice([2, 3])
            if grp >= tot:
                continue
            v = math.factorial(tot - grp + 1) * math.factorial(grp)
            out.append(mk("Permutation & Combination",
                f"In how many ways can {tot} people be seated in a row if {grp} particular people must "
                f"always sit together?", v,
                [math.factorial(tot), math.factorial(tot - grp + 1), math.factorial(tot) // math.factorial(grp)],
                f"Glue the {grp} into one unit, leaving {tot-grp+1} units to arrange in {math.factorial(tot-grp+1)} "
                f"ways, and the glued group arranges internally in {math.factorial(grp)} ways, giving {v}.",
                "Treat the inseparable group as a single object, arrange, then arrange within the group."))
        elif mode == 'atleast':
            r_, b_ = R.choice([4, 5, 6]), R.choice([4, 5, 6, 7])
            k = R.choice([2, 3])
            tot = math.comb(r_ + b_, k)
            none = math.comb(b_, k)
            pr = Fraction(tot - none, tot)
            out.append(mk("Probability",
                f"A bag contains {r_} red and {b_} blue balls. If {k} balls are drawn at random, the "
                f"probability that at least one is red is:", pr,
                [Fraction(none, tot), Fraction(r_, r_ + b_), Fraction(math.comb(r_, k), tot)],
                f"P(at least one red) = 1 − P(no red) = 1 − C({b_},{k})/C({r_+b_},{k}) = "
                f"1 − {none}/{tot} = {pr}.",
                "'At least one' is nearly always faster as one minus the probability of none."))
        elif mode == 'distribute':
            objs, boxes = R.choice([6, 7, 8, 9, 10]), R.choice([3, 4])
            v = math.comb(objs + boxes - 1, boxes - 1)
            out.append(mk("Permutation & Combination",
                f"In how many ways can {objs} identical chocolates be distributed among {boxes} children, "
                f"if a child may receive none?", v,
                [boxes ** objs, math.comb(objs, boxes), objs ** boxes],
                f"This is the stars and bars count C(n + r − 1, r − 1) = C({objs+boxes-1}, {boxes-1}) = {v}.",
                "Identical objects into distinct boxes is stars and bars. Distinct objects would be a different count entirely."))
        else:
            m_, w_ = R.choice([5, 6, 7]), R.choice([4, 5, 6])
            cm, cw = R.choice([2, 3]), R.choice([2, 3])
            v = math.comb(m_, cm) * math.comb(w_, cw)
            out.append(mk("Permutation & Combination",
                f"A committee of {cm} men and {cw} women is to be formed from {m_} men and {w_} women. "
                f"The number of ways is:", v,
                [math.comb(m_ + w_, cm + cw), math.comb(m_, cm) + math.comb(w_, cw),
                 math.perm(m_, cm) * math.perm(w_, cw)],
                f"Choose the men in C({m_},{cm}) = {math.comb(m_,cm)} ways and the women in "
                f"C({w_},{cw}) = {math.comb(w_,cw)} ways, and multiply: {v}.",
                "Independent choices multiply. Adding them is the classic error in committee questions."))
    return [x for x in out if x][:n]


def geometry(n):
    out = []
    for _ in range(n * 4):
        mode = R.choice(['inradius', 'cyclic', 'cone_sphere', 'shaded'])
        if mode == 'inradius':
            a, b, c = R.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (9, 40, 41)])
            k = R.choice([1, 2, 3])
            a, b, c = a * k, b * k, c * k
            r = Fraction(a + b - c, 2)
            out.append(mk("Geometry",
                f"A right triangle has legs {a} cm and {b} cm and hypotenuse {c} cm. The radius of its "
                f"inscribed circle is:", f"{r} cm",
                [f"{Fraction(c,2)} cm", f"{Fraction(a+b+c,2)} cm", f"{r*2} cm"],
                f"For a right triangle the inradius is (a + b − c)/2 = ({a} + {b} − {c})/2 = {r} cm.",
                "Right triangles have a one-step inradius. For other triangles use area divided by the semiperimeter."))
        elif mode == 'cyclic':
            x = R.choice([65, 70, 75, 80, 95, 105, 110])
            out.append(mk("Geometry",
                f"In a cyclic quadrilateral, one angle measures {x}°. Its opposite angle measures:",
                f"{180-x}°", [f"{x}°", f"{360-x}°", f"{90-x if x<90 else x-90}°"],
                f"Opposite angles of a cyclic quadrilateral are supplementary, so the opposite angle is "
                f"180° − {x}° = {180-x}°.",
                "Spot the cyclic quadrilateral first. The supplementary property then answers most such questions in one step."))
        elif mode == 'cone_sphere':
            r_ = R.choice([3, 6, 7, 9, 12])
            h_ = R.choice([6, 9, 12, 15, 24])
            vc = Fraction(22, 7) * r_ * r_ * h_ / 3
            vs = Fraction(4, 3) * Fraction(22, 7) * r_ ** 3
            ratio = Fraction(vc, vs)
            out.append(mk("Mensuration",
                f"A cone of radius {r_} cm and height {h_} cm, and a sphere of radius {r_} cm, are "
                f"compared. The ratio of the cone's volume to the sphere's volume is:",
                f"{ratio.numerator} : {ratio.denominator}",
                [f"{ratio.denominator} : {ratio.numerator}", f"{h_} : {r_}", f"1 : 3"],
                f"Cone volume = ⅓πr²h = {vc} cm³ and sphere volume = (4/3)πr³ = {vs} cm³, so the ratio "
                f"reduces to {ratio.numerator} : {ratio.denominator}. It equals h : 4r, independent of π.",
                "Cancel the shared factors before computing. These ratio questions rarely need the actual volumes."))
        else:
            s = R.choice([14, 21, 28, 42])
            circ = Fraction(22, 7) * Fraction(s, 2) ** 2
            shaded = s * s - circ
            out.append(mk("Mensuration",
                f"A circle is inscribed in a square of side {s} cm. The area inside the square but "
                f"outside the circle is (π = 22/7):", f"{shaded} cm²",
                [f"{circ} cm²", f"{s*s} cm²", f"{shaded*2} cm²"],
                f"The inscribed circle has radius {Fraction(s,2)} cm and area {circ} cm². Subtracting from "
                f"the square's {s*s} cm² leaves {shaded} cm².",
                "Shaded-region questions are always a subtraction. Name the two areas before computing either."))
    return [x for x in out if x][:n]


def misc(n):
    """LOD III for the chapters the other families do not reach."""
    out = []
    for _ in range(n * 4):
        mode = R.choice(['pct_chain', 'ratio_three', 'interest_mix', 'coord_centroid',
                         'func_domain', 'sets_three', 'allig_two'])
        if mode == 'pct_chain':
            a, b, c = R.choice([10, 20, 25]), R.choice([10, 15, 20]), R.choice([10, 25, 50])
            net = (1 + a/100) * (1 - b/100) * (1 + c/100) - 1
            v = round(net * 100, 2)
            out.append(mk("Percentages",
                f"A quantity increases by {a}%, then falls by {b}%, then increases by {c}%. "
                f"The overall change is closest to:", f"{v}%",
                [f"{a-b+c}%", f"{round((a-b+c)/2,2)}%", f"{round(v+7.5,2)}%"],
                f"Multiply the factors: {1+a/100:.2f} × {1-b/100:.2f} × {1+c/100:.2f} = {1+net:.4f}, "
                f"an overall change of {v}%.",
                "Three successive changes still multiply. Never add them, however convenient it looks."))
        elif mode == 'ratio_three':
            a, b = R.choice([2, 3, 4]), R.choice([5, 6, 7])
            c, d = R.choice([3, 4, 5]), R.choice([7, 8, 9])
            A, B, C = a * c, b * c, b * d
            g = math.gcd(math.gcd(A, B), C)
            A, B, C = A // g, B // g, C // g
            out.append(mk("Ratio, Proportion & Variation",
                f"If A : B = {a} : {b} and B : C = {c} : {d}, then A : B : C is:",
                f"{A} : {B} : {C}",
                [f"{a} : {b} : {d}", f"{C} : {B} : {A}", f"{a*c} : {b*d} : {c*d}"],
                f"Scale both ratios so B agrees. A : B = {a*c} : {b*c} and B : C = {b*c} : {b*d}, "
                f"giving A : B : C = {A} : {B} : {C} after reduction.",
                "Make the shared term identical in both ratios before combining. Never multiply across directly."))
        elif mode == 'interest_mix':
            p_ = R.choice([8000, 12000, 16000, 20000])
            r_ = R.choice([10, 20])
            amt = p_ * (1 + r_ / 200) ** 2
            ci = amt - p_
            if abs(ci - round(ci)) > 0.01:
                continue
            si = p_ * r_ * 1 / 100
            out.append(mk("Simple & Compound Interest",
                f"Rs {p_} is invested for one year at {r_}% per annum compounded half-yearly. "
                f"By how much does the interest exceed simple interest at the same rate?",
                round(ci - si), [round(ci), round(si), round((ci - si) * 2)],
                f"Half-yearly compounding halves the rate to {r_/2}% and doubles the periods to 2. "
                f"Amount = {p_}(1 + {r_/2}/100)² = {round(amt)}, so CI = {round(ci)} against SI = {round(si)}, "
                f"a difference of {round(ci-si)}.",
                "Half-yearly compounding changes two things at once: halve the rate and double the periods."))
        elif mode == 'coord_centroid':
            pts = [(R.randrange(-8, 9), R.randrange(-8, 9)) for _ in range(3)]
            cx = Fraction(sum(p[0] for p in pts), 3)
            cy = Fraction(sum(p[1] for p in pts), 3)
            out.append(mk("Coordinate Geometry",
                f"The centroid of the triangle with vertices {pts[0]}, {pts[1]} and {pts[2]} is:",
                f"({cx}, {cy})",
                [f"({cy}, {cx})", f"({cx*3}, {cy*3})",
                 f"({Fraction(pts[0][0]+pts[1][0],2)}, {Fraction(pts[0][1]+pts[1][1],2)})"],
                f"The centroid averages the three vertices: ({cx}, {cy}).",
                "The centroid is the plain average of the vertices. The circumcentre and orthocentre are not."))
        elif mode == 'func_domain':
            a = R.choice([2, 3, 4, 5, 6, 7, 8, 9])
            out.append(mk("Functions",
                f"The domain of f(x) = √(x − {a}) / (x − {a + 2}) is:",
                f"x ≥ {a}, excluding x = {a+2}",
                [f"x > {a}", f"x ≥ {a}", f"x ≤ {a}, excluding x = {a+2}"],
                f"The square root needs x − {a} ≥ 0, so x ≥ {a}. The denominator vanishes at "
                f"x = {a+2}, which must be excluded.",
                "Impose every restriction separately, then intersect them. Square roots and denominators each impose one."))
        elif mode == 'sets_three':
            a_, b_, c_ = R.choice([60, 70, 80]), R.choice([45, 55, 65]), R.choice([35, 40, 50])
            ab, bc, ca = R.choice([20, 25]), R.choice([15, 18]), R.choice([12, 16])
            abc = R.choice([5, 8, 10])
            tot = a_ + b_ + c_ - ab - bc - ca + abc
            out.append(mk("Set Theory",
                f"In a survey, {a_} people read paper A, {b_} read B and {c_} read C. {ab} read both A and B, "
                f"{bc} read both B and C, {ca} read both C and A, and {abc} read all three. How many read "
                f"at least one paper?", tot,
                [a_ + b_ + c_, tot - abc, tot + abc],
                f"Inclusion-exclusion: {a_} + {b_} + {c_} − {ab} − {bc} − {ca} + {abc} = {tot}.",
                "The pairwise figures here already include the triple, so subtract the pairs once and add the triple back once."))
        else:
            c1, c2, c3 = R.choice([15, 18]), R.choice([24, 30]), R.choice([40, 48])
            q1, q2, q3 = R.choice([2, 3]), R.choice([3, 4]), R.choice([4, 5])
            cost = Fraction(c1*q1 + c2*q2 + c3*q3, q1 + q2 + q3)
            out.append(mk("Alligations",
                f"Three varieties costing Rs {c1}, Rs {c2} and Rs {c3} per kg are mixed in the ratio "
                f"{q1} : {q2} : {q3}. The cost of the mixture per kg is:", f"Rs {cost}",
                [f"Rs {Fraction(c1+c2+c3,3)}", f"Rs {c2}", f"Rs {Fraction(c1*q3+c2*q2+c3*q1, q1+q2+q3)}"],
                f"Weighted cost = ({q1}×{c1} + {q2}×{c2} + {q3}×{c3})/({q1}+{q2}+{q3}) = Rs {cost}.",
                "Three-way alligation is just a weighted average. Pair them up only if the question asks for a ratio."))
    return [x for x in out if x][:n]


PLAN = [(numbers, 45), (arithmetic, 55), (algebra, 50), (counting, 45), (geometry, 45), (misc, 110)]


def build():
    out, seen = [], set()
    for fn, cnt in PLAN:
        for rec in fn(cnt):
            if rec['question'] in seen:
                continue
            seen.add(rec['question'])
            out.append(rec)
    for i, r in enumerate(out, 1):
        r['id'] = f"ORIG-L3-{i:04d}"
    return out


if __name__ == '__main__':
    import collections
    qs = build()
    print("generated:", len(qs))
    print(dict(collections.Counter(q['topic'] for q in qs)))
