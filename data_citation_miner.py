#!/usr/bin/env python3
"""
Data Citation Mining Solution for Make Data Count Competition

This script identifies data citations in scientific papers and classifies them
as Primary (data generated for the paper) or Secondary (data reused from existing sources).
"""

import os
import re
import csv
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Set
import argparse

# Available standard libraries for PDF processing
try:
    import fitz  # PyMuPDF
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False

try:
    import xml.etree.ElementTree as ET
    HAS_XML = True
except ImportError:
    HAS_XML = False


class DataCitationMiner:
    """Main class for mining data citations from scientific papers"""
    
    def __init__(self):
        # DOI patterns for known data repositories (Primary indicators)
        self.data_repository_prefixes = {
            '10.5061',      # Dryad
            '10.5281',      # Zenodo  
            '10.6084',      # Figshare
            '10.24433',     # Mendeley Data
            '10.17632',     # Mendeley Data
            '10.7910',      # Dataverse
            '10.18112',     # OpenNeuro
            '10.1594',      # PANGAEA
            '10.21233',     # Neotoma Paleoecology
            '10.3886',      # ICPSR
            '10.7289',      # NOAA NCEI
            '10.5255',      # UK Data Service
            '10.6019',      # EMPIAR
        }
        
        # Publisher DOI prefixes (typically Secondary)
        self.publisher_prefixes = {
            '10.1038', '10.1007', '10.1126', '10.1016', '10.1101', '10.1021', 
            '10.1145', '10.1177', '10.1093', '10.1080', '10.1111', '10.1098',
            '10.1103', '10.1186', '10.1371', '10.7554', '10.1039', '10.1002',
            '10.3390', '10.1073', '10.1097', '10.15252', '10.1136', '10.1091',
            '10.1523', '10.1152', '10.1128', '10.1155', '10.1242', '10.1182'
        }
        
        # Accession ID patterns for biological databases
        self.accession_patterns = [
            r'\bCHEMBL\d+\b',                    # ChEMBL
            r'\bE-(?:GEOD|PROT|MTAB|MEXP)-\d+\b', # ArrayExpress/EMBL-EBI
            r'\bEMPIAR-\d+\b',                  # EMPIAR
            r'\bPRJNA\d+\b',                    # BioProject NCBI
            r'\bPRJEB\d+\b',                    # BioProject ENA
            r'\bPRJDB\d+\b',                    # BioProject DDBJ
            r'\bPXD\d+\b',                      # ProteomeXchange
            r'\bSAMN\d+\b',                     # BioSample
            r'\bGSE\d+\b',                      # GEO Series
            r'\bGSM\d+\b',                      # GEO Sample
            r'\bPDB\s*[1-9][A-Z0-9]{3}\b',      # Protein Data Bank
            r'\b(?:SRP|SRA|ERP|ERX|SRR|ERR|DRR|DRX|DRP)\d+\b', # Sequence Read Archive
            r'\bHMDB\d+\b',                     # Human Metabolome Database
            r'\bMTBLS\d+\b',                    # MetaboLights
            r'\bEMD-\d+\b',                     # Electron Microscopy Data Bank
        ]
        
        # Patterns for DOI identification
        self.doi_pattern = re.compile(r'\b10\.\d{4,}/[^\s\'"<>]+', re.IGNORECASE)
        
        # Primary classification indicators
        self.primary_indicators = [
            r'\b(?:we|our|this\s+(?:study|paper))\s+(?:generated|created|collected|developed|produced)\b',
            r'\b(?:specifically|newly|originally)\s+(?:generated|created|collected|developed)\b',
            r'\b(?:raw|processed)\s+data\s+(?:generated|collected|produced|created)\b',
            r'\bmade\s+(?:publicly\s+)?available\s+(?:for\s+the\s+first\s+time|through\s+this\s+(?:paper|study))\b',
            r'\boriginal\s+(?:data|dataset|contribution)\b',
            r'\b(?:supplementary|supporting)\s+(?:data|materials|information)\b',
            r'\bdeposited\s+(?:at|in|to)\b',
            r'\buploaded\s+(?:to|at)\b',
            r'\bnovel\s+dataset\b',
            r'\bgenerated\s+(?:specifically\s+)?for\s+this\s+study\b',
        ]
        
        # Secondary classification indicators  
        self.secondary_indicators = [
            r'\b(?:obtained|retrieved|downloaded|extracted|acquired)\s+from\b',
            r'\b(?:reused|adopted|used|utilized)\s+(?:the\s+)?(?:existing\s+)?(?:data|dataset)\b',
            r'\b(?:previously\s+)?published\s+(?:by|in|data|dataset)\b',
            r'\bwell-established\s+(?:resource|database|dataset)\b',
            r'\bbenchmark\s+dataset\b',
            r'\bpublicly\s+available\s+data\b',
            r'\breference\b.*\bdatabase\b',
            r'\b(?:database|data)\s+(?:was\s+)?(?:previously\s+)?(?:published|described)\b',
        ]

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        if not HAS_PYMUPDF:
            return ""
            
        try:
            text = ""
            with fitz.open(pdf_path) as doc:
                for page in doc:
                    text += page.get_text()
            return text
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {e}")
            return ""
    
    def extract_text_from_xml(self, xml_path: str) -> str:
        """Extract data availability text from XML file"""
        if not HAS_XML or not os.path.exists(xml_path):
            return ""
            
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            # Look for data availability sections
            data_availability_text = []
            for elem in root.iter():
                if elem.tag.lower().endswith('sec'):
                    title = ""
                    for child in elem:
                        if child.tag.lower().endswith('title'):
                            title = (child.text or '').strip().lower()
                            break
                    
                    if any(keyword in title for keyword in ['data availability', 'availability', 'data access']):
                        sec_text = ''.join(elem.itertext())
                        data_availability_text.append(sec_text)
            
            return '\n\n'.join(data_availability_text)
        except Exception as e:
            print(f"Error extracting XML from {xml_path}: {e}")
            return ""

    def normalize_text(self, text: str) -> str:
        """Normalize text for better pattern matching"""
        # Replace various dash types with standard dash
        text = re.sub(r'[\u2010\u2011\u2012\u2013\u2014\u2212\uFE63\uFF0D]', '-', text)
        # Remove soft hyphens and zero-width characters  
        text = re.sub(r'[\u00AD\u200B\u200C\u200D\u2060\uFEFF]', '', text)
        # Normalize DOI formats
        text = re.sub(r'https?://dx\.doi\.org/', 'https://doi.org/', text)
        text = re.sub(r'\bdoi:\s*', '', text, flags=re.IGNORECASE)
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        return text

    def extract_dois(self, text: str) -> List[str]:
        """Extract DOI identifiers from text"""
        dois = []
        matches = self.doi_pattern.findall(text)
        
        for match in matches:
            # Clean up the DOI - remove trailing punctuation and symbols
            doi = re.sub(r'[^\w\-\./]+$', '', match)
            # Remove common trailing artifacts
            doi = re.sub(r'[\)\]\.;,]+$', '', doi)
            doi = doi.lower().strip()
            
            # Skip very short DOIs
            if len(doi.split('/')) < 2 or len(doi.split('/')[-1]) < 3:
                continue
            
            # Convert to full DOI format
            if not doi.startswith('https://doi.org/'):
                doi = f'https://doi.org/{doi}'
            
            dois.append(doi)
        
        return list(set(dois))  # Remove duplicates

    def extract_accession_ids(self, text: str) -> List[str]:
        """Extract accession IDs from text"""
        accession_ids = []
        
        for pattern in self.accession_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                # Clean up the match
                clean_id = re.sub(r'\s+', '', match)  # Remove spaces
                clean_id = re.sub(r'^PDB\s*', '', clean_id, flags=re.IGNORECASE)  # Remove PDB prefix
                accession_ids.append(clean_id)
        
        return list(set(accession_ids))  # Remove duplicates

    def classify_citation_type(self, dataset_id: str, context: str) -> str:
        """Classify whether a data citation is Primary or Secondary"""
        context_lower = context.lower()
        
        # Check if it's a DOI
        if dataset_id.startswith('https://doi.org/'):
            doi_prefix = dataset_id.replace('https://doi.org/', '').split('/')[0]
            
            # Known data repository = likely Primary
            if doi_prefix in self.data_repository_prefixes:
                # But check for secondary indicators
                secondary_score = sum(1 for pattern in self.secondary_indicators 
                                    if re.search(pattern, context_lower))
                if secondary_score > 0:
                    return 'Secondary'
                return 'Primary'
            
            # Known publisher = likely Secondary  
            if doi_prefix in self.publisher_prefixes:
                # But check for primary indicators
                primary_score = sum(1 for pattern in self.primary_indicators 
                                  if re.search(pattern, context_lower))
                if primary_score > 0:
                    return 'Primary'
                return 'Secondary'
        
        # Check primary indicators in context
        primary_score = sum(1 for pattern in self.primary_indicators 
                          if re.search(pattern, context_lower))
        
        # Check secondary indicators in context
        secondary_score = sum(1 for pattern in self.secondary_indicators 
                            if re.search(pattern, context_lower))
        
        # Decision based on scores
        if primary_score > secondary_score:
            return 'Primary'
        elif secondary_score > primary_score:
            return 'Secondary'
        else:
            # Default classification based on identifier type
            if dataset_id.startswith('https://doi.org/'):
                return 'Primary'  # DOIs default to Primary
            else:
                return 'Secondary'  # Accession IDs default to Secondary

    def get_context_window(self, text: str, identifier: str, window_size: int = 200) -> str:
        """Get context window around an identifier"""
        # Normalize identifier for searching
        search_id = identifier.replace('https://doi.org/', '')
        
        # Try to find the identifier in various forms
        positions = []
        
        # Look for the exact identifier
        for pattern in [identifier, search_id, search_id.upper(), search_id.lower()]:
            match = re.search(re.escape(pattern), text, re.IGNORECASE)
            if match:
                positions.append(match.start())
        
        if not positions:
            return ""
        
        # Use the first found position
        pos = positions[0]
        start_idx = max(0, pos - window_size)
        end_idx = min(len(text), pos + len(identifier) + window_size)
        
        return text[start_idx:end_idx].strip()

    def filter_false_positives(self, article_id: str, dataset_id: str, text: str) -> bool:
        """Filter out likely false positive matches"""
        # Don't include references to the paper itself
        if dataset_id.startswith('https://doi.org/'):
            paper_doi_pattern = article_id.replace('_', '/')
            if paper_doi_pattern in dataset_id:
                return False
        
        # Don't include very short DOI suffixes (likely incomplete)
        if dataset_id.startswith('https://doi.org/'):
            suffix = dataset_id.replace('https://doi.org/', '').split('/')[-1]
            if len(suffix) < 5:
                return False
        
        return True

    def process_article(self, article_id: str, pdf_path: str, xml_path: str = None) -> List[Dict]:
        """Process a single article and extract data citations"""
        # Extract text from PDF
        pdf_text = self.extract_text_from_pdf(pdf_path)
        
        # Extract additional text from XML if available
        xml_text = ""
        if xml_path and os.path.exists(xml_path):
            xml_text = self.extract_text_from_xml(xml_path)
        
        # Combine and normalize text
        full_text = self.normalize_text(pdf_text + "\n\n" + xml_text)
        
        if not full_text.strip():
            return []
        
        # Extract identifiers
        dois = self.extract_dois(full_text)
        accession_ids = self.extract_accession_ids(full_text)
        
        results = []
        
        # Process DOIs
        for doi in dois:
            if self.filter_false_positives(article_id, doi, full_text):
                context = self.get_context_window(full_text, doi)
                citation_type = self.classify_citation_type(doi, context)
                
                results.append({
                    'article_id': article_id,
                    'dataset_id': doi,
                    'type': citation_type
                })
        
        # Process accession IDs
        for acc_id in accession_ids:
            if self.filter_false_positives(article_id, acc_id, full_text):
                context = self.get_context_window(full_text, acc_id)
                citation_type = self.classify_citation_type(acc_id, context)
                
                results.append({
                    'article_id': article_id,
                    'dataset_id': acc_id,
                    'type': citation_type
                })
        
        return results

    def process_directory(self, pdf_dir: str, xml_dir: str = None, output_file: str = "submission.csv") -> None:
        """Process all articles in a directory"""
        pdf_path = Path(pdf_dir)
        xml_path = Path(xml_dir) if xml_dir else None
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF directory not found: {pdf_dir}")
        
        all_results = []
        
        # Find all PDF files
        pdf_files = list(pdf_path.glob("*.pdf")) + list(pdf_path.glob("*.PDF"))
        
        for pdf_file in pdf_files:
            article_id = pdf_file.stem
            
            # Find corresponding XML file
            xml_file = None
            if xml_path and xml_path.exists():
                xml_file = xml_path / f"{article_id}.xml"
                if not xml_file.exists():
                    xml_file = None
            
            print(f"Processing: {article_id}")
            
            try:
                results = self.process_article(article_id, str(pdf_file), str(xml_file) if xml_file else None)
                all_results.extend(results)
                print(f"  Found {len(results)} data citations")
            except Exception as e:
                print(f"  Error processing {article_id}: {e}")
        
        # Write results to CSV
        self.write_submission_csv(all_results, output_file)
        print(f"\nTotal data citations found: {len(all_results)}")
        print(f"Results written to: {output_file}")

    def write_submission_csv(self, results: List[Dict], output_file: str) -> None:
        """Write results to submission CSV file"""
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['row_id', 'article_id', 'dataset_id', 'type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for i, result in enumerate(results):
                writer.writerow({
                    'row_id': i,
                    'article_id': result['article_id'],
                    'dataset_id': result['dataset_id'],
                    'type': result['type']
                })


def main():
    parser = argparse.ArgumentParser(description='Data Citation Mining for Make Data Count Competition')
    parser.add_argument('pdf_dir', help='Directory containing PDF files')
    parser.add_argument('--xml_dir', help='Directory containing XML files (optional)')
    parser.add_argument('--output', default='submission.csv', help='Output CSV file')
    
    args = parser.parse_args()
    
    # Check dependencies
    if not HAS_PYMUPDF:
        print("Warning: PyMuPDF not available. PDF extraction will be skipped.")
        print("Install with: pip install PyMuPDF")
    
    # Create miner and process
    miner = DataCitationMiner()
    miner.process_directory(args.pdf_dir, args.xml_dir, args.output)


if __name__ == "__main__":
    main()