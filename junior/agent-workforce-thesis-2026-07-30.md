# The Non-Human Workforce: what to build, and what just got taken

**Built for Jesse, overnight 30 Jul 2026. Internal. Nothing sent to anyone.**

You merged two of my ideas last night: spend control for agents, and the employment layer for agents. I said I would write it up properly. I did, and the research changed the answer, so this is not the write-up I expected to hand you.

---

## Five lines you can say out loud

1. The thing we merged last night got shipped by Okta and Microsoft in April, while we were talking about it.
2. So the control plane is gone. We would be the fourth identity vendor into an enterprise that already bought two.
3. But the insurance layer I called the endgame got better in the same three months, because the big carriers are running away from it.
4. Nobody can price agent failure, because no one owns a record of what agents actually cost companies when they go wrong.
5. That record is the asset. Not the control plane, not the insurer. The loss data in between.

---

## 1. Why the merged idea is dead

I need to be straight with you rather than defend last night's answer.

- **Okta for AI Agents went generally available on 30 April 2026.** Its stated scope is the full agent lifecycle, "from registration to eventual retirement": own identity, own permissions, own audit trail, own delegation relationship to a human principal. It discovers shadow agents, assigns each one a human owner, and governs access over time.
- **Microsoft Entra Agent ID also reached GA in April 2026**, extending Conditional Access, Identity Protection and Privileged Identity Management to non-human identities.
- Okta has deliberately positioned as the agent layer *on top of* whatever human IdP you already run, including Entra. That removes the "rip and replace" objection that normally protects a startup.

That is our merged product, described in their words, generally available, sold through an enterprise channel we do not have.

I also told you last night that the corporate spend side was unbuilt. **That was wrong and I should correct it plainly:** Ramp has shipped Agent Cards (single-use, merchant-scoped, per-agent limits), Corpay has shipped an Agent Card for supplier payments and procurement, and Oobit launched cards issued per agent as a first-class spender. On the standards side, Google's AP2 hit v0.2 in April 2026 and was donated to the FIDO Alliance, with authority carried as W3C Verifiable Credentials in three signed mandates. The "mandate attached to an agent identity" primitive I described as our unique insight is now a governed open standard with 60+ backers.

**Conclusion: do not build this.** Both halves closed inside four months. The merge was a good instinct and it is now somebody else's product.

---

## 2. What opened while that closed

Here is the part worth your weekend.

The insurance market is actively *withdrawing* from agent risk:

- **AIG, WR Berkley and Chubb are excluding AI mistakes** from commercial policies in 2026. A January 2026 ISO form lets carriers strip generative-AI bodily injury, property damage and advertising injury out of standard general liability.
- **Verisk was reported on 10 July 2026 to be weighing new exclusions for agentic AI risks.** Verisk writes the forms the industry runs on. (Headline verified; the article itself is paywalled and I have not read the full text.)
- Only a handful of standalone AI liability products exist worldwide. **Armilla** is the sole pure-play MGA, a Lloyd's coverholder backed by Chaucer, Axis and Convex, now at $25m+ limits, paired with Chaucer cyber/tech E&O as "Vanguard AI" in February 2026. **Testudo** began underwriting US mid-market in early 2026, also Lloyd's-backed.
- One in five insurance professionals said their insureds have **already taken losses linked to AI risk** (Gallagher, 2026).

Read those together. Demand exists and is realising as actual losses. Supply is contracting. That is not a market with no appetite; that is a market that **cannot price the thing**.

And the reason is specific. A June 2026 paper on trace-economic underwriting states the gap outright: there is **no established dataset of actual losses from autonomous AI agents in production**, no standardised reliability benchmarks across deployment contexts, and **no actuarial base** from which to model loss distributions. Armilla's own product works around this elegantly, by paying out only when a model underperforms **pre-agreed benchmarks**. That insures *model performance*. It does not insure *what the agent did with money, customers or commitments*, because nobody has the loss experience to price that.

---

## 3. The actual gap, stated precisely

Two industries each hold half of what underwriting needs, and neither has a reason to join them:

| Who | Holds | Missing |
|---|---|---|
| Observability vendors (Arize, Braintrust, LangSmith, Langfuse, AgentOps) | Execution traces, at volume, OpenTelemetry-standardised | Any idea what a bad trace *cost* |
| Insurers and their MGAs | Claims and realised loss | Any visibility into the agent behaviour that caused it |

**The join is the asset: agent action → realised financial loss.**

Nobody builds it because of org shape, not difficulty. Observability is sold to engineering leaders who are measured on latency and eval scores. Loss data sits with finance, legal and risk. The two never meet inside the customer, so no vendor is incentivised to carry a record across the boundary.

Whoever assembles that record becomes the party that lets carriers re-enter the market. It is the same structural lock-out I described last night, but sitting one layer lower, where it is still available.

---

## 4. The honest test, which you should apply before anything else

This is the question that decides it, and I am not going to soften it.

**How do you and Felix see enough incidents to matter?**

Underwriting needs base rates, which means volume and diversity. The control plane would have delivered that, and Okta now owns it. So the answer has to come from somewhere else, and there are only three candidates:

