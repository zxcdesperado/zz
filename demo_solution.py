#!/usr/bin/env python3
"""
Final demonstration of the data citation mining solution
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.append('.')

from data_citation_miner import DataCitationMiner

def demo_solution():
    """Demonstrate the complete data citation mining solution"""
    
    print("🔬 Data Citation Mining Solution Demonstration")
    print("=" * 60)
    
    # Initialize the miner
    miner = DataCitationMiner()
    
    print("\n📊 Supported Data Repositories:")
    print("DOI Prefixes (Primary bias):")
    for prefix in sorted(miner.data_repository_prefixes):
        print(f"  • {prefix} (Zenodo, Dryad, Figshare, etc.)")
    
    print(f"\nPublisher Prefixes (Secondary bias): {len(miner.publisher_prefixes)} publishers")
    print(f"Accession Patterns: {len(miner.accession_patterns)} database types")
    
    # Demo text processing
    print("\n📄 Text Processing Demo:")
    sample_text = """
    Data Availability Statement
    
    Raw genomic sequencing data generated for this study has been deposited 
    in the NCBI Sequence Read Archive under BioProject accession PRJNA123456.
    
    Processed variant call datasets are publicly available for the first time 
    through this paper at Zenodo (DOI: 10.5281/zenodo.7777777).
    
    Protein structure coordinates were obtained from the Protein Data Bank 
    entries PDB 1ABC and PDB 2DEF that were previously published by Smith et al.
    
    Gene expression data was retrieved from GEO Series GSE55555 described 
    in the original publication (DOI: 10.1038/nature12345).
    
    Additional chemical compound information was extracted from ChEMBL1234567.
    """
    
    print(f"Sample text length: {len(sample_text)} characters")
    
    # Extract identifiers
    normalized = miner.normalize_text(sample_text)
    dois = miner.extract_dois(normalized)
    accessions = miner.extract_accession_ids(normalized)
    
    print(f"\n🔍 Extracted Identifiers:")
    print(f"DOIs found: {len(dois)}")
    for doi in dois:
        print(f"  • {doi}")
    
    print(f"\nAccession IDs found: {len(accessions)}")
    for acc in accessions:
        print(f"  • {acc}")
    
    # Classification demo
    print(f"\n🎯 Classification Results:")
    article_id = "10.1234/demo.paper"
    results = []
    
    for dataset_id in dois + accessions:
        context = miner.get_context_window(normalized, dataset_id)
        citation_type = miner.classify_citation_type(dataset_id, context)
        
        results.append({
            'article_id': article_id,
            'dataset_id': dataset_id,
            'type': citation_type
        })
        
        print(f"  {dataset_id[:50]:<50} → {citation_type}")
        # Show reasoning
        if citation_type == 'Primary':
            print(f"    💡 Reason: Data repository or generation indicators")
        else:
            print(f"    💡 Reason: Publisher DOI or reuse indicators")
    
    # Generate submission
    print(f"\n📋 Submission Generation:")
    output_file = "demo_submission.csv"
    miner.write_submission_csv(results, output_file)
    
    # Show submission preview
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            lines = f.readlines()
        
        print(f"Generated {output_file} with {len(lines)-1} data citations:")
        print("Preview:")
        for i, line in enumerate(lines[:6]):  # Show header + first 5 rows
            print(f"  {line.strip()}")
        if len(lines) > 6:
            print(f"  ... and {len(lines)-6} more rows")
    
    # Summary statistics
    primary_count = sum(1 for r in results if r['type'] == 'Primary')
    secondary_count = sum(1 for r in results if r['type'] == 'Secondary')
    
    print(f"\n📈 Classification Summary:")
    print(f"  Primary citations:   {primary_count:2d} ({primary_count/len(results)*100:4.1f}%)")
    print(f"  Secondary citations: {secondary_count:2d} ({secondary_count/len(results)*100:4.1f}%)")
    print(f"  Total citations:     {len(results):2d}")
    
    print(f"\n✅ Demo completed successfully!")
    print(f"\nTo process real data, use:")
    print(f"  python data_citation_miner.py /path/to/pdf/directory")

def check_dependencies():
    """Check if all dependencies are available"""
    print("\n🔧 Dependency Check:")
    
    try:
        import fitz
        print("  ✅ PyMuPDF (PDF processing)")
    except ImportError:
        print("  ❌ PyMuPDF not found - install with: pip install PyMuPDF")
    
    try:
        import xml.etree.ElementTree as ET
        print("  ✅ XML processing (built-in)")
    except ImportError:
        print("  ❌ XML processing not available")
    
    try:
        import re
        print("  ✅ Regular expressions (built-in)")
    except ImportError:
        print("  ❌ RE module not available")
    
    try:
        import csv
        print("  ✅ CSV processing (built-in)")
    except ImportError:
        print("  ❌ CSV module not available")

if __name__ == "__main__":
    try:
        check_dependencies()
        demo_solution()
        
        print("\n🎉 Solution is ready for the Make Data Count competition!")
        print("\nNext steps:")
        print("  1. Ensure you have competition data in PDF format")
        print("  2. Run: python data_citation_miner.py /path/to/test/PDF")
        print("  3. Submit the generated submission.csv file")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()