# Zagoria: why the episodes keep failing, and the fix

20 July 2026. Written after Jesse's note on EP004: *"Very poor lip syncing and timing. None of the jokes land."*

Three episodes have now failed the same way. It is not the episode. It is the method. Below is what is actually wrong, measured rather than guessed, and what replaces it.

---

## 1. The lip sync was never there

EP004 has six shots carrying dialogue. **Two** of them were lip-synced. The other four had the voice track laid on top of a motion clip afterwards, so the mouths on screen were animating to nothing at all.

| Shot | Line | How it was made | Lip sync |
|---|---|---|---|
| S1 | "She's ready" / "You said that eighteen months ago" | Kling motion clip + dubbed VO | none |
| S2A | "The last one went into a school" | Kling motion clip + dubbed VO | none |
| S2 | "A closed school" | Kling motion clip + dubbed VO | none |
| S3 | "It closed because of the rocket" | Kling motion clip + dubbed VO | none |
| S4 | "Three. Two. One." | Hedra Character-3 | yes |
| S6 | "Best launch we've ever had" | Hedra Character-3 | yes |

The clips prove it: S1, S2, S2A and S3 have **no audio stream at all**. They are silent video with dialogue mixed over the top at assembly.

This was a deliberate compromise made during the build, recorded in the tool's own comments: Character-3 mis-assigns faces when two characters are in frame, so only single-face shots were sent for lip sync. The compromise was wrong. The answer to "the engine can't sync two faces in one frame" is **never put two speakers in one frame**, not "give up on syncing four of six shots."

## 2. Even the two synced shots had nothing to sync to

The keyframe named `s4_cu_feelon.png` - the "close-up" - is a full-body plate. Feelon's face is **16% of frame height**; his mouth is about 30 pixels wide in a 1080x1920 frame. At 720p output there is barely a mouth there to animate.

So the honest score is not 2 of 6. It is 2 of 6, and both of those were framed too wide to read.

## 3. The edit followed the generator, not the joke

Kling returns fixed 5.04-second blocks. The cut was built around those blocks instead of around the lines. Result, measured across the dialogue shots:

- **10.0 seconds of dead air** inside the talking shots of a 30-second film
- S2: 59% of the shot carries no speech
- S3: 58% of the shot carries no speech, and **2.75 seconds of silence after the last line**
- S6: the closing button, "Best launch we've ever had", is followed by **1.94 seconds of nothing** before the end card

That last one is the whole timing note in a single number. The punchline lands and then the film sits there for two seconds. Comedy needs the cut to arrive on the laugh, not two seconds after it.

## 4. The best joke was thrown away off-camera

The school exchange is the strongest writing in the episode, a clean three-beat reversal:

> **PODCASK:** The last one went into a school.
> **FEELON:** A closed school.
> **PODCASK:** It closed because of the rocket.

The topper - the line the whole joke exists for - was dubbed over S3, the slow push-in on the crowd of children. So the audience is asked to process a dark visual reveal and a verbal punchline at the same moment, with the speaker not on screen. **Both beats lose.** One buries the other.

This is the real answer to "none of the jokes land". The jokes are written. The edit is throwing them away.

## 5. A defect prompting cannot fix

Feelon's model sheet says his eyes are lidless solid black almonds that never close. The generation prompt says so explicitly, in capitals, twice. Measured on a fresh 1.07s generation: **he blinks in roughly half the frames.** Hedra reads a face and applies human facial rigging regardless of what the prompt asks. No amount of prompt wording fixes this, and every episode so far has shipped with it.

---

## The fix, and the proof it works

I rebuilt the school joke tonight under new rules. Attached: `ZAGORIA-lipsync-before-after.mp4`.

**Rule 1 - one speaker per frame, every line lip-synced.** No exceptions, no dubbing over motion clips. If a line is spoken and a mouth is visible, that shot comes from the lip-sync engine and keeps its own baked audio. Result: 3 of 3 talking shots synced, versus 2 of 6.

**Rule 2 - talking shots are cropped to a real close-up before generation.** Feelon's face went from 16% of frame height to 59%. There is now a mouth big enough to animate.

**Rule 3 - the cut follows the audio.** Each beat runs its line plus a tight tail (0.22s, or 0.45s where the hold is the joke). Same three lines: **10.1 seconds before, 5.9 seconds after.** Nothing was cut from the script. The 4.2 seconds removed were entirely dead air.

**Rule 4 - the punchline stays on screen.** The topper now plays on Podcask, in close-up, deadpan, holding the stare after the line. The crowd reveal gets its own space elsewhere instead of competing with it.

**Rule 5 - locked character regions.** New tool, `tools/lock_region.py`. Anything the model sheet says is fixed - Feelon's eyes, a badge, a logo - gets composited back from the keyframe over every frame, tracked to the head using an anchor patch that deliberately excludes the locked region. On Feelon: **81 of 81 frames locked, 0.96 mean tracking confidence.** The eyes are now solid black almonds in every frame, and the lip sync is untouched. This is what "locked character models" means in practice, and it is built and working.

## The gate that stops this repeating

The manual `QC-CHECKLIST.md` existed for all three failures and was not enforced. So the checkable half is now mechanical: `tools/qc_gate.py`.

It reads a manifest of the edit, measures the actual media, and blocks delivery on:

- **F1** dialogue dubbed onto a clip with no baked audio while a mouth is on screen
- **F2** a line whose audio runs past its shot, so the payoff plays over the next one
- **F3** audio/video length mismatch

and warns on dead air, trailing hang after a punchline, repeated framings, and static shots.

Run against EP004 as delivered, it fails with 3 blocking issues and 10 warnings, and reports `lip-synced talking shots: 2/6 (33%)`. Run against tonight's rebuild: passes, `3/3 (100%)`. Exit code is the failure count, so it drops straight into the build script. **Nothing goes to Jesse that does not pass it.**

---

## What I want to do next

1. **Rebuild EP004 whole** under these rules. The script does not need rewriting - it needs re-shooting and re-cutting. My estimate is 30 seconds becomes about 24, and every line lands on the speaker's face.
2. **Redraw the two talking plates as proper close-ups.** Feelon and Podcask both need CU model sheets, not full-body plates cropped after the fact.
3. **Settle the Podcask design question.** The treatment gives him a CRT head, and the current art has a line mouth on the screen that syncs surprisingly well. Worth confirming that is the intended read before more episodes are built on it.

Open question for Jesse: do you want EP004 rebuilt first, or the pipeline locked down and EP005 built clean on it? My recommendation is rebuild EP004 - it is a known script, it proves the pipeline end to end on something you have already seen fail, and it is the fastest honest answer to tonight's note.

---

### Files
- `build/PROOF/ZAGORIA-lipsync-before-after.mp4` - the comparison
- `build/PROOF/ZAGORIA-PROOF-school-joke.mp4` - the rebuilt joke alone
- `tools/qc_gate.py` - the automated gate
- `tools/lock_region.py` - character region lock
- `tools/proof_lipsync.py` - the proof build
- `build/EP004/manifest.json` - EP004 as delivered, in gate format
