#!/usr/bin/env /usr/bin/python3
"""beau-ops-handover.md -> styled HTML -> PDF. System python (has `markdown`)."""
import markdown, pathlib, subprocess, os

here = pathlib.Path(__file__).parent
body = markdown.markdown((here / "beau-ops-handover.md").read_text(),
                         extensions=["extra", "tables", "sane_lists"])

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Inter:wght@300;400;500;600&display=swap');
*{box-sizing:border-box}
body{font-family:'Inter',sans-serif;color:#141414;line-height:1.6;font-size:10.6pt;margin:0;
     -webkit-font-smoothing:antialiased}
h1{font-family:'Barlow Condensed',sans-serif;font-size:34pt;line-height:.96;text-transform:uppercase;
   font-weight:700;margin:0 0 4pt;letter-spacing:-.01em}
h1 + p{color:#6b6b6b;font-size:11pt;margin-bottom:3pt}
h2{font-family:'Barlow Condensed',sans-serif;font-size:24pt;text-transform:uppercase;font-weight:700;
   margin:30pt 0 11pt;border-top:3px solid #8a3b17;padding-top:12pt;
   break-after:avoid;page-break-after:avoid;break-before:page;page-break-before:always}
h2:first-of-type{break-before:auto;page-break-before:auto}
h3{font-family:'Barlow Condensed',sans-serif;font-size:16.5pt;text-transform:uppercase;font-weight:600;
   margin:19pt 0 7pt;color:#8a3b17;break-after:avoid;page-break-after:avoid}
p{margin:0 0 9pt}
strong{font-weight:600;color:#000}
blockquote{margin:11pt 0;padding:10pt 14pt;background:#f4f1ea;border-left:4px solid #8a3b17;
           font-size:11pt;font-style:italic}
blockquote p{margin:0}
hr{border:0;border-top:1px solid rgba(0,0,0,.14);margin:18pt 0}
ol,ul{margin:0 0 10pt 17pt;padding:0}
li{margin-bottom:5pt}
table{border-collapse:collapse;width:100%;margin:11pt 0;font-size:9.4pt;
      break-inside:avoid;page-break-inside:avoid}
th{background:#1b3a2f;color:#f4f1ea;text-align:left;padding:6pt 8pt;font-weight:600;
   font-family:'Barlow Condensed',sans-serif;font-size:11pt;text-transform:uppercase;letter-spacing:.04em}
td{padding:6pt 8pt;border-bottom:1px solid rgba(0,0,0,.12);vertical-align:top}
tr:nth-child(even) td{background:#faf8f4}
em{color:#5a5a5a}
a{color:#141414;text-decoration:none}
"""

html = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"
(here / "beau-ops-handover.html").write_text(html)

env = dict(os.environ, NODE_PATH="/opt/homebrew/lib/node_modules")
subprocess.run(["node", os.path.expanduser("~/agents/shared/tools/html_to_pdf.js"),
                str(here / "beau-ops-handover.html"),
                str(here / "Modern-Savage-Ops-Handover-Beau-Bennett.pdf")], check=True, env=env)
