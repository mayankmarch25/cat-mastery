# -*- coding: utf-8 -*-
"""
The quant syllabus spine.

Structure (blocks, chapter order, LOD I/II/III convention) follows the
organisation of Arun Sharma, "How to Prepare for Quantitative Aptitude for
CAT", 8th edition, McGraw Hill 2018, so that this app and the book can be
worked through together. `ref` on each chapter is where to read in the book.

The teaching content below is ORIGINAL and written for this app. No text,
example or exercise from the book is reproduced here. The book is
copyrighted and its copyright page prohibits reproduction; what is mirrored
is the syllabus organisation, which is what makes the two usable side by side.
"""

TRACK = {
 "book": {
   "title": "How to Prepare for Quantitative Aptitude for CAT",
   "author": "Arun Sharma",
   "edition": "8th edition",
   "publisher": "McGraw Hill Education (India), 2018",
   "note": ("This app follows the book's block and chapter structure and its "
            "LOD I / II / III difficulty convention so the two can be worked "
            "together. All teaching notes and questions here are original. "
            "No text or exercise from the book is reproduced.")
 },
 "lod": {
   "1": {"name": "Level of Difficulty I",
         "aim": "Basic chapter questions. Build the reflex until the method is automatic.",
         "target": "Aim for 100% accuracy. Speed matters more than cleverness here."},
   "2": {"name": "Level of Difficulty II",
         "aim": "Applied questions at roughly CAT level. Most of your time belongs here.",
         "target": "Flowchart the question before computing. Note where time is lost."},
   "3": {"name": "Level of Difficulty III",
         "aim": "Beyond the average CAT question. Treat each as a learning object, not a test.",
         "target": "Do not be discouraged by misses. Review the logic until you would recognise it again."}
 },
 "blocks": [
  {
   "id": "FTF", "name": "First Things First", "subtitle": "Developing your calculations",
   "drillOnly": True,
   "ref": "pp. FTF.1–FTF.17",
   "why": ("Calculation speed is the floor everything else stands on. A student who computes "
           "slowly loses marks in chapters they actually understand, because the clock runs out "
           "before the method does. Work this section before anything else and return to it "
           "weekly."),
   "chapters": [
    {"no": 1, "id": "ftf-add", "name": "Additions and subtractions", "ref": "p. FTF.3",
     "topics": ["Speed Addition"],
     "concepts": [
       "Add left to right, not right to left. Running totals in the hundreds are easier to hold than carries.",
       "Round to a convenient anchor and correct afterwards: 497 + 268 becomes 500 + 268 − 3.",
       "Subtraction is addition of a complement. 1000 − 487 is the number that completes 487 to 1000, found digit by digit as 5, 1, 3."],
     "traps": ["Carrying errors cluster when three or more numbers are added at once. Add in pairs.",
               "Rounding without recording the correction is the commonest silent error."],
     "drill": "Add four three-digit numbers mentally in under eight seconds."},
    {"no": 2, "id": "ftf-mult", "name": "Multiplications", "ref": "p. FTF.7",
     "topics": ["Speed Multiplication"],
     "concepts": [
       "Multiplying by 5, 25, 50 and 125 is division: ×5 is ÷2 then ×10, ×25 is ÷4 then ×100.",
       "Numbers near a base multiply by the difference method: 97 × 96 = (97 − 4) | (3 × 4) = 9312.",
       "Splitting beats long multiplication: 36 × 48 = 36 × 50 − 36 × 2."],
     "traps": ["The base method needs the carry handled when the right part exceeds the base's digit count.",
               "Splitting by subtraction fails if you forget the sign on the correction term."],
     "drill": "Two-digit by two-digit in one line, no intermediate written steps."},
    {"no": 3, "id": "ftf-div", "name": "Divisions, percentage calculations and ratio comparisons", "ref": "p. FTF.12",
     "topics": ["Speed Division", "Percentage Calculations"],
     "concepts": [
       "Memorise fraction-percentage equivalents to 1/16. Most percentage questions are a lookup once you see the fraction.",
       "Build a percentage from pieces you know: 37.5% is 25% + 12.5%; 17% is 10% + 5% + 2%.",
       "Compare two ratios by cross-multiplication, or by asking which numerator grew more in proportion to its denominator."],
     "traps": ["Percentage change always needs its base named out loud before you compute.",
               "A ratio comparison reversed is the most frequent careless mark lost in DI."],
     "drill": "Convert any fraction with denominator under 20 to a percentage in two seconds."},
    {"no": 4, "id": "ftf-sq", "name": "Squares and cubes of numbers", "ref": "p. FTF.14",
     "topics": ["Squares and Cubes"],
     "concepts": [
       "Know squares to 30, cubes to 15, and powers of 2 to 2^12 by recall, not computation.",
       "Squares from 31 to 50 come off 25: 43² = (25 + 18) then 1800 + 7² arrangement, giving 1849.",
       "Numbers ending in 5 square instantly: 65² = 6 × 7 then 25 = 4225.",
       "a² − b² = (a + b)(a − b) turns an ugly subtraction into two easy numbers."],
     "traps": ["Confusing the 31–50 and 51–75 shortcuts, which use different offsets."],
     "drill": "Any two-digit square in under three seconds."}]},

  {
   "id": "I", "name": "Block I", "subtitle": "Numbers",
   "ref": "pp. I.1–I.158",
   "why": ("Historically the single heaviest block in CAT quant, and the one where preparation "
           "pays the most. Number systems rewards pattern recognition over formula recall, which "
           "is exactly what the exam tests."),
   "chapters": [
    {"no": 1, "id": "number-systems", "name": "Number systems", "ref": "p. I.15",
     "topics": ["Number Systems", "Base Systems"],
     "concepts": [
       "Prime factorisation is the master key. Factor count, divisor sums, HCF, LCM and trailing zeros all fall out of it.",
       "Number of factors of N = product of (exponent + 1) over its prime factorisation.",
       "HCF × LCM = product of the two numbers. Use it rather than listing multiples.",
       "Remainders: reduce the base modulo the divisor first, then find the cycle of the exponent. Negative remainders often shorten the work.",
       "Trailing zeros in n! are governed by the count of 5s, since 2s are always in surplus.",
       "Base systems: a number in base b is a polynomial in b. Converting is evaluating that polynomial."],
     "traps": ["Treating a remainder cycle as the exponent's full value rather than its residue.",
               "Forgetting that the last digit of a power cycles with period 1, 2 or 4."],
     "drill": "Given any N under 2000, state its factor count in under ten seconds."},
    {"no": 2, "id": "progressions", "name": "Progressions", "ref": "p. I.95",
     "topics": ["Progressions"],
     "concepts": [
       "AP: Tn = a + (n−1)d, Sn = n/2 [2a + (n−1)d]. The (n−1) is where marks are lost.",
       "An AP's sum equals the number of terms times the average of the first and last. Often faster than the formula.",
       "GP: Tn = ar^(n−1), Sn = a(rⁿ − 1)/(r − 1), and for |r| < 1 the infinite sum is a/(1 − r).",
       "HP is the reciprocal of an AP. Convert, solve as an AP, convert back.",
       "For three terms in AP take a−d, a, a+d; for three in GP take a/r, a, ar. The symmetry cancels variables."],
     "traps": ["Using the infinite GP sum when |r| ≥ 1.",
               "Sum of first n natural numbers, squares and cubes should be recall, not derivation."],
     "drill": "Identify AP, GP or neither from the first four terms, instantly."}]},

  {
   "id": "II", "name": "Block II", "subtitle": "Averages and mixtures",
   "ref": "pp. II.1–II.44",
   "why": ("A short block that returns marks quickly. Alligation in particular converts several "
           "chapters' worth of questions into a one-line cross difference."),
   "chapters": [
    {"no": 3, "id": "averages", "name": "Averages", "ref": "p. II.7",
     "topics": ["Averages and Mixtures"],
     "concepts": [
       "Average = total ÷ count. Almost every question is really about the total.",
       "A replacement changes the total by exactly (count × change in average).",
       "Weighted average sits between the two group averages, closer to the larger group.",
       "Deviation method: pick an assumed mean, average the deviations, add back. Shrinks the arithmetic."],
     "traps": ["Averaging two averages without weighting them by group size."],
     "drill": "Weighted average of two groups in one line, no equation written."},
    {"no": 4, "id": "alligations", "name": "Alligations", "ref": "p. II.32",
     "topics": ["Alligations", "Averages and Mixtures"],
     "concepts": [
       "Ratio of quantities = (higher value − mean) : (mean − lower value). Cross differences, nothing more.",
       "It applies wherever two groups combine into a weighted mean: price, concentration, speed, marks, interest rate.",
       "Repeated replacement of a mixture leaves (1 − x/V)ⁿ of the original substance after n operations."],
     "traps": ["Writing the cross differences in the wrong order and inverting the ratio.",
               "Applying alligation to a quantity that is not a weighted average, such as total cost."],
     "drill": "Any two-component mixture ratio in under five seconds."}]},

  {
   "id": "III", "name": "Block III", "subtitle": "Arithmetic and word-based problems",
   "ref": "pp. III.1–III.230",
   "why": ("The largest block by chapter count and the one most students assume they already know. "
           "The difficulty in CAT is rarely the arithmetic; it is converting a sentence into the "
           "right equation. Read the statement twice before writing anything."),
   "chapters": [
    {"no": 5, "id": "percentages", "name": "Percentages", "ref": "p. III.9",
     "topics": ["Percentages", "Percentage Calculations"],
     "concepts": [
       "Every percentage question needs the base named first. 'More than A' makes A the denominator.",
       "Changes multiply as factors: +20% then −20% is 1.2 × 0.8 = 0.96, a 4% fall.",
       "If A is x% more than B, then B is 100x/(100+x)% less than A. The asymmetry is deliberate in CAT.",
       "Product constancy: if one factor rises by x%, the other must fall by 100x/(100+x)% to hold the product."],
     "traps": ["Adding successive percentage changes.",
               "Switching base mid-question between the original and the new value."],
     "drill": "Successive change net effect, mentally, for any two percentages."},
    {"no": 6, "id": "profit-loss", "name": "Profit and loss", "ref": "p. III.43",
     "topics": ["Profit & Loss"],
     "concepts": [
       "Profit percentage is on cost price; discount is on marked price. Keep the two bases apart.",
       "Chain: MP → discount → SP → profit → CP. Walk it in order and the question solves itself.",
       "Equal selling prices with equal profit and loss percentages always produce a net loss of x²/100 %.",
       "False weights: profit% = shortfall / (actual given) × 100, not shortfall / stated."],
     "traps": ["Computing profit on selling price.",
               "Assuming two successive discounts add."],
     "drill": "Given MP, discount and profit, produce CP in one line."},
    {"no": 7, "id": "interest", "name": "Interest", "ref": "p. III.70",
     "topics": ["Simple & Compound Interest"],
     "concepts": [
       "SI = PRT/100 stays on the original principal. CI compounds, so compute the amount then subtract.",
       "For two years, CI − SI = P(R/100)². For three years, add the extra term P(R/100)²(3 + R/100).",
       "Doubling under SI needs R × T = 100. Under CI, use the rule of 72 as an estimate.",
       "Population growth, depreciation and appreciation are compound interest wearing different names."],
     "traps": ["Half-yearly compounding halves the rate and doubles the periods. Both, not one."],
     "drill": "CI − SI for two years, instantly, without computing either."},
    {"no": 8, "id": "ratio", "name": "Ratio, proportion and variation", "ref": "p. III.113",
     "topics": ["Ratio, Proportion & Variation"],
     "concepts": [
       "Introduce the common multiplier x early: a ratio a : b becomes ax and bx.",
       "Partnership profit follows capital × time, not capital alone.",
       "Direct variation means a constant quotient; inverse variation a constant product. Name which before solving.",
       "When ratios chain (A:B and B:C), scale to make B agree, then read A:B:C off."],
     "traps": ["Adding ratios directly instead of scaling to a common term."],
     "drill": "Chain three ratios into one in a single step."},
    {"no": 9, "id": "time-work", "name": "Time and work", "ref": "p. III.139",
     "topics": ["Time & Work"],
     "concepts": [
       "Add rates, never days. The reciprocal of the combined rate is the time.",
       "Take total work as the LCM of the individual times. The fractions disappear.",
       "Pipes and cisterns is the same chapter with outlets as negative rates.",
       "Efficiency is inversely proportional to time taken. 'A is twice as efficient' means A takes half as long."],
     "traps": ["Averaging the days of two workers.",
               "Losing track of who is still working after someone leaves."],
     "drill": "Combined time for two workers via the LCM method, no fractions written."},
    {"no": 10, "id": "tsd", "name": "Time, speed and distance", "ref": "p. III.156",
     "topics": ["Time, Speed & Distance"],
     "concepts": [
       "For equal distances the average speed is the harmonic mean, 2xy/(x+y). The arithmetic mean is the trap option.",
       "Same direction subtracts speeds, opposite direction adds them.",
       "A train crossing a platform covers its own length plus the platform's.",
       "Boats: downstream = boat + stream, upstream = boat − stream. The round trip is never symmetric in time.",
       "Constant distance means speed and time are inversely proportional, so a speed ratio of 3:4 gives a time ratio of 4:3."],
     "traps": ["Using the arithmetic mean for average speed.",
               "Mixing units: km/h to m/s is × 5/18."],
     "drill": "Average speed for a there-and-back journey, mentally."}]},

  {
   "id": "IV", "name": "Block IV", "subtitle": "Geometry",
   "ref": "pp. IV.1–IV.130",
   "why": ("Geometry rewards a stocked memory. The questions are rarely long, but they assume you "
           "already know the property being tested. Build the property list first, then practise."),
   "chapters": [
    {"no": 11, "id": "geometry", "name": "Geometry and mensuration", "ref": "p. IV.5",
     "topics": ["Geometry", "Mensuration"],
     "concepts": [
       "Know the standard triples (3,4,5), (5,12,13), (8,15,17), (7,24,25) and their multiples by sight.",
       "Similar figures: sides scale as k, areas as k², volumes as k³.",
       "Area of a triangle has four routes: ½bh, Heron, ½ab·sinC, and r × s. Pick by what you are given.",
       "Circle: angle at centre is twice the angle at the circumference; opposite angles of a cyclic quadrilateral sum to 180°; tangents from an external point are equal.",
       "A cone is one third of the cylinder on the same base and height; a sphere is two thirds of its circumscribing cylinder."],
     "traps": ["Using a slant height where a vertical height is needed, and the reverse.",
               "Scaling area linearly when the sides were scaled."],
     "drill": "State every property of a given figure before reading the question."},
    {"no": 12, "id": "coordinate", "name": "Coordinate geometry", "ref": "p. IV.86",
     "topics": ["Coordinate Geometry"],
     "concepts": [
       "Distance, section formula and midpoint are the three that appear most.",
       "Slope: parallel lines share it, perpendicular lines multiply to −1.",
       "Area of a triangle from vertices via the determinant form. Zero area means collinear.",
       "A circle is (x−h)² + (y−k)² = r². Completing the square recovers the centre from the general form."],
     "traps": ["Sign errors in the section formula when the division is external."],
     "drill": "Decide collinearity of three points in one computation."}]},

  {
   "id": "V", "name": "Block V", "subtitle": "Algebra",
   "ref": "pp. V.1–V.140",
   "why": ("Along with Block I, historically the heaviest weight in the paper. These four chapters "
           "interlock: a functions question often resolves into an inequality, and an inequality "
           "into a quadratic. Study them together rather than in isolation."),
   "chapters": [
    {"no": 13, "id": "functions", "name": "Functions", "ref": "p. V.5",
     "topics": ["Functions"],
     "concepts": [
       "Domain is what you may put in, range is what comes out. Most questions are domain questions in disguise.",
       "f(f(x)) questions usually have a short cycle. Compute two or three iterations and look for the repeat.",
       "Even: f(−x) = f(x), symmetric about the y-axis. Odd: f(−x) = −f(x), symmetric about the origin.",
       "Composition is not commutative: f(g(x)) and g(f(x)) differ. Read the order carefully.",
       "Graph transformations: f(x) + a shifts up, f(x + a) shifts left, −f(x) reflects in the x-axis, |f(x)| folds the negative part upward."],
     "traps": ["Assuming an inverse exists when the function is not one-to-one.",
               "Dropping domain restrictions that the denominator or a square root imposes."],
     "drill": "Find the period of f(f(x)) within three iterations."},
    {"no": 14, "id": "inequalities", "name": "Inequalities", "ref": "p. V.41",
     "topics": ["Inequalities"],
     "concepts": [
       "Multiplying or dividing by a negative reverses the sign. This single rule accounts for most errors.",
       "Never cross-multiply an inequality unless you know the sign of the denominator. Bring everything to one side instead.",
       "Wavy curve: mark the roots on a line, test the rightmost interval, alternate signs across simple roots, do not alternate across a repeated root of even multiplicity.",
       "|x − a| < b means a − b < x < a + b. |x − a| > b splits into two rays.",
       "AM ≥ GM ≥ HM for positive numbers, with equality only when all terms are equal. This is how most minimum and maximum questions are meant to be solved."],
     "traps": ["Squaring both sides without checking that both are non-negative.",
               "Forgetting that the denominator's zero is excluded from the solution set."],
     "drill": "Solve a rational inequality by wavy curve in under a minute."},
    {"no": 15, "id": "quadratics", "name": "Quadratic and other equations", "ref": "p. V.71",
     "topics": ["Equations"],
     "concepts": [
       "Sum of roots = −b/a, product = c/a. Nearly every symmetric expression in the roots reduces to these two.",
       "Discriminant b² − 4ac: positive gives two real roots, zero gives equal roots, negative gives none real.",
       "α² + β² = (α+β)² − 2αβ. Build the expression you need from the sum and product rather than finding roots.",
       "For a parabola, the vertex at x = −b/2a gives the minimum when a > 0 and the maximum when a < 0.",
       "Cubics: the sum of roots is −b/a, the sum of pairwise products is c/a, the product is −d/a."],
     "traps": ["Finding the roots when only a symmetric function of them was asked.",
               "Ignoring the condition a ≠ 0 when the coefficient contains a variable."],
     "drill": "Produce α² + β² and α³ + β³ from the coefficients without solving."},
    {"no": 16, "id": "logarithms", "name": "Logarithms", "ref": "p. V.109",
     "topics": ["Logarithms & Indices"],
     "concepts": [
       "A logarithm is an exponent. Rewrite in exponential form the moment you are stuck.",
       "log(mn) = log m + log n; log(m/n) = log m − log n; log(mⁿ) = n log m.",
       "Base change: log_b a = log a / log b. Use it to put everything on one base.",
       "log_b a × log_a b = 1, and a^(log_a x) = x.",
       "The argument must be positive and the base positive and not 1. Check this before accepting a root."],
     "traps": ["Treating log(m + n) as log m + log n.",
               "Keeping a root that makes the argument negative."],
     "drill": "Collapse a three-term log expression to a single logarithm in one step."}]},

  {
   "id": "VI", "name": "Block VI", "subtitle": "Counting",
   "ref": "pp. VI.1–VI.100",
   "why": ("The block where careful reading beats technique. The difference between an arrangement "
           "and a selection, or between 'at least one' and 'exactly one', decides the answer before "
           "any formula is applied."),
   "chapters": [
    {"no": 17, "id": "pnc", "name": "Permutations and combinations", "ref": "p. VI.5",
     "topics": ["Permutation & Combination"],
     "concepts": [
       "Arrangement means order matters, so permutations. Selection means it does not, so combinations.",
       "Repeated objects: divide by the factorial of each repetition count.",
       "Objects that must sit together are glued into one unit, then arranged internally.",
       "Circular arrangements of n objects give (n−1)!, and (n−1)!/2 when reflections are identical.",
       "Distributing n identical objects into r distinct boxes gives C(n+r−1, r−1)."],
     "traps": ["Double counting when cases overlap. Separate the cases so they cannot.",
               "Applying the gap method without checking the arrangement is linear."],
     "drill": "Classify any counting question as permutation or combination before computing."},
    {"no": 18, "id": "probability", "name": "Probability", "ref": "p. VI.43",
     "topics": ["Probability"],
     "concepts": [
       "Probability = favourable ÷ total, with both counted the same way.",
       "'At least one' is almost always faster as 1 − P(none).",
       "Independent events multiply. Mutually exclusive events add. Check which before combining.",
       "Simultaneous draws use combinations; sequential draws without replacement need conditional probability.",
       "Expected value is the sum of outcome × probability."],
     "traps": ["Counting the sample space one way and the favourable cases another.",
               "Assuming independence when the draw is without replacement."],
     "drill": "Rewrite any 'at least one' question as its complement."},
    {"no": 19, "id": "sets", "name": "Set theory", "ref": "p. VI.71",
     "topics": ["Set Theory", "Venn Diagrams"],
     "concepts": [
       "Two sets: n(A∪B) = n(A) + n(B) − n(A∩B).",
       "Three sets: add the singles, subtract the pairs, add back the triple.",
       "Draw the diagram as seven disjoint regions and fill from the centre outward.",
       "'Exactly two' excludes the triple overlap; 'at least two' includes it. Read which is asked.",
       "Subtract the 'neither' group from the total before applying any formula."],
     "traps": ["Confusing 'only A' with 'A', which includes every overlap.",
               "Filling the diagram from the outside in, which forces rework."],
     "drill": "Fill a three-set Venn diagram from the centre in one pass."}]}
 ]
}


def chapter_index():
    """topic name -> (block id, chapter id, chapter no, chapter name)"""
    idx = {}
    for b in TRACK["blocks"]:
        for c in b["chapters"]:
            for t in c["topics"]:
                idx.setdefault(t, (b["id"], c["id"], c["no"], c["name"]))
    return idx


def all_chapters():
    return [(b, c) for b in TRACK["blocks"] for c in b["chapters"]]
