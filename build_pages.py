"""Generate the project pages from one template.

The pages share a structure -- position, findings, recommendation, method -- so
the layout lives here once rather than in five files that drift apart.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "projects"

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Lohan De Silva</title>
<meta name="description" content="{description}">
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>

<div class="wrap">
  <header class="project-head">
    <a class="backlink" href="../index.html">&larr; Lohan De Silva</a>
    <p class="work-domain">{domain}</p>
    <h1>{headline}</h1>
    <p class="lede">{lede}</p>
    <p class="links">
      <a href="{repo}">Repository</a>
      <a href="{repo}/blob/main/reports/executive-summary.md">Executive summary</a>
      <a href="{repo}/blob/main/reports/technical-appendix.md">Technical appendix</a>
    </p>
  </header>

  <div class="keyfigs">
{keyfigs}
  </div>

{body}

  <p class="caveat">{caveat}</p>

  <footer>
    <p>
      <a href="../index.html">Back to all work</a> ·
      <a href="mailto:desilvalohan@gmail.com">desilvalohan@gmail.com</a> ·
      <a href="{repo}">Source and method</a>
    </p>
  </footer>
</div>

</body>
</html>
"""


def keyfig(value: str, label: str) -> str:
    return (f'    <div><span class="fig-value">{value}</span>'
            f'<span class="fig-label">{label}</span></div>')


def figure(src: str, caption: str) -> str:
    return (f'  <figure><img src="../assets/figures/{src}" alt="{caption}">\n'
            f'  <figcaption>{caption}</figcaption></figure>')


def callout(label: str, html: str) -> str:
    return (f'  <div class="callout"><p class="callout-label">{label}</p>\n'
            f'  {html}</div>')


