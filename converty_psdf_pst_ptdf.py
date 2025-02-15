import json
import secrets
import random
from datetime import datetime, timedelta
from random import choice
import uuid
# from faker import Faker
import os
import pandas as pd
import re

# fake = Faker()

directory = '.'  # The directory where the file is located
filename = 'Bidding_zone_EIC_code.csv'

# Enum values for ValueFlowComponentType
ValueFlowComponentType = [
    "allocatedFlow",
    "internalFlow",
    "loopFlow",
    "loopFlowOutsideCore",
    "pstFlow"
]


# Helper function to generate a random value
def get_random_value():
    return round(random.uniform(-1, 1), 2)

def extract_bidding_zone_codes(directory, filename, variable):
    # Construct the full path of the file
    file_path = os.path.join(directory, filename)
    
    # Check if the file exists in the directory
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{filename}' does not exist in the directory '{directory}'")
    
    # Load the CSV file
    df = pd.read_csv(file_path)
    
    # Check if the column 'Bidding Area EIC Code' exists in the file
    if variable not in df.columns:
        raise ValueError(f"The file '{filename}' does not contain the column '{variable}'")
    
    # Extract the variable column and convert it to a list
    bidding_zone_codes = df[variable].tolist()
    
    return bidding_zone_codes

def getBiddingZoneCode():
    return extract_bidding_zone_codes(directory, filename, 'Bidding Area EIC Code')
    # return random.choice(bidding_zones)

def generateBiddingZoneCode():
    bidding_zones = extract_bidding_zone_codes(directory, filename, 'Bidding Area EIC Code')
    return random.choice(bidding_zones)

# Generate biddingZoneList with random values
def generate_bidding_zone_list(size):
    bidding_zone_list = []
    for _ in range(size):
        bidding_zone_list.append({
            "biddingZoneCode": generateBiddingZoneCode(),
            "value": get_random_value()
        })
    return bidding_zone_list

# Calculate the sum of values in biddingZoneList
def calculate_sum(bidding_zone_list):
    return round(sum(zone["value"] for zone in bidding_zone_list), 2)

# Function to generate component flows
def generate_component_flows(bidding_zone_list):
    component_flows = []
    sum_value = calculate_sum(bidding_zone_list)  # Calculate sum once for loopFlow

    for component_type in ValueFlowComponentType:
        # value = sum_value  # Use sum for loopFlow
        # bidding_zone_list_copy = bidding_zone_list  # Use original biddingZoneList
        if component_type == "loopFlow":
            value = sum_value  # Use sum for loopFlow
            bidding_zone_list_copy = bidding_zone_list  # Use original biddingZoneList
        
        # THIS ELSE PORTION MAKES SURE THAT WE SUM UP EACH bidding_zone IN THE LIST AND GIVE THE SUM AS A FLOW TYPE VALUE FOR ALL NON LOOPFLOW 
        else:
            # For other types, create a distinct value
            offset = round(random.uniform(0.1, 0.5), 2)  # Random offset for uniqueness
            value = round(sum_value + offset, 2)  # Apply offset to the sum
            
            # Create a new biddingZoneList that sums to the same total
            bidding_zone_list_copy = []
            total_adjusted = 0  # To keep track of the adjusted total
            
            for zone in bidding_zone_list:
                # Generate a unique random value for each zone
                unique_value = round(zone["value"] + random.uniform(0.01, 0.1), 2)
                bidding_zone_list_copy.append({
                    "biddingZoneCode": zone["biddingZoneCode"],
                    "value": unique_value
                })
                total_adjusted += unique_value

            # Adjust the last zone's value to ensure the sum remains the same
            last_zone_value = round(value - (total_adjusted - bidding_zone_list_copy[-1]["value"]), 2)
            bidding_zone_list_copy[-1]["value"] = last_zone_value

        component_flows.append({
            "componentType": component_type,
            "value": value,
            "biddingZoneList": bidding_zone_list_copy
        })

    return component_flows


