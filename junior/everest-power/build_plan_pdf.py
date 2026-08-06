#!/usr/bin/env /usr/bin/python3
"""PLAN.md -> styled HTML -> PDF. Run with system python (has `markdown`)."""
import markdown, pathlib, subprocess, os

here = pathlib.Path(__file__).parent
md = (here / "PLAN.md").read_text()
body = markdown.markdown(md, extensions=["extra", "sane_lists", "toc"])

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Inter:wght@300;400;500;600&display=swap');
*{box-sizing:border-box}
body{font-family:'Inter',sans-serif;color:#12100e;line-height:1.62;font-size:11.2pt;
     max-width:none;margin:0;-webkit-font-smoothing:antialiased}
h1{font-family:'Barlow Condensed',sans-serif;font-size:38pt;line-height:.95;
   text-transform:uppercase;letter-spacing:-.01em;margin:0 0 2pt;font-weight:700}
h2{font-family:'Barlow Condensed',sans-serif;font-size:19pt;line-height:1.1;
   text-transform:uppercase;color:#6f685c;font-weight:600;margin:0 0 6pt;letter-spacing:.02em}
h2 + hr{display:none}
h3{font-family:'Barlow Condensed',sans-serif;font-size:21pt;text-transform:uppercase;
   font-weight:700;margin:26pt 0 9pt;border-top:3px solid #e0521f;padding-top:11pt;
   break-after:avoid;page-break-after:avoid}
h1 + p em{color:#6f685c}
p{margin:0 0 11pt}
strong{font-weight:600;color:#000}
hr{border:0;border-top:1px solid rgba(18,16,14,.15);margin:20pt 0}
ol,ul{margin:0 0 12pt 18pt;padding:0}
li{margin-bottom:7pt}
a{color:#12100e;text-decoration:none;border-bottom:1px solid rgba(224,82,31,.5)}
code{font-size:10pt;background:#f0ece3;padding:1pt 4pt;border-radius:2px}
h3:first-of-type{border-top:0;margin-top:14pt}
"""

html = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"
(here / "plan.html").write_text(html)

env = dict(os.environ, NODE_PATH="/opt/homebrew/lib/node_modules")
subprocess.run(
    ["node", os.path.expanduser("~/agents/shared/tools/html_to_pdf.js"),
     str(here / "plan.html"), str(here / "Everest-Power-Plan.pdf")],
    check=True, env=env)
