#!/usr/bin/env python3
"""
reference_formatter.py - Format references for LaTeX

This script converts references from different formats to BibTeX format
for use in LaTeX documents.

Usage:
    python reference_formatter.py <source_ref_file> <output_bibtex_file>

Example:
    python reference_formatter.py papers/PHY-SCI-003/references.md papers/PHY-SCI-003/submission_package/latex_final/bibliography.bib

Author: Universe Ontology Research Group
Version: 1.0 (April 21, 2025)
"""

import os
import sys
import re
import argparse
from datetime import datetime

def setup_argument_parser():
    """Set up command line argument parser"""
    parser = argparse.ArgumentParser(description='Format references for LaTeX')
    parser.add_argument('source', help='Source reference file')
    parser.add_argument('output', help='Output BibTeX file')
    parser.add_argument('--check-doi', action='store_true', help='Verify DOIs')
    parser.add_argument('--max-refs', type=int, default=0, help='Maximum number of references (0 for all)')
    return parser.parse_args()

def parse_markdown_references(source_file):
    """Parse references from Markdown format"""
    references = []
    
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Match references in format: [1] Author, A. (Year). Title. Journal, Volume(Issue), Pages.
    ref_pattern = r'\[\d+\]\s+(.*?)\s+\((\d{4})\)\.\s+(.*?)\.\s+(.*?)(?:,\s+(\d+)(?:\((\d+)\))?)?(?:,\s+([\d-]+))?\.?'
    matches = re.finditer(ref_pattern, content, re.DOTALL)
    
    for match in matches:
        reference = {
            'authors': match.group(1).strip(),
            'year': match.group(2),
            'title': match.group(3).strip(),
            'journal': match.group(4).strip() if match.group(4) else '',
            'volume': match.group(5) if match.group(5) else '',
            'issue': match.group(6) if match.group(6) else '',
            'pages': match.group(7) if match.group(7) else ''
        }
        references.append(reference)
    
    return references

def generate_bibtex_key(reference):
    """Generate BibTeX key from reference"""
    # Extract first author's last name
    first_author = reference['authors'].split(',')[0].strip()
    last_name = first_author.split()[-1].lower()
    
    # Remove special characters
    last_name = re.sub(r'[^a-z]', '', last_name)
    
    # Create key: LastnameYear
    return f"{last_name}{reference['year']}"

def convert_to_bibtex(references):
    """Convert references to BibTeX format"""
    bibtex_entries = []
    
    for reference in references:
        # Generate BibTeX key
        key = generate_bibtex_key(reference)
        
        # Determine entry type (article, book, etc.)
        if reference['journal'] and reference['volume']:
            entry_type = 'article'
        elif reference['journal'] and not reference['volume']:
            entry_type = 'book'
        else:
            entry_type = 'misc'
        
        # Create BibTeX entry
        entry = f"@{entry_type}{{{key},\n"
        entry += f"  title={{{reference['title']}}},\n"
        entry += f"  author={{{reference['authors']}}},\n"
        entry += f"  year={{{reference['year']}}},\n"
        
        if reference['journal']:
            entry += f"  journal={{{reference['journal']}}},\n"
        
        if reference['volume']:
            entry += f"  volume={{{reference['volume']}}},\n"
        
        if reference['issue']:
            entry += f"  number={{{reference['issue']}}},\n"
        
        if reference['pages']:
            entry += f"  pages={{{reference['pages']}}},\n"
        
        entry += "}\n\n"
        bibtex_entries.append(entry)
    
    return bibtex_entries

def write_bibtex_file(bibtex_entries, output_file, max_refs=0):
    """Write BibTeX entries to file"""
    # Limit number of references if requested
    if max_refs > 0 and max_refs < len(bibtex_entries):
        bibtex_entries = bibtex_entries[:max_refs]
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"% Bibliography generated on {datetime.now().strftime('%Y-%m-%d')}\n")
        f.write(f"% Contains {len(bibtex_entries)} references\n\n")
        for entry in bibtex_entries:
            f.write(entry)
    
    print(f"BibTeX file generated with {len(bibtex_entries)} references: {output_file}")

def main():
    """Main function"""
    # Parse command line arguments
    args = setup_argument_parser()
    
    # Parse references from source file
    references = parse_markdown_references(args.source)
    print(f"Found {len(references)} references in source file")
    
    # Convert to BibTeX format
    bibtex_entries = convert_to_bibtex(references)
    
    # Write to output file
    write_bibtex_file(bibtex_entries, args.output, args.max_refs)

if __name__ == "__main__":
    main() 