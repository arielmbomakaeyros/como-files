import json
import secrets
import random
from datetime import datetime, timedelta
from random import choice
from faker import Faker
import re

fake = Faker()

# Helper functions to generate sample data for each property
def generate_business_day(start_date, offset_days):
    business_day = start_date + timedelta(days=offset_days)
    return business_day.strftime("%Y-%m-%d")

def generate_business_timestamp(business_day):
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    random_second = random.randint(0, 59)
    return f"{business_day}T{random_hour:02}:{random_minute:02}:{random_second:02}Z"

def generate_crosa_version():
    return random.randint(1, 5)

def generate_tso_code():
    # return random.choice(["dayAhead", "weekAhead", "monthAhead", "Intraday"])
    return random.choice(["CEPS", "APG", "PSE", "MAVIR", "Transelectrica"]),

def generate_cs_process_version():
    return random.randint(1, 5)

def generate_flow_decomposition_id():
    return secrets.token_hex(12)

def generate_id():
    return secrets.token_hex(12)

def generate_mapping_result_id():
    return secrets.token_hex(12)

def generate_selected_xnec_result_id():
    return secrets.token_hex(12)

def generate_time_horizon():
    return random.choice(["dayAhead", "weekAhead", "monthAhead", "Intraday"])

def generate_bidding_zone_cost_list():
    bidding_zones = ["EIC_DE", "EIC_SI", "EIC_NL", "EIC_FR", "EIC_PL", "EIC_SK", "EIC_RO"]
    return [
        {
            "biddingZoneCode": zone,
            "contribution": random.uniform(0, 0.5),
            "cost": random.uniform(0, 25000)
        } for zone in bidding_zones
    ]

def generate_flow_component_list():
    return [generate_flow_component() for _ in range(random.randint(1, 3))]

def generate_flow_component():
    return {
        "appliedThresholdList": generate_applied_threshold_list(),
        "burdeningFlow": random.uniform(200, 500),
        "commonThreshold": random.uniform(0, 100),
        "contribution": random.uniform(0, 100),
        "stackingOrder": random.randint(1, 10),
        "type": random.choice(["allocatedFlow", "internalFlow", "loopFlow", "loopFlowOutsideCore", "pstFlow"])
    }

def generate_applied_threshold_list():
    if random.choice([True, False]):
        return []
    return [generate_applied_threshold() for _ in range(random.randint(1, 5))]

def generate_applied_threshold():
    return {
        "biddingZoneCode": random.choice(["EIC_DE", "EIC_SI", "EIC_PL", "EIC_SK", "EIC_RO"]),
        "burdeningFlow": random.uniform(0, 100),
        "flowAboveThreshold": random.uniform(0, 100),
        "flowBelowThreshold": random.uniform(0, 100),
        "individualThreshold": random.uniform(10, 20)
    }

def generate_tso_cost_list():
    return [generate_tso_cost() for _ in range(random.randint(1, 3))]

def generate_tso_cost():
    return {
        "contribution": random.uniform(0, 0.5),
        "cost": random.uniform(20000, 50000),
        "tsoCode": random.choice(["CEPS", "APG", "PSE", "MAVIR", "Transelectrica"]),
        "tsoShare": random.uniform(0.5, 1.5)
    }

def generate_volume_overload():
    return random.uniform(200, 300)

def generate_xnec_cost_list():
    return [generate_xnec_cost() for _ in range(random.randint(1, 5))]

def generate_xnec_cost():
    return {
        "biddingZoneCostList": generate_bidding_zone_cost_list(),
        "convertedXnecId": f"ID{random.randint(1, 100)}",
        "cost": random.uniform(50000, 100000),
        "flowComponentList": generate_flow_component_list(),
        "tsoCostList": generate_tso_cost_list(),
        "volumeOverload": generate_volume_overload()
    }


def resolve_ref(schema, ref):
    """Resolve a $ref within the schema."""
    parts = ref.lstrip('#/').split('/')
    ref_obj = schema
    for part in parts:
        ref_obj = ref_obj.get(part)
        if ref_obj is None:
            print(f"Unable to resolve reference: {ref}")
            return None
    return ref_obj

