# Zagoria: a production pipeline that holds

**For Jesse. 22 July 2026.**

You asked for this on 18 July, mid EP003 v16: *"I just want to get this one perfect episode. Then we can work together to find a better way to create these in the future because this method isn't very good."*

EP003 shipped. Here is the better way. It is not theory. Every piece below was built and proven on Last Stop over the last three days, on your notes, with you rejecting things until they worked.

---

## 1. What is actually wrong

Not the art, and not the tools. The loop.

**We pay to ask questions.** Every note from you triggered a regenerated keyframe, and every keyframe costs money. EP003 went to v19. A single 2K image edit is 83 Hedra credits; a 1000-credit top-up was nearly gone on one episode's revisions. We were spending generation money to find out whether a booth was in the right place.

**Nothing was enforced.** QC-CHECKLIST.md existed for three episodes and did not stop a single bad delivery, because a checklist a human runs at 2am is a hope, not a gate. EP004 shipped with two of six talking shots actually lip-synced and four dubbed over silent motion clips. The same failure, three episodes running.

**The expensive step happened once per note instead of once per asset.** That is the whole problem in one line.

---

## 2. The six rules

### Rule 1 — Approve geometry before art, on something cheap

Build the scene as a grey-box 3D blockout first. No texture, no light, no style. Labels on. Renders in under a second and costs nothing.

This is the single biggest change. On Last Stop you revised the room five times in ninety minutes: booth orientation, door position, a curved corner, booth scale and a window sill, then continuous glazing. Each revision cost seconds, because it was a change to a model rather than an art pass. Under the old method that is five paid rounds and half a day.

It also catches things nobody flags. When you said "the booths aren't correct", the model showed the booths were rotated 90 degrees off the plan, benches were solid slabs with the table buried inside them, and there were four where the plan had two, one of them blocking the entrance. An art pass would have painted all of that beautifully.

**Corollary:** render the blockout top-down as well, in the floor plan's own orientation, so the two lie side by side. Checking a perspective render against a plan by eye is how a 90-degree booth rotation survived three review rounds. Check in the source's coordinates.

### Rule 2 — Backgrounds are locked plates. Characters composite in. They never generate together.

Generate the room ONCE, empty. Then composite characters onto it. Validated on Last Stop: the trio into the locked diner plate with zero room drift.

This kills the whole family of Zagoria glitches at the source. Morphing background guests, the green skyline bleed, the guest standing on the pool water, the invented cook line: all of those are the room being re-rolled because a character changed. If the room is a fixed asset, it cannot drift, and a character note costs one composite instead of a whole frame.

### Rule 3 — "Keep this, change only X" is an EDIT with ONE reference

Two reference images means the model composes. It rebuilds the scene from its own generic logic and quietly ignores your layout. One reference plus edit phrasing means it modifies what you gave it.

This is the rule I broke on Last Stop and got twelve rejected plates for. Laying each painting next to the grey box it was built on showed it immediately: one frame had lost its window, another the south glazing, half had imported a cook line into plain walls. The model had treated the approved layout as a mood board.

Related, and it cost a full round to learn: a full-frame style reference donates its **composition**, not just its palette. Crop it into a tiled swatch and it can only donate the look.

### Rule 4 — Geometry lives in words. References cannot carry it.

A floor plan passed as a reference image does not tell the model which wall is glass or which side is which. You caught floor plan errors in five of ten plates from exactly that gap.

So: lead the prompt with the camera, state what must NOT be in frame, and name the geometry explicitly. A reference image gives you look and materials, and it will override your framing if you let it.

### Rule 5 — Machine gates, not eyes

Two are already written and running.

- **`plate_drift.py`** — region-by-region SSIM against the locked plate, so a frame that changed the room gets blocked automatically. Worth knowing why it works: image models repaint the whole frame every call, so raw pixel difference flags everything and is useless. Structure compared on a blurred greyscale is the answer, and the blur was calibrated rather than guessed. A known-good pair scores 0.989; the frame that invented a new cooktop scores 0.734. Layout survives the blur, brushwork does not, and layout is what must not move.
- **`qc_gate.py`** — blocks dubbed dialogue, orphaned punchlines, A/V drift, repeated framing and static shots. Exit code is the failure count so it drops straight into a build script. A cut that fails does not reach you.

The standard: the gate should be harder to satisfy than my own judgement at 2am.

### Rule 6 — When a note can't be resolved, render the options

Do not guess and do not ask an open question. Build the cheap lettered variants and have you point at one.

On Last Stop that got an exact answer in a single message, including a correction to my vocabulary I would never have got from prose. It is the cheapest form of communication available now that the artefact costs nothing to make.

---

## 3. What this changes about money

Expensive generation happens **once per asset**, not once per note.

| | Now | Under this pipeline |
|---|---|---|
| Layout change | paid regen, ~83 credits, minutes | free, seconds |
| Character note | whole frame re-rolled, room may drift | one composite, room cannot drift |
| Background | re-generated per shot, morphs | generated once, locked |
| Bad frame caught | by your eye, after delivery | by a gate, before delivery |
| Talking shot | dubbed VO over motion clip (broken) | lip-synced clip, gate refuses otherwise |

EP003 took nineteen versions. Most of those versions existed to answer questions the blockout answers for free.

---

## 4. What already exists

Not a plan to build. Built, on the shelf, proven this week.

- `laststop/tools/diner3d.py` — parametric grey-box set builder, plan render included
- `laststop/tools/plate_edit.py` — single-reference edit (supersedes the two-reference version that failed)
- `laststop/tools/plate_drift.py` — the automated room-drift gate
- `zagoria-factory/tools/qc_gate.py` — the automated delivery gate
- `zagoria-factory/tools/lock_region.py` — composites fixed character features back over generated frames, tracked. Fixes defects prompting cannot.

---

## 5. What it takes to move Zagoria across

Four things, in this order.

1. **Blockout the recurring Zagoria sets.** The pool deck first, since it carries most episodes. One day. After that every layout note in every future episode is free.
2. **Lock the eight founding cast as fixed assets.** Canonical pose and expression library per character, composited rather than re-generated per shot. This is what kills off-model drift and missing limbs permanently, and it is the piece EP003 spent the most money fighting.
3. **Animatic before any render.** Storyboard, scratch VO, still keyframes, your sign-off. The biggest single waste on EP003 was rendering a whole Flare beat and a swivel that were then cut at v18. Cuts should be decided on stills, for free.
4. **Wire both gates into the build script.** No delivery reaches you without passing them.

One honest note on the wider direction: for a talking-heads sitcom, one-shot video generation is the expensive way to do it. Proper 2D puppet rigs driven by audio (Live2D or After Effects) give consistency by construction rather than by fighting for it, and revisions genuinely approach free. The five moves above work either way, so I would not block on that decision. But it is the destination.

ElevenLabs voices stay. They are the one part of the current stack that has never been the problem.

---

## 6. What I need from you

Only one answer: do I blockout the pool deck next, or do you want the character-locking done first? Everything else I can run.
