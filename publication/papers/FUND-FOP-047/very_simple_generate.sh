#!/bin/bash
# Ultra-simplified PDF generator script for FUND-FOP-047
# Avoiding LaTeX Unicode issues by using minimal options

# Set basic variables
PAPER_ID="FUND-FOP-047"
PAPER_TITLE="Golden Ratio, Euler's Number, Pi, and Fine Structure Constant: Collapse Breathing Proportions"
AUTHORS="Haobo Ma and Wen Niu"
DATE=$(date +%Y-%m-%d)

# Create output directory
mkdir -p pdf_output

echo "======================================================"
echo "Generating basic PDF for $PAPER_ID"
echo "Title: $PAPER_TITLE"
echo "Authors: $AUTHORS"
echo "Date: $DATE"
echo "======================================================"

# Create simple HTML versions first, then convert to PDF
echo "Converting manuscript.md to HTML..."
pandoc \
  manuscript.md \
  -o pdf_output/manuscript.html \
  --standalone \
  --metadata title="$PAPER_TITLE" \
  --metadata author="$AUTHORS" \
  --metadata date="$DATE"

echo "HTML version created at pdf_output/manuscript.html"

# Try generating PDF with minimal options and no specific fonts
echo "Using pandoc's native PDF generation with minimal options..."
pandoc \
  manuscript.md \
  -o pdf_output/manuscript.pdf \
  --pdf-engine=xelatex \
  --standalone \
  --metadata title="$PAPER_TITLE" \
  --metadata author="$AUTHORS" \
  --metadata date="$DATE"

# Copy figures to output directory
mkdir -p pdf_output/figures
cp -r figures/* pdf_output/figures/

# Additionally create a Word document as backup
echo "Creating Word document version..."
pandoc \
  manuscript.md \
  -o pdf_output/manuscript.docx \
  --standalone \
  --metadata title="$PAPER_TITLE" \
  --metadata author="$AUTHORS" \
  --metadata date="$DATE"

echo "======================================================"
echo "File generation complete. Files available at:"
echo "pdf_output/manuscript.html"
echo "pdf_output/manuscript.pdf (if successful)"
echo "pdf_output/manuscript.docx (Word document backup)"
echo "======================================================"

# Make the script executable
chmod +x "$0" 