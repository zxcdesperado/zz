#!/usr/bin/env python3
"""
Debug classification logic with full demo text
"""

import sys
sys.path.append('.')

from data_citation_miner import DataCitationMiner
import re

def debug_full_demo():
    miner = DataCitationMiner()
    
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
    
    dataset_id = "https://doi.org/10.5281/zenodo.7777777"
    normalized = miner.normalize_text(sample_text)
    context = miner.get_context_window(normalized, dataset_id)
    
    print(f"Dataset ID: {dataset_id}")
    print(f"Normalized text length: {len(normalized)}")
    print(f"Context window: '{context}'")
    print(f"Context length: {len(context)}")
    
    # Check DOI prefix
    doi_prefix = dataset_id.replace('https://doi.org/', '').split('/')[0]
    print(f"\nDOI prefix: {doi_prefix}")
    print(f"Is data repository: {doi_prefix in miner.data_repository_prefixes}")
    print(f"Is publisher: {doi_prefix in miner.publisher_prefixes}")
    
    # Check patterns
    context_lower = context.lower()
    
    print(f"\nPrimary indicators found:")
    primary_matches = []
    for pattern in miner.primary_indicators:
        if re.search(pattern, context_lower):
            print(f"  ✓ {pattern}")
            primary_matches.append(pattern)
    
    print(f"\nSecondary indicators found:")
    secondary_matches = []
    for pattern in miner.secondary_indicators:
        if re.search(pattern, context_lower):
            print(f"  ✓ {pattern}")
            secondary_matches.append(pattern)
    
    print(f"\nScores: Primary={len(primary_matches)}, Secondary={len(secondary_matches)}")
    
    result = miner.classify_citation_type(dataset_id, context)
    print(f"Final classification: {result}")

if __name__ == "__main__":
    debug_full_demo()