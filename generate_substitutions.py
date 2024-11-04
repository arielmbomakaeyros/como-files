import xml.etree.ElementTree as ET
import os
import random
import string


def generate_random_mrid(length=36):
    """Generate a random UUID-like string for mRID."""
    return '-'.join([''.join(random.choices(string.hexdigits.lower(), k=8)),
                     ''.join(random.choices(string.hexdigits.lower(), k=4)),
                     ''.join(random.choices(string.hexdigits.lower(), k=4)),
                     ''.join(random.choices(string.hexdigits.lower(), k=4)),
                     ''.join(random.choices(string.hexdigits.lower(), k=12))])

def build_modified_elements(input_file: str, output_dir: str, setting_count: int, element_to_modify: str, output_file_name: str, keep_schedule: bool):
    """
    Modifies the XML file by locating specified elements and setting a subset of them to duplicate values.
    
    Parameters:
        input_file (str): Path to the XML input file.
        output_dir (str): Directory to save the modified XML output.
        setting_count (int): Number of element_to_modify elements to duplicate.
        output_file_name (str): Name of the output XML file.
        keep_schedule (bool): Flag indicating whether to keep RemedialActionSchedule references.
    """
    try:
        # Parse the XML file and capture namespaces
        namespaces = {}
        for event, elem in ET.iterparse(input_file, events=('start-ns',)):
            prefix, uri = elem
            namespaces[prefix] = uri

        # Re-parse the input XML file
        tree = ET.parse(input_file)
        root = tree.getroot()

        # Register each namespace for proper output
        for prefix, uri in namespaces.items():
            ET.register_namespace(prefix, uri)


        
        
        # RASP 25
        # # Modify the mRID of the RemedialActionSchedule element
        # for elem in root.findall(".//nc:RemedialActionSchedule", namespaces):
        #     mRID_elem = elem.find("cim:IdentifiedObject.mRID", namespaces)
        #     if mRID_elem is not None:
        #         # Set mRID to an incorrect value
        #         mRID_elem.text = generate_random_mrid()  # Generate a random mRID
        
        # Modify the rdf:resource of nc:RemedialActionCost.RemedialActionSchedule
        for elem in root.findall(".//nc:RemedialActionCost", namespaces):
            remedial_action_schedule = elem.find("nc:RemedialActionCost.RemedialActionSchedule", namespaces)
            if remedial_action_schedule is not None:
                # Generate a new random mRID for the rdf:resource
                new_resource = f"{generate_random_mrid()}"
                print(remedial_action_schedule, "....", new_resource)
                remedial_action_schedule.set('rdf:resource', new_resource)

        # # Modify the mRID in RedispatchScheduleAction or RemedialActionCost
        # for elem in root.findall(".//nc:RedispatchScheduleAction", namespaces):
        #     remedial_action_schedule = elem.find("nc:PowerScheduleAction.RemedialActionSchedule", namespaces)
        #     if remedial_action_schedule is not None:
        #         # Replace with an incorrect mRID
        #         remedial_action_schedule.set('rdf:resource', 'urn:uuid:incorrect-mrid-value')

        # for elem in root.findall(".//nc:RemedialActionCost", namespaces):
        #     remedial_action_schedule = elem.find("nc:RemedialActionCost.RemedialActionSchedule", namespaces)
        #     if remedial_action_schedule is not None:
        #         # Replace with an incorrect mRID
        #         remedial_action_schedule.set('rdf:resource', 'urn:uuid:incorrect-mrid-value')


        # # RASP 24
        # # # ===================================================================
        # # Set mRID of RemedialActionSchedule elements to empty
        # for elem in root.findall(".//nc:RemedialActionSchedule", namespaces):
        #     mRID_elem = elem.find("cim:IdentifiedObject.mRID", namespaces)
        #     if mRID_elem is not None:
        #         mRID_elem.text = ""  # Make mRID empty

        

        # RASP 10
        # # ===================================================================
        # # Remove RemedialActionSchedule or RemedialActionCost based on keep_schedule flag
        # if keep_schedule:
        #     for elem in root.findall(".//nc:RemedialActionCost", namespaces):
        #         root.remove(elem)
        # else:
        #     for elem in root.findall(".//nc:RemedialActionSchedule", namespaces):
        #         root.remove(elem)

        # # Remove RemedialActionSchedule references if keep_schedule is False
        # if keep_schedule:
        #     for element in root.findall(".//nc:PowerScheduleAction", namespaces):
        #         remedial_action_schedule = element.find("nc:PowerScheduleAction.RemedialActionSchedule", namespaces)
        #         if remedial_action_schedule is not None:
        #             element.remove(remedial_action_schedule)

        #     for element in root.findall(".//nc:RemedialActionCost", namespaces):
        #         remedial_action_schedule = element.find("nc:RemedialActionCost.RemedialActionSchedule", namespaces)
        #         if remedial_action_schedule is not None:
        #             element.remove(remedial_action_schedule)

        # Modify specific elements if needed (not related to mRID)
        # Further custom modifications could be added here

        # Save the modified XML file
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, output_file_name)
        tree.write(output_path, encoding="utf-8", xml_declaration=True)
        print(f"Modified XML file saved to {output_path}")

    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
