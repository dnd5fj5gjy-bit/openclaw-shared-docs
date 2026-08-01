# Dream Bank - Financial Analysis

**1 August 2026.** Source: "Dream Bank Financial Model.xlsx", sent by Jack Whettingsteel 31 July 2026.
Ten sheets, monthly build to March 2030. Every figure below is read from the model or calculated from it.

---

## 1. What it is

Dream Bank is not a bank. It has no banking licence and is not applying for one. It is a customer-facing
brand sitting on top of ClearBank, which holds the licence, the accounts and the money. ClearBank is the
supplier for everything: the accounts, the payments, the identity checks, the platform.

Practically, Dream Bank owns the app, the brand and the customer relationship. ClearBank owns the banking.

---

## 2. How it makes money

One line does almost all of it. Customers open free accounts and leave money in them. Dream Bank earns
interest on those balances and passes none of it back. Savings pass-through is set to zero for both
personal and business.

| Revenue source | Year 1 | Year 3 | Share of Y3 |
|---|---|---|---|
| Interest on deposits | £797,070 | £13,757,960 | 90% |
| Card interchange | £262,501 | £1,522,500 | 10% |
| Account fees | £0 | £0 | 0% |
| **Core total** | **£1,059,571** | **£15,280,460** | |

Everything else in the plan, the free banking, the community, the mission, is the mechanism for gathering
deposits. There is no paywall and no subscription anywhere in the model.

A second layer arrives later: selling insurance, loans, accounting and legal services to the account base.
That is ten products, none built, no partners named, first revenue late 2027. It contributes £4.8m of
Year 3 revenue and £3.9m of Year 3 margin. It should be read as a roadmap, not a forecast.

**Card interchange carries a warning in the model itself.** The 0.10% rate is an explicit estimate and
ClearBank may retain all of it, which would remove £2.4m of revenue across three years.

---

## 3. What ClearBank takes

This is the heart of it, and the model does not present it in one place.

ClearBank is paid twice. First it keeps 35 basis points of the interest before Dream Bank sees anything.
Then it invoices for the platform, per account, per transaction and per identity check.

### The invoiced fees

| Fee line | Year 1 | Year 2 | Year 3 | 3-year total |
|---|---|---|---|---|
| FPS transaction fees | £786,437 | £1,661,600 | £3,264,000 | £5,712,037 |
| Platform licence | £360,000 | £540,000 | £540,000 | £1,440,000 |
| KYC / KYB onboarding | £170,500 | £170,500 | £511,500 | £852,500 |
| Account fees | £94,500 | £216,250 | £423,000 | £733,750 |
| BACS transaction fees | £54,000 | £124,200 | £222,800 | £401,000 |
| **Total invoiced** | **£1,465,437** | **£2,712,550** | **£4,961,300** | **£9,139,287** |
| Plus retained interest margin | £82,051 | £372,337 | £1,416,260 | £1,870,648 |
| **Total ClearBank take** | **£1,547,488** | **£3,084,887** | **£6,377,560** | **£11,009,935** |

A further £180,000 implementation fee was paid up front, on a Letter of Commitment signed 15 May 2026.

### What that means

**Fees as a share of Dream Bank's interest income: 184% in Year 1, 75% in Year 2, 36% in Year 3. Roughly
50% across the three years.**

Year 1 is the striking one. Transaction fees alone, FPS plus BACS, come to £840,437 against £797,070 of
interest income. ClearBank's payment charges exceed the entire interest line before the platform licence,
the account fees or the identity checks are added. The model flags this itself in a note: *"Transaction
costs alone exceed interest income in Year 1 at the current account mix."*

Taking the three years together: customer deposits generate roughly **£20.0m of gross interest**.
ClearBank ends up with **£11.0m of it, about 55%**. Dream Bank retains **£9.0m, about 45%**, and out of
that has to pay its own staff, offices, marketing and legal, which run to £5.1m. The residual is about
£3.9m over three years, before the card interchange and the Phase 2/3 products.

### The structural problem inside those fees

The largest ClearBank line is not the licence. It is **per-transaction payment fees, £5.7m over three
years**, and those scale with how much the accounts are *used*.

Revenue, however, comes from how much money *sits still*. So the economics reward a dormant account
holding a large balance and penalise an active one. A busy business account making thirty payments a
month costs Dream Bank money while contributing the same interest as an idle one holding the same balance.

That sits awkwardly against a product aimed at entrepreneurs actively running businesses.

**Two mitigations, both real.** Transaction pricing tiers down with volume, from 9p to 5p per payment, so
unit costs improve at scale. And per-account fees fall from 30p to 20p. The model applies both correctly.
But Years 2 and 3 carry committed minimum volumes, 30,000 accounts a month then 75,000, paid upfront
regardless of actual accounts. In the base case those commitments are comfortably exceeded. In a downside
they become a fixed bill for accounts that were never opened.

---

## 4. The plan, in numbers

| | Pre-launch | Year 1 | Year 2 | Year 3 |
|---|---|---|---|---|
| Accounts (year end) | 0 | 50,000 | 100,000 | 250,000 |
| Average deposits | 0 | £23.4m | £106.4m | £404.6m |
| Combined revenue | 0 | £1.29m | £5.88m | £20.04m |
| **Combined EBITDA** | **(£0.96m)** | **(£1.37m)** | **£0.84m** | **£11.50m** |

Peak cash need £2.63m in September 2028. Monthly breakeven 17 months after launch. Cash repaid July 2029.

**Funding.** The model calculates a requirement of £3.96m in the base case and £5.19m under stress. The
planned raise is £3.5m. That is 0.88x cover in the base case and 0.67x under stress. The model marks this
HIGH risk against itself. On its own arithmetic the round is short before it closes.

