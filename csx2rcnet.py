import uuid
from utils import *
class_names = set()
tree = ET.parse(r"C:\<projectpath>.CSX")
root = tree.getroot()

def main():

    for child in root:
        # Ask user for class base address
        address = input(f"Base address for {child.get('Name')}:")
        child.set('address',f"{address}")
        itterate_node(child)
    # We need to do a second pass to pull out all child class elements and put them in their own struct
    for child in root:
        for sub_child in child:
            pull_out_class(sub_child)
    if (root.tag == 'Structures'):
        root.tag = 'classes'
    with open("Data.xml", 'w') as output:
        output.write('''<?xml version="1.0" encoding="utf-8"?>
<!--ReClass.NET 1.2 by KN4CK3R-->
<!--Website: https://github.com/ReClassNET/ReClass.NET-->
<reclass version="65537" type="x64">
  <custom_data />
  <type_mapping>
    <TypeBool>bool</TypeBool>
    <TypeInt8>int8_t</TypeInt8>
    <TypeInt16>int16_t</TypeInt16>
    <TypeInt32>int32_t</TypeInt32>
    <TypeInt64>int64_t</TypeInt64>
    <TypeNInt>ptrdiff_t</TypeNInt>
    <TypeUInt8>uint8_t</TypeUInt8>
    <TypeUInt16>uint16_t</TypeUInt16>
    <TypeUInt32>uint32_t</TypeUInt32>
    <TypeUInt64>uint64_t</TypeUInt64>
    <TypeNUInt>size_t</TypeNUInt>
    <TypeFloat>float</TypeFloat>
    <TypeDouble>double</TypeDouble>
    <TypeVector2>Vector2</TypeVector2>
    <TypeVector3>Vector3</TypeVector3>
    <TypeVector4>Vector4</TypeVector4>
    <TypeMatrix3x3>Matrix3x3</TypeMatrix3x3>
    <TypeMatrix3x4>Matrix3x4</TypeMatrix3x4>
    <TypeMatrix4x4>Matrix4x4</TypeMatrix4x4>
    <TypeUtf8Text>char</TypeUtf8Text>
    <TypeUtf16Text>wchar_t</TypeUtf16Text>
    <TypeUtf32Text>char32_t</TypeUtf32Text>
    <TypeFunctionPtr>void*</TypeFunctionPtr>
  </type_mapping>
  <enums />\n''')
        output.write(prettify(root))
        output.write('</reclass>')
    file_compress(['Data.xml'],'output.rcnet')

def pull_out_class(node):
    if node.tag =='class':
        # We replace the type with a classtype
        node.tag = 'node'
        old_name = node.get('name')
        new_class_uuid = str(uuid.uuid4())
        node.set('reference',new_class_uuid)
        node.set('name',f"{old_name}_class_ptr")
        node.set('type','ClassInstanceNode')
        new_class = ET.SubElement(root, 'class')
        new_class.set('name',old_name)
        new_class.set('uuid',new_class_uuid)

        for i in range(len(node)):
            new_class.append(node[0])
            node.remove(node[0])

        return
    for child in node:
        pull_out_class(child)
    return

def itterate_node(node):
    global class_names
    addParentInfo(node)
    if(node.tag == 'Element'):
        node.tag='node'
        # Conversion from CE Type to reclass type
        if(node.get('Vartype')=="Byte"):
            if(node.get('DisplayMethod')=="Unsigned Integer"):
                node.set("type","UInt8Node")
            elif (node.get('DisplayMethod') == "Hexadecimal"):
                    node.set("type", "Hex8Node")
        elif (node.get('Vartype') == "2 Bytes"):
            if (node.get('DisplayMethod') == "Unsigned Integer"):
                node.set("type", "UInt16Node")
            elif (node.get('DisplayMethod') == "Hexadecimal"):
                    node.set("type", "Hex16Node")
        elif(node.get('Vartype')=="4 Bytes"):
            if (node.get('DisplayMethod') == "Unsigned Integer"):
                node.set("type", "UInt32Node")
            elif (node.get('DisplayMethod') == "Hexadecimal"):
                    node.set("type", "Hex32Node")
        elif(node.get('Vartype')=="8 Bytes"):
            if (node.get('DisplayMethod') == "Unsigned Integer"):
                node.set("type", "UInt64Node")
            elif (node.get('DisplayMethod') == "Hexadecimal"):
                    node.set("type", "Hex64Node")
        elif (node.get('Vartype') == "Pointer"):
            if (node.get('Description') == "VTable"):
                node.set("type", "VirtualMethodTableNode")
            else:
                node.set("type", "PointerNode")
        elif (node.get('Vartype') == "Float"):
            node.set("type", "FloatNode")
        elif (node.get('Vartype') == "String"):
            node.set("type", "Utf8TextNode")
            node.set("length", f"{node.get('Bytesize')}")
        elif (node.get('Vartype') == "Unicode String"):
            node.set("type", "Utf16TextNode")
            node.set("length", f"{node.get('Bytesize')}")
        else:
            node.set("type", "Hex64Node")
    if(node.tag == 'Structure'):
        node.tag ='class'
        #node.tag = 'node'
        #node.set('type','ClassInstanceNode')
        # Class nodes need a uuid
        node.set('uuid',str(uuid.uuid4()))
    if (node.tag == 'Structures'):
        node.tag = 'classes'
    if (node.tag == 'Elements'):
        parent = getParent(node)
        for i,child in enumerate(node):
            parent.insert(i,child)
        parent.remove(node)
        # This doesn't translate well to Reclass;
        # We skip this node and assign it's children to the parent
    if (node.get('Name')):
        node.set('name', node.get('Name'))
    elif (node.get('Description')):
        node.set('name', node.get('Description'))
    elif(node.get('name')):
        pass
    else:
        node.set('name', str(uuid.uuid4().hex))
    if node.tag == 'class':
        class_names.add(node.get('name'))

    # print(f"{node.tag} | {node.attrib}")
    for child in node:
        itterate_node(child)
    # Clean up attributes
    pop_node_attrib(node, "Offset")
    pop_node_attrib(node, "Vartype")
    pop_node_attrib(node, "Bytesize")
    pop_node_attrib(node, "RLECount")
    pop_node_attrib(node, "OffsetHex")
    pop_node_attrib(node, "Description")
    pop_node_attrib(node, "DisplayMethod")
    pop_node_attrib(node, "RLECompression")
    pop_node_attrib(node, "DoNotSaveLocal")
    pop_node_attrib(node, "DefaultHex")
    pop_node_attrib(node, "AutoCreateStructsize")
    pop_node_attrib(node, "AutoDestroy")
    pop_node_attrib(node, "AutoCreate")
    pop_node_attrib(node, "AutoFill")
    pop_node_attrib(node, "Name")
    pop_node_attrib(node, "ChildStructStart")


    # Add empty attributes to make it rcnet friendly
    node.set("comment","")
    node.set("hidden","false")
    stripParentInfo(node)
    return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
