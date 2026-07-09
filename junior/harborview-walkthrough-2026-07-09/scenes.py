# -*- coding: utf-8 -*-
# Scene definitions for the Harborview / Ted's Health white-label walkthrough.
# Run with system python3 (has Pillow). Writes audio/<id>.txt and captions/<id>.png
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1600, 900

SCENES = [
 dict(id="01-intro", eyebrow="TED'S HEALTH  ·  WHITE-LABEL PLATFORM", title="A complete men's health clinic, in a box",
   vo="This is a complete men's health clinic, delivered as a white-label platform by Ted's Health. A clinic signs up, and on day one they have a premium patient website, an intelligent health assessment, blood testing, and an automated supplement engine, all under their own brand. Let me walk you through it."),
 dict(id="02-whitelabel", eyebrow="FULLY CUSTOMISABLE", title="Every clinic gets its own brand",
   vo="Everything you are about to see is fully customisable by the clinic. This is the Branding Studio. The clinic sets its name, its message, and its brand colours, and the entire site re-themes instantly, the landing page and the patient portal together. One codebase, and every clinic its own brand."),
 dict(id="03-quiz", eyebrow="THE HEALTH ASSESSMENT", title="An assessment people actually finish",
   vo="It starts with the health assessment. We made it effortless on purpose. Instead of a blank box to type into, the patient simply taps what applies, so we capture rich information without anyone quitting halfway through. Energy, sleep, symptoms, lifestyle. The more they tell us, the sharper the plan, and every answer is data the clinic can act on."),
 dict(id="04-results", eyebrow="AI PLAN  +  SUPPLEMENT ENGINE", title="Answers become a plan, and a sale",
   vo="In seconds, the AI turns those answers into a clear, clinician-reviewed plan. It shows the patient exactly where to focus. And here is the commercial engine: it immediately recommends a supplement matched to their answers, ready to add to basket, on a subscription that bills every single month. The upsell is built directly into the care."),
 dict(id="05-bloods", eyebrow="BLOOD TESTING", title="Order clinician-reviewed bloods directly",
   vo="Patients can also order blood tests directly, with no assessment required. Clinician-reviewed panels, priced clearly and bookable in a couple of taps."),
 dict(id="06-bloodreview", eyebrow="NEW  ·  AI BLOOD REVIEW", title="The AI reads your bloods, then builds the stack",
   vo="And this is the new part. When the results come back, the AI reviews every biomarker against clinical ranges in seconds. It flags what is low, explains it in plain English, and then automatically assembles a supplement stack matched to those exact results. The patient just taps, add my stack. So off the back of every blood test, we are upselling the right products automatically, and it feels like care, not a sales pitch."),
 dict(id="07-portal", eyebrow="THE PATIENT PORTAL", title="One branded home for everything",
   vo="It all lives inside one branded patient portal. Their results, their recommendations, their supplement subscription, and their next appointment, in a single place they keep coming back to."),
 dict(id="08-close", eyebrow="WHY THIS WINS", title="Recurring revenue, infinitely re-brandable",
   vo="So why does this win? For the patient, it is genuinely better care: fast, personal, and clinician-backed. For the clinic, it is three revenue lines, assessments, blood tests, and a recurring supplement subscription, from one platform, under their own brand, with almost no overhead. And for a buyer, this is the rare thing: a beautifully built, fully white-label health platform with recurring revenue designed in from the start. One codebase, infinitely re-brandable, ready to sell to every clinic in the market."),
]

def font(path, size):
    return ImageFont.truetype(path, size)

GEORGIA = "/System/Library/Fonts/Supplemental/Georgia.ttf"
GEORGIA_B = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
ARIAL_B = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

def make_caption(sc):
    img = Image.new("RGBA", (W, H), (0,0,0,0))
    d = ImageDraw.Draw(img)
    # bottom gradient scrim for legibility
    grad_h = 240
    for i in range(grad_h):
        a = int(150 * (i/grad_h)**1.6)
        d.line([(0, H-grad_h+i), (W, H-grad_h+i)], fill=(8,30,36,a))
    # lower-third text block
    x = 70
    eb_f = font(ARIAL_B, 21)
    ti_f = font(GEORGIA_B, 46)
    # eyebrow (gold)
    d.text((x, H-150), sc["eyebrow"], font=eb_f, fill=(214,158,80,255))
    # title (white)
    d.text((x, H-118), sc["title"], font=ti_f, fill=(255,255,255,255))
    img.save(os.path.join(HERE, "captions", sc["id"]+".png"))

def main():
    os.makedirs(os.path.join(HERE,"audio"), exist_ok=True)
    os.makedirs(os.path.join(HERE,"captions"), exist_ok=True)
    for sc in SCENES:
        with open(os.path.join(HERE,"audio",sc["id"]+".txt"),"w") as f:
            f.write(sc["vo"])
        make_caption(sc)
    print("wrote %d narration files + captions" % len(SCENES))

if __name__ == "__main__":
    main()
