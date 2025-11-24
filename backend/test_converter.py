import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))

from converter import convert_musicxml_to_abc

def test_conversion():
    test_file = r"c:\Clef.ai\MusicXML_test\der-leiermann.mxl"
    if not os.path.exists(test_file):
        print(f"Test file not found: {test_file}")
        return

    print(f"Converting {test_file}...")
    abc = convert_musicxml_to_abc(test_file)
    
    if abc:
        print("Conversion successful!")
        print("First 200 chars:")
        print(abc[:200])
    else:
        print("Conversion failed.")

if __name__ == "__main__":
    test_conversion()
