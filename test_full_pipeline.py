#!/usr/bin/env python3
"""
Full end-to-end test of the data citation miner
"""

import sys
import os
sys.path.append('.')

from data_citation_miner import DataCitationMiner

def test_full_pipeline():
    """Test the complete pipeline"""
    
    print("=== Testing Full Data Citation Mining Pipeline ===\n")
    
    # Create miner instance
    miner = DataCitationMiner()
    
    # Test with sample text (simulating extracted PDF/XML content)
    sample_article_content = {
        "10.1234/test.paper.1": """
        Methods
        We collected genomic sequencing data from 100 patients and generated raw sequencing reads
        specifically for this study. The data has been deposited at Zenodo (DOI: 10.5281/zenodo.1234567)
        and is made publicly available for the first time through this paper.
        
        Our novel protein structure dataset containing 500 structures was uploaded to 
        the Protein Data Bank with accession numbers PDB 1ABC through PDB 1XYZ.
        
        BioProject PRJNA123456 contains the raw sequencing reads we generated.
        """,
        
        "10.1234/test.paper.2": """
        Analysis
        We obtained publicly available gene expression data from GEO Series GSE12345 
        that was previously published by Smith et al. (Nature, 2020).
        
        Additional protein structures were retrieved from PDB entries 2ABC and 3DEF.
        
        Chemical compound data was extracted from the ChEMBL database (ChEMBL1234567).
        
        The reference dataset described in DOI: 10.1038/nature12345 was also analyzed.
        """,
        
        "10.1234/test.paper.3": """
        Data Availability
        Supplementary data files containing our processed genomic variants are available 
        at Dryad (https://doi.org/10.5061/dryad.abc123).
        
        Raw metabolomics data generated for this work has been uploaded to 
        MetaboLights under accession MTBLS5678.
        
        The imaging dataset we created is deposited at Figshare (DOI: 10.6084/m9.figshare.999888).
        """
    }
    
    all_results = []
    
    # Process each sample article
    for article_id, content in sample_article_content.items():
        print(f"Processing article: {article_id}")
        
        # Normalize text
        normalized_text = miner.normalize_text(content)
        
        # Extract identifiers
        dois = miner.extract_dois(normalized_text)
        accessions = miner.extract_accession_ids(normalized_text)
        
        print(f"  Found {len(dois)} DOIs and {len(accessions)} accession IDs")
        
        # Process DOIs
        for doi in dois:
            if miner.filter_false_positives(article_id, doi, normalized_text):
                context = miner.get_context_window(normalized_text, doi)
                citation_type = miner.classify_citation_type(doi, context)
                
                result = {
                    'article_id': article_id,
                    'dataset_id': doi,
                    'type': citation_type
                }
                all_results.append(result)
                print(f"    DOI: {doi} -> {citation_type}")
        
        # Process accession IDs
        for acc_id in accessions:
            if miner.filter_false_positives(article_id, acc_id, normalized_text):
                context = miner.get_context_window(normalized_text, acc_id)
                citation_type = miner.classify_citation_type(acc_id, context)
                
                result = {
                    'article_id': article_id,
                    'dataset_id': acc_id,
                    'type': citation_type
                }
                all_results.append(result)
                print(f"    ACC: {acc_id} -> {citation_type}")
        
        print()
    
    # Write submission file
    output_file = "test_submission.csv"
    miner.write_submission_csv(all_results, output_file)
    
    print(f"=== Summary ===")
    print(f"Total citations found: {len(all_results)}")
    
    # Count by type
    primary_count = sum(1 for r in all_results if r['type'] == 'Primary')
    secondary_count = sum(1 for r in all_results if r['type'] == 'Secondary')
    
    print(f"Primary citations: {primary_count}")
    print(f"Secondary citations: {secondary_count}")
    print(f"Submission file created: {output_file}")
    
    # Show sample of results
    print(f"\n=== Sample Results ===")
    for i, result in enumerate(all_results[:10]):
        print(f"{i:2d}. {result['article_id']} | {result['dataset_id'][:50]:<50} | {result['type']}")
    
    if len(all_results) > 10:
        print(f"... and {len(all_results) - 10} more")
    
    return all_results

def test_edge_cases():
    """Test edge cases and error handling"""
    print("\n=== Testing Edge Cases ===")
    
    miner = DataCitationMiner()
    
    # Test empty text
    empty_results = miner.extract_dois("")
    print(f"Empty text DOIs: {len(empty_results)}")
    
    # Test text with no identifiers
    no_id_text = "This is a paper about general topics with no specific data citations."
    no_id_dois = miner.extract_dois(no_id_text)
    no_id_accs = miner.extract_accession_ids(no_id_text)
    print(f"No identifier text - DOIs: {len(no_id_dois)}, Accessions: {len(no_id_accs)}")
    
    # Test malformed DOIs
    malformed_text = "Bad DOI: 10./bad and incomplete DOI: 10.1234 and good DOI: 10.1234/good.doi"
    malformed_dois = miner.extract_dois(malformed_text)
    print(f"Malformed DOI text: {malformed_dois}")
    
    print("Edge case testing completed.")

if __name__ == "__main__":
    try:
        all_results = test_full_pipeline()
        test_edge_cases()
        print("\n✓ All tests completed successfully!")
        
        # Verify submission file format
        if os.path.exists("test_submission.csv"):
            with open("test_submission.csv", 'r') as f:
                lines = f.readlines()
                print(f"\n=== Submission File Check ===")
                print(f"File has {len(lines)} lines (including header)")
                if len(lines) > 0:
                    print(f"Header: {lines[0].strip()}")
                if len(lines) > 1:
                    print(f"Sample row: {lines[1].strip()}")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()