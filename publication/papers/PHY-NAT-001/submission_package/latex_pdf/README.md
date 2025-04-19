# Compiled PDF Files

This directory will contain the final compiled PDF files after LaTeX processing:

1. `manuscript.pdf` - The main manuscript PDF ready for submission
2. `supplementary.pdf` - The supplementary materials PDF

## Compilation Process

The PDF files are generated from the LaTeX source files in the `../latex_final/` directory using the following compilation sequence:

```
cd ../latex_final/
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
mv main.pdf ../latex_pdf/manuscript.pdf

pdflatex supplementary.tex
bibtex supplementary
pdflatex supplementary.tex
pdflatex supplementary.tex
mv supplementary.pdf ../latex_pdf/supplementary.pdf
```

## File Specifications

- **Format**: PDF 1.5 or higher
- **Compliance**: PDF/A for archival purposes
- **Fonts**: All fonts embedded
- **Resolution**: All images at 600 dpi or higher
- **Color space**: CMYK for print (with RGB version for online submission)
- **File size**: Under journal-specific limits (typically 20MB per file)

## Validation

Before submission, all PDF files have been validated for:

- Proper rendering of mathematical equations
- Figure quality and proper embedding
- Correct handling of references and citations
- Compliance with journal-specific formatting requirements
- Accessibility features as required by the publication

## Note for Nature Physics Submission

Nature Physics requires the main manuscript and supplementary materials as separate files. Both files should include all relevant metadata and be fully self-contained.

Version: v38.0 