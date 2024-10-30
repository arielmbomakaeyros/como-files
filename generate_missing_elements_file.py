import xml.etree.ElementTree as ET
import os

def build_missing_element(input_file: str, output_dir: str, endsWith: str, result_to_achieve: str, new_value: str):
    try:
        # Parse the input XML file and capture namespaces
        namespaces = {}
        for event, elem in ET.iterparse(input_file, events=('start-ns',)):
            prefix, uri = elem
            print(prefix, uri, "=================>")
            namespaces[prefix] = uri

        # Re-parse the input XML file with namespaces now captured
        tree = ET.parse(input_file)
        root = tree.getroot()

        # Register each namespace to ensure prefixes are preserved in the output
        for prefix, uri in namespaces.items():
            ET.register_namespace(prefix, uri)

        print(root, "...........................................")

        # Locate elements with local name 'version' and clear their content
        for elem in root.iter():
            if elem.tag.endswith(endsWith):  # Checking if tag ends with 'version'
                print("0000, ", elem)
                elem.text = new_value  # Clear the content for any version tag

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Construct the output file path
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(output_dir, f"____{base_name}_{ result_to_achieve }_{endsWith}_.xml")

        # Write the modified XML to the output file, preserving original namespaces
        tree.write(output_file, encoding="utf-8", xml_declaration=True)
        print(f"Modified XML file generated as '{output_file}'")

    except ET.ParseError:
        print("Error: The XML file could not be parsed. Please check the file format.")
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage
directory_name = 'xml_results'
schema_file_path = 'AMP_2024_01_202404181542_indicative.xml'
variable = 'version'
result_to_achieve = "wrong_formated"
# result_to_achieve = "missing"
new_value = "version"
# new_value = ""

build_missing_element(schema_file_path, directory_name, variable, result_to_achieve, new_value)
















# HERE I SEARCH FOR THE PREFIX AND THE ELEMENT AT THE SAME TIME BUT NOW I WANT TO SERACH ONLY FOR THE ELEMENT WITHOUT THE PREFIX
# import xml.etree.ElementTree as ET
# import os

# def modify_xml(input_file: str, output_dir: str):
#     try:
#         # Parse the input XML file and capture namespaces
#         namespaces = {}
#         for event, elem in ET.iterparse(input_file, events=('start-ns',)):
#             prefix, uri = elem
#             namespaces[prefix] = uri

#         # Re-parse the input XML file with namespaces now captured
#         tree = ET.parse(input_file)
#         root = tree.getroot()

#         # Register each namespace to ensure prefixes are preserved in the output
#         for prefix, uri in namespaces.items():
#             ET.register_namespace(prefix, uri)

#         # Locate <dcat:version> elements and clear their content
#         dcat_ns = namespaces.get('dcat')
#         if dcat_ns:
#             for version in root.findall(f'.//{{{dcat_ns}}}version'):
#                 version.text = ''  # Clear the content for any value

#         # Ensure output directory exists
#         os.makedirs(output_dir, exist_ok=True)

#         # Construct the output file path
#         base_name = os.path.splitext(os.path.basename(input_file))[0]
#         output_file = os.path.join(output_dir, f"{base_name}_1.xml")

#         # Write the modified XML to the output file, preserving original namespaces
#         tree.write(output_file, encoding="utf-8", xml_declaration=True)
#         print(f"Modified XML file generated as '{output_file}'")

#     except ET.ParseError:
#         print("Error: The XML file could not be parsed. Please check the file format.")
#     except FileNotFoundError:
#         print(f"Error: The file '{input_file}' was not found.")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")

# # Example usage
# directory_name = 'xml_results'
# schema_file_path = 'AMP_2024_01_202404181542_indicative.xml'

# modify_xml(schema_file_path, directory_name)

















# import xml.etree.ElementTree as ET
# import os

# def modify_xml(input_file: str, output_dir: str):
#     try:
#         # Parse the input XML file and capture namespaces
#         namespaces = {}
#         for event, elem in ET.iterparse(input_file, events=('start-ns',)):
#             prefix, uri = elem
#             namespaces[prefix] = uri

#         # Re-parse the input XML file with namespaces now captured
#         tree = ET.parse(input_file)
#         root = tree.getroot()

#         # Register each namespace to ensure prefixes are preserved in the output
#         for prefix, uri in namespaces.items():
#             ET.register_namespace(prefix, uri)

#         # Locate <dcat:version> elements and update if the text is '1.0'
#         dcat_ns = namespaces.get('dcat')
#         if dcat_ns:
#             for version in root.findall(f'.//{{{dcat_ns}}}version'):
#                 if version.text == '1.0':
#                     version.text = ''  # Clear the content if the text is '1.0'

#         # Ensure output directory exists
#         os.makedirs(output_dir, exist_ok=True)