# FUNCTION TO GENERATE RANDOM DATE VALUES
def generate_random_date():
    # Example function to generate a random date
    return fake.date()

# FUNCTION TO GENERATE RANDOM TIMESTAMP VALUES
def generate_random_timestamp():
    # Example function to generate a random timestamp
    return fake.iso8601()

pattern = r'^(xnec.*Id|.*xnecId)$'
patternXra = r'^(xra.*Id|.*xraId)$'


# FUNCTION TO GENERATE VALUES BASED ON DESCRIPTION AND TYPES (MANUAL CHECK)
def ai_generate_based_on_description(description, data_type):
    # This would be replaced with actual AI model inference
    # For example purposes, this is a simple mapping.
    prompt = "Once upon a time"
    if "date" in description.lower():
        return "2024-08-23"
        # return generate_text(prompt)
    if "date" in description.lower() and data_type.lower() == "string":
        return generate_random_date ()
        # return generate_text(prompt)
    elif "timestamp" in description.lower() and data_type.lower() == "string":
        return generate_random_timestamp () # "2024-08-23T12:34:56Z"
        # return generate_text(prompt)
    elif "timestamp" in description.lower() and data_type.lower() == "date":
        return generate_random_timestamp () # "2024-08-23T12:34:56Z"
        # return generate_text(prompt)
    elif "version" in description.lower() or "identifier" in description.lower():
        return random.randint(1, 100)
        # return generate_text(prompt)
    elif "code" in description.lower():
        return "ABC123"
        # return generate_text(prompt)
    else:
        # Use a language model to generate a string based on description
        # return "sample data based on description"
        if data_type == 'number':
            # return random.uniform(0, 100)
            return random.randint(1, 100)
        elif data_type == 'integer':
            # return round(random.uniform(0, 10000), 2)
            return random.randint(1, 100)
        elif data_type == 'string':
            # return round(random.uniform(0, 10000), 2)
            return generate_flow_decomposition_id ()
    
# GENERATE SAMPLE DATA
def generate_sample_data(schema, full_schema):
    """Generate sample data based on a JSON schema."""
    if 'type' in schema:
        if schema['type'] == 'object':
            obj = {}
            for prop, prop_schema in schema.get('properties', {}).items():
                obj[prop] = generate_sample_data(prop_schema, full_schema)
            return obj

        elif schema['type'] == 'array':
            item_schema = schema['items']
            if '$ref' in item_schema:
                ref_schema = resolve_ref(full_schema, item_schema['$ref'])
                if ref_schema is None:
                    return []
                return [generate_sample_data(ref_schema, full_schema)]
            else:
                return [generate_sample_data(item_schema, full_schema)]

        elif schema['type'] == 'string':

            description = schema.get('description', '')
            if 'enum' in schema:
                return choice(schema['enum'])
            else:
                return ai_generate_based_on_description(description, 'string')

        elif schema['type'] == 'integer':
            description = schema.get('description', '')
            return ai_generate_based_on_description(description, 'integer')

        elif schema['type'] == 'number':
            description = schema.get('description', '')
            return ai_generate_based_on_description(description, 'number')

        elif schema['type'] == 'boolean':
            return random.choice([True, False])

    elif '$ref' in schema:
        ref_schema = resolve_ref(full_schema, schema['$ref'])
        if ref_schema is not None:
            return generate_sample_data(ref_schema, full_schema)

    return None



