"""Build the study guide.

1. Run every cell of every file in snippets/ (fails loudly on any error, so
   every code sample in the PDF is known to work).
2. Replace each {{file:cell}} marker in guide/template.html with the
   highlighted code and its real output.
3. Print the HTML to PDF with headless Chromium (tools/make_pdf.js), read the
   page numbers of each part back from the PDF, fill the table of contents
   and print again.

Usage:  python3 tools/build.py            # HTML + PDF
        python3 tools/build.py --html     # HTML only (no Chromium needed)

Cell syntax inside snippets/*.py:
    # %% cell_name [annotate] [hidden] [noout]
annotate  every top-level expression gets its value appended as "# → value"
hidden    run the cell but do not render it (setup code)
noout     render the code but not its printed output
"""

import ast
import contextlib
import html
import io
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

ROOT = Path(__file__).resolve().parent.parent
SNIPPETS = ROOT / "snippets"
TEMPLATE = ROOT / "guide" / "template.html"
OUT_HTML = ROOT / "guide" / "guide.html"
OUT_PDF = ROOT / "Python-Live-Coding-Guide-FA.pdf"

CELL_RE = re.compile(r"^# %% (\w+)((?: \w+)*)\s*$")
MARKER_RE = re.compile(r"\{\{(\w+):(\w+)\}\}")
MAX_WIDTH = 84          # characters that fit in one code line on A4


def split_cells(text):
    cells, name, flags, lines = [], None, set(), []
    for line in text.splitlines():
        m = CELL_RE.match(line)
        if m:
            if name:
                cells.append((name, flags, "\n".join(lines).strip("\n")))
            name, flags, lines = m.group(1), set(m.group(2).split()), []
        elif name:
            lines.append(line)
    if name:
        cells.append((name, flags, "\n".join(lines).strip("\n")))
    return cells


def is_print(node):
    return (isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Name)
            and node.value.func.id == "print")


MUTATORS = {"append", "extend", "insert", "remove", "sort", "reverse",
            "update", "add", "clear", "appendleft", "write"}


def is_mutator(node):
    """Calls like lst.append(x) return None; don't annotate them."""
    return (isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Attribute)
            and node.value.func.attr in MUTATORS)


def run_cell(code, ns, annotate, label):
    tree = ast.parse(code)
    notes, buf = {}, io.StringIO()
    with contextlib.redirect_stdout(buf):
        for node in tree.body:
            if annotate and isinstance(node, ast.Expr) and not is_print(node):
                expr = compile(ast.Expression(node.value), label, "eval")
                value = eval(expr, ns)
                if value is not None or not is_mutator(node):
                    notes[node.end_lineno] = repr(value)
            else:
                exec(compile(ast.Module([node], []), label, "exec"), ns)
    return notes, buf.getvalue()


def render_code(code, notes):
    formatter = HtmlFormatter(nowrap=True)
    lines = highlight(code, PythonLexer(), formatter).rstrip("\n").split("\n")
    raw = code.split("\n")
    assert len(lines) == len(raw), "pygments changed the line count"
    col = max((len(raw[n - 1]) for n in notes), default=0)
    col = min(col, 34)
    out = []
    for i, (hl, src) in enumerate(zip(lines, raw), start=1):
        if not src.strip() and out and not out[-1].strip():
            continue                     # PEP 8 double blank lines -> one
        if i in notes:
            note = html.escape(notes[i])
            pad = max(col - len(src), 0) + 2
            if len(src) + pad + len(notes[i]) + 4 <= MAX_WIDTH:
                hl += " " * pad + f'<span class="ann"># → {note}</span>'
            else:
                indent = len(src) - len(src.lstrip()) + 4
                hl += "\n" + " " * indent + f'<span class="ann"># → {note}</span>'
        out.append(hl)
    return "\n".join(out)


def build_cells():
    rendered, problems = {}, []
    for path in sorted(SNIPPETS.glob("*.py")):
        key = re.sub(r"^\d+_", "", path.stem)
        ns = {"__name__": f"snippet_{key}"}
        cwd = os.getcwd()
        os.chdir(tempfile.mkdtemp(prefix=f"guide_{key}_"))
        try:
            for name, flags, code in split_cells(path.read_text("utf-8")):
                label = f"{path.name}:{name}"
                try:
                    notes, output = run_cell(code, ns, "annotate" in flags,
                                             label)
                except Exception as exc:
                    sys.exit(f"FAILED {label}: {type(exc).__name__}: {exc}")
                if "hidden" in flags:
                    continue
                for n, line in enumerate(code.split("\n"), start=1):
                    if len(line) > MAX_WIDTH:
                        problems.append(f"{label} line {n} too long")
                for line in output.split("\n"):
                    if len(line) > MAX_WIDTH + 4:
                        problems.append(f"{label} output line too long")
                n_lines = code.count("\n") + output.count("\n") + 2
                keep = " keep" if n_lines <= 26 else ""
                block = [f'<div class="codeblock{keep}">',
                         f'<pre class="code" dir="ltr">'
                         f'{render_code(code, notes)}</pre>']
                if output.strip() and "noout" not in flags:
                    block.append('<div class="out-label" dir="ltr">Output</div>'
                                 f'<pre class="out" dir="ltr">'
                                 f'{html.escape(output.rstrip())}</pre>')
                block.append("</div>")
                rendered[(key, name)] = "\n".join(block)
        finally:
            os.chdir(cwd)
    return rendered, problems


def build_html(toc_pages=None):
    rendered, problems = build_cells()
    template = TEMPLATE.read_text("utf-8")
    used = set()

    def replace(m):
        k = (m.group(1), m.group(2))
        if k not in rendered:
            sys.exit(f"unknown marker {m.group(0)}")
        used.add(k)
        return rendered[k]

    page = MARKER_RE.sub(replace, template)
    for k in sorted(set(rendered) - used):
        problems.append(f"cell {k[0]}:{k[1]} is never used in the template")
    css = HtmlFormatter(style="friendly").get_style_defs(".code")
    page = page.replace("/*PYGMENTS*/", css)
    if toc_pages:
        for part, num in toc_pages.items():
            page = page.replace(f'<span class="pg" data-part="{part}"></span>',
                                f'<span class="pg">{num}</span>')
    OUT_HTML.write_text(page, "utf-8")
    for p in problems:
        print("WARNING:", p)
    print(f"ran {len(rendered)} cells -> {OUT_HTML.relative_to(ROOT)}")


def print_pdf():
    subprocess.run(["node", str(ROOT / "tools" / "make_pdf.js"),
                    str(OUT_HTML), str(OUT_PDF)], check=True)


def find_part_pages():
    from pypdf import PdfReader
    pages = {}
    for i, page in enumerate(PdfReader(OUT_PDF).pages, start=1):
        text = page.extract_text() or ""
        # the kicker is letter-spaced, so pypdf may return "P A R T  0 1"
        for a, b in re.findall(r"P\s*A\s*R\s*T\s+(\d)\s*(\d)", text):
            pages.setdefault(a + b, i)
    return pages


if __name__ == "__main__":
    build_html()
    if "--html" not in sys.argv:
        print_pdf()
        build_html(find_part_pages())
        print_pdf()
        print(f"PDF -> {OUT_PDF.relative_to(ROOT)}")