PROJECTS = {
"customer-churn": dict(
    title="Churn and retention economics",
    domain="Subscription economics · Telecommunications",
    headline="Churn takes a quarter of the customers and a third of the revenue",
    description=("Retention economics on a 7,043-account telecom book: survival "
                 "analysis, a targeting model and the offer size that actually pays."),
    lede=("A 7,043-account telecom book, read for what churn is costing, which "
          "accounts carry the loss, and what a retention programme has to achieve "
          "before it pays for itself."),
    repo="https://github.com/Lohandesilva/customer-churn-analysis",
    keyfigs=[("$1.67M", "annualised revenue lost, on a $5.47M book"),
             ("30.5%", "of revenue lost, against 26.5% of accounts"),
             ("0.836", "holdout AUC on the targeting model"),
             ("9.5%", "save rate the recommended offer needs to break even")],
    caveat=("Save rates are modelled, not observed — the extract has no campaign "
            "history — which is why the case is anchored on the break-even rather "
            "than the assumption. Contribution margin and cost of capital are "
            "supplied from outside the data and swept; the recommendation holds "
            "anywhere above a 50% margin. Nothing here is causal: the first "
            "recommendation is to run a controlled test."),
    body=f"""
  <h2>The position</h2>
  <p>The book carries $456,117 of monthly recurring revenue. In the observation
  month 1,869 accounts closed — 26.5% of customers, but <strong>30.5% of
  revenue</strong>. Leavers were billing $74.44 a month against $61.27 for the
  accounts that stayed.</p>
  <p>That gap is the finding that should change how the programme is funded.
  Churn here is not a low-value-customer problem, and treating it as one has been
  costing the higher-margin end of the book.</p>

  <h2>Contract term decides tenure; price barely moves it</h2>
  <p>Month-to-month accounts churn at 42.7%, one-year at 11.3%, two-year at 2.8%.
  Median tenure on month-to-month is 35 months; neither annual contract reaches
  50% attrition inside six years. Log-rank χ² = 2,353 across the three curves.</p>
  <p>Once contract type and product mix are held constant, each additional dollar
  on the monthly bill is associated with slightly <em>lower</em> churn odds — the
  opposite of where the commercial conversation usually starts.</p>
{figure("churn/01-retention-by-contract.png", "Kaplan-Meier retention by contract type, with 95% intervals. Tenure is read as time on book, leavers as events and retained accounts as right-censored.")}

  <h2>Fibre is the problem product, not the premium product</h2>
  <p>Holding contract, tenure, bill size and every attached service constant, a
  fibre line carries <strong>4.38x</strong> the churn odds of the reference
  customer (95% CI 2.68–7.17). It is the largest effect in the model by a wide
  margin, and month-to-month fibre is 30% of the base but <strong>72% of all lost
  revenue</strong>.</p>
  <p>Attached support products pull the other way. Online security (0.78x) and
  tech support (0.79x) both reduce churn odds significantly, which makes
  attachment a retention lever and not only an ARPU lever.</p>
{figure("churn/03-churn-drivers.png", "Odds ratios from a logistic regression on 4,930 training accounts, significant terms only, with 95% Wald intervals.")}

  <h2>The offer size matters more than the audience size</h2>
  <p>The scoring model reaches AUC 0.836 on a 30% holdout. Its top decile churns
  at 76.6% — 2.89x the base rate — and the top two deciles hold 56% of the lost
  revenue while covering 20% of customers.</p>
  <p>That precision is what makes an intervention viable, because the offer cost
  is paid on everyone contacted while the benefit only lands on the people who
  would otherwise have left. Even in the top two deciles, 457 of 1,409 contacts
  were staying anyway.</p>
  <div class="table-scroll">
  <table>
    <thead><tr><th>Offer</th><th>Cost</th><th>Benefit</th><th>Net value</th><th>Return</th></tr></thead>
    <tbody>
      <tr><td>10%</td><td>$155,222</td><td>$275,432</td><td class="pos">$120,210</td><td>1.77x</td></tr>
      <tr><td>15%</td><td>$224,379</td><td>$275,432</td><td>$51,053</td><td>1.23x</td></tr>
      <tr><td>20%</td><td>$293,537</td><td>$275,432</td><td class="neg">−$18,104</td><td>0.94x</td></tr>
    </tbody>
  </table>
  </div>
{callout("Recommendation", '''<p>Contact the top two modelled risk deciles — 1,409 accounts — with a 10%
  bill reduction held for twelve months, conditional on moving off month-to-month.
  <strong>$120,210 of net contribution against $155,222 of spend, and it stays
  positive down to a 9.5% save rate.</strong></p>
  <p>Do not extend the discount past 10% to buy acceptance. Raising it inflates
  the cost across all 1,409 contacts while the addressable saves stay fixed at
  952. A 20% offer is loss-making. If budget is tight, cut depth rather than
  generosity — the top decile alone returns 2.02x.</p>''')}
{figure("churn/04-targeting-gains.png", "Cumulative share of lost revenue reached as the base is contacted highest-risk first.")}
""",
),

"sales-margin": dict(
    title="Sales performance and the cost of discounting",
    domain="Pricing and commercial policy · Retail",
    headline="Revenue grew 51%. The discount ate the margin.",
    description=("A four-year order book read for why margin stopped following "
                 "revenue: the discount cliff, a profit bridge, and a cap worth 71% "
                 "of company profit."),
    lede=("A four-year order book — 9,994 lines, $2.30M of revenue — read for the "
          "question the growth numbers hide: the business is growing, so why is "
          "margin not?"),
    repo="https://github.com/Lohandesilva/sales-performance-analytics",
    keyfigs=[("$566,734", "given away in discount — 19.8% of list value"),
             ("1.57", "margin points lost per discount point"),
             ("−$135,376", "booked on $362,770 sold above a 20% discount"),
             ("+71%", "profit recovered by capping the discount at 20%")],
    caveat=("The cap counterfactual holds volume constant. It has to — there is no "
            "price test, no quote-to-order data and no lost-deal record anywhere in "
            "the file — which is why the recommendation is argued on the walk-away "
            "logic rather than on the $204,135. Four years of one retailer, ending "
            "2018: the mechanism generalises, the 20% break-even does not."),
    body=f"""
  <h2>The source file is three worksheets</h2>
  <p>The published CSV is 10,800 rows. The first 9,994 are order lines; the rest
  are the workbook's People and Returns sheets written underneath, each introduced
  by a header sitting in the first two columns of an otherwise blank row. Read
  naively this looks like 806 rows of missing data and gets dropped.</p>
  <p>Parsing the blocks out recovers <strong>800 return records covering 296
  orders</strong> — a table the standard read of this dataset discards, and one
  that turns out to decide whether the main recommendation is safe.</p>

  <h2>Growth was bought, not earned</h2>
  <p>Revenue rose from $484,247 to $733,215, a 14.8% compound rate. Margin went
  10.2% → 13.1% → 13.4% → 12.7%: it improved for two years and then gave back a
  third of the gain. The discount rate tracks it exactly.</p>
{figure("sales/01-growth-versus-margin.png", "Revenue and margin as separate panels. A dual axis here would invite the exact misreading the chart exists to prevent.")}
  <p>The 2017–2018 bridge makes the mechanism explicit. Profit rose $11,644 — the
  net of a <strong>$16,650 volume gain and a $13,545 discount give-back</strong>.
  Higher discounting consumed 81% of what the extra revenue earned.</p>
{figure("sales/04-profit-bridge.png", "Sequential bridge. Volume is valued at last year's margin; mix and execution is the unexplained residual, reported rather than absorbed.")}

  <h2>Discounting has a cliff, not a slope</h2>
  <p>Lines sold at list carry a 29.5% margin. At 16–20% discount, 11.8%. At
  21–30%, <strong>−10.0%</strong> — and 91.6% of the lines in that band lose money
  individually. Past 40%, every single line loses money. At 71% and above the
  margin is −180%: the business pays $1.80 for every dollar it books.</p>
{figure("sales/02-discount-cliff.png", "Aggregate margin at each discount level the business issues, sized by revenue at that level. Both the empirical crossing and a revenue-weighted fit put the break-even near 20%.")}

  <h2>The regional gap is a policy gap, not a selling gap</h2>
  <p>Central runs 4.6 margin points below the company. The instinct is to look at
  the sales team. Decomposing the gap into what the region's own discount mix
  explains and what it does not: <strong>5.3 of those points are the discount
  Central is giving</strong> — 24.0% on average, against 10.9% in West — and its
  execution is 0.8 points <em>better</em> than the discounts would predict.</p>
{figure("sales/05-margin-variance.png", "Each region's margin gap against the company average, split into the part its discount mix explains and the part it does not.")}

  <h2>Returns do not rise with discount</h2>
  <p>The obvious objection to a margin curve like this is that it understates the
  problem: if deeply discounted goods also come back more often, discounting costs
  more than the P&amp;L shows. It does not. Lines on returned orders carry a
  <strong>14.3% average discount against 15.7% on lines that were kept</strong>,
  and the rank correlation between discount and return is −0.019 (p = 0.052).</p>
  <p>A null result, and a useful one: the margin curve can be taken at face value.</p>
{callout("Recommendation", '''<p>Cap the line-level discount at 20% and route anything deeper through a
  named approver. 1,393 lines — 13.9% of the book, $362,770 of revenue — sit above
  that cap and lose $135,376 between them. Repriced at 20%, the same list value
  earns $68,759: a <strong>$204,135 swing, a 71% increase on total company
  profit, from 14% of the order lines</strong>.</p>
  <p>The usual counter is that some of that revenue walks away. Here that does not
  survive the arithmetic — the capped lines lose money as they stand, so revenue
  walking away is itself a gain. There is no walk-away rate at which the cap stops
  paying.</p>''')}
""",
),

"sp500-profitability": dict(
    title="S&amp;P 500 profitability and valuation",
    domain="Equity analysis · Capital markets",
    headline="Rebuilding index fundamentals from ratios alone",
    description=("503 S&P 500 constituents: fundamentals reconstructed from "
                 "accounting identities, a variance decomposition on margin, and a "
                 "funding-gap screen."),
    lede=("An extract with no income statement and no balance sheet. Every "
          "fundamental here is reconstructed from accounting identities — and two "
          "received ideas do not survive the test."),
    repo="https://github.com/Lohandesilva/financial-performance-analysis",
    keyfigs=[("26%", "of EBITDA margin variance explained by sector"),
             ("R² 0.002", "on the naive quality-versus-price relationship"),
             ("69 of 285", "companies priced above the growth they can fund"),
             ("$4.24tn", "of index capitalisation in that funding deficit")],
    caveat=("The file is an undated point-in-time snapshot with no as-of column, and "
            "the publisher overwrites it in place; 17 constituents carry no market "
            "data at all, several of them names that have left the index, so the "
            "roster and the price vector were struck at different times. Twenty-eight "
            "loss-making companies have no P/E and drop out, which biases the "
            "retained sample toward profitability. Both are stated rather than "
            "corrected."),
    body=f"""
  <h2>The reconstruction</h2>
  <p>The extract carries prices and multiples but no statements. Revenue, net
  income, return on equity and payout are all recoverable from identities:</p>
  <ul>
    <li>Revenue = market cap ÷ price-to-sales</li>
    <li>Net income = earnings per share × shares outstanding</li>
    <li><strong>ROE = (P/B) ÷ (P/E)</strong>, since (P/B) × (E/P) = E/B</li>
    <li><strong>Payout = dividend yield × (P/E)</strong>, since (D/P) × (P/E) = D/E</li>
    <li>Sustainable growth = ROE × (1 − payout)</li>
  </ul>
  <p>The algebra is implemented twice — once in Python and again in SQL — so the
  two paths can be reconciled against each other.</p>

  <h2>Sector explains far less of margin than the medians suggest</h2>
  <p>Sector medians span 43 points of EBITDA margin, which reads as though
  industry determines profitability. A one-way analysis of variance puts the
  actual figure at <strong>η² = 0.261</strong> (F = 15.7, p &lt; 0.001, n = 455).
  Seventy-four per cent of the variation sits <em>within</em> sectors.</p>
  <p>Strip out Financials and Real Estate — whose "margins" are interest and rent
  and are not comparable — and it falls to 0.149. At sub-industry level it reaches
  0.587, which is where the real grouping is.</p>
{figure("sp500/01-margin-dispersion-by-sector.png", "EBITDA margin distribution by sector. The within-sector spread is the finding.")}

  <h2>The market pays for size, not for margin</h2>
  <p>Regressing log P/E on EBITDA margin and log market cap: margin
  <strong>−0.607</strong> (p = 0.002), size <strong>+0.144</strong> (p &lt; 0.001),
  R² = 0.091. Higher-margin companies trade on <em>lower</em> multiples once size
  is controlled for.</p>
  <p>The naive specification — earnings yield on ROE — returns R² = 0.002. That is
  a genuine null and it is reported as one. The reason is mechanical and worth
  stating: ROE = (P/B) ÷ (P/E) and net margin = (E/P) × (P/S) are both
  rearrangements of the multiples, so regressing one on the other is closer to an
  identity check than to a test. EBITDA margin is the only price-free measure of
  quality in the file.</p>
{figure("sp500/02-quality-versus-price.png", "Valuation against margin, with the fitted relationship and the largest residuals labelled.")}

  <h2>Where the book multiple comes from</h2>
  <p>log(P/B) = log(ROE) + log(P/E) exactly. Decomposing the variance:
  <strong>91% is variance in ROE</strong>, 53% is valuation, and −44% is
  covariance between them — the market marks down the multiple on high-return
  companies, with corr(log ROE, log P/E) = −0.32.</p>
{figure("sp500/03-book-multiple-decomposition.png", "Variance decomposition of the price-to-book multiple into return on equity, valuation and their covariance.")}

  <h2>The funding-gap screen</h2>
  <p>Comparing what each company can grow at from retained earnings against what
  its multiple implies the market is pricing in: <strong>69 of 285 screened
  companies are priced above what they can fund</strong> — $4.24tn, 6.4% of index
  capitalisation. The deficit group pays out a median 66% of earnings on a median
  8.8% ROE; the surplus group pays 22% on 21.2%. Twenty-one of the 29 screened
  utilities are on the list, which is what you would expect from a regulated
  sector and is a useful check that the screen is behaving.</p>
{callout("What this is for", '''<p>The screen is a starting list, not a conclusion. A company can be priced
  above its self-funded growth rate for good reasons — a credible acquisition
  programme, a deliberate leverage step, a payout it intends to cut. What the
  screen does is put the 69 names where that argument has to be made explicitly,
  and quantify what is riding on it.</p>''')}
""",
),

"credit-risk": dict(
    title="Credit portfolio risk and the limit decision",
    domain="Credit risk · Consumer banking",
    headline="A scorecard that gives up nothing by leaving demographics out",
    description=("A 30,000-account credit card book: roll rates, a behavioural "
                 "scorecard built without protected characteristics, IFRS 9 expected "
                 "loss and a limit-cut decision."),
    lede=("A 30,000-account credit card book — NT$5.02bn of committed limits "
          "against NT$1.54bn drawn — read for where the delinquency is going, what "
          "it is worth in expected loss, and which credit lines stop paying for "
          "themselves."),
    repo="https://github.com/Lohandesilva/credit-portfolio-risk",
    keyfigs=[("0.003", "Gini given up by excluding protected characteristics"),
             ("0.539", "holdout Gini on behavioural variables alone"),
             ("51%", "of expected credit loss in 17% of exposure"),
             ("1.64%", "probability of default at which a limit cut breaks even")],
    caveat=("Loss given default is an assumption, not an observation — the file has "
            "no recovery data — so it is stated in configuration and swept rather "
            "than argued for. The book is 2005 Taiwanese and six months long: the "
            "roll rates are a snapshot of one point in one credit cycle in one "
            "jurisdiction, and nothing here should be carried to another market "
            "without re-estimation."),
    body=f"""
  <h2>The fair-lending decision, and what it costs</h2>
  <p>Sex, education and marital status are excluded from the scorecard. That is a
  conduct decision, not a modelling one, and it is usually argued against on the
  grounds that the bank gives up predictive power.</p>
  <p>So I measured it. Fitting the same model with those fields included and
  comparing on the same holdout: the exclusion costs <strong>0.003 of Gini</strong>
  — 0.5388 against 0.5418. Three of the four demographic fields fail the standard
  information-value screen outright before they reach the model.</p>
  <p>There is no efficiency argument left. A scorecard built on behaviour alone
  performs indistinguishably from one that uses who the customer is.</p>
{figure("credit/07-fair-lending-cost.png", "Discrimination with and without protected characteristics, on the same holdout sample.")}

  <h2>Delinquency escalates, and cures are rarer than rolls</h2>
  <p>Across consecutive months the pooled roll-forward rate — current to one cycle
  past due — is <strong>4.9%</strong>, and it rises from 3.2% in the earliest
  month observed to 5.8% in the latest. The pooled cure rate is 28.2%.</p>
  <p>Default probability escalates sharply with the delinquency bucket an account
  is sitting in, which is what makes the state variable the strongest single input
  to the scorecard and the natural basis for the staging in the loss model.</p>
{figure("credit/01-delinquency-escalation.png", "Default rate by current delinquency bucket.")}

  <h2>The scorecard</h2>
  <p>Logistic regression on behavioural variables only: repayment status history,
  utilisation, payment ratios, limit and bill trajectory. <strong>AUC 0.769, Gini
  0.539, KS 0.414</strong> on a 9,000-account holdout, against 0.775 in sample.</p>
  <p>Discrimination is not the whole test. A scorecard that ranks well but is
  poorly calibrated cannot be used for provisioning, because the expected loss
  numbers it produces will be wrong even where the ranking is right. Seven of the
  score bands sit within two standard errors of their observed default rate, with
  a largest gap of 2.8 percentage points.</p>
{figure("credit/04-calibration.png", "Predicted against observed default rate by score band, on the holdout sample.")}

  <h2>Where the expected loss actually sits</h2>
  <p>Expected credit loss is PD × LGD × EAD, in an IFRS 9 frame. The
  concentration is what matters for action: <strong>51% of the expected loss sits
  in the worst two score bands, which carry 17% of exposure</strong>.</p>
{figure("credit/05-ecl-concentration.png", "Expected credit loss and exposure at default by score band.")}
{callout("Recommendation", '''<p>The limit-cut decision reduces to a single probability threshold. On the
  base case, cutting an undrawn line pays for itself above a <strong>1.64%
  probability of default</strong>; on the most adverse revenue assumption tested,
  above 3.11%. Both thresholds sit far below the default rate in the worst score
  bands, so the decision is not close for those accounts.</p>
  <p>Cut the top three bands. The value-maximising depth is deeper than that, but
  the marginal bands trade a large increase in customers affected for a small
  increase in loss avoided, and the customer cost of a limit cut is not in this
  data.</p>''')}
""",
),

"clinic-capacity": dict(
    title="Outpatient non-attendance and clinic capacity",
    domain="Operations · Healthcare",
    headline="The most-quoted finding in this dataset is a confounding artefact",
    description=("110,521 outpatient appointments: the SMS reminder paradox resolved "
                 "by stratification, a leakage-safe behaviour model, and an "
                 "overbooking rule."),
    lede=("110,521 public outpatient appointments, read for how much capacity "
          "non-attendance takes, what actually predicts it, and what a service "
          "manager can do about it on Monday."),
    repo="https://github.com/Lohandesilva/healthcare-operations-analytics",
    keyfigs=[("20.2%", "of appointments not attended — 20 points of slot utilisation"),
             ("1.90 → 0.77", "SMS odds ratio, before and after controlling for lead time"),
             ("4.6% → 33%", "non-attendance, same-day booking versus a month out"),
             ("23:1", "slots recovered per patient turned away, under the overbooking rule")],
    caveat=("Six weeks of one Brazilian public health service in 2016. Capacity is "
            "inferred from the booked list, so rostered-but-unbooked slots are "
            "invisible and true utilisation may be worse. The overbooking case rests "
            "on unmet demand the data cannot verify — roughly 725 extra patients per "
            "clinic day would have to exist — and that is the largest risk to the "
            "recommendation, stated as such in the memo."),
    body=f"""
  <h2>The scale of it</h2>
  <p>Of 110,521 appointments across 27 clinic days, <strong>22,314 were not
  attended</strong> — 20.2%, or 826 unused slots every clinic day. Slot
  utilisation runs at 79.8%. Over the six-week window that is 5.4 clinic days of
  capacity simply gone.</p>

  <h2>Lead time is the lever</h2>
  <p>Same-day bookings are missed 4.6% of the time. Next-day bookings, 21.4% — a
  4.6x step in twenty-four hours. Beyond a month the rate plateaus around 33%.</p>
  <p>The distributional consequence is the operational one: same-day bookings are
  35% of the book but only 8% of the leakage, while appointments booked more than
  a week out are 36% of the book and <strong>57% of everything lost</strong>.</p>
{figure("clinic/01-lead-time-curve.png", "Non-attendance against days between booking and appointment, with the booking volume behind each point.")}

  <h2>The SMS paradox</h2>
  <p>In the raw data, patients who received an SMS reminder missed appointments
  more often than those who did not: 27.6% against 16.7%, an odds ratio of
  <strong>1.90</strong>. This result is repeated across dozens of published
  analyses of this dataset, usually with some speculation about reminder fatigue.</p>
  <p>It is an artefact of who gets sent one. SMS coverage is <strong>0% on
  same-day bookings</strong>, 6% at one to three days, and around 60% beyond a
  week. Median lead time is 14 days in the SMS arm and 0 in the no-SMS arm — 51%
  of which is same-day bookings, the group that almost never misses.</p>
  <p>Stratify by lead time and the sign reverses. Within every band SMS is
  favourable. A Mantel-Haenszel estimate across 105 exact lead-day strata gives
  <strong>OR 0.769 (0.742–0.797)</strong>. A nested logistic model tells the same
  story: 1.899 falls to 0.789 on adding lead time alone, and to 0.790 after eight
  further covariates. One confounder does all of the work.</p>
{figure("clinic/02-sms-paradox.png", "The naive comparison against the lead-time-stratified one. The empty same-day SMS arm is not a gap in the table; it is the evidence.")}

  <h2>Prior behaviour, without leaking the answer</h2>
  <p>Patients recur in this data, so history is available — but it has to be built
  from appointments strictly earlier than the one being predicted, ordered by
  booking time. Built naively it leaks the target and the model looks far better
  than it is.</p>
  <p>Constructed safely: patients who have never missed run at 15.2%; one prior
  miss, 25.1%; two, 27.0%; three or more, <strong>38.0%</strong>. It is the
  largest term in the model at an odds ratio of 2.83.</p>
{figure("clinic/03-prior-behaviour.png", "Non-attendance by number of prior missed appointments, using an expanding count shifted by one.")}

  <h2>Overbooking, with the arrival assumption tested</h2>
  <p>The marginal overbooking rule is P(fill) &lt; 1/(1+M), and the unit cost
  cancels out of it. The standard derivation assumes binomial arrivals; that
  assumption is testable here and it fails — session counts are twice as dispersed
  as binomial, 1.62x after modelling. The published rule takes the haircut.</p>
  <p>On a typical 63-slot session at 80% attendance that is <strong>+11
  bookings</strong>, 8.3 slots recovered against 0.46 expected overflow, and
  utilisation moving from 80% to 93%. Across the portfolio: 14,874 slots recovered
  against 658 expected overflow — a <strong>23:1 ratio</strong> — worth BRL 5.37M
  a year at the stated slot cost.</p>
{figure("clinic/05-overbooking-frontier.png", "Recovered capacity against expected overflow as the overbooking depth increases.")}
{callout("Recommendation", '''<p>Overbook to the marginal rule, and shorten lead times second. This is not
  the ordering I expected: lead-time compression is the cleaner intervention and
  it recovers 3,145 slots (BRL 1.31M a year), roughly a quarter of what
  overbooking is worth.</p>
  <p>They are sequenced rather than alternatives. Lead times cannot be shortened
  without near-term capacity to shorten them into, and overbooking is what creates
  that capacity. The ranking is invariant to the cost-per-slot assumption across
  the whole range swept.</p>''')}
""",
),
}


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for slug, p in PROJECTS.items():
        html = TEMPLATE.format(
            title=p["title"],
            description=p["description"],
            domain=p["domain"],
            headline=p["headline"],
            lede=p["lede"],
            repo=p["repo"],
            keyfigs="\n".join(keyfig(v, l) for v, l in p["keyfigs"]),
            body=p["body"],
            caveat=p["caveat"],
        )
        (OUT / f"{slug}.html").write_text(html)
        print(f"wrote projects/{slug}.html")


if __name__ == "__main__":
    main()
