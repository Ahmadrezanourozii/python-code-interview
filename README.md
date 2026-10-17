# Python Live Coding: Interview Prep (FA)

A short Persian study guide for a *small live coding task in Python*.
Every code sample in the PDF is run while the guide is built, and the output
shown under each sample is the real output.

**Read this:** [`Python-Live-Coding-Guide-FA.pdf`](Python-Live-Coding-Guide-FA.pdf)

| Folder | What is in it |
| --- | --- |
| `snippets/` | All code from the guide as plain Python files, e.g. `python3 snippets/07_lists.py` |
| `guide/template.html` | The guide text (Persian) with `{{file:cell}}` markers for code |
| `tools/build.py` | Runs every snippet, fills the template, prints the PDF |
| `tools/make_pdf.js` | Headless Chromium (Playwright) HTML → PDF |

## Rebuild

```bash
pip install pygments pandas pypdf pytest
python3 tools/build.py          # needs Node + Playwright for the PDF step
python3 tools/build.py --html   # HTML only
```

Fonts: Vazirmatn and JetBrains Mono (both SIL OFL, licences in `guide/fonts/`).
