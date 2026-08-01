# Dream Bank - Financial Model Analysis

**Prepared for Jesse Grylls | 1 August 2026**
Source: "Dream Bank Financial Model.xlsx", attached to Jack Whettingsteel's email of 31 July 2026, 14:11 BST.
Ten sheets, monthly build Jul 2026 to Mar 2030. All figures below are read directly from the model.

---

## 1. The one-paragraph version

Dream Bank is not a bank. It is a consumer front end sitting on ClearBank's licence, and every material
cost line in the model is a ClearBank invoice. The model is honest, well built and self-critical, which is
rare and counts for something. But it rests on one assumption doing almost all the work: that a very large
audience converts into bank accounts at essentially no acquisition cost. Marketing is £5,000 a month, flat,
for all three years, against 250,000 accounts. That is Bear's reach and Simon's reach being spent as the
customer acquisition budget. The model values that input at zero, and then asks Bear to write a £100,000
cheque to supply it.

---

## 2. What is actually being asked

Jack's email of 31 July: *"For most people, we are suggesting an initial 100k cheque in this founding round."*

That resolves the question left open after the intro call. The ask is capital. Not name, not time, not
audience alone.

| | |
|---|---|
| Suggested initial cheque | £100,000 |
| Their planned raise | £3,500,000 |
| Raise the model says is required, base case | £3,960,724 (rounded £4.0m) |
| Raise the model says is required, stress case | £5,189,329 (rounded £5.25m) |
| Cover: planned raise vs requirement, base | **0.88x** |
| Cover: planned raise vs requirement, stress | **0.67x** |

The plan is underfunded by its own arithmetic before a single cheque lands. The model flags this itself, as
a HIGH risk: *"Stress case requires roughly £4.5m against a £3.5m plan."*

A £100k cheque is 2.5% of what the model says the business needs. Whatever it buys, it will be diluted by a
second round that the model has already predicted.

---

## 3. The headline numbers

Combined view, Phase 1 core banking plus Phase 2/3 product roadmap:

| | Pre-launch | Year 1 | Year 2 | Year 3 |
|---|---|---|---|---|
| Total accounts (year end) | 0 | 50,000 | 100,000 | 250,000 |
| Average deposits (£) | 0 | 23.4m | 106.4m | 404.6m |
| Combined revenue (£) | 0 | 1,288,685 | 5,882,746 | 20,035,619 |
| Combined cost (£) | 962,522 | 2,659,583 | 5,041,096 | 8,534,661 |
| **Combined EBITDA (£)** | **(962,522)** | **(1,370,898)** | **841,650** | **11,500,958** |

Peak cash deficit: **£2,630,933**, reached September 2028.
Monthly EBITDA breakeven: 17 months after launch.
Cumulative cash repaid: July 2029.

The capital logic here is correct and worth crediting. An earlier version of this model summed three annual
deficits and produced a £17m raise against a real peak need of about £2.1m. Someone caught it and wrote the
correction into the sheet in plain English. That is a good sign about the person holding the pen.

---

## 4. Where the money actually comes from

This is the finding that matters most for how the deal should be structured.

| | Year 1 | Year 3 |
|---|---|---|
| Interest income (£) | 797,070 | 13,757,960 |
| Card interchange (£) | 262,501 | 1,522,500 |
| Account fees (£) | 0 | 0 |
| **Interest as % of core revenue** | **75%** | **90%** |

Dream Bank is a spread business. It takes deposits, passes nothing back to the customer (pass-through is set
to 0% for both personal and business savings), and earns the Bank of England base rate less ClearBank's 35bps.

That means the value of the whole enterprise is set by the Monetary Policy Committee, not by the brand, not
by the product, and not by anything management can control. Their own risk register says it: a 100bp cut
removes roughly £4m of Year 3 EBITDA. The sensitivity tab confirms it - a 30% cut to the net rate takes Year
3 EBITDA from £11.5m to £7.4m, a bigger swing than any other driver including account growth.

**Rate check.** The model uses 3.70%, sourced "BoE, March 2026". The actual Bank Rate is 3.75%, held on 30
July 2026 on a 6-3 vote, next decision 17 September. So the model is marginally conservative on the level,
which is fine. But a 6-3 vote is a committee leaning toward cuts, and the model's single largest revenue
line is a one-way bet on rates staying where they are for three years.

---

## 5. The growth assumption, which is the whole model

Launch month, March 2027: **10,000 business accounts and 2,500 personal accounts open on day one.**

The model annotates this itself: that is 13% of the current HelpBnk user base converting immediately. Not
signing up over a quarter. In month one.

For context, 40,000 business current accounts in a first year from a standing start would be among the
fastest business banking ramps the UK has seen. Starling took years to reach that kind of scale.

Two structural tells in the shape of the curve:

1. **After the month-one spike, growth is a dead straight line.** 682 personal and 2,727 business accounts
   every single month for eleven months. Straight lines are placeholders, not forecasts. Nobody has modelled
   a funnel here.
2. **Year 3 growth triples with no corresponding spend.** New business accounts jump from 3,333/month to
   10,000/month in April 2029, while marketing stays at £5,000/month.

**The acquisition cost implied.** Marketing is £60,000 a year, every year. Year 3 adds 150,000 net accounts.
That is **40 pence per account acquired**. UK challenger banks typically spend £20 to £50 or more. The model
is assuming an acquisition cost roughly fifty times below market and not saying so out loud.

That gap is Bear and Simon. It is the largest single input in the model and it is the only one with no price
against it.

---

## 6. Unit economics