directory_name = 'xml_results'
schema_file_path = 'AMP_2024_01_202404181542_indicative.xml'
setting_count = 2  # Number of mRID elements to set to the same value
output_file_str = 'RASP25.xml'
variableTOManipulate = 'mRID'
keep_schedule = True  # Set to True to keep RemedialActionSchedule, False to keep RemedialActionCost

build_modified_elements(schema_file_path, directory_name, setting_count, variableTOManipulate, output_file_str, keep_schedule)
























# import xml.etree.ElementTree as ET
# import os
# import random
# import string

# def build_modified_mrid_elements(input_file: str, output_dir: str, setting_count: int, element_to_modify: str, output_file_name: str, keep_schedule: bool):
#     """
#     Modifies the XML file by locating mRID elements and setting a subset of them to duplicate values.
    
#     Parameters:
#         input_file (str): Path to the XML input file.
#         output_dir (str): Directory to save the modified XML output.
#         setting_count (int): Number of element_to_modify elements to duplicate.
#         setting_count (int): Number of element_to_modify elements to modify with long values.
#         output_file_name (str): Name of the output XML file.
#     """
#     try:
#         # Parse the XML file and capture namespaces
#         namespaces = {}
#         for event, elem in ET.iterparse(input_file, events=('start-ns',)):
#             prefix, uri = elem
#             namespaces[prefix] = uri

#         # Re-parse the input XML file
#         tree = ET.parse(input_file)
#         root = tree.getroot()

#         # Register each namespace for proper output
#         for prefix, uri in namespaces.items():
#             ET.register_namespace(prefix, uri)

        

#         # # Locate all element_to_modify elements
#         # mRID_elements = [elem for elem in root.iter() if elem.tag.endswith(element_to_modify)]
        
#         # # Get a random subset of element_to_modify elements to duplicate values
#         # if setting_count > len(mRID_elements):
#         #     print(f"Warning: setting_count exceeds the number of ${ element_to_modify } elements. Setting setting_count to {len(mRID_elements)}.")
#         #     setting_count = len(mRID_elements)
        
#         # # ===================================================================
#         # # Select random element_to_modify elements to duplicate their values
#         # duplicated_values = random.sample(mRID_elements, setting_count)
#         # if duplicated_values:
#         #     duplicate_value = duplicated_values[0].text  # Take one value to duplicate
#         #     for elem in duplicated_values:
#         #         elem.text = duplicate_value  # Set selected elements to duplicate value

#         # # ===================================================================
#         # # Select random element_to_modify elements to modify with long values
#         # elements_to_modify = random.sample(mRID_elements, setting_count)
#         # for elem in elements_to_modify:
#         #     # Generate a random string longer than 60 characters
#         #     long_value = ''.join(random.choices(string.ascii_letters + string.digits, k=65))
#         #     elem.text = long_value  # Set selected elements to a long value

#         # ===================================================================
#         # Remove RemedialActionSchedule or RemedialActionCost based on keep_schedule flag
#         if keep_schedule:
#             for elem in root.findall(".//nc:RemedialActionCost", namespaces):
#                 root.remove(elem)
#         else:
#             for elem in root.findall(".//nc:RemedialActionSchedule", namespaces):
#                 root.remove(elem)

#         # Ensure output directory exists
#         os.makedirs(output_dir, exist_ok=True)

#         # Construct output file path
#         # base_name = os.path.splitext(os.path.basename(input_file))[0]
#         # output_file = os.path.join(output_dir, f"{base_name}_duplicate_mRID.xml")
#         output_file = os.path.join(output_dir, f"{ output_file_name }")

#         # Write modified XML to the output file, preserving namespaces
#         tree.write(output_file, encoding="utf-8", xml_declaration=True)
#         # print(f"Modified XML file generated as '{output_file}' with {setting_count} duplicated { element_to_modify } values.")

#     except ET.ParseError:
#         print("Error: The XML file could not be parsed. Please check the file format.")
#     except FileNotFoundError:
#         print(f"Error: The file '{input_file}' was not found.")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")

# # Example usage
# directory_name = 'xml_results'
# schema_file_path = 'AMP_2024_01_202404181542_indicative.xml'
# setting_count = 2  # Number of mRID elements to set to the same value
# output_file_str = 'RASP9.xml'
# variableTOManipulate = 'mRID'
# keep_schedule = False  # Set to True to keep RemedialActionSchedule, False to keep RemedialActionCost

# build_modified_mrid_elements(schema_file_path, directory_name, setting_count, variableTOManipulate, output_file_str, keep_schedule)















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

