"""
Generates original CAT-level QA questions.

Every answer is COMPUTED, not authored, so correctness is structural rather
than a matter of trust. Distractors come from realistic error patterns
(wrong base in a percentage, forgetting to subtract, swapping rate and time)
so the options discriminate instead of padding.
"""
import random, math
from fractions import Fraction

R = random.Random(20261022)


def fmt(x):
    if isinstance(x, Fraction):
        if x.denominator == 1:
            return str(x.numerator)
        return f"{x.numerator}/{x.denominator}"
    if isinstance(x, float):
        if abs(x - round(x)) < 1e-9:
            return str(int(round(x)))
        return f"{x:.2f}".rstrip('0').rstrip('.')
    return str(x)


_seq = {'n': 0}


def mk(topic, difficulty, question, correct, wrongs, explanation, how, stimulus=""):
    """Build one record. Returns None if distractors collapse onto the answer."""
    c = fmt(correct)
    seen = {c}
    opts = []
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
    return {
        "id": f"ORIG-QA-{_seq['n']:04d}",
        "section": "QA",
        "type": "MCQ",
        "topic": topic,
        "difficulty": difficulty,
        "sourceType": "ORIGINAL",
        "sourceLabel": "Original CAT-level practice (computed answer)",
        "sourceUrl": "",
        "year": None,
        "slot": None,
        "title": f"QA · {topic}",
        "stimulus": stimulus,
        "question": question,
        "options": opts,
        "answer": opts.index(c),
        "answerText": c,
        "explanation": explanation,
        "howToThink": how,
        "explanationStatus": "FULL",
    }


# ---------------------------------------------------------------- percentages
def gen_percentages(n):
    out = []
    for _ in range(n * 3):
        mode = R.choice(['successive', 'reverse', 'compare', 'expenditure'])
        if mode == 'successive':
            a, b = R.choice([10, 15, 20, 25, 30, 40]), R.choice([10, 20, 25, 30, 50])
            sign = R.choice([1, -1])
            net = (1 + a / 100) * (1 + sign * b / 100) - 1
            pct = round(net * 100, 2)
            op = 'increased' if sign == 1 else 'decreased'
            q = (f"The price of a commodity is first increased by {a}% and then {op} by {b}%. "
                 f"The net change in the price is closest to:")
            w = [round(a + sign * b, 2), round(sign * b - a, 2), round(abs(a - b), 2)]
            e = (f"Net multiplier = {1 + a/100:.2f} × {1 + sign*b/100:.2f} = {1+net:.4f}, "
                 f"so the net change is {pct}%.")
            h = "Percentage changes multiply, they do not add. Convert each change into a multiplier first."
            out.append(mk("Percentages", "Easy", q, f"{pct}%", [f"{x}%" for x in w], e, h))
        elif mode == 'reverse':
            p = R.choice([12, 15, 20, 25, 35, 40])
            final = R.choice([552, 690, 828, 920, 1035, 1150])
            orig = Fraction(final * 100, 100 + p)
            if orig.denominator != 1:
                continue
            orig = orig.numerator
            q = (f"After an increase of {p}%, a quantity becomes {final}. What was the original value?")
            w = [round(final * (100 - p) / 100), final - p, round(final / (1 - p / 100))]
            e = f"Original × (1 + {p}/100) = {final}, so original = {final} × 100/{100+p} = {orig}."
            h = "Work backward with a multiplier. Never subtract the same percentage to undo an increase."
            out.append(mk("Percentages", "Easy", q, orig, w, e, h))
        elif mode == 'compare':
            x, y = R.choice([40, 50, 60, 75, 80]), R.choice([120, 150, 160, 200, 240])
            if x >= y:
                continue
            more = round((y - x) * 100 / x, 2)
            less = round((y - x) * 100 / y, 2)
            q = f"If A = {x} and B = {y}, then B is what percentage more than A?"
            e = f"Difference = {y-x}. Taking A as the base, ({y-x})/{x} × 100 = {more}%."
            h = "'More than A' fixes A as the base. Changing the base is the single most common slip here."
            out.append(mk("Percentages", "Easy", q, f"{more}%",
                          [f"{less}%", f"{round((y-x)*100/(x+y),2)}%", f"{y-x}%"], e, h))
        else:
            inc = R.choice([10, 20, 25, 30])
            cut = R.choice([8, 10, 12, 15, 16])
            net = round(((1 + inc / 100) * (1 - cut / 100) - 1) * 100, 2)
            q = (f"The price of rice rises by {inc}%. A family reduces its consumption by {cut}%. "
                 f"The change in the family's expenditure on rice is closest to:")
            e = (f"Expenditure = price × consumption = {1+inc/100:.2f} × {1-cut/100:.2f} = "
                 f"{(1+inc/100)*(1-cut/100):.4f}, a change of {net}%.")
            h = "Expenditure is a product of two quantities, so combine the two multipliers."
            out.append(mk("Percentages", "Medium", q, f"{net}%",
                          [f"{inc-cut}%", f"{cut-inc}%", f"{round(inc*cut/100,2)}%"], e, h))
    return [x for x in out if x][:n]