| Per account, per year | Year 1 | Year 2 | Year 3 |
|---|---|---|---|
| Revenue | £33.91 | £55.32 | £84.31 |
| ClearBank cost | £46.89 | £35.19 | £27.37 |
| Operating cost | £28.51 | £20.48 | £14.40 |
| **Total cost** | **£75.41** | **£55.67** | **£41.77** |
| **Margin** | **(£41.50)** | **(£0.35)** | **£42.54** |

Every account loses roughly £41 in Year 1 and breaks even in Year 2. Year 3 only works because average
business balances are assumed to rise from £600 to £3,000, a five-fold increase, with no stated mechanism.

To their credit, the model notes that the average UK business account holds about £30,000, so £3,000 is
conservative against the market. But the personal side has a tension: it models 8 FPS transactions a month
including "salary in, rent, transfers, DDs", which describes a primary current account, while assuming a
£300 balance, which describes a secondary one. It should pick one. If these are secondary accounts, the
balance growth that drives Year 3 does not happen.

---

## 7. Six things I would put in writing before any cheque

**1. ClearBank's pricing has expired.** The commercial proposal was valid to 31 March 2026. Every cost line
in this model flows from terms that lapsed four months ago. The model marks this HIGH risk itself.

**2. £180,000 is already spent.** The implementation fee was paid on a signed Letter of Commitment dated 15
May 2026. Money and contractual commitment are already out the door, ahead of the round.

**3. The Mandated Minimum Balance is missing entirely.** The signed Letter of Commitment requires an MMB
transfer under the CCT, and the model says plainly that no amount for it appears anywhere. That is an
unquantified cash requirement sitting outside a £4m raise. Ask ClearBank for the figure. It could be
material enough to change the raise.

**4. Card interchange may be worth nothing.** The 0.10% net rate is an explicit estimate; ClearBank may
retain all of it. That is £262k in Year 1 and £1.52m in Year 3 that may not exist.

**5. There is an internal contradiction on the fee scenario.** On the same row of the Assumptions tab, one
note says £2 personal plus £2 business adds about £750k in Year 1, £1.85m in Year 2, £4.35m in Year 3.
Another note on that same row says Year 1 +£1.56m and Year 2 +£3.0m. The first reconciles to the model
(31,250 average accounts x £2 x 12 = £750k). The second does not. Someone ran the scenario twice and left
both answers in. Ask which is live.

**6. There is still no Dream Bank company.** Verified at Companies House on 29 July 2026: the only UK entity
is HELPBNK UK LIMITED (14844480), incorporated May 2023, SIC 73110 advertising agencies, with Simon Squibb
as sole director and sole person of significant control holding 75%+. No Dream Bank, DreamFund, Dream Media
or DreamBrew entity exists. This model is titled "Dream Bank" on every sheet and raises £4m for a company
that has not been incorporated. That needs resolving before, not after.

---

## 8. Phase 2/3 - where the profit is, and where the evidence is thinnest

Year 3 combined EBITDA of £11.5m includes £3.86m of margin from ten products that do not exist yet:
insurance (four lines), business loans, invoice factoring, accounting, mortgages, credit cards and legal.

Every one assumes a launch date is hit, an attach rate lands, and a white-label or referral partner is
signed. None of those partners is named. Four of the ten lose money even at maturity in the model's own
numbers: invoice factoring (-£85k in Year 3), credit cards (-£4.6k in Year 3), mortgages (-£93k in Year 2),
and three more that are loss-making in Year 1.

This is a roadmap presented as a forecast. It is reasonable as a direction of travel. It should not carry
a third of the Year 3 profit in a document used to raise money.

---

## 9. What this means for Bear Grylls Ventures

**The model has no line for Bear.** No ambassador fee, no equity charge, no marketing spend attributable to
acquiring the accounts his reach delivers. He is simultaneously the single largest assumption in the
business and absent from its cost base.

That is the whole negotiation, and it points the same way it did before the financials arrived. Bear's reach
is the input this business monetises. It should be paid out of the revenue it creates, not swapped for a
minority stake in a company that does not exist yet and is underfunded on its own numbers.

**Recommended shape, in order:**

1. **Revenue share on attributable accounts.** Simplest, needs no new entity and no valuation fight. If
   Bear's audience opens the accounts, the deposits those accounts hold generate interest income, and a
   share of that flows back. It scales with exactly the thing he is providing.
2. **Name and likeness licence with a creditable annual minimum.** A floor costs a genuine performer nothing
   and prices the risk that the growth curve does not land. Credit it against the revenue share so they
   never pay twice.
3. **Equity, parked.** Not because it is wrong in principle, but because there is nothing to hold it. Revisit
   when a Dream Bank entity exists, the ClearBank terms are re-signed, and the MMB is quantified.

If a cheque is written at all, £100k against a £4m requirement buys a small position in a round that will
need a follow-on. The stronger play is to be paid for the input rather than pay to supply it.

---

## 10. Fair credit where it is due

This is a better model than most that arrive at a family office. It labels its own estimates, distinguishes
hardcoded inputs from assumptions, carries a genuine risk register that raises the hardest questions against
itself, and documents a material error it previously made and corrected. Guy Davis has done real work here.

The problems above are not fabrications or spin. Almost every one of them is flagged somewhere inside the
model itself. The issue is that the flags have not yet been resolved, and the raise is being marketed before
they are.

---

*Junior, Executive Assistant to Jesse Grylls. Analysis based solely on the model as supplied on 31 July 2026
and Companies House records verified 29 July 2026. Figures are management projections, not audited.*
