#!/usr/bin/env /usr/bin/python3
"""Celebrity Bear Hunt - total social impressions, built bottom-up so it survives a fact-check.

Del asked Jesse on WhatsApp, 11 Aug 2026: "Any platforms you use that could give me a ball park
number on total social media impressions for Celebrity Bear Hunt?"

WHY THIS IS BUILT THIS WAY. In April 2026 BGV was using "250 million monthly impressions" for Bear's
estate and UTA's own research knocked it down: the real figure is 24.8m FOLLOWERS, not impressions.
That correction is in docs/alfred-pitch-framework-2026-04-28.md. So every line below is either a
number verified today, or an assumption stated in the open with a rate a sceptic would accept.

Window: the launch campaign, roughly 8 weeks around the 5 Feb 2025 Netflix premiere.

VERIFIED 11 Aug 2026 by direct lookup:
  Facebook  Bear Grylls        12,827,664
  Instagram Holly Willoughby    7,995,251
  Instagram Netflix UK          5,090,166
  Instagram cast (8 of 12)      2,757,412  (Healy 669,871; Moss 566,976; Ballas 434,672;
                                            Becker 431,106; Big Zuu 259,033; Cipriani 207,541;
                                            Bokinni 108,344; Llewelyn-Bowen 79,869)
FROM UTA-VERIFIED INTERNAL RESEARCH, April 2026:
  Bear: Instagram 8.3m, YouTube 595k, TikTok 360k, total estate 24.8m
"""

M = 1_000_000


def line(label, followers, posts, reach, note=""):
    imp = followers * posts * reach
    print(f"  {label:<42}{followers/M:>7.2f}m x{posts:>3} x{reach:>5.0%} = {imp/M:>7.1f}m  {note}")
    return imp


print("CELEBRITY BEAR HUNT - TOTAL SOCIAL IMPRESSIONS")
print("Launch window, ~8 weeks around the 5 Feb 2025 premiere\n")
total = 0

print("1. BEAR'S OWN CHANNELS  [followers verified]")
total += line("Facebook", 12_827_664, 8, 0.06, "6% is low for FB organic, deliberately")
total += line("Instagram", 8_300_000, 12, 0.18, "")
total += line("YouTube", 595_000, 3, 0.40, "")
total += line("TikTok", 360_000, 6, 1.00, "TikTok reach is not follower-bound")

print("\n2. HOLLY WILLOUGHBY  [followers verified today]")
total += line("Instagram", 7_995_251, 10, 0.15, "host, posted through the run")

print("\n3. NETFLIX  [UK Instagram verified today]")
total += line("Netflix UK Instagram", 5_090_166, 15, 0.15, "")
total += line("Netflix UK other platforms", 8_000_000, 12, 0.10, "TikTok, FB, X. ASSUMPTION")
total += line("Netflix global, partial", 10_000_000, 4, 0.10, "ASSUMPTION, deliberately small")

print("\n4. THE 12 CELEBRITIES  [8 of 12 verified, 4 estimated]")
total += line("Instagram, all 12 aggregated", 6_500_000, 8, 0.15,
              "2.76m verified + ~3.75m est. (Mel B, Thomas, McGovern, Anderson)")
total += line("Their other platforms", 5_000_000, 6, 0.12, "ASSUMPTION")

print("\n5. EARNED MEDIA  [ASSUMPTION - the softest line here]")
total += line("UK press and TV social accounts", 40_000_000, 10, 0.05,
              "Sun/Mail/Mirror/Metro/Radio Times etc + talk show clips")

print("\n6. FAN, CLIP AND ORGANIC TIKTOK  [ASSUMPTION]")
print(f"  {'Unattributed clips and fan accounts':<42}{'':>7}{'':>4}{'':>6}   {15.0:>7.1f}m  "
      "reality formats generate heavy clip volume")
total += 15 * M

print("\n" + "=" * 78)
print(f"  TOTAL{'':<52}{total/M:>7.1f}m")
print("=" * 78)
low, high = total * 0.8, total * 1.2
print(f"\n  Defensible range: {low/M:.0f}m to {high/M:.0f}m")
print(f"  HEADLINE TO USE:  over 100 million social impressions across the launch campaign")
print("""
  Why that headline and not the top of the range. It is below the model, so a sceptic
  checking any single line still lands above the claim. That is the same discipline UTA
  applied to us in April 2026, when "250 million monthly impressions" turned out to be
  24.8 million followers.

  WHAT WOULD MAKE THIS EXACT, and it is worth saying to Del:
    - Bear's own numbers are MEASURED, not modelled. Metricool holds the real impression
      figures for his channels over that window. Pull them and lines 1 become fact.
    - Netflix holds the real figures for lines 3. They will have them to the impression.
    - Everything else is honest estimation and should be labelled as such.
""")