#         # Construct the output file path
#         base_name = os.path.splitext(os.path.basename(input_file))[0]
#         output_file = os.path.join(output_dir, f"{base_name}_modified_4.xml")

#         # Write the modified XML to the output file, preserving original namespaces
#         tree.write(output_file, encoding="utf-8", xml_declaration=True)
#         print(f"Modified XML file generated as '{output_file}'")

#     except ET.ParseError:
#         print("Error: The XML file could not be parsed. Please check the file format.")
#     except FileNotFoundError:
#         print(f"Error: The file '{input_file}' was not found.")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")

# # Example usage
# directory_name = 'xml_results'
# schema_file_path = 'AMP_2024_01_202404181542_indicative.xml'

# modify_xml(schema_file_path, directory_name)

















# i had this error: An unexpected error occurred: dictionary update sequence element #0 has length 48; 2 is required
# reason The error occurs because of the way we attempted to capture namespaces. The regular expression approach does not yield the expected structure for dictionary creation. Let's fix this by using ET.iterparse to capture namespaces more accurately and handle them properly.

# import xml.etree.ElementTree as ET
# import os
# import re

# def modify_xml(input_file: str, output_dir: str):
#     try:
#         # Parse the input XML file
#         tree = ET.parse(input_file)
#         root = tree.getroot()

#         # Extract all namespaces from the root element
#         namespaces = dict([
#             node for _, node in re.findall(r'\sxmlns:([^\s]+)="([^"]+)"', ET.tostring(root, encoding='unicode'))
#         ])

#         # Register each namespace to ensure the prefixes are preserved in output
#         for prefix, uri in namespaces.items():
#             ET.register_namespace(prefix, uri)

#         # Locate <dcat:version> elements and update if the text is '1.0'
#         for version in root.findall('.//dcat:version', {'dcat': namespaces.get('dcat')}):
#             if version.text == '1.0':
#                 version.text = ''  # Clear the content if the text is '1.0'

#         # Ensure output directory exists
#         os.makedirs(output_dir, exist_ok=True)

#         # Construct the output file path
#         base_name = os.path.splitext(os.path.basename(input_file))[0]
#         output_file = os.path.join(output_dir, f"{base_name}_modified_2.xml")

#         # Write the modified XML to the output file, preserving original namespaces
#         tree.write(output_file, encoding="utf-8", xml_declaration=True)
#         print(f"Modified XML file generated as '{output_file}'")

#     except ET.ParseError:
#         print("Error: The XML file could not be parsed. Please check the file format.")
#     except FileNotFoundError:
#         print(f"Error: The file '{input_file}' was not found.")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")

# # Example usage
# directory_name = 'xml_results'
# schema_file_path = 'AMP_2024_01_202404181542_indicative.xml'

# modify_xml(schema_file_path, directory_name)























# import xml.etree.ElementTree as ET
# import os

# def modify_xml(input_file: str, output_dir: str):
#     try:
#         # Parse the input XML file
#         tree = ET.parse(input_file)
#         root = tree.getroot()
        
#         # Define the namespace map as it appears in the input XML file
#         namespaces = {
#             'dcat': 'http://www.w3.org/ns/dcat#',
#             'md': 'http://www.metadata.com/schema'  # Adjust to match actual input namespace
#         }
        
#         # Register namespaces to ensure prefixes are preserved
#         for prefix, uri in namespaces.items():
#             ET.register_namespace(prefix, uri)

#         # Locate <dcat:version> elements and update if the text is '1.0'
#         for version in root.findall('.//dcat:version', namespaces):
#             if version.text == '1.0':
#                 version.text = ''  # Clear the content if the text is '1.0'

#         # Ensure output directory exists
#         os.makedirs(output_dir, exist_ok=True)
        
#         # Construct the output file path
#         base_name = os.path.splitext(os.path.basename(input_file))[0]
#         output_file = os.path.join(output_dir, f"{base_name}_modified_1.xml")
        
#         # Write the modified XML to the output file, preserving original namespaces
#         tree.write(output_file, encoding="utf-8", xml_declaration=True)
#         print(f"Modified XML file generated as '{output_file}'")
        
#     except ET.ParseError:
#         print("Error: The XML file could not be parsed. Please check the file format.")
#     except FileNotFoundError:
#         print(f"Error: The file '{input_file}' was not found.")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")

# # Example usage
# directory_name = 'xml_results'
# schema_file_path = 'AMP_2024_01_202404181542_indicative.xml'

# modify_xml(schema_file_path, directory_name)




















# import xml.etree.ElementTree as ET
# import os

# def modify_xml(input_file: str, output_dir: str):
#     try:
#         # Parse the input XML file
#         tree = ET.parse(input_file)
#         root = tree.getroot()

#         # Define the namespace
#         namespaces = {'dcat': 'http://www.w3.org/ns/dcat#'}