def generate_sample_data_final(schema, full_schema, start_date, offset_days):
    obj = {}

    for prop, prop_schema in schema.get('properties', {}).items():
        # Check if the property has an enum and select a random value from it
        if 'enum' in prop_schema:
            obj[prop] = random.choice(prop_schema['enum'])
        elif re.search(r'businessDay', prop, re.IGNORECASE):
            obj[prop] = generate_business_day(start_date, offset_days)
        elif re.search(r'businessTimestamp', prop, re.IGNORECASE):
            obj[prop] = generate_business_timestamp(obj.get('businessDay'))
        elif re.search(r'crosaVersion', prop, re.IGNORECASE):
            obj[prop] = generate_crosa_version()
        elif re.search(r'csProcessVersion', prop, re.IGNORECASE):
            obj[prop] = generate_cs_process_version()
        elif re.search(r'flowDecompositionId', prop, re.IGNORECASE):
            obj[prop] = generate_flow_decomposition_id()
        elif re.search(r'^id$', prop, re.IGNORECASE):
            obj[prop] = generate_id()
        elif re.search(r'timestamp', prop, re.IGNORECASE):
            obj[prop] = generate_random_timestamp()
        elif re.search(r'mappingResultId', prop, re.IGNORECASE):
            obj[prop] = generate_mapping_result_id()
        elif re.search(r'selectedXnecResultId', prop, re.IGNORECASE):
            obj[prop] = generate_selected_xnec_result_id()
        elif re.search(r'timeHorizon', prop, re.IGNORECASE):
            obj[prop] = generate_time_horizon()
        elif re.search(pattern, prop, re.IGNORECASE):
            obj[prop] = generate_selected_xnec_result_id()
        elif re.search(patternXra, prop, re.IGNORECASE):
            obj[prop] = generate_selected_xnec_result_id()
        elif re.search(r'xnecCostList', prop, re.IGNORECASE):
            obj[prop] = generate_xnec_cost_list()
        elif re.search(r'tsoCode', prop, re.IGNORECASE):
            obj[prop] = random.choice(["CEPS", "APG", "PSE", "MAVIR", "Transelectrica"])
        elif re.search(r'convertedXnecId', prop, re.IGNORECASE):
            obj[prop] = generate_selected_xnec_result_id()
        else:
            if '$ref' in prop_schema:
                ref_schema = resolve_ref(full_schema, prop_schema['$ref'])
                if ref_schema:
                    obj[prop] = generate_sample_data_final(ref_schema, full_schema, start_date, offset_days)
                else:
                    obj[prop] = None
            elif prop_schema.get('type') == 'array' and 'items' in prop_schema:
                items_schema = prop_schema['items']
                if '$ref' in items_schema:
                    ref_schema = resolve_ref(full_schema, items_schema['$ref'])
                    if ref_schema:
                        obj[prop] = [generate_sample_data_final(ref_schema, full_schema, start_date, offset_days)]
                    else:
                        obj[prop] = None
                else:
                    obj[prop] = [generate_sample_data_final(items_schema, full_schema, start_date, offset_days)]
            else:
                obj[prop] = generate_sample_data(prop_schema, full_schema)

    return obj


# Main function to load schema, generate data, and write to multiple files
def generate_sample_data_files(schema_file_path, output_file_prefix, num_samples=10):
    # Load the schema from the file
    with open(schema_file_path, 'r') as f:
        schema = json.load(f)

    # Start date for the first sample
    start_date = datetime(2024, 1, 1)

    # Generate and save multiple samples
    for i in range(num_samples):
        sample_data = generate_sample_data_final(schema, schema, start_date, i)
        output_file_path = f"{output_file_prefix}_{i+1}.json"
        with open(output_file_path, 'w') as f:
            json.dump(sample_data, f, indent=4)

# # Example usage
# schema_file_path = 'CostDistribution_Schema_fixed.json'
# output_file_prefix = 'como_sample_data'
# Example usage
baseFineName = "MappingDetailedResults"
schema_file_path = 'MappingDetailedResults_Schema_fixed.json'
output_file_prefix = f'{baseFineName}_file'
generate_sample_data_files(schema_file_path, output_file_prefix)



























# import json
# import random
# import uuid
# import datetime
# import os
# import pandas as pd

# directory = '.'  # The directory where the file is located
# filename = 'Bidding_zone_EIC_code.csv'

# # Read schema from input file
# def read_schema(file_path):
#     with open(file_path, 'r') as file:
#         return json.load(file)

# # Enum values for ValueFlowComponentType
# ValueFlowComponentType = [
#     "allocatedFlow",
#     "internalFlow",
#     "loopFlow",
#     "loopFlowOutsideCore",
#     "pstFlow"
# ]

