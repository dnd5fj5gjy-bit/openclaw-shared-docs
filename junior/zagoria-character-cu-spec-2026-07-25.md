# Feelon and Podcask need different lip-sync pipelines, not better model sheets

**25 Jul 2026, early hours. Zagoria. Work valid under either branch of the EP004 decision.**

The open note said Feelon and Podcask "need proper CU model sheets, not cropped full-body plates". I went to measure the plates to spec the model sheets and found something more useful by looking at them.

---

## What the plates actually are

Both are single front-on full-body references, one pose, one expression, no profile and no three-quarter.

| | plate | head region | 1080p CU at 70% frame | 4K CU |
|---|---|---|---|---|
| Feelon | 454 x 1495 | approx 326 x 574 | 1.3x upscale | 2.6x upscale |
| Podcask | 663 x 1471 | approx 663 x 653 | 1.2x upscale | 2.3x upscale |

Head-region figures are approximate: I measured them from the alpha silhouette and that method is unreliable on these designs, so treat them as within about 10%.

So resolution is **not** the real problem. For 1080p these plates are marginal but usable. For 4K they are not, and the fine stippling and thin linework in both will soften visibly under a 2.5x upscale.

The real problem is that one front-on pose cannot serve a dialogue scene at all.

## The finding that matters: these two characters are not the same problem

**Podcask's face is a screen.** His head is a boxy vintage television. The single eye and the flat mouth line are 2D graphics drawn on a flat white panel, roughly 500 x 400 px of unobstructed near-white surface facing directly at camera.

This means a generative talking-head model is the wrong tool for him, and probably always was. Those models expect a human face with jaw, lips and cheeks, and they will hallucinate anatomy onto a television. **Podcask's lip-sync should be 2D compositing: replace the mouth graphic on the screen panel, frame by frame, driven by the audio.** That is deterministic, free of drift, perfectly on-model every frame, and cheap. It also gives expression range for nothing, since the eye is the same kind of flat graphic.

**Feelon is the opposite.** He has a conventional face, eyes, nose and mouth, so a face model can drive him. But his brain sits in a **clear glass dome** with speculars and transparency, and that is exactly the class of element generative models repaint rather than preserve. `tools/lock_region.py` already exists for this, so the approach is: drive the face, lock the dome and the collar, and gate every frame.

## Why this is worth acting on

The standing diagnosis on record is that talking shots were dubbed over silent clips. If Podcask was being run through a face model that cannot see a face, that is a sufficient explanation on its own for why his talking shots never worked, and no quantity of better model sheets would have fixed it.

I have not tested either approach. What would confirm it: one Podcask line composited as screen-content replacement, against one attempt through the current pipeline, same audio. That is a cheap experiment and it settles the question.

## What the model sheets still need, if we build them

Front, three-quarter left, profile left, plus a mouth-shape set. Mirror for the right side rather than drawing it, both characters are symmetrical enough. For Podcask the "mouth shapes" are flat vector graphics on the screen panel, not drawn lips, so his sheet is much cheaper than Feelon's.

**Never text-generate either character.** Everything derives from these two locked plates by edit, per the standing rule.

---

**Status:** analysis only. Nothing generated, no API spend, no asset changed. Valid whether EP004 is rebuilt whole or the pipeline is locked first, which is why I did it while that decision is still open.
