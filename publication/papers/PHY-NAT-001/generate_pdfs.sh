#!/bin/bash
# Simplified PDF generation script for PHY-NAT-001
# Date: April 19, 2025
# Version: v38.0

echo "Generating PDFs for PHY-NAT-001 submission..."

# Create output directory
mkdir -p pdf_output

# Convert manuscript to PDF using pandoc
echo "Converting manuscript.md to PDF..."
pandoc manuscript.md -o pdf_output/manuscript.pdf --pdf-engine=xelatex

# Convert supplementary materials to PDF
echo "Converting supplementary materials to PDF..."
pandoc supplementary/mathematical_proofs.md supplementary/experimental_protocols.md supplementary/data_availability.md -o pdf_output/supplementary.pdf --pdf-engine=xelatex

# Convert cover letter to PDF
echo "Converting cover letter to PDF..."
pandoc cover_letter.md -o pdf_output/cover_letter.pdf --pdf-engine=xelatex

# Convert highlights to PDF
echo "Converting highlights to PDF..."
pandoc highlights.md -o pdf_output/highlights.pdf --pdf-engine=xelatex

# Convert submission inventory to PDF
echo "Converting submission inventory to PDF..."
pandoc 001_final_submission.md -o pdf_output/001_final_submission.pdf --pdf-engine=xelatex

# Convert submission summary to PDF
echo "Converting submission summary to PDF..."
pandoc 001_submission_summary.md -o pdf_output/001_submission_summary.pdf --pdf-engine=xelatex

# Convert additional documents to PDF
echo "Converting additional documents..."
mkdir -p pdf_output/additional_documents
for file in submission_additional_documents/*.md; do
  filename=$(basename "$file" .md)
  pandoc "$file" -o "pdf_output/additional_documents/${filename}.pdf" --pdf-engine=xelatex
done

echo "PDF generation complete. Files are available in the pdf_output directory." 