# # Helper function to generate a random value between -1 and 1
# def get_random_value():
#     return round(random.uniform(-1, 1), 2)

# def extract_bidding_zone_codes(directory, filename, variable):
#     # Construct the full path of the file
#     file_path = os.path.join(directory, filename)
    
#     # Check if the file exists in the directory
#     if not os.path.exists(file_path):
#         raise FileNotFoundError(f"The file '{filename}' does not exist in the directory '{directory}'")
    
#     # Load the CSV file
#     df = pd.read_csv(file_path)
    
#     # Check if the column 'Bidding Area EIC Code' exists in the file
#     if variable not in df.columns:
#         raise ValueError(f"The file '{filename}' does not contain the column '{variable}'")
    
#     # Extract the variable column and convert it to a list
#     bidding_zone_codes = df[variable].tolist()
    
#     return bidding_zone_codes

# def generateBiddingZoneCode():
#     bidding_zones = extract_bidding_zone_codes(directory, filename, 'Bidding Area EIC Code')
#     return random.choice(bidding_zones)

# # Generate biddingZoneList with random values
# def generate_bidding_zone_list(size):
#     bidding_zone_list = []
#     for i in range(size):
#         bidding_zone_list.append({
#             "biddingZoneCode": generateBiddingZoneCode(),
#             "value": get_random_value()
#         })
#     return bidding_zone_list

# # Calculate the sum of values in biddingZoneList
# def calculate_sum(bidding_zone_list):
#     return round(sum(zone["value"] for zone in bidding_zone_list), 2)

# # Function to generate component flows
# def generate_component_flows(bidding_zone_list):
#     component_flows = []
#     sum_value = calculate_sum(bidding_zone_list)  # Calculate sum once for loopFlow

#     for component_type in ValueFlowComponentType:
#         if component_type == "loopFlow":
#             value = sum_value  # Use sum for loopFlow
#             component_flows.append({
#                 "componentType": component_type,
#                 "value": value,
#                 "biddingZoneList": bidding_zone_list  # Keep original biddingZoneList for loopFlow
#             })
#         else:
#             # Generate a new random value for the component
#             new_value = get_random_value()
#             # Create a new biddingZoneList with all zones having the same new value
#             bidding_zone_list_copy = [
#                 {**zone, "value": new_value} for zone in bidding_zone_list
#             ]
#             component_flows.append({
#                 "componentType": component_type,
#                 "value": new_value,  # The value for non-loopFlow types matches the new value in biddingZoneList
#                 "biddingZoneList": bidding_zone_list_copy  # Update biddingZoneList with the new value
#             })
    
#     return component_flows

# # Function to generate xnecFlowComponent
# def generate_xnec_flow_component():
#     bidding_zone_list = generate_bidding_zone_list(size=random.randint(2, 5))
#     component_list = generate_component_flows(bidding_zone_list)

#     return {
#         "adjustedFmax": round(random.uniform(150, 200), 2),
#         "componentList": component_list,
#         "convertedXnecId": str(uuid.uuid4()),
#         "totalFlow": round(random.uniform(0, 100), 2)
#     }

# # Function to generate the main object based on the schema
# def generate_flow_decomposition_result():
#     now = datetime.datetime.utcnow()
#     return {
#         "timestamp": now.isoformat() + 'Z',
#         "xnecFlowComponent": generate_xnec_flow_component()
#     }

# # Example usage
# result = generate_flow_decomposition_result()
# print(json.dumps(result, indent=2))








# def generate_sample_data_final(schema, full_schema, start_date, offset_days):
#     obj = {}