# Function to generate xnecFlowComponent
def generate_xnec_flow_component():
    bidding_zone_list = generate_bidding_zone_list(size=random.randint(2, 5))
    component_list = generate_component_flows(bidding_zone_list)

    return {
        "adjustedFmax": round(random.uniform(150, 200), 2),
        "componentList": component_list,
        "convertedXnecId": str(uuid.uuid4()),
        "totalFlow": round(random.uniform(0, 100), 2)
    }

def generate_comp_list():
    bidding_zone_list = generate_bidding_zone_list(size=random.randint(2, 5))
    return generate_component_flows(bidding_zone_list)

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
    # return random.randint(1, 5)
    return random.randint(1, 1)

def generate_tso_code():
    # return random.choice(["dayAhead", "weekAhead", "monthAhead", "Intraday"])
    return random.choice(["CEPS", "APG", "PSE", "MAVIR", "Transelectrica"]),

def generate_cs_process_version():
    return random.randint(1, 5)
    # return random.randint(1, 1)

def generate_flow_decomposition_id():
    return secrets.token_hex(12)

def generate_id():
    return secrets.token_hex(12)

def generate_mapping_result_id():
    return secrets.token_hex(12)

def generate_selected_xnec_result_id():
    return secrets.token_hex(12)

def generate_time_horizon():
    # return random.choice(["dayAhead", "weekAhead", "monthAhead", "Intraday"])
    return random.choice(["dayAhead"])



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
        # "biddingZoneCode": random.choice(["EIC_DE", "EIC_SI", "EIC_PL", "EIC_SK", "EIC_RO"]),
        "biddingZoneCode": random.choice([generateBiddingZoneCode()]),
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


def generate_bidding_zone_cost_list():
    # bidding_zones = ["EIC_DE", "EIC_SI", "EIC_NL", "EIC_FR", "EIC_PL", "EIC_SK", "EIC_RO"]
    bidding_zones = random.sample(getBiddingZoneCode (), 5)

    cost_list = []
    # for _ in range(random.randint(1, 3)):
    for zone in bidding_zones:
        item = {
            # "biddingZoneCode": generateBiddingZoneCode(),
            "biddingZoneCode": zone,
            "contribution": random.uniform(0, 0.5),
            "cost": random.uniform(0, 25000)
        }
        # print(f"Individual Cost for {item['biddingZoneCode']}: {item['cost']}")
        cost_list.append(item)
    return cost_list

def generate_xnec_cost():
    bidding_zone_cost_list = generate_bidding_zone_cost_list()

    # Print each cost value before summing
    for item in bidding_zone_cost_list:
        print("Individual Cost:", item["cost"])

    total_cost = sum(item["cost"] for item in bidding_zone_cost_list)
    print(total_cost, "================")
    return {
        "biddingZoneCostList": bidding_zone_cost_list,
        # "convertedXnecId": f"ID{random.randint(1, 100)}",
        "convertedXnecId": str(uuid.uuid4()),
        "cost": total_cost,
        "flowComponentList": generate_flow_component_list(),
        "tsoCostList": generate_tso_cost_list(),
        "volumeOverload": generate_volume_overload()
    }

cumulative_costs_ora = 0
cumulative_costs_pst = 0

def generate_string_off_dat ():
    # Generate a random date within the past year
    start = datetime.now() - timedelta(days=365)  # One year ago from today
    end = datetime.now()
    random_date = start + (end - start) * random.random()

    # Randomly choose either 01:30 or 02:30 for the time
    hour = random.choice([1, 2])
    random_date = random_date.replace(hour=hour, minute=30, second=0, microsecond=0)

    # Format the date and timestamp
    business_day = random_date.strftime('%Y-%m-%d')
    # business_timestamp = random_date.isoformat()
    business_timestamp = random_date.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'  # Add 'Z' for UTC

    # Step 1: Extract the date part and remove hyphens
    date_part = business_timestamp.split("T")[0].replace("-", "")

    # Step 2: Define the static middle part
    middle_part = "_DA_CROSA_ORA_"

    # Step 3: Generate a random 4-digit number
    random_value = random.randint(1000, 9999)  # Random 4-digit number

    # Construct the final string
    final_string = f"{date_part}{middle_part}{random_value}"  # Pad with zeros to make it 4 digits
    return final_string





