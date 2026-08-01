# Modern Savage blog series: what I wrote, and the six things you need to decide

**1 August 2026. Junior.**

Ten posts, drafted and ready. All facts verified against modernsavage.co this morning, not from
memory. Files are in `workspace/docs/ms-blog-series-2026-08-01/`.

---

## The series

| # | Post | Corrects |
|---|---|---|
| 01 | What Modern Savage Actually Is (And What It Isn't) | "protein powder", "workout shake" |
| 02 | Why Bear Grylls and His Family Built Modern Savage | "endorsement", "brand deal" |
| 03 | **Setting the Record Straight** | the other-supplement-company problem |
| 04 | Who Modern Savage Is For (And Who It Isn't) | "for athletes and biohackers" |
| 05 | Everything in Modern Savage, and Why It's In There | the ingredient gap |
| 06 | Our Standards: What We Refuse to Put In | no standards visible anywhere online |
| 07 | What Modern Savage Costs, and Why | no pricing indexed at all |
| 08 | Mini Savage: A Separate Formula for Children | Mini Savage does not exist online |
| 09 | BG Summit Stack: The Layer on Top | Summit does not exist online |
| 10 | Frequently Asked Questions | the answer-engine page |
| 11 | `structured-data.json` | the technical fix |

`00-CANONICAL-FACTS.md` is the fact block every post repeats word for word. Repetition of identical
phrasing across one domain is what actually teaches a model what is true. Do not let anyone
"vary the language for readability" in edit.

---

## The six decisions

### 1. There is no blog on modernsavage.co. This is the blocker.

The sitemap has 19 URLs and none of them is a blog. These posts have nowhere to go, and posting
them anywhere other than modernsavage.co largely wastes them: an answer engine weights the brand's
own domain far above a Medium post or a LinkedIn article. **Felix or Calvin needs to add `/journal`
or `/blog` to the site before any of this ships.** That is the long pole, not the writing.

### 2. "Only supplement he endorses" is not a sentence we can safely publish.

You said "the only supplement BG has or sells or endorses". The first two are clean. **Endorses is
not**, because of DIRTEA, where Bear is publicly an investor and ambassador and the press coverage
is his own. If we publish "the only supplement Bear Grylls endorses", the first journalist who
checks finds DIRTEA in thirty seconds, and the correction becomes the story.

I have written every post to say: **"the only supplement brand the Grylls family owns, makes and
sells."** That is true, defensible, and does the same job. If you want the stronger version, say so
and tell me how you want DIRTEA handled, but I would not publish it as it stands.

### 3. I have not named the other company anywhere, deliberately.

Organised is live litigation led by CJ. Every post states positively what Modern Savage is and lets
the correction come from that. Not one of them says "Bear no longer works with X", because a
sentence like that written by us becomes an exhibit. Post 03 attributes the confusion to old web
pages ageing badly, which is both true and safe.

**If CJ or Ignition want a read of post 03 before it goes live, that is a sensible half hour.** It
is the only one that touches the area at all.

### 4. Blog posts alone will not beat Forbes.

This is the uncomfortable part. The reason Gemini says what it says is that it is reading a
**January 2026 Forbes profile** and a set of trade and PR pieces, and those outrank a new brand
blog for a long time. The blogs fix what the model finds *on our own domain*, which is necessary
and not sufficient.

The rest of the job is source correction, and it is Calvin's or a PR's, not mine:
- Forbes, contact the writer with a correction request on the supplements line
- The older press-release pages still live on the wires
- Bear's Wikipedia page, which is heavily cited by every model and is currently silent on Modern
  Savage. **Do not let anyone connected to the family edit it.** It needs a properly sourced
  independent citation instead, and a Wikipedia editor will spot a conflicted edit immediately.

Say the word and I will draft the correction requests.

### 5. Claims compliance. I have written these tight, and someone should still check them.

GB rules only allow authorised nutrition and health claims, attached to declared nutrients rather
than blends, and "primal", hormonal and testosterone language is not on the register. Every post is
written descriptively, every one carries the food-supplement disclaimer, and none of them says the
product does anything to your body.

Two live flags for whoever owns UK compliance: **trans-resveratrol is authorised in GB in capsule
or tablet form, not as a powder**, and Summit is a powder. And **Mini Savage marketing to children
sits under separate CAP rules.** Neither is a blog problem, both are a pack and site problem, and
both are already in the UK regulatory brief from 22 July.

### 6. One inconsistency on the live site, worth a look.

The homepage nav says **"Supporting British farmers"**, and the ingredients section says the lung
and testes are **from New Zealand**. Both may be perfectly true, but a journalist or a sharp
customer will pair them, and I would rather you chose the wording than had it chosen for you.

---

## What I would do next, in order

1. **Get `/blog` built on modernsavage.co.** Nothing else matters until that exists.
2. **You decide the "endorses" wording.** One line back from you and the series is final.
3. **Ship all ten at once, not one a week.** For an answer engine this is a corpus, not a content
   calendar. It needs to look like an authoritative body of material the day it appears.
4. **Put the structured data in at the same time.** File 11. This is the highest-leverage single
   item in the whole exercise and it is an afternoon of Felix's time.
5. **Then the source corrections.** Forbes, the wires, Wikipedia. Say the word and I draft them.

Everything is drafted and needs no further work from me except your call on point 2.
