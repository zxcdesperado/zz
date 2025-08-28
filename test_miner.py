#!/usr/bin/env python3
"""
Test the data citation miner functionality
"""

import sys
sys.path.append('.')

from data_citation_miner import DataCitationMiner

def test_text_processing():
    """Test the core text processing functionality"""
    
    miner = DataCitationMiner()
    
    # Test text from our sample
    test_text = """
    This study analyzes genomic sequencing data from multiple sources to understand genetic variations.
    
    We collected raw sequencing data and deposited it at Zenodo (DOI: 10.5281/zenodo.1234567).
    Additional protein structure data was obtained from the Protein Data Bank entry PDB 1ABC.
    Gene expression data was retrieved from GEO Series GSE12345.
    
    Data previously published by Smith et al. (DOI: 10.1038/nature12345) was also analyzed.
    
    Our novel dataset containing 1000 samples is made publicly available for the first time 
    through this paper at Dryad (https://doi.org/10.5061/dryad.xyz123).
    
    The BioProject accession PRJNA123456 contains the raw sequencing reads we generated 
    specifically for this study.
    
    Database reference: ChEMBL1234567.
    """
    
    # Normalize text
    normalized_text = miner.normalize_text(test_text)
    print("=== Normalized Text ===")
    print(normalized_text[:200] + "...")
    
    # Extract DOIs
    dois = miner.extract_dois(normalized_text)
    print(f"\n=== DOIs Found ({len(dois)}) ===")
    for doi in dois:
        print(f"  {doi}")
    
    # Extract accession IDs
    accessions = miner.extract_accession_ids(normalized_text)
    print(f"\n=== Accession IDs Found ({len(accessions)}) ===")
    for acc in accessions:
        print(f"  {acc}")
    
    # Test classification
    print(f"\n=== Classification Tests ===")
    for dataset_id in dois + accessions:
        context = miner.get_context_window(normalized_text, dataset_id)
        citation_type = miner.classify_citation_type(dataset_id, context)
        print(f"  {dataset_id[:50]:<50} -> {citation_type}")
        print(f"    Context: {context[:100]}")

def test_xml_processing():
    """Test XML processing"""
    miner = DataCitationMiner()
    
    xml_path = "test_data/XML/10.1234_test.paper.xml"
    xml_text = miner.extract_text_from_xml(xml_path)
    
    print(f"\n=== XML Text Extraction ===")
    print(f"Extracted {len(xml_text)} characters from XML")
    print(f"Preview: {xml_text[:200]}...")
    
    # Extract identifiers from XML
    dois = miner.extract_dois(xml_text)
    accessions = miner.extract_accession_ids(xml_text)
    
    print(f"\nFrom XML - DOIs: {len(dois)}, Accessions: {len(accessions)}")

if __name__ == "__main__":
    print("Testing Data Citation Miner...")
    test_text_processing()
    test_xml_processing()
    print("\nTest completed!")