def basic_psdf_data ():
    # Generate a random positive real number
    positive_real = abs(random.random() * random.randint(1, 10_000))
    precision = 3
    random_decimal = round(positive_real, precision)
    return {
        "convertedXnecId": str(uuid.uuid4()),
        "pstId": str(uuid.uuid4()), # secrets.token_hex(12), # generate_string_off_dat (), # str(uuid.uuid4()),
        "sensitivity": random_decimal,
    }

def generate_psdf_data(final_string):
    num_objects = random.randint(1, 5)
    # Generate a random positive real number
    psdf_data = [basic_psdf_data() for _ in range(num_objects)]
    return psdf_data

# FUNCTION NOT USED
def generate_pst_data():
    # Generate a random positive real number
    return {
        "costsPst": round(random.uniform(150, 200), 2),
        "pstId": str(uuid.uuid4()),
        "tapAfter": round(random.uniform(0, 100), 2),
        "tapBefore": round(random.uniform(150, 200), 2)
    }

# Function to generate an array of random objects and calculate cumulative costsOra
def generate_random_objects_and_cumulative_pst_cost(psdf_data):
    xnec_data = []

    for entry in psdf_data:
        converted_pst_Id = entry.get("pstId")

        # Create the xnecData object
        xnec_data.append({
            "costsPst": round(random.uniform(150, 200), 2),
            "pstId": converted_pst_Id,
            "tapAfter": round(random.uniform(0, 100), 2),
            "tapBefore": round(random.uniform(150, 200), 2)
        })

    # Calculate the cumulative value of pstCost
    precision = 3
    cumulative_costs_pst = round(sum(obj["costsPst"] for obj in xnec_data), precision)

    return {
        "pstData": xnec_data, 
        "cumulative_costs_pst": cumulative_costs_pst
    }

# WE MUST FIND A WAY TO INJECT THESE OBJECT INSIDE xnecData (WE CREATE AS MANY xnecData OBJECT CORRESPONDING to ptdf object (convertedXnecId))
number_of_ptdf_objects = 0
# WE MUST FIND A WAY TO INJECT THESE OBJECT INSIDE xnecData (WE CREATE AS MANY xnecData OBJECT CORRESPONDING to psdf object (convertedXnecId))
number_of_psdf_objects = 0

def basic_ptdf_data ():
    # Generate a random decimal between 0 and 1 (3 decimal)
    random_decimal = random.uniform(0, 1)

    # Specify the number of decimal places (e.g., 2 decimal places)
    precision = 3
    random_decimal = round(random_decimal, precision)
    return {
        "convertedXnecId": str(uuid.uuid4()),
        "raId": generate_string_off_dat (),
        "sensitivity": random_decimal,
    }

def generate_ptdf_data(final_string):
    num_objects = random.randint(1, 5)
    # Generate a random positive real number
    ptdf_data = [basic_ptdf_data() for _ in range(num_objects)]
    return ptdf_data

# NOT USED NOW
def generate_ra_data(final_string):
    # Generate a random positive real number
    return {
        "costsOra": round(random.uniform(150, 200), 2),
        "costsOraVariable": round(random.uniform(150, 200), 2),
        "hourlyCostsAfterFixedCosts": round(random.uniform(150, 200), 2),
        "hourlyCostsAfterReallocation": round(random.uniform(150, 200), 2),
        "hourlyCostsFiltered": round(random.uniform(0, 100), 2),
        "raId": final_string, # str(uuid.uuid4()),
        "variableCostFinal": round(random.uniform(150, 200), 2),
        "variableCostIntermediate": round(random.uniform(150, 200), 2)
    }

# Function to generate an array of random objects and calculate cumulative costsOra
def generate_random_objects_and_cumulative_ra_cost(ptdf_data):
    # Generate a random number of objects between 1 and 5
    raData = []

    for entry in ptdf_data:
        converted_ra_Id = entry.get("raId")

        # Create the xnecData object
        raData.append({
            "costsOra": round(random.uniform(150, 200), 2),
            "costsOraVariable": round(random.uniform(150, 200), 2),
            "hourlyCostsAfterFixedCosts": round(random.uniform(150, 200), 2),
            "hourlyCostsAfterReallocation": round(random.uniform(150, 200), 2),
            "hourlyCostsFiltered": round(random.uniform(0, 100), 2),
            "raId": converted_ra_Id, # str(uuid.uuid4()),
            "variableCostFinal": round(random.uniform(150, 200), 2),
            "variableCostIntermediate": round(random.uniform(150, 200), 2)
        })
    
    # Calculate the cumulative value of costsOra
    precision = 3
    cumulative_costs_ora = round(sum(obj["costsOra"] for obj in raData), precision)
    
    return {
        "raData": raData, 
        "cumulative_costs_ora": cumulative_costs_ora
    }

