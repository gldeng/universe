#!/bin/bash

# Script to convert SVG to PNG and PDF for paper figures

convert_figures() {
  PAPER_DIR="$1"
  echo "Processing figures for $PAPER_DIR..."
  cd "publication/papers/$PAPER_DIR/figures" || exit 1
  
  # For each SVG file, create PNG and PDF
  for svg_file in svg/*.svg; do
    base_name=$(basename "$svg_file" .svg)
    echo "Converting $base_name.svg to PNG and PDF..."
    
    # Convert SVG to PNG at 600 DPI
    rsvg-convert -d 600 -p 600 "$svg_file" -o "png/${base_name}.png" || echo "Error converting to PNG: $base_name"
    
    # Convert SVG to PDF
    rsvg-convert -f pdf "$svg_file" -o "pdf/${base_name}.pdf" || echo "Error converting to PDF: $base_name"
  done
  
  echo "Conversion complete for $PAPER_DIR"
  cd - > /dev/null
}

# Convert figures for all three papers
convert_figures "PHY-NAT-001"
convert_figures "PHY-PRL-002"
convert_figures "PHY-SCI-003"

echo "All figure conversions completed successfully."