#     for prop, prop_schema in schema.get('properties', {}).items():
#         # Check if the property has an enum and select a random value from it
#         if 'enum' in prop_schema:
#             obj[prop] = random.choice(prop_schema['enum'])
#         elif re.search(r'businessDay', prop, re.IGNORECASE):
#             obj[prop] = generate_business_day(start_date, offset_days)
#         elif re.search(r'businessTimestamp', prop, re.IGNORECASE):
#             obj[prop] = generate_business_timestamp(obj.get('businessDay'))
#         elif re.search(r'crosaVersion', prop, re.IGNORECASE):
#             obj[prop] = generate_crosa_version()
#         elif re.search(r'csProcessVersion', prop, re.IGNORECASE):
#             obj[prop] = generate_cs_process_version()
#         elif re.search(r'flowDecompositionId', prop, re.IGNORECASE):
#             obj[prop] = generate_flow_decomposition_id()
#         elif re.search(r'^id$', prop, re.IGNORECASE):
#             obj[prop] = generate_id()
#         elif re.search(r'timestamp', prop, re.IGNORECASE):
#             obj[prop] = generate_random_timestamp()
#         elif re.search(r'mappingResultId', prop, re.IGNORECASE):
#             obj[prop] = generate_mapping_result_id()
#         elif re.search(r'selectedXnecResultId', prop, re.IGNORECASE):
#             obj[prop] = generate_selected_xnec_result_id()
#         elif re.search(r'timeHorizon', prop, re.IGNORECASE):
#             obj[prop] = generate_time_horizon()
#         elif re.search(pattern, prop, re.IGNORECASE):
#             obj[prop] = generate_selected_xnec_result_id()
#         elif re.search(patternXra, prop, re.IGNORECASE):
#             obj[prop] = generate_selected_xnec_result_id()
#         elif re.search(r'xnecCostList', prop, re.IGNORECASE):
#             obj[prop] = generate_xnec_cost_list()
#         elif re.search(r'tsoCode', prop, re.IGNORECASE):
#             obj[prop] = random.choice(["CEPS", "APG", "PSE", "MAVIR", "Transelectrica"])
#         elif re.search(r'convertedXnecId', prop, re.IGNORECASE):
#             obj[prop] = generate_selected_xnec_result_id()
#         else:
#             if '$ref' in prop_schema:
#                 ref_schema = resolve_ref(full_schema, prop_schema['$ref'])
#                 if ref_schema:
#                     obj[prop] = generate_sample_data_final(ref_schema, full_schema, start_date, offset_days)
#                 else:
#                     obj[prop] = None
#             elif prop_schema.get('type') == 'array' and 'items' in prop_schema:
#                 items_schema = prop_schema['items']
#                 if '$ref' in items_schema:
#                     ref_schema = resolve_ref(full_schema, items_schema['$ref'])
#                     if ref_schema:
#                         obj[prop] = [generate_sample_data_final(ref_schema, full_schema, start_date, offset_days)]
#                     else:
#                         obj[prop] = None
#                 else:
#                     obj[prop] = [generate_sample_data_final(items_schema, full_schema, start_date, offset_days)]
#             else:
#                 obj[prop] = generate_sample_data(prop_schema, full_schema)

#     return obj



















# import json
# import random
# import uuid
# import datetime
# import os
# import pandas as pd

# directory = '.'  # The directory where the file is located
# filename = 'Bidding_zone_EIC_code.csv'

# # Read schema from input file
# def read_schema(file_path):
#     with open(file_path, 'r') as file:
#         return json.load(file)

# # Enum values for ValueFlowComponentType
# ValueFlowComponentType = [
#     "allocatedFlow",
#     "internalFlow",
#     "loopFlow",
#     "loopFlowOutsideCore",
#     "pstFlow"
# ]

# # Helper function to generate a random value between -1 and 1
# def get_random_value():
#     return round(random.uniform(-1, 1), 2)

# def extract_bidding_zone_codes(directory, filename, variable):
#     # Construct the full path of the file
#     file_path = os.path.join(directory, filename)
    
#     # Check if the file exists in the directory
#     if not os.path.exists(file_path):
#         raise FileNotFoundError(f"The file '{filename}' does not exist in the directory '{directory}'")
    
#     # Load the CSV file
#     df = pd.read_csv(file_path)
    
#     # Check if the column 'Bidding Area EIC Code' exists in the file
#     if variable not in df.columns:
#         raise ValueError(f"The file '{filename}' does not contain the column '{variable}'")
    
#     # Extract the variable column and convert it to a list
#     bidding_zone_codes = df[variable].tolist()
    
