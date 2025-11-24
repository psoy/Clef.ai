import music21
import os

mxl_path = r"c:\Clef.ai\MusicXML_test\der-leiermann.mxl"
xml_path = r"c:\Clef.ai\MusicXML_test\der-leiermann.xml"

print(f"Converting {mxl_path} to {xml_path}")
score = music21.converter.parse(mxl_path)
score.write('xml', fp=xml_path)
print("Conversion done.")

# Read first few lines
with open(xml_path, 'r', encoding='utf-8') as f:
    print(f.read(500))
