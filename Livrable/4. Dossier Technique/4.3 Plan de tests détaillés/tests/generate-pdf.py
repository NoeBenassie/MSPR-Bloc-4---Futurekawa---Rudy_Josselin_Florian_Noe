#!/usr/bin/env python3
"""
Génère documentation-tests-futurekawa.pdf à partir des fichiers Markdown du dossier tests/.
Usage : python tests/generate-pdf.py
Prérequis : pip install markdown weasyprint  (déjà dans API-exploitation/venv)
"""
import os
import re
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.join(os.path.dirname(TESTS_DIR), "PDF")
OUTPUT_PDF = os.path.join(PDF_DIR, "documentation-tests-futurekawa.pdf")

FILES = [
    "README.md",
    "01-introduction.md",
    "02-lancement.md",
    "03-couverture-api-exploitation.md",
    "04-couverture-api-siege.md",
    "05-couverture-simu-sensor.md",
    "06-couverture-front-exploitation.md",
    "07-couverture-front-siege.md",
    "08-couverture-broker.md",
    "09-couverture-iot.md",
]

# Mapping nom de fichier → ancre PDF interne
FILE_TO_ANCHOR = {f: f"section-{i}" for i, f in enumerate(FILES)}

try:
    import markdown
    from weasyprint import HTML, CSS
except ImportError as e:
    print(f"Dépendance manquante : {e}")
    print("Installe-les avec : pip install markdown weasyprint")
    sys.exit(1)


EMOJI_MAP = {
    "✅": "Oui",
    "❌": "Non",
    "⚠️": "",
    "⚠": "",
}

def replace_emojis(content):
    for emoji, replacement in EMOJI_MAP.items():
        content = content.replace(emoji, replacement)
    return content


def fix_internal_links(content):
    """Convertit les liens ./fichier.md en ancres internes #section-N pour le PDF."""
    def replace(m):
        label, target = m.group(1), m.group(2)
        key = target.lstrip("./")
        anchor = FILE_TO_ANCHOR.get(key)
        if anchor:
            return f"[{label}](#{anchor})"
        return m.group(0)
    return re.sub(r'\[([^\]]+)\]\((\.\/[^)]+\.md)\)', replace, content)


def load_and_clean(filepath):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    # Supprime les lignes de navigation inter-fichiers (← … | … | …)
    content = re.sub(r"^\[←[^\]]*\].*\n?", "", content, flags=re.MULTILINE)
    content = re.sub(r"^---\n?", "\n", content, flags=re.MULTILINE)
    # Remplace les emojis par du texte brut (non rendu par WeasyPrint)
    content = replace_emojis(content)
    # Convertit les liens fichiers en ancres PDF cliquables
    content = fix_internal_links(content)
    return content


def build_toc(files_content):
    """Construit un sommaire HTML avec ancres vers chaque section."""
    toc_items = []
    for idx, (filename, content) in enumerate(files_content):
        # Cherche le titre H1
        m = re.search(r"^# (.+)$", content, re.MULTILINE)
        if m:
            title = m.group(1).strip()
            anchor = f"section-{idx}"
            toc_items.append(f'<li><a href="#{anchor}">{title}</a></li>')
    return "<ul>\n" + "\n".join(toc_items) + "\n</ul>"


CSS_STYLE = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

* { box-sizing: border-box; }

body {
    font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    font-size: 12.5pt;
    line-height: 1.65;
    color: #1a1a1a;
    margin: 0;
    padding: 0;
}

.cover {
    page-break-after: always;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    height: 297mm;
    text-align: center;
    background: #0f3d1f;
    color: white;
    padding: 130px 60px 60px;
    overflow: hidden;
}

