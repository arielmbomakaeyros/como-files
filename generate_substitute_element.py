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
        
        # Find the original mRID from nc:RemedialActionSchedule/cim:IdentifiedObject.mRID
        original_mrid = None
        remedial_action_schedule = root.find(".//nc:RemedialActionSchedule/cim:IdentifiedObject.mRID", namespaces)
        if remedial_action_schedule is not None:
            print(remedial_action_schedule.text.strip(), "wanda.com")
            original_mrid = remedial_action_schedule.text.strip()
        else:
            print("Original mRID not found in RemedialActionSchedule.")
            return

        # Generate a new random mRID
        new_mrid = f"#{generate_random_mrid()}"

        # Modify the rdf:resource in one instance of RedispatchScheduleAction or RemedialActionCost
        modified = False
        for elem in root.findall(".//nc:RedispatchScheduleAction", namespaces):
            schedule_action = elem.find("nc:PowerScheduleAction.RemedialActionSchedule", namespaces)
            print(schedule_action.get('rdf:resource'), original_mrid)
            if schedule_action is not None and schedule_action.get('rdf:resource') == f"#{original_mrid}":
                print("inside the if, ", new_mrid)
                schedule_action.set('rdf:resource', new_mrid)
                modified = True
                break  # Modify only one instance

        # If not modified in RedispatchScheduleAction, attempt to modify in RemedialActionCost
        if not modified:
            for elem in root.findall(".//nc:RemedialActionCost", namespaces):
                cost_schedule = elem.find("nc:RemedialActionCost.RemedialActionSchedule", namespaces)
                if cost_schedule is not None and cost_schedule.get('rdf:resource') == f"#{original_mrid}":
                    cost_schedule.set('rdf:resource', new_mrid)
                    break  # Modify only one instance

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
