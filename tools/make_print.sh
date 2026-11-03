#!/bin/sh
# Builds the printable PDF: print/kazakh-heritage-book-A4.pdf
# Usage: sh tools/make_print.sh [https://your-site]   (default: https://kazakhheritage.netlify.app)
# Needs Python 3 + Pillow + numpy + scipy (for the illustrations), Node.js 18+ and Google Chrome or Chromium.
set -e
cd "$(dirname "$0")"
SITE="${1:-https://kazakhheritage.netlify.app}"
python3 print_stills.py
node print_book.mjs "$SITE"
CHROME="$(command -v google-chrome || command -v chromium || command -v chromium-browser)"
"$CHROME" --headless=new --no-sandbox --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$(pwd)/../print/kazakh-heritage-book-A4.pdf" "file://$(pwd)/../print/book.html"
echo "PDF: print/kazakh-heritage-book-A4.pdf"
