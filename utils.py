import zipfile
import xml.etree.ElementTree as ET
from lxml import etree

# Function : file_compress
def file_compress(inp_file_names, out_zip_file):
    """
    function : file_compress
    args : inp_file_names : list of filenames to be zipped
    out_zip_file : output zip file
    return : none
    assumption : Input file paths and this code is in same directory.
    """
    # Select the compression mode ZIP_DEFLATED for compression
    # or zipfile.ZIP_STORED to just store the file
    compression = zipfile.ZIP_STORED
    print(f" *** Input File name passed for zipping - {inp_file_names}")

    # create the zip file first parameter path/name, second mode
    print(f' *** out_zip_file is - {out_zip_file}')
    zf = zipfile.ZipFile(out_zip_file, mode="w")

    try:
        for file_to_write in inp_file_names:
            # Add file to the zip file
            # first parameter file to zip, second filename in zip
            print(f' *** Processing file {file_to_write}')
            zf.write(file_to_write, file_to_write, compress_type=compression)

    except FileNotFoundError as e:
        print(f' *** Exception occurred during zip process - {e}')
    finally:
        # Don't forget to close the file!
        zf.close()

import zipfile
import os

def file_decompress(zip_file, out_folder):
    """
    Function: file_decompress
    Args:
    - zip_file: input zip file to be decompressed
    - out_folder: output folder where the files will be extracted
    Return: None
    """
    # Check if the output folder exists, if not create it
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    # Open the zip file
    with zipfile.ZipFile(zip_file, 'r') as zf:
        # Extract all the contents into the output folder
        zf.extractall(out_folder)

# Example usage:
# file_decompress("output.rcnet", "decompressed_folder")

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.fromstring(ET.tostring(elem, 'utf-8',xml_declaration=False).decode('utf-8'),parser=parser)
    rough_string = etree.tostring(tree, encoding='UTF-8', xml_declaration=False,pretty_print=True)
    return rough_string.decode('utf-8')

def addParentInfo(et):
    for child in et:
        child.attrib['__my_parent__'] = et
        addParentInfo(child)

def stripParentInfo(et):
    for child in et:
        child.attrib.pop('__my_parent__', 'None')
        stripParentInfo(child)

def getParent(et):
    if '__my_parent__' in et.attrib:
        return et.attrib['__my_parent__']
    else:
        return None

def pop_node_attrib(anode, name):
    try:
        anode.attrib.pop(name)
    except:
        pass
    return