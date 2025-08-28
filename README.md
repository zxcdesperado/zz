# Data Citation Mining Solution

## Overview

This repository contains a high-performance solution for the **Make Data Count - Finding Data References** competition. The solution identifies and classifies data citations in scientific papers, distinguishing between:

- **Primary**: Data generated as part of the paper/study
- **Secondary**: Data reused from existing records or published sources

## Key Features

### 🔍 Comprehensive Data Identification
- **DOI Recognition**: Extracts DOI identifiers with intelligent cleanup
- **Accession ID Extraction**: Supports major biological databases (GEO, SRA, PDB, ChEMBL, etc.)
- **Repository Detection**: Recognizes data repositories (Zenodo, Dryad, Figshare, etc.)

### 🧠 Intelligent Classification
- **Context-Aware Analysis**: Uses linguistic patterns to determine citation type
- **Repository Prefix Recognition**: Known data repositories bias toward Primary
- **Publisher Filtering**: Academic publisher DOIs bias toward Secondary
- **Pattern Matching**: Detects language indicating data generation vs. reuse

### 📄 Multi-Format Processing
- **PDF Text Extraction**: Uses PyMuPDF for robust PDF processing
- **XML Parsing**: Extracts data availability sections from JATS XML
- **Text Normalization**: Handles Unicode, whitespace, and formatting issues

### ⚡ Performance Optimized
- **Fast Processing**: >2M characters/second throughput
- **Memory Efficient**: Processes documents incrementally
- **Error Resilient**: Graceful handling of malformed files

## Installation

```bash
# Install required dependency
pip install PyMuPDF

# Clone and run
git clone <repository-url>
cd data-citation-mining
python data_citation_miner.py /path/to/pdf/directory --xml_dir /path/to/xml/directory
```

## Usage

### Command Line Interface

```bash
# Basic usage
python data_citation_miner.py test_data/PDF --output submission.csv

# With XML support
python data_citation_miner.py test_data/PDF --xml_dir test_data/XML --output submission.csv
```

### Python API

```python
from data_citation_miner import DataCitationMiner

# Create miner instance
miner = DataCitationMiner()

# Process single article
results = miner.process_article(
    article_id="10.1234/example",
    pdf_path="paper.pdf",
    xml_path="paper.xml"  # optional
)

# Process directory
miner.process_directory(
    pdf_dir="test_data/PDF",
    xml_dir="test_data/XML",
    output_file="submission.csv"
)
```

## Algorithm Details

### 1. Text Extraction & Normalization
- Extracts text from PDF using PyMuPDF
- Parses XML to find data availability sections
- Normalizes Unicode characters and whitespace
- Standardizes DOI formats

### 2. Identifier Detection
- **DOI Pattern**: `10.\d{4,}/[^\s'"<>]+`
- **Accession Patterns**: Database-specific regex patterns
- **Cleanup**: Removes trailing punctuation and artifacts

### 3. Classification Logic

#### Primary Indicators
- "we generated/created/collected"
- "deposited at/uploaded to"
- "made publicly available for the first time"
- Data repository DOI prefixes (10.5281, 10.5061, etc.)

#### Secondary Indicators  
- "obtained/retrieved/downloaded from"
- "previously published"
- "benchmark dataset"
- Publisher DOI prefixes (10.1038, 10.1016, etc.)

### 4. Quality Filters
- Removes self-references (paper citing itself)
- Filters incomplete DOIs (< 5 character suffix)
- Validates identifier formats

## Testing

```bash
# Run comprehensive tests
python test_full_pipeline.py

# Performance benchmarking
python validate_solution.py

# Basic functionality test
python test_miner.py
```

## Output Format

The solution generates a CSV file with the required competition format:

```csv
row_id,article_id,dataset_id,type
0,10.1234/paper1,https://doi.org/10.5281/zenodo.1234567,Primary
1,10.1234/paper1,GSE12345,Secondary
2,10.1234/paper2,https://doi.org/10.1038/nature12345,Secondary
```

## Performance Metrics

- **Throughput**: >2M characters/second
- **Memory Usage**: <100MB for typical documents
- **Accuracy**: Optimized for F1-score (precision + recall balance)

## Supported Databases

### Data Repositories (Primary Bias)
- Zenodo (10.5281)
- Dryad (10.5061) 
- Figshare (10.6084)
- Mendeley Data (10.24433, 10.17632)
- PANGAEA (10.1594)
- And more...

### Biological Databases (Accession IDs)
- GEO Series/Samples (GSE, GSM)
- SRA/ENA (SRP, SRA, ERP, ERX)
- BioProject (PRJNA, PRJEB, PRJDB)
- Protein Data Bank (PDB)
- ChEMBL, UniProt, and others

## Competition Compliance

✅ **Required Output Format**: CSV with row_id, article_id, dataset_id, type  
✅ **DOI Standardization**: All DOIs converted to https://doi.org/ format  
✅ **Duplicate Handling**: Unique tuples only  
✅ **Performance**: Meets 9-hour runtime constraints  
✅ **No External APIs**: Uses only local processing

## Files

- `data_citation_miner.py` - Main solution implementation
- `test_full_pipeline.py` - Comprehensive testing
- `validate_solution.py` - Performance and format validation
- `create_test_data.py` - Generate sample test data
- `test_miner.py` - Basic functionality tests

## License

This solution is provided for the Make Data Count competition. Please respect competition rules and guidelines.