1. **Sit under the observability layer.** They have the traces and no route to the money. A join partnership is plausible and cheap to test, and it is a dependency on somebody else's customer relationship.
2. **Go direct to the demand side.** Carriers and MGAs need this to write business at all. Armilla, Testudo and Verisk are commissioning parties, not just acquirers. This is the shortest path and it means selling into insurance, which is slow and relationship-led.
3. **Start with an incident ledger, not a data platform.** Standardised, structured post-incident records of autonomous action failures, contributed by companies deploying agents, in exchange for benchmark reporting they cannot get elsewhere. This is how every actuarial base in history started, including cyber.

Route 3 is the two-person version, and it is the one where being Jesse is not obviously an advantage. **That is the weakness in this idea and you should weigh it.** Insurance data is a credibility market, not a brand market. It is also the reason nobody has done it: it looks like unglamorous plumbing for the first eighteen months.

---

## 5. v1 scope, if you go

Small enough for two people. Deliberately not a platform.

- A **taxonomy of autonomous-action failure**: wrong recipient paid, unauthorised commitment made, wrong advice given at scale, unbounded spend loop, data disclosed, action taken outside mandate. Six to ten classes with clean definitions. This artefact alone has value; the industry has no shared vocabulary.
- An **incident schema** that captures trace context and financial consequence in one record, aligned to OpenTelemetry on the trace side so it ingests from what teams already run.
- A **contribute-to-see-benchmarks loop**: a company files structured incidents, gets a comparative report on how its agent fleet fails relative to peers. That report is the product people say yes to; the dataset is what you are actually building.
- A **quarterly loss report**, published. This is the credibility engine and the cheapest possible marketing into insurance. Cyber's actuarial base was built this way.
- Explicitly **not** in v1: no underwriting, no capital, no control plane, no identity, no policy issuance.

**Likely acquirers, in order of fit:** Verisk and Moody's (they buy risk data as their core business), Munich Re and Swiss Re (both already underwrite tech performance risk and need agentic base rates), Armilla or Testudo (the join makes their book pricable), then Okta or Microsoft (attaches loss context to a control plane that currently only proves an agent had permission, not that granting it was wise).

**The float endgame you keep circling:** once you hold the base rate, you become the MGA, then the capacity. Premium held is float, and that is the only genuinely passive structure in business, as I argued on Tuesday. Honest caveat: Armilla needed a Lloyd's coverholder arrangement and named syndicate capital to do it. That path is real but it is regulated, and it is years three to five, not year one.

---

## 6. What I recommend

Do not build the control plane. It is gone, and losing four months to discovering that in the market would be the expensive version of this document.

Spend one week, not one weekend, testing route 2 before committing to anything. Specifically: get on a call with Armilla and with one Lloyd's syndicate writing tech E&O, and ask a single question. *If you had a credible loss-experience dataset for autonomous agent action, would you write the book you are currently declining?* If the answer is yes, this is a business and the data is the whole company. If they tell you they would still decline because the tail is uncapped regardless of data, then the gap is structural rather than informational, and I will have saved you a build.

**The one decision only you can make:** whether you are willing to spend eighteen months building unglamorous risk plumbing to reach a passive, sellable asset, when everything else in your portfolio is big, visible and story-driven. That is a taste question, not an analysis question, and I got it wrong seven times yesterday by trying to answer it for you.

---

### Sources
- Okta for AI Agents (GA 30 Apr 2026): https://www.okta.com/products/govern-ai-agent-identity/ · https://www.okta.com/blog/ai/agent-idp-identity-stack/ · https://www.okta.com/identity-101/ai-agent-lifecycle-management/
- Microsoft Entra Agent ID: https://learn.microsoft.com/en-us/entra/agent-id/what-is-microsoft-entra-agent-id
- Ramp agent spend controls: https://ramp.com/blog/ai-agent-spending-controls · Corpay Agent Card: https://e-commerce.news/story/corpay-launches-agent-card-for-ai-business-payments · Oobit Agent Cards: https://newsroom.oobit.com/software-is-the-new-employee-now-it-has-a-corporate-card/
- AP2 / W3C Verifiable Credential mandates, v0.2 and FIDO donation: https://ap2-protocol.org/ · https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol · https://fidoalliance.org/fido-alliance-to-develop-standards-for-trusted-ai-agent-interactions/
- Carrier withdrawal and standalone AI liability market: https://www.theinsurer.com/program-manager/news/standalone-ai-liability-market-takes-shape-with-underwriting-discipline-key-to-2026-04-24/ · https://www.insurancebusinessmag.com/us/news/technology/insurers-face-hidden-ai-liability-as-agent-risks-multiply-582433.aspx
- Verisk weighing agentic exclusions, 10 Jul 2026 (headline only, paywalled): https://www.theinsurer.com/ti/news/verisk-weighs-new-exclusions-for-agentic-ai-risks-2026-07-10/
- Armilla / Lloyd's / Chaucer: https://www.armilla.ai/ai-insurance · https://www.lloyds.com/insights/lloyds-lab/programmes-and-initiatives/lloyds-lab-accelerator/alumni/armilla-ai
- Trace-economic underwriting, no loss dataset / no actuarial base (Jun 2026): https://arxiv.org/pdf/2606.16465 · Insurance of Agentic AI: https://arxiv.org/html/2606.05449v1
- Non-human identity funding context (Oasis ~$195m total, GitGuardian $50m): https://www.scworld.com/brief/oasis-security-raises-120-million-for-non-human-identity-management · https://siliconangle.com/2026/02/11/gitguardian-raises-50m-expand-non-human-identity-ai-agent-security/
