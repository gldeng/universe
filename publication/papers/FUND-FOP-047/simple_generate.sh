#!/bin/bash
# Simple PDF generator script for FUND-FOP-047

# Set basic variables
PAPER_ID="FUND-FOP-047"
PAPER_TITLE="Golden Ratio φ, e, π and Fine Structure Constant α: Collapse Breathing Proportions"
AUTHORS="Haobo Ma and Wen Niu"
DATE=$(date +%Y-%m-%d)
VERSION="v38.0"

# Create output directory
mkdir -p submission_package/latex_pdf/additional_documents

echo "======================================================"
echo "Generating simplified PDF for $PAPER_ID"
echo "Title: $PAPER_TITLE"
echo "Authors: $AUTHORS"
echo "Date: $DATE"
echo "======================================================"

# Convert main document
echo "Converting manuscript.md to PDF..."
pandoc \
  --standalone \
  --from markdown \
  --variable title="$PAPER_TITLE" \
  --variable author="$AUTHORS" \
  --variable date="$DATE" \
  --highlight-style=tango \
  --pdf-engine=pdflatex \
  --output=submission_package/latex_pdf/manuscript.pdf \
  manuscript.md

echo "Main document PDF generation complete."

# Convert figures to PDF
echo "Converting figures to PDF format..."
mkdir -p submission_package/latex_pdf/figures

# Convert SVG figures to PDF
if command -v rsvg-convert &> /dev/null; then
  echo "Using rsvg-convert for SVG conversion..."
  find figures -name "*.svg" | while read file; do
    filename=$(basename "$file" .svg)
    echo "Processing $file..."
    rsvg-convert -f pdf -o "submission_package/latex_pdf/figures/${filename}.pdf" "$file"
  done
elif command -v convert &> /dev/null; then
  echo "Using ImageMagick convert for SVG conversion..."
  find figures -name "*.svg" | while read file; do
    filename=$(basename "$file" .svg)
    echo "Processing $file..."
    convert "$file" "submission_package/latex_pdf/figures/${filename}.pdf"
  done
else
  echo "WARNING: No SVG conversion tool found. SVG figures may not appear in PDFs."
  cp figures/*.svg submission_package/latex_pdf/figures/
fi

# Convert supplementary materials
echo "Converting supplementary materials to PDF..."
find supplementary -name "*.md" | while read file; do
  filename=$(basename "$file" .md)
  echo "Processing $file..."
  
  pandoc \
    --standalone \
    --from markdown \
    --variable title="Supplementary Material: $filename" \
    --variable author="$AUTHORS" \
    --variable date="$DATE" \
    --highlight-style=tango \
    --pdf-engine=pdflatex \
    --output="submission_package/latex_pdf/supplementary_${filename}.pdf" \
    "$file"
done

echo "Supplementary materials PDF generation complete."

# Convert additional documents
echo "Converting additional documents to PDF..."
find submission_additional_documents -name "*.md" | while read file; do
  filename=$(basename "$file" .md)
  echo "Processing $file..."
  
  pandoc \
    --standalone \
    --from markdown \
    --variable title="$filename" \
    --variable author="$AUTHORS" \
    --variable date="$DATE" \
    --highlight-style=tango \
    --pdf-engine=pdflatex \
    --output="submission_package/latex_pdf/additional_documents/${filename}.pdf" \
    "$file"
done

# Process other documents
for file in cover_letter.md highlights.md submission_checklist.md; do
  if [ -f "$file" ]; then
    filename=$(basename "$file" .md)
    echo "Processing $file..."
    
    pandoc \
      --standalone \
      --from markdown \
      --variable title="$filename" \
      --variable author="$AUTHORS" \
      --variable date="$DATE" \
      --highlight-style=tango \
      --pdf-engine=pdflatex \
      --output="submission_package/latex_pdf/${filename}.pdf" \
      "$file"
  fi
done

echo "Additional documents PDF generation complete."

# Create a combined PDF of all materials
echo "Creating combined PDF of all materials..."
pdfs=()
if [ -f "submission_package/latex_pdf/manuscript.pdf" ]; then
  pdfs+=("submission_package/latex_pdf/manuscript.pdf")
fi

for pdf in submission_package/latex_pdf/supplementary_*.pdf; do
  if [ -f "$pdf" ]; then
    pdfs+=("$pdf")
  fi
done

if [ ${#pdfs[@]} -gt 0 ]; then
  echo "Combining ${#pdfs[@]} PDFs into complete_manuscript.pdf..."
  if command -v pdfunite &> /dev/null; then
    pdfunite "${pdfs[@]}" "submission_package/latex_pdf/complete_manuscript.pdf"
  elif command -v gs &> /dev/null; then
    gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile="submission_package/latex_pdf/complete_manuscript.pdf" "${pdfs[@]}"
  else
    echo "WARNING: No PDF combination tool found. Cannot create complete manuscript."
  fi
fi

echo "======================================================"
echo "PDF generation complete. Files available at:"
echo "submission_package/latex_pdf/"
echo "======================================================"

# Add execution permissions
chmod +x "$0" 