---

## 5. The growth assumption

In launch month, March 2027, the model opens **10,000 business accounts and 2,500 personal accounts**. The
sheet annotates it: that is 13% of the current HelpBnk user base converting immediately, in month one.

After that spike, growth is a perfectly straight line, 682 personal and 2,727 business accounts every month
for eleven months. Straight lines are placeholders. No funnel, no conversion rate and no channel mix sits
behind them. In Year 3 the monthly rate triples again with nothing changing to cause it.

**Marketing is £5,000 a month, flat, across all three years.** Against 250,000 accounts that is about
**40p to acquire a customer**. UK challenger banks typically spend £20 to £50. The plan therefore assumes
that founder-led organic reach does essentially all of the customer acquisition for free, and there is no
budget anywhere in the model to buy growth if that reach underdelivers.

For scale, 40,000 business current accounts in a first year would be among the fastest ramps in UK banking
history.

---

## 6. Rate sensitivity, which is the real risk

With no account fees, interest is 90% of Year 3 core revenue. The Bank of England therefore sets the value
of this business, and management cannot influence it.

The asymmetry matters: **revenue moves with rates, ClearBank's fees do not.** Payment and account charges
are fixed in pence and stay exactly where they are.

| Base rate | Y3 interest income | Y3 combined EBITDA |
|---|---|---|
| 3.75% (model) | £13.76m | £11.50m |
| 2.00% | £6.68m | £4.42m |
| 1.00% | £2.63m | £0.37m |

At a 1% base rate the business is at breakeven even if every growth assumption lands perfectly.

The Bank held at 3.75% on 30 July 2026, but on a 6-3 vote, with the next decision on 17 September. A
committee splitting that way is a committee leaning toward cuts. The model's own risk register puts this
first and says a 100bp cut removes about £4m of Year 3 profit.

*A note on the rate cells: the Assumptions tab lists the base rate as 3.70% sourced "March 2026", while
the net rate it actually uses, 3.40%, implies a 3.75% base less 35bps. The number driving revenue matches
today's actual rate, so the revenue is right and the label is stale.*

---

## 7. Open items

Six things are unresolved, and five of them are flagged inside the model by its own authors.

1. **ClearBank's pricing has expired.** The commercial proposal was valid to 31 March 2026. Every cost line
   in this analysis flows from lapsed terms. Marked HIGH risk.
2. **A Mandated Minimum Balance is missing entirely.** The signed Letter of Commitment requires an MMB
   transfer, and the model states plainly that no amount for it appears anywhere. That is an unquantified
   cash requirement sitting outside the £4m.
3. **Card interchange is a guess.** ClearBank may keep all of it. £2.4m of three-year revenue at risk.
4. **The round is short of its own requirement.** £3.5m against £3.96m base, £5.19m stress.
5. **Contradictory fee-scenario notes.** Two notes on the same row of the Assumptions tab give different
   answers for what charging £2 a month would add. One reconciles to the model, the other does not.
6. **No Dream Bank company exists.** Verified at Companies House 29 July 2026: the only UK entity is
   HELPBNK UK LIMITED (14844480), incorporated May 2023, registered as an advertising agency, with Simon
   Squibb as sole director and sole controlling shareholder at 75% or more. There is no Dream Bank,
   DreamFund, Dream Media or DreamBrew company. The model raises £4m for an entity not yet incorporated.

The model also contains **no valuation, no share price, no cap table and no mention of equity anywhere.**

---

## 8. Can this actually become big?

Yes, but the size is set by two numbers, and neither is controlled by Dream Bank.

**The case for scale is real.** Deposit economics improve sharply with volume. ClearBank's fees tier down
while interest income scales linearly, so the gap widens in Dream Bank's favour the larger it gets. At
£600m of deposits the model shows £11.5m of profit. At £2bn, interest income alone would be roughly £68m
against a fee base growing far more slowly. This is a genuine compounding machine if the deposits arrive.
Distribution is also genuinely unusual here, and unusual distribution is the hardest thing to buy.

**The case against is equally real.** The business is a leveraged bet on the base rate holding, with a
single supplier who currently takes 55% of the gross interest and whose pricing has expired. Growth is a
straight line with no funnel behind it, acquisition is costed at roughly fiftieth of the market rate, and
a third of the Year 3 profit comes from ten products that do not exist. There is no entity, no valuation
and the round is underfunded on its own numbers.

**The honest summary.** This is a plausible business with a credible route to being large, wrapped in a
plan that is not yet finished. The economics work at scale and fail below it, and the point at which they
turn is a long way out: seventeen months of trading losses and £2.6m of cash before the curve bends.

**Four things would have to be true for the big outcome.** Deposits reach hundreds of millions. Rates stay
near where they are for years. ClearBank re-prices without taking more. And the acquisition happens
organically, because there is no money in the plan to pay for it. Each is individually plausible. All four
together is a demanding ask, and the model prices only the version in which they all hold.

---

## 9. Credit where it is due

This is a better model than most that reach a family office. It separates hard inputs from assumptions,
labels its own estimates, carries a real risk register that raises the hardest questions against itself,
and documents in plain English a material error a previous version made, where three annual deficits were
wrongly summed to produce a £17m raise against a real need of about £2.1m.

Almost every criticism in this document is already flagged somewhere inside the spreadsheet. Guy Davis has
done honest work. The issue is not the modelling. It is that the raise is being marketed before the flags
have been resolved.

---

*Prepared by Junior, Executive Assistant to Jesse Grylls. Based on the model as supplied 31 July 2026,
Companies House records verified 29 July 2026, and the Bank of England rate decision of 30 July 2026.
Figures are unaudited management projections.*
