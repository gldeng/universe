#!/usr/bin/env python3
"""
md_to_latex.py - Convert Markdown files to LaTeX format

This script converts Markdown format papers to LaTeX format
for submission to academic journals.

Usage:
    python md_to_latex.py <source_markdown> <target_latex_dir> [--template <template_name>]

Example:
    python md_to_latex.py papers/PHY-SCI-003/manuscript.md papers/PHY-SCI-003/submission_package/latex_final --template science

Author: Universe Ontology Research Group
Version: 1.0 (April 21, 2025)
"""

import os
import sys
import re
import argparse
import shutil
from datetime import datetime

def setup_argument_parser():
    """Set up command line argument parser"""
    parser = argparse.ArgumentParser(description='Convert Markdown to LaTeX format')
    parser.add_argument('source', help='Source Markdown file')
    parser.add_argument('target_dir', help='Target LaTeX directory')
    parser.add_argument('--template', default='default', help='LaTeX template to use')
    return parser.parse_args()

def extract_sections(markdown_content):
    """Extract different sections from Markdown content"""
    sections = {
        'title': '',
        'abstract': '',
        'introduction': '',
        'methods': '',
        'theory': '',
        'verification': '',
        'discussion': '',
        'conclusion': '',
        'acknowledgments': ''
    }
    
    # Extract title (first level-1 heading)
    title_match = re.search(r'^# (.+)$', markdown_content, re.MULTILINE)
    if title_match:
        sections['title'] = title_match.group(1)
    
    # Extract abstract
    abstract_match = re.search(r'^## Abstract\s+(.+?)(?=^##)', markdown_content, re.MULTILINE | re.DOTALL)
    if abstract_match:
        sections['abstract'] = abstract_match.group(1).strip()
    
    # Extract other sections
    for section in ['introduction', 'methods', 'theory', 'verification', 'discussion', 'conclusion', 'acknowledgments']:
        section_match = re.search(r'^## ' + section.capitalize() + r'\s+(.+?)(?=^##|\Z)', 
                                  markdown_content, re.MULTILINE | re.DOTALL | re.IGNORECASE)
        if section_match:
            sections[section] = section_match.group(1).strip()
    
    return sections

def process_equations(text):
    """Convert Markdown equations to LaTeX format"""
    # Convert inline equations: $x$ → $x$
    text = re.sub(r'\$`(.+?)`\$', r'$\1$', text)
    
    # Convert display equations: $$equation$$ → \begin{equation}equation\end{equation}
    text = re.sub(r'\$`(.+?)`\$', r'\\begin{equation}\1\\end{equation}', text)
    
    return text

def process_figures(text, figure_dir):
    """Process figure references"""
    # Replace Markdown figure syntax with LaTeX figure environment
    def figure_replace(match):
        alt_text = match.group(1)
        path = match.group(2)
        filename = os.path.basename(path)
        return f"\\begin{{figure}}[ht]\n\\centering\n\\includegraphics[width=0.8\\textwidth]{{{figure_dir}/{filename}}}\n\\caption{{{alt_text}}}\n\\label{{fig:{filename.split('.')[0]}}}\n\\end{{figure}}"
    
    text = re.sub(r'!\[(.*?)\]\((.*?)\)', figure_replace, text)
    return text

def process_references(text):
    """Convert Markdown citations to LaTeX citations"""
    # Replace [Author, Year] with \cite{AuthorYear}
    text = re.sub(r'\[([^,]+), (\d{4})\]', r'\\cite{\1\2}', text)
    
    # Replace other citation formats as needed
    # ...
    
    return text

def convert_markdown_to_latex(source_file, target_dir, template_name='default'):
    """Convert Markdown file to LaTeX format"""
    # Read markdown file
    with open(source_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Extract sections
    sections = extract_sections(markdown_content)
    
    # Process each section
    for section, content in sections.items():
        if content:
            # Process equations
            content = process_equations(content)
            
            # Process figures
            content = process_figures(content, 'figures')
            
            # Process references
            content = process_references(content)
            
            # Write to separate .tex file
            with open(os.path.join(target_dir, f"{section}.tex"), 'w', encoding='utf-8') as f:
                f.write(content)
    
    print(f"Conversion complete. LaTeX files written to {target_dir}")

def main():
    """Main function"""
    # Parse command line arguments
    args = setup_argument_parser()
    
    # Ensure target directory exists
    os.makedirs(args.target_dir, exist_ok=True)
    
    # Convert markdown to latex
    convert_markdown_to_latex(args.source, args.target_dir, args.template)

if __name__ == "__main__":
    main() 