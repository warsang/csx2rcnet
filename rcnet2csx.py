import xml.etree.ElementTree as ET
from utils import *
import uuid
import re


def extract_after_enums(input_string):
    pattern = re.compile(r'<enums\s*/>\s*(.*)', re.DOTALL)
    match = pattern.search(input_string)

    if match:
        result = match.group(1)
        return result.strip()
    else:
        return input_string

def main():
    # Read the .rcnet file
    file_decompress("output.rcnet","decompressed_out")
    with open("decompressed_out/Data.xml", 'r') as input_file:
        content = input_file.read()

    removed_garbage = extract_after_enums(content).replace('</reclass>', '')
    # Parse the .rcnet content
    root = ET.fromstring(removed_garbage)

    for child in root:
        reverse_itterate_node(child)
    # We need to do a second pass to pull out all child class elements and put them in their own struct
    for child in root:
        for sub_child in child:
            reverse_pull_out_class(sub_child)
    if (root.tag == 'classes'):
        root.tag = 'Structures'
    # Convert the XML structure
    convert_structure(root)

    # Write the new structure to a .ctx file
    with open("output.ctx", 'w') as output_file:
        output_file.write(prettify(root))

def reverse_pull_out_class(node):
    if node.tag == 'node' and node.get('type') == 'ClassInstanceNode':
        # Reverse the class instance node conversion
        old_name = node.get('name').replace('_class_ptr', '')
        reference = node.get('reference')

        # Find the corresponding class node
        class_node = find_class_node(node, reference)

        # Replace the class instance node with the original class node
        if class_node is not None:
            class_node.tag = 'class'
            class_node.set('name', old_name)
            class_node.set('uuid', reference)

            # Remove unnecessary attributes
            for attr in ['reference', 'name', 'type']:
                class_node.attrib.pop(attr, None)

            # Move child nodes to the original class node
            for child in node:
                class_node.append(child)

            # Remove the class instance node
            node.getparent().remove(node)

    # Recursively process child nodes
    for child in node:
        reverse_pull_out_class(child)

# Helper function to find the class node with the given reference
def find_class_node(root, reference):
    for child in root.iter('class'):
        if child.get('uuid') == reference:
            return child
    return None

def reverse_itterate_node(node):
    if node.tag == 'node':
        # Reverse the type conversion from reclass type to CE Type
        if node.get('type') == 'UInt8Node':
            node.set("Vartype", "Byte")
            node.set("DisplayMethod", "Unsigned Integer")
        elif node.get('type') == 'Hex8Node':
            node.set("Vartype", "Byte")
            node.set("DisplayMethod", "Hexadecimal")
        elif node.get('type') == 'UInt16Node':
            node.set("Vartype", "2 Bytes")
            node.set("DisplayMethod", "Unsigned Integer")
        elif node.get('type') == 'Hex16Node':
            node.set("Vartype", "2 Bytes")
            node.set("DisplayMethod", "Hexadecimal")
        elif node.get('type') == 'UInt32Node':
            node.set("Vartype", "4 Bytes")
            node.set("DisplayMethod", "Unsigned Integer")
        elif node.get('type') == 'Hex32Node':
            node.set("Vartype", "4 Bytes")
            node.set("DisplayMethod", "Hexadecimal")
        elif node.get('type') == 'UInt64Node':
            node.set("Vartype", "8 Bytes")
            node.set("DisplayMethod", "Unsigned Integer")
        elif node.get('type') == 'Hex64Node':
            node.set("Vartype", "8 Bytes")
            node.set("DisplayMethod", "Hexadecimal")
        elif node.get('type') == 'VirtualMethodTableNode':
            node.set("Vartype", "Pointer")
            node.set("Description", "VTable")
        elif node.get('type') == 'PointerNode':
            node.set("Vartype", "Pointer")
            pop_node_attrib(node,"Description")
        elif node.get('type') == 'FloatNode':
            node.set("Vartype", "Float")
        elif node.get('type') == 'Utf8TextNode':
            node.set("Vartype", "String")
            node.set("Bytesize", node.get("length", "0"))
        elif node.get('type') == 'Utf16TextNode':
            node.set("Vartype", "Unicode String")
            node.set("Bytesize", node.get("length", "0"))
        else:
            node.set("Vartype", "Hex64Node")

        # Remove unnecessary attributes
        for attr in ['type', 'comment', 'hidden']:
            pop_node_attrib(node,attr)

    if node.tag == 'class':
        # Reverse the class node conversion
        node.tag = 'Structure'
        reference = node.get('uuid')
        name = node.get('name')

        # Find the corresponding structure node
        structure_node = find_structure_node(node, reference)

        # Replace the class node with the original structure node
        if structure_node is not None:
            structure_node.tag = 'Structure'
            structure_node.set('Name', name)
            structure_node.set('UUID', reference)

            # Remove unnecessary attributes
            for attr in ['name', 'uuid']:
                pop_node_attrib(structure_node,attr)

            # Move child nodes to the original structure node
            for child in node:
                structure_node.append(child)

            # Remove the class node
            node.getparent().remove(node)

    # Remove useless rcnet net attributes
    pop_node_attrib(node,"comment")
    pop_node_attrib(node,"hidden")


    # Recursively process child nodes
    for child in node:
        reverse_itterate_node(child)

# Helper function to find the structure node with the given reference
def find_structure_node(root, reference):
    for child in root.iter('Structure'):
        if child.get('UUID') == reference:
            return child
    return None


def convert_structure(node):
    for child in node:
        # Handle class nodes
        if child.tag == 'class':
            convert_class(child)

        # Recursively process child nodes
        convert_structure(child)

def convert_class(node):
    # Convert class nodes to their original format
    if node.tag == 'class':
        reference = node.get('reference')
        name = node.get('name')

        # Find the corresponding structure node
        structure_node = find_structure_node(node, reference)

        # Replace the class node with the original structure node
        if structure_node is not None:
            structure_node.tag = 'Structure'
            structure_node.set('Name', name)
            structure_node.set('UUID', reference)

            # Remove unnecessary attributes
            for attr in ['name', 'reference', 'type']:
                structure_node.attrib.pop(attr, None)

            # Move child nodes to the original structure node
            for child in node:
                structure_node.append(child)

            # Remove the class node
            node.getparent().remove(node)

def find_structure_node(root, reference):
    # Find the structure node with the given reference
    for child in root.iter('Structure'):
        if child.get('UUID') == reference:
            return child
    return None


if __name__ == '__main__':
    main()
