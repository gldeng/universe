#!/usr/bin/env python3
"""
latex_compiler.py - Compile LaTeX files to PDF

This script compiles LaTeX files to PDF format using pdflatex and bibtex.
It handles the multi-pass compilation process needed for proper references.

Usage:
    python latex_compiler.py <latex_dir> [--output <output_dir>] [--name <output_name>]

Example:
    python latex_compiler.py papers/PHY-SCI-003/submission_package/latex_final --output papers/PHY-SCI-003/submission_package/latex_pdf --name manuscript

Author: Universe Ontology Research Group
Version: 1.0 (April 21, 2025)
"""

import os
import sys
import argparse
import subprocess
import shutil
from datetime import datetime

def setup_argument_parser():
    """Set up command line argument parser"""
    parser = argparse.ArgumentParser(description='Compile LaTeX to PDF')
    parser.add_argument('latex_dir', help='Directory containing LaTeX files')
    parser.add_argument('--output', help='Output directory for PDF files')
    parser.add_argument('--name', default='manuscript', help='Output filename (without extension)')
    parser.add_argument('--draft', action='store_true', help='Generate draft version with line numbers')
    return parser.parse_args()

def ensure_directory(directory):
    """Ensure directory exists"""
    os.makedirs(directory, exist_ok=True)
    
def compile_latex(latex_dir, output_dir=None, output_name='manuscript', draft=False):
    """Compile LaTeX to PDF"""
    # Set default output directory if not specified
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(latex_dir), 'latex_pdf')
    
    # Ensure output directory exists
    ensure_directory(output_dir)
    
    # Store current directory
    original_dir = os.getcwd()
    
    try:
        # Change to LaTeX directory
        os.chdir(latex_dir)
        
        # Create temporary files for missing sections
        section_files = ['introduction.tex', 'methods.tex', 'theory.tex', 
                         'verification.tex', 'discussion.tex', 'conclusion.tex', 
                         'acknowledgments.tex']
        
        for section_file in section_files:
            if not os.path.exists(section_file):
                with open(section_file, 'w') as f:
                    f.write(f"% Placeholder for {section_file}\n")
                print(f"Created placeholder for {section_file}")
        
        # Run pdflatex (first pass)
        print("Running pdflatex (first pass)...")
        result = subprocess.run(['pdflatex', 'main.tex'], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE, 
                               universal_newlines=True)
        
        if result.returncode != 0:
            print("Error during first pdflatex pass:")
            print(result.stderr)
            return False
        
        # Run bibtex if bibliography.bib exists
        if os.path.exists('bibliography.bib'):
            print("Running bibtex...")
            result = subprocess.run(['bibtex', 'main'], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE, 
                                  universal_newlines=True)
            
            if result.returncode != 0:
                print("Error during bibtex:")
                print(result.stderr)
                return False
        
        # Run pdflatex (second pass)
        print("Running pdflatex (second pass)...")
        result = subprocess.run(['pdflatex', 'main.tex'], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE, 
                               universal_newlines=True)
        
        if result.returncode != 0:
            print("Error during second pdflatex pass:")
            print(result.stderr)
            return False
        
        # Run pdflatex (third pass)
        print("Running pdflatex (third pass)...")
        result = subprocess.run(['pdflatex', 'main.tex'], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE, 
                               universal_newlines=True)
        
        if result.returncode != 0:
            print("Error during third pdflatex pass:")
            print(result.stderr)
            return False
        
        # Copy PDF to output directory
        if os.path.exists('main.pdf'):
            # Rename to requested output name
            output_file = os.path.join(output_dir, f"{output_name}.pdf")
            shutil.copy('main.pdf', output_file)
            print(f"PDF successfully generated: {output_file}")
            return True
        else:
            print("PDF generation failed: output file not found")
            return False
    
    finally:
        # Return to original directory
        os.chdir(original_dir)

def cleanup_temp_files(latex_dir):
    """Clean up temporary LaTeX files"""
    extensions = ['.aux', '.log', '.out', '.toc', '.lof', '.lot', '.bbl', '.blg']
    for ext in extensions:
        files = [f for f in os.listdir(latex_dir) if f.endswith(ext)]
        for file in files:
            try:
                os.remove(os.path.join(latex_dir, file))
            except:
                pass
    print("Temporary files cleaned up")

def main():
    """Main function"""
    # Parse command line arguments
    args = setup_argument_parser()
    
    # Compile LaTeX
    success = compile_latex(args.latex_dir, args.output, args.name, args.draft)
    
    # Clean up temporary files if successful
    if success:
        cleanup_temp_files(args.latex_dir)
        print("LaTeX compilation completed successfully")
    else:
        print("LaTeX compilation failed")
        sys.exit(1)

if __name__ == "__main__":
    main() 