#         # Locate <dcat:version> elements and update as needed
#         for version in root.findall('.//dcat:version', namespaces):
#             if version.text == '1.0':
#                 version.text = ''  # Clear the content if the text is '1.0'

#         # Ensure output directory exists
#         os.makedirs(output_dir, exist_ok=True)

#         # Construct the output file path
#         base_name = os.path.splitext(os.path.basename(input_file))[0]
#         output_file = os.path.join(output_dir, f"{base_name}_modified.xml")

#         # Write the modified XML to the output file
#         tree.write(output_file, encoding="utf-8", xml_declaration=True)
#         print(f"Modified XML file generated as '{output_file}'")

#     except ET.ParseError:
#         print("Error: The XML file could not be parsed. Please check the file format.")
#     except FileNotFoundError:
#         print(f"Error: The file '{input_file}' was not found.")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")

# # Example usage
# directory_name = 'xml_results'
# schema_file_path = 'AMP_2024_01_202404181542_indicative.xml'

# modify_xml(schema_file_path, directory_name)



















# import xml.etree.ElementTree as ET
# import os

# def modify_xml(input_file: str, output_dir: str):
#     # Parse the input XML file
#     tree = ET.parse(input_file)
#     root = tree.getroot()
    
#     # Define the namespace if it exists in the XML tags (adjust if necessary)
#     namespaces = {'dcat': 'http://www.w3.org/ns/dcat#'}
    
#     # Find the <dcat:version> tag and check if it has content '1.0'
#     for version in root.findall('.//dcat:version', namespaces):
#         if version.text == '1.0':
#             version.text = ''  # Clear the content if condition is met
    
#     # Define the output directory and ensure it exists
#     # output_dir = 'xml_results'
#     os.makedirs(output_dir, exist_ok=True)
    
#     # Generate the output file path within the xml_results folder
#     output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file))[0] + "_modified.xml")
    
#     # Write the modified XML to the new output file
#     tree.write(output_file, encoding="utf-8", xml_declaration=True)
#     print(f"Modified XML file generated as '{output_file}'")

# # Example usage:
# directory_name = 'xml_results'
# schema_file_path = 'AMP_2024_01_202404181542_indicative.xml'

# modify_xml(schema_file_path, directory_name)











# import xml.etree.ElementTree as ET
# from xml.dom import minidom

# # Define namespaces with desired prefixes
# namespaces = {
#     "ModelDescription": "http://iec.ch/TC57/61970-552/ModelDescription/1#",
#     "ind": "http://www.w3.org/ns/ind#",
#     "dcterms": "http://purl.org/dc/terms/#",
#     "dcat": "http://www.w3.org/ns/dcat#",
#     "nc": "http://entsoe.eu/ns/nc#",
#     "cim": "http://iec.ch/TC57/CIM100#"
# }

# # Register namespaces for output
# for prefix, uri in namespaces.items():
#     ET.register_namespace(prefix, uri)

# # Build the XML structure
# root = ET.Element("rdf:RDF", {
#     "xmlns:rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
#     **{f"xmlns:{prefix}": uri for prefix, uri in namespaces.items()}
# })

# # Sample data for FullModel
# full_model = ET.SubElement(root, "ModelDescription:FullModel", {"rdf:about": "urn:uuid:3d899608-c4f6-4553-9a4d-1ce58f60c60a"})
# ET.SubElement(full_model, "ind:generatedAtTime").text = "2024-02-18T13:42:00Z"
# ET.SubElement(full_model, "dcterms:issued").text = "2024-02-18T13:42:00Z"
# ET.SubElement(full_model, "dcterms:publisher", {"rdf:resource": "http://energy.referencedata.eu/EIC/10X1001A1001A094"})
# ET.SubElement(full_model, "dcat:keyword").text = "RAS"
# ET.SubElement(full_model, "dcterms:references", {"rdf:resource": "urn:uuid:541e7344-547c-11ef-ae40-0242ac120003"})
# ET.SubElement(full_model, "dcterms:license", {"rdf:resource": "https://creativecommons.org/licenses/by/4.0/"})
# ET.SubElement(full_model, "dcterms:accessRights", {"rdf:resource": "http://energy.referencedata.eu/Confidentiality/4cd9b326-1275-4da7-9724-28c5e1deeb87"})
# ET.SubElement(full_model, "dcterms:identifier").text = "urn:uuid:3d899608-c4f6-4553-9a4d-1ce58f60c60a"

# # Beautify and save XML
# def prettify(element):
#     rough_string = ET.tostring(element, 'utf-8')
#     reparsed = minidom.parseString(rough_string)
#     return reparsed.toprettyxml(indent="	")

# xml_str = prettify(root)

# # Write to XML file in xml_results directory
# with open("xml_results/schema_file_path.xml", "w", encoding="utf-8") as f:
#     f.write(xml_str)

# print("XML file saved in xml_results/output.xml with specified namespace prefixes.")