# def generate_xnec_data(convertedXnecId):
#     # Generate a random positive real number
#     return {
#         "convertedXnecId": convertedXnecId,
#         "fLimit": round(random.uniform(0, 100), 2),
#         "fPrimeB": round(random.uniform(0, 100), 2),
#         "fWithoutOrasAndPsts": round(random.uniform(150, 200), 2)
#     }

def generate_xnec_data(psdf_data, ptdf_data):
    """
    Generate xnecData objects based on psdfData and ptdfData.

    Args:
        psdf_data (list): List of psdfData objects.
        ptdf_data (list): List of ptdfData objects.

    Returns:
        list: List of xnecData objects with calculated properties.
    """
    xnec_data = []

    # Combine psdfData and ptdfData based on convertedXnecId
    combined_data = psdf_data + ptdf_data

    for entry in combined_data:
        converted_xnec_id = entry.get("convertedXnecId")

        # Calculate properties (for simplicity, use random values or example calculations)
        f_limit = round(random.uniform(30.0, 50.0), 2)  # Example random value for fLimit
        f_prime_b = round(random.uniform(80.0, 100.0), 2)  # Example random value for fPrimeB
        f_without_oras_and_psts = round((f_limit + f_prime_b) / 2, 2)  # Example calculation

        # Create the xnecData object
        xnec_data.append({
            "convertedXnecId": converted_xnec_id,
            "fLimit": f_limit,
            "fPrimeB": f_prime_b,
            "fWithoutOrasAndPsts": f_without_oras_and_psts,
        })

    return xnec_data


def generate_xnec_cost_list():
    return [generate_xnec_cost() for _ in range(random.randint(1, 5))]



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

pattern = r'^(xnec.*Id|.*xnecId)$'
patternXra = r'^(xra.*Id|.*xraId)$'


def resolve_reference(schema, ref):
    """Resolve a reference within the JSON schema."""
    ref_path = ref.replace("#/", "").split("/")
    ref_schema = schema
    for part in ref_path:
        ref_schema = ref_schema.get(part, {})
    return ref_schema


# GENERATE SAMPLE DATA
def generate_sample_data(schema, root_schema):
    """Generate sample data based on the provided JSON schema."""
    start = datetime.now() - timedelta(days=365)  # One year ago from today
    end = datetime.now()
    random_date = start + (end - start) * random.random()

    # Randomly choose either 01:30 or 02:30 for the time
    hour = random.choice([1, 2])
    random_date = random_date.replace(hour=hour, minute=30, second=0, microsecond=0)

    # Format the date and timestamp
    business_day = random_date.strftime('%Y-%m-%d')

    # Detect and handle `oneOf` property
    if 'oneOf' in schema:
        # Randomly select one of the schemas from `oneOf`
        chosen_schema = random.choice(schema['oneOf'])
        print(f"Chosen schema from oneOf: {chosen_schema}")  # For analysis
        return generate_sample_data(chosen_schema, root_schema)

    # Determine the type of the schema
    schema_type = schema.get('type')
    if isinstance(schema_type, list):
        print ("print it here")
        # If type is an array, handle the types that exist in the array
        if 'null' in schema_type:
            # Randomly decide if we should return None (null)
            if random.choice([True, False]):
                return None
        # Set schema_type to first non-null type
        schema_type = next(t for t in schema_type if t != 'null')
        print("print it here-------", schema_type)

    # Check if the schema has a 'const' property and return its value if so
    if 'const' in schema:
        return schema['const']

    # Handle each type accordingly
    if schema_type == 'string':
        if 'enum' in schema:
            return random.choice(schema['enum'])
        if 'format' in schema and schema['format'] == 'date-time':
            return business_day
        return generate_selected_xnec_result_id()

    elif schema_type == 'integer':
        return random.randint(1, 100)

    elif schema_type == 'number':
        # print(schema, "999000999")
        return round(random.uniform(1.0, 100.0), 2)

    elif schema_type == 'boolean':
        return random.choice([True, False])

    elif schema_type == 'array':
        items_schema = schema.get('items', {})
        # print(items_schema, "llllllll")
        # return [generate_sample_data_final(items_schema, root_schema, start_date, offset_days)]
        return [generate_sample_data(items_schema, root_schema) for _ in range(random.randint(1, 3))]

    elif schema_type == 'object':
        properties = schema.get('properties', {})
        obj = {}
        for key, prop_schema in properties.items():
            if '$ref' in prop_schema:
                # Resolve the reference and generate sample for it
                resolved_schema = resolve_reference(root_schema, prop_schema['$ref'])
                obj[key] = generate_sample_data(resolved_schema, root_schema)
            else:
                obj[key] = generate_sample_data(prop_schema, root_schema)
        return obj

    if '$ref' in schema:
        # Resolve reference and generate sample
        resolved_schema = resolve_reference(root_schema, schema['$ref'])
        return generate_sample_data(resolved_schema, root_schema)

    return None


