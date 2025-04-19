#!/bin/bash
# PHY-NAT-001 Submission Compilation Script
# Date: April 19, 2025
# Version: v38.0

echo "Starting compilation of PHY-NAT-001 submission package..."

# Set directories
CURRENT_DIR=$(pwd)
LATEX_DIR="${CURRENT_DIR}/submission_package/latex_final"
PDF_DIR="${CURRENT_DIR}/submission_package/latex_pdf"
FINAL_DIR="${CURRENT_DIR}/submission_package/final_submission"

# Create final submission directory if it doesn't exist
mkdir -p $FINAL_DIR

# Step 1: Compile LaTeX to PDF
echo "Compiling LaTeX files to PDF..."

cd $LATEX_DIR

# Compile main manuscript
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
mv main.pdf $PDF_DIR/manuscript.pdf

# Compile supplementary materials
pdflatex supplementary.tex
bibtex supplementary
pdflatex supplementary.tex
pdflatex supplementary.tex
mv supplementary.pdf $PDF_DIR/supplementary.pdf

# Clean up LaTeX temporary files
rm -f *.aux *.log *.out *.bbl *.blg *.dvi

echo "LaTeX compilation complete. PDFs generated in $PDF_DIR"

# Step 2: Prepare all submission documents
echo "Preparing final submission package..."

# Copy main documents
cp $PDF_DIR/manuscript.pdf $FINAL_DIR/
cp $PDF_DIR/supplementary.pdf $FINAL_DIR/
cp $CURRENT_DIR/cover_letter.md $FINAL_DIR/
cp $CURRENT_DIR/highlights.md $FINAL_DIR/

# Convert Markdown to PDF where needed
pandoc $CURRENT_DIR/cover_letter.md -o $FINAL_DIR/cover_letter.pdf
pandoc $CURRENT_DIR/highlights.md -o $FINAL_DIR/highlights.pdf

# Copy additional documents
mkdir -p $FINAL_DIR/additional_documents
cp $CURRENT_DIR/submission_additional_documents/*.md $FINAL_DIR/additional_documents/

# Convert additional documents to PDF
for file in $FINAL_DIR/additional_documents/*.md; do
  filename=$(basename "$file" .md)
  pandoc "$file" -o "$FINAL_DIR/additional_documents/$filename.pdf"
done

# Copy figures
mkdir -p $FINAL_DIR/figures
cp $CURRENT_DIR/figures/*.svg $FINAL_DIR/figures/

# Copy simulation code
mkdir -p $FINAL_DIR/code
cp -r $CURRENT_DIR/code/* $FINAL_DIR/code/

# Generate submission inventory
cp $CURRENT_DIR/001_final_submission.md $FINAL_DIR/
pandoc $CURRENT_DIR/001_final_submission.md -o $FINAL_DIR/001_final_submission.pdf

# Create submission metadata file
cat > $FINAL_DIR/submission_metadata.txt << EOF
Title: XOR-SHIFT Operations Unifying Quantum and Relativistic Frameworks
Author: Auric
Target Journal: Nature Physics
Submission Date: August 2025
Version: v38.0
Compiled: $(date)
Word Count: 3,982
Figure Count: 5
Supplementary Files: 3
EOF

# Create a zip archive of the entire submission
cd $CURRENT_DIR
zip -r submission_package/PHY-NAT-001_submission.zip $FINAL_DIR/*

echo "Submission package preparation complete."
echo "Final submission files are available in: $FINAL_DIR"
echo "Zip archive created: submission_package/PHY-NAT-001_submission.zip"
echo "Done." 