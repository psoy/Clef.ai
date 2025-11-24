import subprocess
import os
import sys

import music21
import time

def convert_musicxml_to_abc(xml_file_path: str) -> str:
    """
    Converts a MusicXML file to ABC notation using xml2abc.py.
    Handles .mxl by converting to .xml first.
    
    Args:
        xml_file_path (str): Path to the MusicXML file.
        
    Returns:
        str: The ABC notation string.
    """
    temp_xml_path = None
    try:
        # Path to xml2abc.py
        script_dir = os.path.dirname(os.path.abspath(__file__))
        xml2abc_path = os.path.join(script_dir, "xml2abc.py")
        
        if not os.path.exists(xml2abc_path):
            print(f"xml2abc.py not found at {xml2abc_path}")
            return ""

        # If file is .mxl, convert to .xml using music21 first
        target_file = xml_file_path
        if xml_file_path.endswith('.mxl'):
            print(f"Converting MXL to XML: {xml_file_path}")
            score = music21.converter.parse(xml_file_path)
            temp_xml_path = xml_file_path.replace('.mxl', '.xml')
            score.write('xml', fp=temp_xml_path)
            target_file = temp_xml_path
            print(f"Created temp XML: {target_file}")
            time.sleep(1) # Wait for file write

        # Run xml2abc.py
        # Command: python xml2abc.py <xml_file> -o <output_dir>
        # We will output to the same directory as the input file to avoid path issues
        output_dir = os.path.dirname(target_file)
        cmd = [sys.executable, xml2abc_path, target_file, "-o", output_dir]
        
        print(f"Running command: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
        
        if result.stderr:
            print(f"Stderr: {result.stderr}")
        
        if result.returncode != 0:
            print(f"xml2abc failed with return code {result.returncode}")
            return ""
            
        # xml2abc creates a file with .abc extension in the output directory
        # The filename is derived from the input filename
        base_name = os.path.splitext(os.path.basename(target_file))[0]
        abc_output_path = os.path.join(output_dir, base_name + ".abc")
        
        if os.path.exists(abc_output_path):
            with open(abc_output_path, 'r', encoding='utf-8') as f:
                abc_content = f.read()
            
            # Clean up the generated ABC file
            try:
                os.remove(abc_output_path)
            except:
                pass
            return abc_content
        else:
            print(f"Expected ABC file not found at {abc_output_path}")
            return ""
        
    except Exception as e:
        print(f"Error converting {xml_file_path}: {e}")
        import traceback
        traceback.print_exc()
        return ""
    finally:
        # Clean up temp XML file if it was created from MXL
        if temp_xml_path and os.path.exists(temp_xml_path):
            try:
                os.remove(temp_xml_path)
                print(f"Removed temp XML: {temp_xml_path}")
            except:
                pass

if __name__ == "__main__":
    # Test with a dummy file if needed
    pass
