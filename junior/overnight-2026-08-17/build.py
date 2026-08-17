#!/usr/bin/env python3
"""Rebuild the combined overnight PDF from the markdown sections.

Order matches the original 16 Aug build. Rebuilt 17 Aug 2026 because
04-other-business.md gained two items (Henley Commerce, Tyler Ball) after
the first PDF was rendered, so the PDF on disk was missing them.
"""
import pathlib
import subprocess
import sys

import markdown

HERE = pathlib.Path(__file__).parent
ORDER = [
    "00-SUMMARY.md",
    "11-bmf-farren-withdrew.md",
    "09-uk-competitive.md",
    "01-modern-savage-marketing.md",
    "07-the-bear-ask-and-tiktok.md",
    "08-funnel-audit.md",
    "03-commercial-findings.md",
    "13-technical-seo-and-ai.md",
    "10-uk-search-content.md",
    "12-press-and-owned-media.md",
    "02-bg-partnerships.md",
    "04-other-business.md",
    "05-waitlist-email-sequence.md",
    "00-BLOCKERS.md",
]

STYLE = """
body{font-family:-apple-system,'Helvetica Neue',Arial,sans-serif;color:#1a1a1a;line-height:1.55;max-width:820px;margin:0 auto;padding:44px 40px;font-size:14.5px}
h1{font-size:27px;margin:34px 0 14px;letter-spacing:-.4px;border-bottom:3px solid #1a1a1a;padding-bottom:9px}
h2{font-size:20px;margin:30px 0 11px;letter-spacing:-.2px}
h3{font-size:16.5px;margin:24px 0 8px}
h4{font-size:14.5px;margin:18px 0 6px;text-transform:uppercase;letter-spacing:.6px;color:#555}
p{margin:10px 0}
table{border-collapse:collapse;width:100%;margin:16px 0;font-size:13px}
th{background:#1a1a1a;color:#fff;text-align:left;padding:8px 10px;font-weight:600}
td{border-bottom:1px solid #ddd;padding:8px 10px;vertical-align:top}
tr:nth-child(even) td{background:#fafafa}
blockquote{margin:14px 0;padding:12px 18px;background:#f6f6f4;border-left:4px solid #8a8a80;border-radius:0 4px 4px 0}
blockquote p{margin:7px 0}
code{background:#f0f0ee;padding:1.5px 5px;border-radius:3px;font-size:12.5px;font-family:'SF Mono',Menlo,monospace}
hr{border:0;border-top:1px solid #ddd;margin:26px 0}
ul,ol{margin:10px 0;padding-left:24px} li{margin:5px 0}
a{color:#0a58a6;text-decoration:none}
strong{font-weight:650}
.pb{page-break-after:always}
@media print{body{padding:22px}}
"""


def main() -> int:
    parts = []
    for name in ORDER:
        path = HERE / name
        if not path.exists():
            print(f"MISSING {name}", file=sys.stderr)
            return 1
        html = markdown.markdown(
            path.read_text(), extensions=["tables", "sane_lists", "attr_list"]
        )
        parts.append(f'<section class="pb">{html}</section>')

    out_html = HERE / "overnight-2026-08-17.html"
    out_html.write_text(
        '<!doctype html><html><head><meta charset="utf-8">'
        f"<title>Overnight work</title><style>{STYLE}</style></head>"
        f"<body>{''.join(parts)}</body></html>"
    )

    pdf = HERE / "overnight-2026-08-17.pdf"
    subprocess.run(
        [
            "node",
            str(pathlib.Path.home() / "agents/shared/tools/html_to_pdf.js"),
            str(out_html),
            str(pdf),
        ],
        check=True,
    )
    print(f"built {pdf} ({pdf.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
