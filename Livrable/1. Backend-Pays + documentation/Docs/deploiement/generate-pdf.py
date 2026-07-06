#!/usr/bin/env python3
"""
Génère documentation-deploiement-futurekawa.pdf à partir des fichiers Markdown du dossier deploiement/.
Usage : python livrables/deploiement/generate-pdf.py
Prérequis : pip install markdown weasyprint
"""
import os
import re
import sys

DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.join(os.path.dirname(DOCS_DIR), "PDF")
OUTPUT_PDF = os.path.join(PDF_DIR, "documentation-deploiement-futurekawa.pdf")

FILES = [
    "README.md",
    "01-architecture.md",
    "02-docker.md",
    "03-terraform.md",
    "04-variables-env.md",
]

try:
    import markdown
    from weasyprint import HTML, CSS
except ImportError as e:
    print(f"Dépendance manquante : {e}")
    print("Installe avec : pip install markdown weasyprint")
    sys.exit(1)

CSS_STYLE = CSS(string="""
    @page { margin: 5mm 5mm 6mm 5mm; size: A4; }
    body { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 12.5pt; color: #0f172a; line-height: 1.65; }
    h1 { font-size: 22pt; color: #1e293b; border-bottom: 2px solid #334155; padding-bottom: 6px; margin-top: 40px; }
    h2 { font-size: 15pt; color: #334155; border-bottom: 1px solid #cbd5e1; padding-bottom: 4px; margin-top: 30px; }
    h3 { font-size: 12pt; color: #475569; margin-top: 20px; }
    table { border-collapse: collapse; width: 100%; margin: 16px 0; font-size: 11pt; table-layout: fixed; }
    thead { display: table-header-group; }
    th { background: #1e293b; color: white; padding: 8px 12px; text-align: left; word-break: break-word; overflow-wrap: break-word; }
    td { padding: 7px 12px; border-bottom: 1px solid #e2e8f0; word-break: break-word; overflow-wrap: break-word; }
    tr { page-break-inside: avoid; }
    tr:nth-child(even) { background: #f8fafc; }
    code { background: #f1f5f9; padding: 2px 5px; border-radius: 3px; font-family: monospace; font-size: 10.5pt; }
    pre { background: #1e293b; color: #e2e8f0; padding: 16px; border-radius: 6px; font-size: 9pt; white-space: pre-wrap; word-break: break-all; overflow-wrap: break-word; }
    pre code { background: none; color: inherit; }
    hr { border: none; border-top: 1px solid #e2e8f0; margin: 24px 0; }
    a { color: #2563eb; }
""")

def build_html():
    combined = ""
    for filename in FILES:
        path = os.path.join(DOCS_DIR, filename)
        if not os.path.exists(path):
            print(f"Fichier manquant : {filename}")
            continue
        with open(path, encoding="utf-8") as f:
            content = f.read()
        content = re.sub(r'\[.*?\]\(\.\/.*?\)', '', content)
        combined += content + "\n\n---\n\n"
    return markdown.markdown(combined, extensions=["tables", "fenced_code", "toc"])

print("Génération du PDF...")
html_content = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"></head>
<body>{build_html()}</body></html>"""

HTML(string=html_content, base_url=DOCS_DIR).write_pdf(OUTPUT_PDF, stylesheets=[CSS_STYLE])
print(f"PDF généré : {OUTPUT_PDF}")
