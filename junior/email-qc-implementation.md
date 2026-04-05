# Email QA Implementation

## What changed
I implemented a stricter outbound email QA workflow for Junior so drafts are cleaned, checked, saved as a canonical version, and blocked from send unless they pass QA and a human explicitly approves.

## Recommendation summary

### Recommended stack
**Primary recommendation: LanguageTool in self-hosted server mode, with local rule-based QA in front of it.**

Why:
- The local rule layer catches Jesse-specific failures immediately, especially em dashes, shorthand, repeated punctuation, weak openings, and missing signature.
- LanguageTool adds broad grammar and style coverage through an HTTP API that is easy to call from Python.
- Self-hosting keeps drafts private and avoids sending email content to a third-party SaaS endpoint.
- It is practical to stub today and fully enable later once Java and the server process are available.

### Tool research

#### 1) LanguageTool
**Pros**
- Real HTTP API with JSON responses.
- Can be self-hosted or used as a hosted API.
- Strong fit for a pre-send hook.
- Supports disabling or tuning rules.
- Good privacy story when self-hosted.
- Public docs mention on-premise options, a 60,000 character request limit, and no text storage.

**Cons**
- Self-hosted mode requires Java.
- Server startup adds operational overhead.
- Hosted API pricing/details are less frictionless than pure developer-first API products.
- Rule quality is solid but not perfect, so it should sit behind the custom email_qc rules, not replace them.

**Cost / dependencies / latency**
- Dependency: Java runtime for self-hosted server mode.
- Self-hosted cost: mostly infra and maintenance.
- Hosted API: commercial plan, details depend on plan level.
- Latency: low on localhost, moderate over network.

**Verdict**
Best option for this workflow.

#### 2) Grammarly API
**Pros**
- High-quality writing analysis.
- Real REST API exists for enterprise use cases.
- Useful for scoring and thresholds at scale.

**Cons**
- Enterprise-oriented access, not a simple public self-serve drop-in for this agent.
- Likely approval, credentials, and commercial setup needed.
- Harder to rely on as an immediate guardrail in a local assistant workflow.
- Privacy and vendor dependency concerns if used for every draft.

**Cost / dependencies / latency**
- Cost: enterprise/commercial, likely sales-led.
- Dependency: API credentials and org setup.
- Latency: network call, likely acceptable once provisioned.

**Verdict**
Good long-term enterprise option, bad immediate implementation choice.

#### 3) Ginger
**Pros**
- Good consumer-facing correction and rewrite features.
- Positions itself as helpful for long emails.

**Cons**
- No clear developer API path suitable for this automation.
- Site positioning is app/add-in centric rather than robust programmatic QA.
- Hard to integrate cleanly into a deterministic pre-send pipeline.

**Cost / dependencies / latency**
- Cost: consumer premium plans exist.
- Dependency: unclear API availability.
- Latency: unknown for automation because API path is unclear.

**Verdict**
Not recommended for this pipeline.

#### 4) DeepL Write / API
**Pros**
- Strong developer documentation and official client libraries.
- Good data protection positioning.
- Useful for rewrite quality if Write endpoints are available for the team plan.

**Cons**
- DeepL API is primarily translation-first.
- DeepL Write availability depends on product tier and plan setup.
- More useful as a rewrite enhancer than a strict grammar gate.
- Would still need our own email-specific rule layer.

**Cost / dependencies / latency**
- Cost: public API pricing exists, usage-based and plan-based.
- Dependency: API key.
- Latency: network call, generally acceptable.

**Verdict**
Possible secondary option later, not the best primary enforcement layer.

#### 5) Microsoft Editor
**Pros**
- Natural ecosystem fit with Outlook and Microsoft 365.
- Familiar UI-side grammar support for humans.

**Cons**
- No straightforward Microsoft Graph grammar-check endpoint for this use case.
- Good product, weak headless automation story for this agent.
- Best for manual composition in Microsoft apps, not for our scripted QA pipeline.

**Cost / dependencies / latency**
- Cost: usually bundled with Microsoft 365 tiers.
- Dependency: Microsoft app surface, not a simple API call.
- Latency: not the real issue; the missing automation interface is.