.cover h1 { font-size: 38pt; margin-bottom: 12px; color: #ffffff; }
.cover .subtitle { font-size: 18pt; opacity: 0.85; }
.cover .meta { margin-top: 60px; font-size: 10pt; opacity: 0.7; line-height: 2; }

.toc-page {
    page-break-after: always;
    padding: 48px 64px;
}
.toc-page h2 { font-size: 18pt; border-bottom: 2px solid #0f3d1f; padding-bottom: 8px; }
.toc-page ul { list-style: none; padding: 0; }
.toc-page li { padding: 6px 0; border-bottom: 1px solid #eee; }
.toc-page a { color: #0f3d1f; text-decoration: none; font-weight: 600; }
.toc-page a:hover { text-decoration: underline; }

.section {
    padding: 48px 64px;
    page-break-before: always;
}

h1 { font-size: 22pt; color: #0f3d1f; margin-top: 0; border-bottom: 3px solid #0f3d1f; padding-bottom: 8px; }
h2 { font-size: 15.5pt; color: #1a5c30; margin-top: 28px; }
h3 { font-size: 12.5pt; color: #2d7a47; }

table {
    border-collapse: collapse;
    width: 100%;
    margin: 16px 0;
    font-size: 11pt;
    table-layout: fixed;
}
thead { display: table-header-group; }
th {
    background: #0f3d1f;
    color: white;
    padding: 8px 12px;
    text-align: left;
    font-weight: 600;
    word-break: break-word;
    overflow-wrap: break-word;
}
td { padding: 7px 12px; border-bottom: 1px solid #e0e0e0; word-break: break-word; overflow-wrap: break-word; }
tr { page-break-inside: avoid; }
tr:nth-child(even) td { background: #f5f9f6; }

code {
    background: #f0f4f1;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 10.5pt;
    color: #0f3d1f;
}
pre {
    background: #f0f4f1;
    border-left: 4px solid #0f3d1f;
    padding: 14px 18px;
    border-radius: 4px;
    margin: 16px 0;
    white-space: pre-wrap;
    word-break: break-all;
    overflow-wrap: break-word;
}
pre code { background: none; padding: 0; color: #1a1a1a; white-space: pre-wrap; }

blockquote {
    border-left: 4px solid #0f3d1f;
    margin: 16px 0;
    padding: 10px 18px;
    background: #f5f9f6;
    color: #333;
    font-style: italic;
}

a { color: #0f3d1f; }

@page {
    margin: 5mm 5mm 6mm 5mm;
    @bottom-right {
        content: counter(page);
        font-size: 9pt;
        color: #888;
    }
    @bottom-center {
        content: "FutureKawa — Rapport de Tests";
        font-size: 9pt;
        color: #aaa;
    }
}

@page :first {
    margin: 0;
    @bottom-center { content: none; }
    @bottom-right  { content: none; }
}
"""


def parse_cover(filepath):
    """Lit 00-couverture.md et extrait titre (H1), sous-titre (H2) et métadonnées (liste)."""
    if not os.path.exists(filepath):
        return {"title": "FutureKawa", "subtitle": "", "meta": ""}
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    title = re.search(r"^# (.+)$", content, re.MULTILINE)
    subtitle = re.search(r"^## (.+)$", content, re.MULTILINE)
    meta_items = re.findall(r"^- (.+)$", content, re.MULTILINE)
    return {
        "title": title.group(1).strip() if title else "FutureKawa",
        "subtitle": subtitle.group(1).strip() if subtitle else "",
        "meta": "<br>".join(meta_items),
    }


def main():
    md_parser = markdown.Markdown(extensions=["tables", "fenced_code", "toc"])

    cover = parse_cover(os.path.join(TESTS_DIR, "00-couverture.md"))

    files_content = []
    for filename in FILES:
        path = os.path.join(TESTS_DIR, filename)
        if os.path.exists(path):
            files_content.append((filename, load_and_clean(path)))
        else:
            print(f"Avertissement : {filename} introuvable, ignoré.")

    toc_html = build_toc(files_content)

    sections_html = ""
    for idx, (filename, content) in enumerate(files_content):
        md_parser.reset()
        html_body = md_parser.convert(content)
        anchor = f"section-{idx}"
        html_body = re.sub(r'<h1>', f'<h1 id="{anchor}">', html_body, count=1)
        sections_html += f'<div class="section">\n{html_body}\n</div>\n'

    full_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>{cover["title"]} — {cover["subtitle"]}</title>
<style>{CSS_STYLE}</style>
</head>
<body>

<div class="cover">
  <h1>{cover["title"]}</h1>
  <div class="subtitle">{cover["subtitle"]}</div>
  <div class="meta">{cover["meta"]}</div>
</div>

<div class="toc-page">
  <h2>Sommaire</h2>
  {toc_html}
</div>

{sections_html}

</body>
</html>"""

    print(f"Génération de {OUTPUT_PDF} ...")
    HTML(string=full_html, base_url=TESTS_DIR).write_pdf(OUTPUT_PDF)
    print(f"PDF généré : {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