#     return bidding_zone_codes

# def generateBiddingZoneCode():
#     bidding_zones = extract_bidding_zone_codes(directory, filename, 'Bidding Area EIC Code')
#     return random.choice(bidding_zones)

# # Generate biddingZoneList with random values
# def generate_bidding_zone_list(size):
#     bidding_zone_list = []
#     for i in range(size):
#         bidding_zone_list.append({
#             "biddingZoneCode": generateBiddingZoneCode(),
#             "value": get_random_value()
#         })
#     return bidding_zone_list

# # Calculate the sum of values in biddingZoneList
# def calculate_sum(bidding_zone_list):
#     return round(sum(zone["value"] for zone in bidding_zone_list), 2)

# # Function to generate component flows
# def generate_component_flows(bidding_zone_list):
#     component_flows = []
#     sum_value = calculate_sum(bidding_zone_list)  # Calculate sum once for reuse
    
#     for component_type in ValueFlowComponentType:
#         if component_type == "loopFlow":
#             value = sum_value  # Use sum for loopFlow
#         else:
#             value = sum_value  # Set the same value as the sum for others

#         # Update biddingZoneList values to be the same for non-loopFlow types
#         bidding_zone_list_copy = [
#             {**zone, "value": sum_value} for zone in bidding_zone_list
#         ] if component_type != "loopFlow" else bidding_zone_list

#         component_flows.append({
#             "componentType": component_type,
#             "value": value,
#             "biddingZoneList": bidding_zone_list_copy
#         })
    
#     return component_flows

# # Function to generate xnecFlowComponent
# def generate_xnec_flow_component():
#     bidding_zone_list = generate_bidding_zone_list(size=random.randint(2, 5))
#     component_list = generate_component_flows(bidding_zone_list)

#     return {
#         "adjustedFmax": round(random.uniform(150, 200), 2),
#         "componentList": component_list,
#         "convertedXnecId": str(uuid.uuid4()),
#         "totalFlow": round(random.uniform(0, 100), 2)
#     }

# # Function to generate the main object based on the schema
# def generate_flow_decomposition_result():
#     now = datetime.datetime.utcnow()
#     business_day = now.date().isoformat()  # Extract the date part for businessDay
#     business_timestamp = now.isoformat()   # Full UTC timestamp for businessTimestamp
    
#     return {
#         "businessDay": business_day,
#         "businessTimestamp": business_timestamp,
#         "crosaVersion": random.randint(1, 1),
#         "csProcessVersion": random.randint(1, 1),
#         "id": str(uuid.uuid4()),
#         "selectedXnecResultId": str(uuid.uuid4()),
#         "timeHorizon": random.choice([
#             "dayAhead", "intraday", "monthAhead", "twoDaysAhead", "weekAhead", "yearAhead"
#         ]),
#         "xnecList": [generate_xnec_flow_component()]  # Ensure only one element in xnecList
#     }

# # Write generated data to output file
# def write_sample_data(output_path, data):
#     with open(output_path, 'w') as file:
#         json.dump(data, file, indent=2)

# # Main function that reads schema, generates sample data, and writes it to multiple files
# def generate_data_from_schema(input_schema_file, output_directory, num_files=10):
#     # Read the schema (for reference or validation, if necessary)
#     schema = read_schema(input_schema_file)
    
#     # Generate and write the specified number of sample data files
#     for i in range(num_files):
#         # Generate sample data according to schema (ignoring validation for simplicity)
#         sample_data = generate_flow_decomposition_result()
        
#         # Create a unique filename for each output file
#         output_data_file = os.path.join(output_directory, f'Flow_Decomposition_Schema_fixed_{i+1}.json')
        
#         # Write the generated sample data to the output file
#         write_sample_data(output_data_file, sample_data)
#         print(f'Generated file: {output_data_file}')

# # Example usage
# input_schema_file = 'Flow_Decomposition_Schema_fixed.json'  # Path to the schema file
# output_directory = '.'  # Directory to save generated sample data

# generate_data_from_schema(input_schema_file, output_directory, num_files=10)