**Verdict**
Good human-side editor, poor programmable gate.

## Implementation plan and timeline

### Phase 1 - done now
- Harden local QA rules in `scripts/email_qc.py`.
- Add pre-send enforcement hook in `scripts/pre_send_hook.py`.
- Add safe wrapper in `scripts/send_with_qc.py`.
- Add rewrite retry helper in `scripts/rewrite_until_pass.py`.
- Expand examples and create training set.
- Add tests in `scripts/email_qc_test.py`.
- Update the skill documentation.

### Phase 2 - 30 to 60 minutes once Java is available
- Install Java runtime.
- Run a local LanguageTool server.
- Set `EMAIL_QA_GRAMMAR_PROVIDER=languagetool`.
- Set `LANGUAGETOOL_URL=http://127.0.0.1:8010`.
- Re-run tests plus one manual draft smoke test.

### Phase 3 - 30 minutes
- Optionally extend the M365 script to update an existing draft rather than always creating a fresh one.
- Add subject/recipient/body hash metadata for even stronger wrong-draft detection.
- Add a regression suite for real historical failure cases.

## Files created or modified

### Modified
- `scripts/email_qc.py`
- `skills/email-qc/SKILL.md`
- `skills/email-qc/references/examples.md`

### Added
- `scripts/pre_send_hook.py`
- `scripts/send_with_qc.py`
- `scripts/rewrite_until_pass.py`
- `scripts/email_qc_test.py`
- `skills/email-qc/references/training.jsonl`
- `skills/email-qc/references/prompt-templates.md`
- `docs/email-qc-implementation.md`

## How to use

### 1) Run tests
```bash
python3 scripts/email_qc_test.py
```

### 2) QA a draft only
```bash
python3 scripts/pre_send_hook.py \
  --to "person@example.com" \
  --subject "Subject" \
  --body-file draft.txt \
  --grammar-provider none \
  --json
```

### 3) QA and create an M365 draft after passing
```bash
python3 scripts/pre_send_hook.py \
  --to "person@example.com" \
  --subject "Subject" \
  --body-file draft.txt \
  --grammar-provider none \
  --create-draft \
  --json
```

### 4) Wrapper flow
```bash
python3 scripts/send_with_qc.py \
  --to "person@example.com" \
  --subject "Subject" \
  --body-file draft.txt \
  --create-draft
```
This stops after QA and draft creation. No send happens.

## LanguageTool enablement
Example local server flow once Java is installed:
```bash
# Example only
java -cp languagetool-server.jar org.languagetool.server.HTTPServer --port 8010
export EMAIL_QA_GRAMMAR_PROVIDER=languagetool
export LANGUAGETOOL_URL=http://127.0.0.1:8010
```
Then run the same hook or wrapper commands again.

## What is enforced now
- no em dashes
- no shorthand like `lmk`, `asap`, `wanna`, `gonna`, `u`, `soz`, `thx`
- no repeated punctuation like `!!` or `??`
- normalized spacing and line endings
- signature warning
- opening greeting warning
- canonical cleaned draft save before any send path
- send blocked unless QA passes and `--approved` is present

## What is not fully implemented yet
- Live third-party grammar API use is stubbed unless LanguageTool server is configured.
- The current M365 helper creates drafts but does not update an existing draft in place.
- Wrong-draft detection is rule-based rather than semantic.

## Revert plan
To roll back:
1. Delete the added scripts.
2. Restore the previous versions of `scripts/email_qc.py`, `skills/email-qc/SKILL.md`, and `skills/email-qc/references/examples.md`.
3. Stop using `scripts/send_with_qc.py` and `scripts/pre_send_hook.py`.

## Validation run
- Implemented all requested workspace changes.
- Added 38 training pairs.
- Added tests covering examples and training file presence.
- Did not send any emails.

## Notes on limitations encountered
- `web_search` was unavailable because Brave API key was not configured, so research used direct vendor page fetches instead.
- No third-party grammar API keys were added.
- LanguageTool live integration is implemented as a callable hook, but the server must be installed and running to activate it.