# -------------------------------------------------------------- profit & loss
def gen_profit_loss(n):
    out = []
    for _ in range(n * 3):
        mode = R.choice(['basic', 'discount', 'dishonest', 'twoarticles'])
        if mode == 'basic':
            cp = R.choice(range(100, 1801, 20))
            p = R.choice([12, 15, 20, 25, 30, 40])
            sp = cp * (100 + p) // 100
            if cp * (100 + p) % 100:
                continue
            q = f"An article costing Rs {cp} is sold at a profit of {p}%. The selling price is:"
            e = f"SP = {cp} × (100 + {p})/100 = Rs {sp}."
            h = "Profit percentage is always on cost price unless the question says otherwise."
            out.append(mk("Profit & Loss", "Easy", q, sp, [cp + p, cp * (100 - p) // 100, sp + cp // 10], e, h))
        elif mode == 'discount':
            mp = R.choice([800, 1000, 1200, 1500, 2000])
            d = R.choice([10, 15, 20, 25])
            p = R.choice([8, 12, 20, 25])
            sp = mp * (100 - d) / 100
            cp = sp * 100 / (100 + p)
            if abs(cp - round(cp)) > 1e-9:
                continue
            cp = int(round(cp))
            q = (f"A shopkeeper marks an item at Rs {mp}, allows a discount of {d}% and still earns a "
                 f"profit of {p}%. The cost price is:")
            e = (f"SP = {mp} × {100-d}/100 = Rs {int(sp)}. CP = SP × 100/(100+{p}) = "
                 f"{int(sp)} × 100/{100+p} = Rs {cp}.")
            h = "Go marked price → selling price → cost price. Discount sits on MP, profit sits on CP."
            out.append(mk("Profit & Loss", "Medium", q, cp, [int(sp), mp - d * 10, int(sp * (100 - p) / 100)], e, h))
        elif mode == 'dishonest':
            g = R.choice([10, 20, 25])
            gain = round(g * 100 / (100 - g), 2)
            q = (f"A trader sells goods at cost price but uses a weight that is {g}% less than the "
                 f"stated weight. His actual profit percentage is:")
            e = (f"He gives {100-g} g for every 100 g charged. Profit% = {g}/{100-g} × 100 = {gain}%.")
            h = "The gain sits on what he actually gives away, so the shortfall is the denominator."
            out.append(mk("Profit & Loss", "Hard", q, f"{gain}%", [f"{g}%", f"{round(100*g/(100+g),2)}%", f"{g*2}%"], e, h))
        else:
            price = R.choice([840, 960, 1200, 1800])
            p = R.choice([20, 25, 30])
            cp1 = price * 100 / (100 + p)
            cp2 = price * 100 / (100 - p)
            net = round((2 * price - cp1 - cp2) / (cp1 + cp2) * 100, 2)
            q = (f"Two articles are each sold for Rs {price}. One is sold at a profit of {p}% and the "
                 f"other at a loss of {p}%. The net result of the transaction is:")
            e = (f"CP of the first = {cp1:.2f}, CP of the second = {cp2:.2f}. Total CP = {cp1+cp2:.2f} "
                 f"against total SP = {2*price}, a net loss of {abs(net)}%.")
            h = f"Equal SP with equal profit and loss percentages always gives a loss of (x²/100)% = {round(p*p/100,2)}%."
            out.append(mk("Profit & Loss", "Medium", q, f"Loss of {abs(net)}%",
                          ["No profit, no loss", f"Profit of {abs(net)}%", f"Loss of {p}%"], e, h))
    return [x for x in out if x][:n]


# ------------------------------------------------------------------- interest
def gen_interest(n):
    out = []
    for _ in range(n * 3):
        mode = R.choice(['si', 'ci', 'diff', 'double'])
        p = R.choice(range(4000, 40001, 1000))
        r = R.choice([5, 8, 10, 12, 15, 20])
        t = R.choice([2, 3])
        if mode == 'si':
            si = p * r * t / 100
            q = f"The simple interest on Rs {p} at {r}% per annum for {t} years is:"
            e = f"SI = P×R×T/100 = {p}×{r}×{t}/100 = Rs {int(si)}."
            h = "Simple interest stays on the original principal every year."
            out.append(mk("Simple & Compound Interest", "Easy", q, int(si),
                          [int(p * ((1 + r / 100) ** t - 1)), int(si / t), int(si * 2)], e, h))
        elif mode == 'ci':
            amt = p * (1 + r / 100) ** t
            ci = amt - p
            if abs(ci - round(ci)) > 0.01:
                continue
            q = f"The compound interest on Rs {p} at {r}% per annum, compounded annually for {t} years, is:"
            e = f"Amount = {p}(1 + {r}/100)^{t} = Rs {round(amt)}. CI = {round(amt)} − {p} = Rs {round(ci)}."
            h = "Compute the amount first, then subtract the principal. Do not add yearly interest."
            out.append(mk("Simple & Compound Interest", "Medium", q, round(ci),
                          [int(p * r * t / 100), round(amt), round(ci / t)], e, h))
        elif mode == 'diff':
            d = p * (r / 100) ** 2
            if abs(d - round(d)) > 0.01:
                continue
            q = (f"The difference between compound interest and simple interest on Rs {p} at {r}% per "
                 f"annum for 2 years is:")
            e = f"For 2 years the difference is P(R/100)² = {p} × ({r}/100)² = Rs {round(d)}."
            h = "For two years the gap is exactly the interest earned on the first year's interest."
            out.append(mk("Simple & Compound Interest", "Medium", q, round(d),
                          [round(d * 2), round(p * r / 100), round(d / 2)], e, h))
        else:
            yrs = R.choice([4, 5, 8, 10])
            rate = round(100 / yrs, 2)
            q = (f"A sum of money doubles itself in {yrs} years under simple interest. "
                 f"The rate of interest per annum is:")
            e = f"To double, SI must equal P. So P = P×R×{yrs}/100, giving R = 100/{yrs} = {rate}%."
            h = "Doubling means the interest earned equals the principal itself."
            out.append(mk("Simple & Compound Interest", "Easy", q, f"{rate}%",
                          [f"{round(200/yrs,2)}%", f"{yrs}%", f"{round(100/(yrs*2),2)}%"], e, h))
    return [x for x in out if x][:n]


# ------------------------------------------------------------------ time work
def gen_time_work(n):
    out = []
    for _ in range(n * 4):
        mode = R.choice(['together', 'third', 'pipes', 'leave'])
        a, b = R.sample([4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 30], 2)
        if mode == 'together':
            t = Fraction(a * b, a + b)
            q = (f"A can finish a piece of work in {a} days and B in {b} days. Working together, "
                 f"they will finish it in:")
            e = (f"One day's work = 1/{a} + 1/{b} = {Fraction(1,a)+Fraction(1,b)}. "
                 f"Time = {t} days.")
            h = "Add rates, not days. The reciprocal of the combined rate gives the time."
            out.append(mk("Time & Work", "Easy", q, f"{t} days",
                          [f"{a+b} days", f"{Fraction(a+b,2)} days", f"{abs(a-b)} days"], e, h))
        elif mode == 'third':
            c = R.choice([12, 15, 20, 24, 30])
            rate = Fraction(1, a) + Fraction(1, b) + Fraction(1, c)
            t = 1 / rate
            q = (f"A, B and C can complete a task alone in {a}, {b} and {c} days respectively. "
                 f"Working together they finish it in:")
            e = f"Combined rate = 1/{a} + 1/{b} + 1/{c} = {rate}. Time = {t} days."
            h = "Use a common total of work, often the LCM of the individual times, to avoid fractions."
            out.append(mk("Time & Work", "Medium", q, f"{t} days",
                          [f"{Fraction(a+b+c,3)} days", f"{a+b+c} days", f"{Fraction(a*b,a+b)} days"], e, h))
        elif mode == 'pipes':
            fill, empty = R.choice([6, 8, 10, 12]), R.choice([15, 18, 20, 24, 30])
            if fill >= empty:
                continue
            rate = Fraction(1, fill) - Fraction(1, empty)
            t = 1 / rate
            q = (f"A pipe fills a tank in {fill} hours while an outlet empties it in {empty} hours. "
                 f"If both are opened together, the tank fills in:")
            e = f"Net rate = 1/{fill} − 1/{empty} = {rate} per hour, so the tank fills in {t} hours."
            h = "An outlet is a negative rate. Subtract it, then invert."
            out.append(mk("Time & Work", "Medium", q, f"{t} hours",
                          [f"{Fraction(fill*empty, fill+empty)} hours", f"{empty-fill} hours", f"{fill+empty} hours"], e, h))
        else:
            days = R.choice([2, 3, 4])
            rate_a, rate_b = Fraction(1, a), Fraction(1, b)
            done = (rate_a + rate_b) * days
            if done >= 1:
                continue
            rem = (1 - done) / rate_b
            q = (f"A and B can do a job alone in {a} and {b} days respectively. They work together for "
                 f"{days} days, after which A leaves. B alone will need how many more days to finish?")
            e = (f"Work done in {days} days = {days}(1/{a} + 1/{b}) = {done}. "
                 f"Remaining = {1-done}, and B needs {1-done} ÷ 1/{b} = {rem} days.")
            h = "Track the fraction of work completed, then divide the remainder by the remaining worker's rate."
            out.append(mk("Time & Work", "Hard", q, f"{rem} days",
                          [f"{b-days} days", f"{Fraction(b,2)} days", f"{done*b} days"], e, h))
    return [x for x in out if x][:n]


# ------------------------------------------------------------------ speed dist
def gen_tsd(n):
    out = []
    for _ in range(n * 4):
        mode = R.choice(['average', 'boat', 'train', 'relative'])
        if mode == 'average':
            s1, s2 = R.sample([20, 30, 40, 45, 50, 60, 72, 80], 2)
            avg = Fraction(2 * s1 * s2, s1 + s2)
            q = (f"A car covers a distance at {s1} km/h and returns along the same route at {s2} km/h. "
                 f"Its average speed for the whole journey is:")
            e = (f"For equal distances the average is the harmonic mean: 2×{s1}×{s2}/({s1}+{s2}) "
                 f"= {avg} km/h.")
            h = "Equal distances need the harmonic mean. The arithmetic mean is the trap option."
            out.append(mk("Time, Speed & Distance", "Medium", q, f"{avg} km/h",
                          [f"{Fraction(s1+s2,2)} km/h", f"{s1+s2} km/h", f"{abs(s1-s2)} km/h"], e, h))
        elif mode == 'boat':
            b, s = R.choice([10, 12, 15, 18, 20]), R.choice([2, 3, 4, 5])
            if s >= b:
                continue
            d = R.choice([24, 36, 48, 60])
            t = Fraction(d, b + s) + Fraction(d, b - s)
            q = (f"A boat whose speed in still water is {b} km/h travels {d} km downstream and returns. "
                 f"If the stream flows at {s} km/h, the total time taken is:")
            e = (f"Downstream speed = {b+s}, upstream = {b-s}. Time = {d}/{b+s} + {d}/{b-s} = {t} hours.")
            h = "Downstream adds the current, upstream subtracts it. Time is never symmetric."
            out.append(mk("Time, Speed & Distance", "Hard", q, f"{t} hours",
                          [f"{Fraction(2*d,b)} hours", f"{Fraction(d,b)} hours", f"{Fraction(2*d,b+s)} hours"], e, h))
        elif mode == 'train':
            L = R.choice([120, 150, 180, 200, 240])
            sp = R.choice([36, 45, 54, 72, 90])
            plat = R.choice([100, 180, 250, 300])
            t = Fraction((L + plat) * 18, sp * 5)
            q = (f"A train {L} m long running at {sp} km/h crosses a platform {plat} m long in:")
            e = (f"Total distance = {L} + {plat} = {L+plat} m. Speed = {sp} × 5/18 = {Fraction(sp*5,18)} m/s. "
                 f"Time = {t} seconds.")
            h = "Crossing a platform means the train covers its own length plus the platform."
            out.append(mk("Time, Speed & Distance", "Easy", q, f"{t} seconds",
                          [f"{Fraction(L*18,sp*5)} seconds", f"{Fraction(plat*18,sp*5)} seconds",
                           f"{Fraction((L+plat)*5,sp*18)} seconds"], e, h))
        else:
            u, v = R.choice([40, 50, 60]), R.choice([70, 80, 90, 100])
            gap = R.choice([60, 90, 120, 150])
            t = Fraction(gap, v - u)
            q = (f"Two cars start from the same point in the same direction, one at {u} km/h and the "
                 f"other at {v} km/h. If the slower car starts {gap} km ahead, the faster car catches "
                 f"up in:")
            e = f"Relative speed = {v} − {u} = {v-u} km/h. Time = {gap}/{v-u} = {t} hours."
            h = "Same direction subtracts speeds, opposite directions adds them."
            out.append(mk("Time, Speed & Distance", "Easy", q, f"{t} hours",
                          [f"{Fraction(gap,v+u)} hours", f"{Fraction(gap,v)} hours", f"{Fraction(gap,u)} hours"], e, h))
    return [x for x in out if x][:n]


# ------------------------------------------------------------ averages/mixture
def gen_averages(n):
    out = []
    for _ in range(n * 3):
        mode = R.choice(['replace', 'alligation', 'newavg', 'weighted'])
        if mode == 'replace':
            k = R.choice([8, 10, 12, 15])
            old_avg = R.choice([30, 35, 40, 45])
            inc = R.choice([2, 3, 4, 5])
            leaving = R.choice([20, 25, 28])
            new_person = leaving + k * inc
            q = (f"The average age of {k} people is {old_avg} years. When a person aged {leaving} is "
                 f"replaced by a new person, the average rises by {inc} years. The new person's age is:")
            e = (f"Total rises by {k} × {inc} = {k*inc} years, so the new person is "
                 f"{leaving} + {k*inc} = {new_person} years old.")
            h = "A replacement changes the total by exactly (count × change in average)."
            out.append(mk("Averages and Mixtures", "Medium", q, new_person,
                          [leaving + inc, old_avg + inc, k * inc], e, h))
        elif mode == 'alligation':
            c1, c2 = R.choice([20, 24, 30]), R.choice([40, 45, 50, 60])
            if c1 >= c2:
                continue
            mean = R.choice([x for x in range(c1 + 2, c2, 2)])
            ratio = Fraction(c2 - mean, mean - c1)
            q = (f"In what ratio must tea costing Rs {c1}/kg be mixed with tea costing Rs {c2}/kg so "
                 f"that the mixture costs Rs {mean}/kg?")
            e = (f"By alligation, ratio = ({c2} − {mean}) : ({mean} − {c1}) = {c2-mean} : {mean-c1} "
                 f"= {ratio.numerator} : {ratio.denominator}.")
            h = "Alligation gives the ratio as the cross differences from the mean price."
            out.append(mk("Averages and Mixtures", "Medium", q,
                          f"{ratio.numerator} : {ratio.denominator}",
                          [f"{ratio.denominator} : {ratio.numerator}", f"{c1} : {c2}", f"{mean-c1} : {c2}"], e, h))
        elif mode == 'newavg':
            k = R.choice([10, 12, 15, 20])
            avg = R.choice([40, 50, 60])
            extra = R.choice([65, 72, 80, 95])
            new = Fraction(k * avg + extra, k + 1)
            q = (f"The average of {k} numbers is {avg}. If a new number {extra} is included, the "
                 f"new average becomes:")
            e = f"New average = ({k}×{avg} + {extra})/{k+1} = {k*avg+extra}/{k+1} = {new}."
            h = "Rebuild the total, then divide by the new count."
            out.append(mk("Averages and Mixtures", "Easy", q, f"{new}",
                          [f"{Fraction(avg+extra,2)}", f"{avg}", f"{Fraction(k*avg+extra,k)}"], e, h))
        else:
            n1, n2 = R.choice([12, 15, 20]), R.choice([25, 30, 36])
            a1, a2 = R.choice([60, 65, 70]), R.choice([40, 45, 50])
            w = Fraction(n1 * a1 + n2 * a2, n1 + n2)
            q = (f"A class of {n1} boys averages {a1} marks and a class of {n2} girls averages {a2} "
                 f"marks. The combined average is:")
            e = (f"Combined = ({n1}×{a1} + {n2}×{a2})/({n1}+{n2}) = {n1*a1+n2*a2}/{n1+n2} = {w}.")
            h = "Weight each average by its group size. The plain midpoint is the trap."
            out.append(mk("Averages and Mixtures", "Easy", q, f"{w}",
                          [f"{Fraction(a1+a2,2)}", f"{a1}", f"{a2}"], e, h))
    return [x for x in out if x][:n]


# ----------------------------------------------------------- ratio/proportion
def gen_ratio(n):
    out = []
    for _ in range(n * 3):
        mode = R.choice(['divide', 'partnership', 'change'])
        if mode == 'divide':
            a, b, c = R.sample([2, 3, 4, 5, 6, 7, 8, 9], 3)
            total = (a + b + c) * R.choice([12, 15, 20, 24, 30])
            share = total * b // (a + b + c)
            q = (f"Rs {total} is divided among X, Y and Z in the ratio {a} : {b} : {c}. "
                 f"Y's share is:")
            e = f"Total parts = {a+b+c}. Y gets {b}/{a+b+c} × {total} = Rs {share}."
            h = "Convert the ratio to parts, value one part, then scale."
            out.append(mk("Ratio, Proportion & Variation", "Easy", q, share,
                          [total * a // (a + b + c), total * c // (a + b + c), total // 3], e, h))
        elif mode == 'partnership':
            ca, cb = R.choice([12000, 15000, 20000]), R.choice([18000, 24000, 30000])
            ma, mb = R.choice([12, 8, 6]), R.choice([12, 9, 6])
            profit = R.choice([12000, 18000, 24000, 30000])
            wa, wb = ca * ma, cb * mb
            sa = Fraction(profit * wa, wa + wb)
            q = (f"A invests Rs {ca} for {ma} months and B invests Rs {cb} for {mb} months. "
                 f"If the total profit is Rs {profit}, A's share is:")
            e = (f"Capital-months: A = {ca}×{ma} = {wa}, B = {cb}×{mb} = {wb}. "
                 f"A's share = {wa}/({wa}+{wb}) × {profit} = Rs {sa}.")
            h = "Profit follows capital multiplied by time invested, not capital alone."
            out.append(mk("Ratio, Proportion & Variation", "Medium", q, f"{sa}",
                          [f"{Fraction(profit*ca, ca+cb)}", f"{profit//2}", f"{Fraction(profit*wb, wa+wb)}"], e, h))
        else:
            a, b = R.choice([3, 4, 5]), R.choice([7, 8, 9, 11])
            add = R.choice([6, 8, 10, 12])
            na, nb = R.choice([2, 3]), R.choice([3, 4, 5])
            # (ax + add)/(bx + add) = na/nb  ->  x
            denom = (a * nb - b * na)
            if denom == 0:
                continue
            x = Fraction(add * (na - nb), denom)
            if x <= 0 or x.denominator != 1:
                continue
            x = x.numerator
            q = (f"Two numbers are in the ratio {a} : {b}. If {add} is added to each, the ratio becomes "
                 f"{na} : {nb}. The smaller number is:")
            e = (f"Let the numbers be {a}x and {b}x. Then ({a}x+{add})/({b}x+{add}) = {na}/{nb}, "
                 f"giving x = {x}. The smaller number is {a}×{x} = {a*x}.")
            h = "Introduce the common multiplier x, then cross-multiply once."
            out.append(mk("Ratio, Proportion & Variation", "Medium", q, a * x,
                          [b * x, a * x + add, x], e, h))
    return [x for x in out if x][:n]


# ------------------------------------------------------------- number systems
def gen_numbers(n):
    out = []
    for _ in range(n * 4):
        mode = R.choice(['lastdigit', 'remainder', 'factors', 'hcflcm', 'trailingzeros'])
        if mode == 'lastdigit':
            base = R.choice([2, 3, 4, 7, 8, 9, 12, 13, 17])
            p = R.choice([25, 33, 47, 58, 64, 81, 99, 123])
            d = pow(base, p, 10)
            q = f"The units digit of {base}^{p} is:"
            e = (f"The units digit of powers of {base} repeats in a cycle of length "
                 f"{len(set(pow(base,k,10) for k in range(1,5)))}. "
                 f"Reducing the exponent within that cycle gives {d}.")
            h = "Units digits cycle with period 1, 2 or 4. Reduce the exponent modulo the cycle length."
            out.append(mk("Number Systems", "Medium", q, d, [(d + 1) % 10, (d + 3) % 10, (d + 7) % 10], e, h))
        elif mode == 'remainder':
            a = R.choice([17, 23, 29, 31, 37])
            p = R.choice([15, 21, 28, 35])
            m = R.choice([7, 9, 11, 13])
            rem = pow(a, p, m)
            q = f"What is the remainder when {a}^{p} is divided by {m}?"
            e = (f"Reduce the base first: {a} ≡ {a%m} (mod {m}). Then {a%m}^{p} mod {m} = {rem}.")
            h = "Reduce the base modulo the divisor before touching the exponent, then look for a cycle."
            out.append(mk("Number Systems", "Hard", q, rem, [(rem + 1) % m, (rem + 2) % m, (rem + m - 1) % m], e, h))
        elif mode == 'factors':
            x = R.choice([360, 420, 540, 600, 720, 840, 900, 1080, 1200])
            cnt, t, d = 1, x, 2
            fac = []
            while d * d <= t:
                if t % d == 0:
                    e_ = 0
                    while t % d == 0:
                        t //= d
                        e_ += 1
                    fac.append((d, e_))
                    cnt *= (e_ + 1)
                d += 1
            if t > 1:
                fac.append((t, 1))
                cnt *= 2
            fs = " × ".join(f"{p}^{k}" for p, k in fac)
            q = f"How many factors does {x} have?"
            e = f"{x} = {fs}. The number of factors is the product of (exponent + 1), which gives {cnt}."
            h = "Prime factorise, add one to each exponent, multiply."
            out.append(mk("Number Systems", "Medium", q, cnt, [cnt + 2, cnt - 2, cnt * 2], e, h))
        elif mode == 'hcflcm':
            a, b = R.choice([24, 36, 48, 60, 72]), R.choice([90, 108, 120, 144, 180])
            g = math.gcd(a, b)
            l = a * b // g
            q = f"The LCM of {a} and {b} is:"
            e = f"HCF({a}, {b}) = {g}, and LCM = product/HCF = {a}×{b}/{g} = {l}."
            h = "HCF × LCM = product of the two numbers. Use it to avoid listing multiples."
            out.append(mk("Number Systems", "Easy", q, l, [g, a * b, l // 2], e, h))
        else:
            k = R.choice([15, 20, 25, 30, 40, 50])
            z, p5 = 0, 5
            while p5 <= k:
                z += k // p5
                p5 *= 5
            q = f"The number of trailing zeros in {k}! is:"
            e = (f"Count the factors of 5: " + " + ".join(f"[{k}/{5**i}]" for i in range(1, 4) if 5**i <= k)
                 + f" = {z}.")
            h = "Trailing zeros are governed by the number of 5s, since 2s are always in surplus."
            out.append(mk("Number Systems", "Medium", q, z, [z + 1, z - 1, k // 5], e, h))
    return [x for x in out if x][:n]


# --------------------------------------------------------------- algebra
def gen_algebra(n):
    out = []
    for _ in range(n * 4):
        mode = R.choice(['quadroots', 'sumprod', 'linear', 'surd'])
        if mode == 'quadroots':
            r1, r2 = R.sample([-6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7], 2)
            b, c = -(r1 + r2), r1 * r2
            sgn = lambda v: f"+ {v}" if v >= 0 else f"- {abs(v)}"
            q = f"The roots of x² {sgn(b)}x {sgn(c)} = 0 are:"
            e = f"Factorising, (x − {r1})(x − {r2}) = 0, so the roots are {r1} and {r2}."
            h = "Look for two numbers whose sum is −b and whose product is c before using the formula."
            out.append(mk("Equations", "Easy", q, f"{r1} and {r2}",
                          [f"{-r1} and {-r2}", f"{r1} and {-r2}", f"{r1+1} and {r2-1}"], e, h))
        elif mode == 'sumprod':
            a = R.choice([1, 2, 3])
            b = R.choice([-12, -10, -8, 6, 9, 14])
            c = R.choice([-15, -8, 6, 12, 20])
            s = Fraction(-b, a)
            p = Fraction(c, a)
            val = s * s - 2 * p
            q = (f"If α and β are the roots of {a}x² + ({b})x + ({c}) = 0, then α² + β² equals:")
            e = (f"α + β = {-b}/{a} = {s} and αβ = {c}/{a} = {p}. "
                 f"α² + β² = (α+β)² − 2αβ = {s}² − 2({p}) = {val}.")
            h = "Convert to sum and product of roots. Almost every symmetric expression reduces to those two."
            out.append(mk("Equations", "Medium", q, f"{val}",
                          [f"{s*s}", f"{s*s + 2*p}", f"{p*p}"], e, h))
        elif mode == 'linear':
            x0, y0 = R.choice([2, 3, 4, 5, 6]), R.choice([1, 2, 3, 4, 7])
            a1, b1 = R.choice([2, 3, 5]), R.choice([1, 2, 4])
            a2, b2 = R.choice([1, 4, 7]), R.choice([3, 5, 6])
            if a1 * b2 - a2 * b1 == 0:
                continue
            c1, c2 = a1 * x0 + b1 * y0, a2 * x0 + b2 * y0
            q = f"Solve for x: {a1}x + {b1}y = {c1} and {a2}x + {b2}y = {c2}."
            e = (f"Eliminating y gives x = {x0} (and y = {y0}). Substituting back satisfies both equations.")
            h = "Eliminate the variable with the easier coefficient match rather than substituting blindly."
            out.append(mk("Equations", "Easy", q, x0, [y0, x0 + y0, x0 * 2], e, h))
        else:
            k = R.choice([2, 3, 5, 6, 7, 8, 10])
            a = R.choice([2, 3, 4])
            val = a ** k
            q = f"If log₍{a}₎ N = {k}, then N equals:"
            e = f"log₍{a}₎ N = {k} means N = {a}^{k} = {val}."
            h = "A logarithm is just an exponent. Rewrite it in exponential form immediately."
            out.append(mk("Logarithms & Indices", "Easy", q, val, [a * k, k ** a, val // a], e, h))
    return [x for x in out if x][:n]


# -------------------------------------------------------------- progressions
def gen_progressions(n):
    out = []
    for _ in range(n * 3):
        mode = R.choice(['apterm', 'apsum', 'gpsum', 'gpterm'])
        if mode == 'apterm':
            a, d = R.choice([3, 5, 7, 11]), R.choice([2, 3, 4, 6])
            k = R.choice([12, 15, 20, 25, 30])
            t = a + (k - 1) * d
            q = f"The {k}th term of the arithmetic progression {a}, {a+d}, {a+2*d}, ... is:"
            e = f"Tₙ = a + (n−1)d = {a} + {k-1}×{d} = {t}."
            h = "Use (n − 1), not n. Off-by-one is the standard error in AP terms."
            out.append(mk("Progressions", "Easy", q, t, [a + k * d, t - d, a * k], e, h))
        elif mode == 'apsum':
            a, d = R.choice([2, 4, 5, 6]), R.choice([3, 4, 5, 7])
            k = R.choice([10, 12, 15, 18, 20])
            s = k * (2 * a + (k - 1) * d) // 2
            q = f"The sum of the first {k} terms of the AP with first term {a} and common difference {d} is:"
            e = f"Sₙ = n/2 [2a + (n−1)d] = {k}/2 [2×{a} + {k-1}×{d}] = {s}."
            h = "Either average the first and last terms, or use the standard sum formula."
            out.append(mk("Progressions", "Hard", q, s, [s + d * k, k * a, s // 2], e, h))
        elif mode == 'gpsum':
            a, r = R.choice([2, 3, 5]), R.choice([2, 3])
            k = R.choice([5, 6, 7, 8])
            s = a * (r ** k - 1) // (r - 1)
            q = f"The sum of the first {k} terms of the GP {a}, {a*r}, {a*r*r}, ... is:"
            e = f"Sₙ = a(rⁿ − 1)/(r − 1) = {a}({r}^{k} − 1)/({r} − 1) = {s}."
            h = "Check the ratio is constant before applying the GP sum formula."
            out.append(mk("Progressions", "Medium", q, s, [a * r ** k, s - a, s + a], e, h))
        else:
            a, r = R.choice([3, 4, 6]), R.choice([2, 3])
            k = R.choice([6, 7, 8])
            t = a * r ** (k - 1)
            q = f"The {k}th term of the geometric progression {a}, {a*r}, {a*r*r}, ... is:"
            e = f"Tₙ = ar^(n−1) = {a}×{r}^{k-1} = {t}."
            h = "The exponent is (n − 1), matching the number of steps taken from the first term."
            out.append(mk("Progressions", "Easy", q, t, [a * r ** k, t // r, a * r * k], e, h))
    return [x for x in out if x][:n]


# ------------------------------------------------------------------ geometry
def gen_geometry(n):
    out = []
    triples = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (9, 40, 41), (20, 21, 29)]
    for _ in range(n * 4):
        mode = R.choice(['pythagoras', 'triarea', 'circle', 'coord', 'similar', 'polygon'])
        if mode == 'pythagoras':
            a, b, c = R.choice(triples)
            k = R.choice([1, 2, 3])
            a, b, c = a * k, b * k, c * k
            q = f"In a right-angled triangle the legs measure {a} cm and {b} cm. The hypotenuse is:"
            e = f"Hypotenuse = √({a}² + {b}²) = √{a*a+b*b} = {c} cm."
            h = "Recognise the standard triples. They appear far more often than the formula is needed."
            out.append(mk("Geometry", "Easy", q, f"{c} cm", [f"{a+b} cm", f"{c-1} cm", f"{(a+b)//2} cm"], e, h))
        elif mode == 'triarea':
            b_, h_ = R.choice(range(6, 41, 2)), R.choice(range(5, 31))
            ar = Fraction(b_ * h_, 2)
            q = f"A triangle has base {b_} cm and height {h_} cm. Its area is:"
            e = f"Area = ½ × base × height = ½ × {b_} × {h_} = {ar} cm²."
            h = "Height must be perpendicular to the base chosen."
            out.append(mk("Geometry", "Easy", q, f"{ar} cm²",
                          [f"{b_*h_} cm²", f"{b_+h_} cm²", f"{Fraction(b_*h_,3)} cm²"], e, h))
        elif mode == 'circle':
            r = R.choice([7, 14, 21, 28, 35, 42, 49, 56, 70])
            sub = R.choice(['area', 'circum', 'sector'])
            if sub == 'area':
                ar = Fraction(22, 7) * r * r
                q = f"The area of a circle of radius {r} cm is (take π = 22/7):"
                e = f"Area = πr² = 22/7 × {r}² = {ar} cm²."
                h = "Radii that are multiples of 7 are a signal to use 22/7."
                out.append(mk("Geometry", "Easy", q, f"{ar} cm²",
                              [f"{Fraction(44,7)*r} cm²", f"{ar*2} cm²", f"{Fraction(22,7)*r} cm²"], e, h))
            elif sub == 'circum':
                ci = Fraction(44, 7) * r
                q = f"The circumference of a circle of radius {r} cm is (take π = 22/7):"
                e = f"Circumference = 2πr = 2 × 22/7 × {r} = {ci} cm."
                h = "Circumference is linear in r, area is quadratic. Check which the question wants."
                out.append(mk("Geometry", "Easy", q, f"{ci} cm",
                              [f"{Fraction(22,7)*r*r} cm", f"{ci/2} cm", f"{ci*2} cm"], e, h))
            else:
                ang = R.choice([60, 90, 120, 180])
                ar = Fraction(22, 7) * r * r * Fraction(ang, 360)
                q = f"A sector of a circle of radius {r} cm subtends {ang}° at the centre. Its area is (π = 22/7):"
                e = f"Sector area = (θ/360) × πr² = ({ang}/360) × 22/7 × {r}² = {ar} cm²."
                h = "A sector is a simple fraction θ/360 of the full circle."
                out.append(mk("Geometry", "Medium", q, f"{ar} cm²",
                              [f"{Fraction(22,7)*r*r} cm²", f"{ar*2} cm²", f"{Fraction(44,7)*r*Fraction(ang,360)} cm²"], e, h))
        elif mode == 'coord':
            x1, y1 = R.choice(range(-9, 10)), R.choice(range(-9, 10))
            dx, dy = R.choice([(3,4),(6,8),(9,12),(12,16),(5,12),(10,24),(8,15),(16,30),(7,24),(20,21),(9,40)])
            x2, y2 = x1 + dx, y1 + dy
            d = int(math.hypot(dx, dy))
            q = f"The distance between the points ({x1}, {y1}) and ({x2}, {y2}) is:"
            e = f"Distance = √(({x2}−{x1})² + ({y2}−{y1})²) = √({dx}² + {dy}²) = {d}."
            h = "Differences first, square, then add. Sign errors vanish once you square."
            out.append(mk("Coordinate Geometry", "Easy", q, d, [dx + dy, d + 1, abs(dx - dy)], e, h))
        elif mode == 'similar':
            k = R.choice([2, 3, 4])
            a1 = R.choice(range(8, 61, 2))
            a2 = a1 * k * k
            q = (f"Two similar triangles have corresponding sides in the ratio 1 : {k}. If the smaller "
                 f"triangle has area {a1} cm², the larger has area:")
            e = f"Areas scale as the square of the side ratio, so area = {a1} × {k}² = {a2} cm²."
            h = "Sides scale linearly, areas as the square, volumes as the cube."
            out.append(mk("Geometry", "Medium", q, f"{a2} cm²",
                          [f"{a1*k} cm²", f"{a1*k**3} cm²", f"{a1+k} cm²"], e, h))
        else:
            s = R.choice([5,6,7,8,9,10,12,15,18,20,24,30,36])
            interior = Fraction((s - 2) * 180, s)
            q = f"Each interior angle of a regular polygon with {s} sides measures:"
            e = f"Interior angle = (n−2)×180/n = ({s}−2)×180/{s} = {interior}°."
            h = "Exterior angle is 360/n. Interior is its supplement, which is often the faster route."
            out.append(mk("Geometry", "Medium", q, f"{interior}°",
                          [f"{Fraction(360,s)}°", f"{(s-2)*180}°", f"{Fraction(180,s)}°"], e, h))
    return [x for x in out if x][:n]


# ---------------------------------------------------------------- mensuration
def gen_mensuration(n):
    out = []
    for _ in range(n * 3):
        shape = R.choice(['cuboid', 'cylinder', 'cone', 'sphere'])
        if shape == 'cuboid':
            l, b, h = R.choice(range(4, 21)), R.choice(range(3, 16)), R.choice(range(2, 14))
            v = l * b * h
            q = f"The volume of a cuboid measuring {l} cm × {b} cm × {h} cm is:"
            e = f"Volume = l × b × h = {l} × {b} × {h} = {v} cm³."
            h_ = "Volume multiplies all three dimensions; surface area pairs them."
            out.append(mk("Mensuration", "Easy", q, f"{v} cm³",
                          [f"{2*(l*b+b*h+h*l)} cm³", f"{l+b+h} cm³", f"{v//2} cm³"], e, h_))
        elif shape == 'cylinder':
            r, h = R.choice([7, 14, 21, 28, 35]), R.choice(range(4, 26))
            v = Fraction(22, 7) * r * r * h
            q = f"A cylinder has radius {r} cm and height {h} cm. Its volume is (π = 22/7):"
            e = f"Volume = πr²h = 22/7 × {r}² × {h} = {v} cm³."
            h_ = "A cylinder is a circle extruded, so it is base area times height."
            out.append(mk("Mensuration", "Medium", q, f"{v} cm³",
                          [f"{Fraction(44,7)*r*h} cm³", f"{v/3} cm³", f"{Fraction(22,7)*r*h} cm³"], e, h_))
        elif shape == 'cone':
            r, h = R.choice([7, 14, 21]), R.choice([6, 9, 12, 24])
            v = Fraction(22, 7) * r * r * h / 3
            q = f"A cone has radius {r} cm and height {h} cm. Its volume is (π = 22/7):"
            e = f"Volume = ⅓πr²h = ⅓ × 22/7 × {r}² × {h} = {v} cm³."
            h_ = "A cone is exactly one third of the cylinder on the same base and height."
            out.append(mk("Mensuration", "Medium", q, f"{v} cm³",
                          [f"{v*3} cm³", f"{Fraction(22,7)*r*h} cm³", f"{v/2} cm³"], e, h_))
        else:
            r = R.choice([3, 6, 7, 9, 21])
            v = Fraction(4, 3) * Fraction(22, 7) * r ** 3
            q = f"The volume of a sphere of radius {r} cm is (π = 22/7):"
            e = f"Volume = (4/3)πr³ = 4/3 × 22/7 × {r}³ = {v} cm³."
            h_ = "Surface area is 4πr², volume is (4/3)πr³. Keep the two apart."
            out.append(mk("Mensuration", "Medium", q, f"{v} cm³",
                          [f"{4*Fraction(22,7)*r*r} cm³", f"{v*3/4} cm³", f"{Fraction(22,7)*r**3} cm³"], e, h_))
    return [x for x in out if x][:n]


# ------------------------------------------------------------- counting/prob
def gen_counting(n):
    out = []
    for _ in range(n * 4):
        mode = R.choice(['comb', 'perm', 'word', 'prob_dice', 'prob_ball'])
        if mode == 'comb':
            tot, k = R.choice(range(7, 16)), R.choice([2, 3, 4, 5])
            c = math.comb(tot, k)
            q = f"In how many ways can a committee of {k} be chosen from {tot} people?"
            e = f"Order does not matter, so the count is C({tot},{k}) = {c}."
            h = "Selection means combinations; arrangement means permutations."
            out.append(mk("Permutation & Combination", "Easy", q, c,
                          [math.perm(tot, k), math.comb(tot, k + 1), tot * k], e, h))
        elif mode == 'perm':
            tot, k = R.choice(range(5, 13)), R.choice([2, 3, 4])
            p = math.perm(tot, k)
            q = f"In how many ways can {k} prizes be awarded to {tot} students, no student getting more than one?"
            e = f"Order matters here, so the count is P({tot},{k}) = {p}."
            h = "Distinct prizes make the arrangement matter, so use permutations."
            out.append(mk("Permutation & Combination", "Medium", q, p,
                          [math.comb(tot, k), tot ** k, tot * k], e, h))
        elif mode == 'word':
            word, cnt = R.choice([("LEVEL", 30), ("BANANA", 60), ("SUCCESS", 420),
                                  ("LETTER", 180), ("MISSISSIPPI", 34650)])
            q = f"How many distinct arrangements can be made of the letters of the word {word}?"
            e = (f"Divide the factorial of the length by the factorial of each repeated letter's count, "
                 f"which gives {cnt}.")
            h = "Repeated letters are over-counted. Divide by the factorial of each repetition."
            out.append(mk("Permutation & Combination", "Medium", q, cnt,
                          [math.factorial(len(word)), cnt * 2, cnt // 2], e, h))
        elif mode == 'prob_dice':
            target = R.choice([5, 6, 7, 8, 9, 10])
            ways = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == target)
            pr = Fraction(ways, 36)
            q = f"Two fair dice are rolled. The probability that the sum is {target} is:"
            e = f"There are {ways} favourable outcomes out of 36, giving {pr}."
            h = "Enumerate the favourable pairs. The sample space is always 36 for two dice."
            out.append(mk("Probability", "Easy", q, f"{pr}",
                          [f"{Fraction(ways,12)}", f"{Fraction(1,6)}", f"{Fraction(ways+1,36)}"], e, h))
        else:
            r_, b_ = R.choice(range(3, 10)), R.choice(range(3, 11))
            pr = Fraction(math.comb(r_, 2), math.comb(r_ + b_, 2))
            q = (f"A bag has {r_} red and {b_} blue balls. Two balls are drawn at random. "
                 f"The probability that both are red is:")
            e = (f"Favourable = C({r_},2) = {math.comb(r_,2)}; total = C({r_+b_},2) = "
                 f"{math.comb(r_+b_,2)}. Probability = {pr}.")
            h = "Use combinations for simultaneous draws; sequential draws need conditional probability."
            out.append(mk("Probability", "Medium", q, f"{pr}",
                          [f"{Fraction(r_,r_+b_)}", f"{Fraction(r_*r_,(r_+b_)**2)}",
                           f"{Fraction(math.comb(b_,2), math.comb(r_+b_,2))}"], e, h))
    return [x for x in out if x][:n]


# ------------------------------------------------------------------ set theory
def gen_sets(n):
    out = []
    for _ in range(n * 3):
        mode = R.choice(['two', 'three'])
        if mode == 'two':
            tot = R.choice([100, 120, 150, 200])
            a = R.choice([60, 70, 80, 90])
            b = R.choice([50, 55, 65, 75])
            none = R.choice([5, 10, 15])
            both = a + b - (tot - none)
            if both <= 0 or both > min(a, b):
                continue
            q = (f"In a group of {tot} students, {a} study Economics and {b} study Statistics. "
                 f"If {none} study neither, how many study both?")
            e = (f"Students studying at least one = {tot} − {none} = {tot-none}. "
                 f"n(A∩B) = {a} + {b} − {tot-none} = {both}.")
            h = "Subtract the 'neither' group first, then apply the two-set inclusion-exclusion formula."
            out.append(mk("Set Theory", "Easy", q, both, [a + b - tot, both + none, tot - a - b], e, h))
        else:
            only_a, only_b, only_c = R.choice([20, 25, 30]), R.choice([15, 18, 22]), R.choice([10, 12, 16])
            ab, bc, ca, abc = R.choice([8, 10]), R.choice([6, 9]), R.choice([5, 7]), R.choice([3, 4])
            total = only_a + only_b + only_c + ab + bc + ca + abc
            q = (f"In a survey, {only_a} people liked only tea, {only_b} only coffee and {only_c} only juice. "
                 f"{ab} liked exactly tea and coffee, {bc} exactly coffee and juice, {ca} exactly juice and tea, "
                 f"and {abc} liked all three. How many people were surveyed, assuming everyone liked at least one?")
            e = (f"Add all disjoint regions: {only_a}+{only_b}+{only_c}+{ab}+{bc}+{ca}+{abc} = {total}.")
            h = "Draw the Venn diagram as seven disjoint regions and simply add them."
            out.append(mk("Set Theory", "Medium", q, total,
                          [total - abc, only_a + only_b + only_c, total + abc], e, h))
    return [x for x in out if x][:n]


PLAN = [
    (gen_percentages, 70), (gen_profit_loss, 85), (gen_interest, 75),
    (gen_time_work, 80), (gen_tsd, 85), (gen_averages, 65),
    (gen_ratio, 60), (gen_numbers, 95), (gen_algebra, 85),
    (gen_progressions, 60), (gen_geometry, 150), (gen_mensuration, 80),
    (gen_counting, 110), (gen_sets, 40),
]


def build():
    out, seen = [], set()
    for fn, cnt in PLAN:
        for rec in fn(cnt):
            key = rec['question'].strip()
            if key in seen:
                continue
            seen.add(key)
            out.append(rec)
    for i, r in enumerate(out, 1):
        r['id'] = f"ORIG-QA-{i:04d}"
    return out


if __name__ == '__main__':
    import json, collections
    qs = build()
    print("generated:", len(qs))
    print("unique stems:", len({q['question'] for q in qs}))
    print(dict(collections.Counter(q['topic'] for q in qs)))