def generate_random_number ():
    return random.randint(1000, 9999)

def generate_sample_data_final(schema, full_schema, start_date, offset_days):
    # Generate a random date within the past year
    start = datetime.now() - timedelta(days=365)  # One year ago from today
    end = datetime.now()
    random_date = start + (end - start) * random.random()

    # Randomly choose either 01:30 or 02:30 for the time
    hour = random.choice([1, 2])
    random_date = random_date.replace(hour=hour, minute=30, second=0, microsecond=0)

    # Format the date and timestamp
    business_day = random_date.strftime('%Y-%m-%d')
    # business_timestamp = random_date.isoformat()
    business_timestamp = random_date.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'  # Add 'Z' for UTC

    # Step 1: Extract the date part and remove hyphens
    date_part = business_timestamp.split("T")[0].replace("-", "")

    # Step 2: Define the static middle part
    middle_part = "_DA_CROSA_ORA_"

    # Step 3: Generate a random 4-digit number
    random_value = random.randint(1000, 9999)  # Random 4-digit number

    # Construct the final string
    final_string = f"{date_part}{middle_part}{random_value}"  # Pad with zeros to make it 4 digits
    print(final_string)  # Output: 20220227_DA_CROSA_ORA_0601
    obj = {}

    

    for prop, prop_schema in schema.get('properties', {}).items():
        # Check if the property has an enum and select a random value from it
        if 'enum' in prop_schema:
            obj[prop] = random.choice(prop_schema['enum'])
        elif re.search(r'businessDay', prop, re.IGNORECASE):
            obj[prop] = business_day
        elif re.search(r'businessTimestamp', prop, re.IGNORECASE):
            obj[prop] = business_timestamp
        elif re.search(r'crosaVersion', prop, re.IGNORECASE):
            obj[prop] = generate_crosa_version()
        elif re.search(r'csProcessVersion', prop, re.IGNORECASE):
            obj[prop] = generate_cs_process_version()
        elif re.search(r'flowDecompositionId', prop, re.IGNORECASE):
            obj[prop] = generate_flow_decomposition_id()
        elif re.search(r'^id$', prop, re.IGNORECASE):
            obj[prop] = generate_id()
        elif re.search(r'timestamp', prop, re.IGNORECASE):
            obj[prop] = business_timestamp
        elif re.search(r'mappingResultId', prop, re.IGNORECASE):
            obj[prop] = generate_mapping_result_id()
        elif re.search(r'selectedXnecResultId', prop, re.IGNORECASE):
            obj[prop] = generate_selected_xnec_result_id()
        elif re.search(r'timeHorizon', prop, re.IGNORECASE):
            obj[prop] = generate_time_horizon()
        elif re.search(pattern, prop, re.IGNORECASE):
            obj[prop] = generate_selected_xnec_result_id()
        elif prop == "biddingZoneCode":
            obj[prop] = generateBiddingZoneCode()
        elif prop == "componentList":
            obj[prop] = generate_comp_list()
        elif re.search(patternXra, prop, re.IGNORECASE):
            obj[prop] = generate_selected_xnec_result_id()
        elif re.search(r'xnecCostList', prop, re.IGNORECASE):
            obj[prop] = generate_xnec_cost_list()
        elif re.search(r'tsoCode', prop, re.IGNORECASE):
            obj[prop] = random.choice(["CEPS", "APG", "PSE", "MAVIR", "Transelectrica"])
        elif re.search(r'convertedXnecId', prop, re.IGNORECASE):
            obj[prop] = generate_selected_xnec_result_id()
        elif re.search(r'psdfData', prop, re.IGNORECASE):
            number_of_psdf_objects = generate_psdf_data (f"{date_part}{middle_part}{generate_random_number ()}")
            # print(number_of_psdf_objects, "---------->")
            obj[prop] = number_of_psdf_objects
        elif re.search(r'ptdfData', prop, re.IGNORECASE):
            number_of_ptdf_objects = generate_ptdf_data (f"{date_part}{middle_part}{generate_random_number ()}")
            # print(number_of_ptdf_objects, "==========>")
            obj[prop] = number_of_ptdf_objects
        elif re.search(r'raData', prop, re.IGNORECASE):
            result = generate_random_objects_and_cumulative_ra_cost (number_of_ptdf_objects)
            cumulative_costs_ora = result ["cumulative_costs_ora"]
            obj[prop] = result ["raData"]
        elif re.search(r'xnecData', prop, re.IGNORECASE):
            # print(number_of_psdf_objects, "-----4444----->")
            # print(number_of_ptdf_objects, "=====3333=====>")
            result = generate_xnec_data (number_of_psdf_objects, number_of_ptdf_objects)
            obj[prop] = result
        elif re.search(r'pstData', prop, re.IGNORECASE):
            result = generate_random_objects_and_cumulative_pst_cost (number_of_psdf_objects)
            cumulative_costs_pst = result ["cumulative_costs_pst"]
            obj[prop] = result ["pstData"]
        elif re.search(r'totalCostsAllOras', prop, re.IGNORECASE):
            obj[prop] = cumulative_costs_ora
        elif re.search(r'totalCostsAllPsts', prop, re.IGNORECASE):
            obj[prop] = cumulative_costs_pst
        else:
            if '$ref' in prop_schema:
                ref_schema = resolve_ref(full_schema, prop_schema['$ref'])
                if ref_schema:
                    # obj[prop] = generate_sample_data_final(ref_schema, full_schema, start_date, offset_days)
                    obj[prop] = generate_sample_data(prop_schema, full_schema)
                else:
                    obj[prop] = None
            elif ('array' in prop_schema.get('type', []) if isinstance(prop_schema.get('type'), list) else prop_schema.get('type') == 'array') and 'items' in prop_schema:
                items_schema = prop_schema['items']
                if '$ref' in items_schema:
                    # print("77490000", items_schema['$ref'])
                    ref_schema = resolve_ref(full_schema, items_schema['$ref'])
                    # print("64792840", ref_schema)
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
baseFineName = "CostDistribution"
schema_file_path = 'CostDistribution_Schema_fixed.json'

# Example usage
# baseFineName = "MappingDetailedResults"
# schema_file_path = 'MappingDetailedResults_Schema_fixed.json'

# baseFineName = "Flow_Decomposition"
# schema_file_path = 'Flow_Decomposition_Schema_fixed.json'

# baseFineName = "SelectedXnecResult_"
# schema_file_path = 'SelectedXnecResult_Scheme_fixed.json'

# baseFineName = "MappingTSOdata_IntermediateResultsPerHour_"
# schema_file_path = 'MappingTSOdata_IntermediateResultsPerHour_fixed.json'

# baseFineName = "FlowDecompositionIntermediateResult_Schema_fixed"
# schema_file_path = 'FlowDecompositionIntermediateResult_Schema_fixed.json'



# baseFineName = "CostDistribution"
# schema_file_path = 'CostDistribution_Schema_fixed.json'


# Flow_Decomposition_Schema_fixed.json
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