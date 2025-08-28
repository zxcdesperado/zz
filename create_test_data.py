#!/usr/bin/env python3
"""
Test script to create sample PDF and XML files for testing the data citation miner
"""

import os
from pathlib import Path

# Create a simple test PDF using text (since we don't have complex PDF libraries)
test_pdf_content = """
Scientific Paper Title: Analysis of Genomic Data

Abstract
This study analyzes genomic sequencing data from multiple sources to understand genetic variations.

Methods
We collected raw sequencing data and deposited it at Zenodo (DOI: 10.5281/zenodo.1234567).
Additional protein structure data was obtained from the Protein Data Bank entry PDB 1ABC.
Gene expression data was retrieved from GEO Series GSE12345.

Data previously published by Smith et al. (DOI: 10.1038/nature12345) was also analyzed.

Results
Our novel dataset containing 1000 samples is made publicly available for the first time 
through this paper at Dryad (https://doi.org/10.5061/dryad.xyz123).

The BioProject accession PRJNA123456 contains the raw sequencing reads we generated 
specifically for this study.

References
1. Smith, J. et al. Previous work. Nature 123, 456-789 (2020). DOI: 10.1038/nature12345
2. Database reference. ChEMBL Database (CHEMBL1234567).
"""

test_xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<article>
    <front>
        <article-meta>
            <title-group>
                <article-title>Analysis of Genomic Data</article-title>
            </title-group>
        </article-meta>
    </front>
    <body>
        <sec sec-type="data-availability">
            <title>Data Availability</title>
            <p>Raw sequencing data generated for this study has been deposited in the 
            Sequence Read Archive under BioProject PRJNA123456. Processed datasets 
            are available at Figshare (DOI: 10.6084/m9.figshare.987654).</p>
            <p>Additional supplementary data is available at our institutional repository 
            (DOI: 10.5281/zenodo.1234567).</p>
        </sec>
    </body>
</article>
"""

def create_test_files():
    """Create test PDF and XML files"""
    
    # For testing, we'll create text files that our miner can process
    # In a real scenario, these would be actual PDF files
    test_dir = Path("test_data")
    pdf_dir = test_dir / "PDF"
    xml_dir = test_dir / "XML"
    
    # Create test PDF (as text file for now - our miner handles missing PDF gracefully)
    pdf_file = pdf_dir / "10.1234_test.paper.pdf"
    
    # Create test XML
    xml_file = xml_dir / "10.1234_test.paper.xml"
    xml_file.write_text(test_xml_content)
    
    print(f"Created test files:")
    print(f"  XML: {xml_file}")
    print(f"  Note: PDF processing requires actual PDF files")
    
    # Create a simple text version for testing text extraction
    text_file = test_dir / "sample_text.txt"
    text_file.write_text(test_pdf_content)
    print(f"  Text sample: {text_file}")

if __name__ == "__main__":
    create_test_files()