# Technical SEO and AI discoverability: mostly excellent, one real bug

I audited this expecting to find the usual mess. I did not, and it is worth saying so plainly before
the one thing that is wrong.

---

## What is already right, and it is a lot

- **Titles, meta descriptions, OG tags, canonical URLs**: all present and well written across the
  homepage, product pages and handbook. One H1 per page.
- **Structured data is rich**: Organization, Brand, Person, WebSite, Product, Offer,
  MerchantReturnPolicy, OfferShippingDetails, ShippingDeliveryTime. Six JSON-LD blocks on a product
  page. Most brands manage none of this.
- **Full sitemap**, 20 URLs, including individual recipe pages.
- **AI crawlers are explicitly allowlisted**, individually: GPTBot, OAI-SearchBot, ChatGPT-User,
  ClaudeBot, anthropic-ai, Claude-Web, PerplexityBot, Perplexity-User, Google-Extended,
  Applebot-Extended, CCBot, Meta-ExternalAgent.
- **There is an `llms.txt` and an `llms-full.txt`**, and they are good. Accurate, well written, with
  product detail down to scoop weights.

Somebody has done serious work here and it deserves acknowledging rather than a list of improvements.
**The technical foundation for the UK content play I recommended is already in place**, which means
articles published on this domain will actually rank rather than sitting in a badly built site. That
raises the return on the content work rather than lowering it.

---

## The one real bug: our structured data says we ship to 28 countries. We ship to two.

The `MerchantReturnPolicy` inside the Product schema on `/shop/modern-savage` declares
`applicableCountry` as:

> GB, US, **CA**, AT, BE, BG, HR, CZ, DK, EE, FI, FR, DE, GR, HU, IE, IT, LV, LT, LU, NL, PL, PT, RO,
> SK, SI, ES, SE

That is the UK, the US, Canada and 25 EU member states.

**The shipping page says something completely different**, and says it clearly:

> We ship Modern Savage to the UK and the United States.

And, specifically about Canada:

> A note for our Canadian customers: pre-orders are not open in Canada yet, and **no Canadian address
> can be entered at checkout for now.** Canadian parcels have to cross the border from our US
> warehouse, which is slow and can attract customs duty, so we would rather open Canada once we are
> dispatching from stock than take your money.

That Canada note is a good, honest, customer-first decision. **And the structured data quietly
contradicts it.**

### Why this matters more than a normal markup error

Structured data is not decoration. It is the machine-readable version of the site, and it is what
Google Shopping, rich results and every AI assistant on that allowlist actually read. We have gone to
real trouble to make this site legible to AI crawlers, which means **this particular error is
amplified by the very thing that was done well.**

The likely outcome is a Canadian or EU customer being shown Modern Savage as available and returnable
in their country by Google or an AI assistant, clicking through, and finding they cannot enter their
address. That is a wasted visit, and for Canada specifically it undoes a decision that was taken
deliberately to avoid exactly that experience.

**The fix is a one-line change** to the country array: `GB` and `US`. Ten minutes, including
redeploying.

---

## A smaller thing worth noticing

`llms.txt` carries product detail that the customer-facing site does not:

> Mini Savage: built for children. Same standards as the adult blend, dosed for small bodies, with
> bovine colostrum. **22g scoop, 616g.**

The `/ingredients` page has no entry for Mini Savage at all. So **the file written for AI crawlers is
currently more informative about our children's product than anything a parent can read.**

That is an easy win rather than a criticism. The content exists and is accurate. It just needs to be
on the page a customer sees, which is the same point made in the commercial findings.

---

## Two things I would add, both small

1. **No `aggregateRating` or `review` in the Product schema**, because there are no reviews. That is
   why we get no star ratings in search results, and stars are one of the largest single influences on
   click-through in a shopping listing. This is the structured-data expression of the social proof gap.
   Reviews cannot exist before the product ships, so the honest sequence is to plan the review capture
   into the October dispatch email rather than to bolt it on later.
2. **The Offer block hard-codes `priceCurrency: USD, price: 79.00`** on a site that serves UK
   customers in pounds. A UK searcher may be shown a dollar price that does not match the page. Worth
   emitting the correct currency per region if the platform allows it.
