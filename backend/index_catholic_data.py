"""
Script to index Catholic hymn data.
Since we have PDFs, we need to:
1. Convert PDFs to MusicXML using OMR (Oemer or similar)
2. Index the MusicXML files

For now, we'll create a simple script that checks if we have XML/MXL files
and indexes those. PDF conversion can be done separately.
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag_indexer import get_index

def main():
    print("Starting Catholic hymn indexing...")
    print("Note: This will only index .xml and .mxl files.")
    print("PDFs need to be converted to MusicXML first using OMR tools.\n")
    
    # Check what files we have
    data_dir = Path("data/Catholic")
    if not data_dir.exists():
        print(f"Error: {data_dir} does not exist")
        return
    
    xml_files = list(data_dir.glob("*.xml"))
    mxl_files = list(data_dir.glob("*.mxl"))
    pdf_files = list(data_dir.glob("*.pdf"))
    
    print(f"Found {len(xml_files)} XML files")
    print(f"Found {len(mxl_files)} MXL files")
    print(f"Found {len(pdf_files)} PDF files (will be skipped)\n")
    
    if len(xml_files) + len(mxl_files) == 0:
        print("No MusicXML files found. Please convert PDFs to MusicXML first.")
        print("You can use tools like Oemer (https://github.com/BreezeWhite/oemer)")
        return
    
    # Index the files
    try:
        index = get_index(data_dir="data/Catholic", persist_dir="data/chromadb")
        if index:
            print("\n✓ Indexing completed successfully!")
            print("The RAG system is ready to use.")
        else:
            print("\n✗ Indexing failed.")
    except Exception as e:
        print(f"\n✗ Error during indexing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
