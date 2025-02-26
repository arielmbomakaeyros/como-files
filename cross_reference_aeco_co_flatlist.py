import os
import json
import csv
import uuid
from datetime import datetime, timedelta
import random

# Function to load TSO EIC codes and corresponding Area Codes from the CSV file
def load_tso_eic_and_area_codes(csv_file_path):
    tso_eic_to_area_code = {}  # Dictionary to map TSO EIC code to Area Code
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tso_eic_to_area_code[row['TSO EIC code']] = row['TSO bidding-zone-code']
    return tso_eic_to_area_code

# # Helper function to generate a time interval and ensure businessTimestamp is within it
# def generate_time_interval_and_business_timestamp(start_date, offset_days):
#     from_date = start_date + timedelta(days=offset_days)
#     to_date = from_date + timedelta(hours=random.randint(1, 24))
#     business_timestamp = from_date + timedelta(seconds=random.randint(0, int((to_date - from_date).total_seconds())))
#     return {
#         "from": from_date.isoformat(),
#         "to": to_date.isoformat()
#     }, business_timestamp.isoformat()

# Helper function to generate a time interval and ensure businessTimestamp is the middle of the hour
def generate_time_interval_and_business_timestamp(start_date, offset_days):
    # Calculate the start of the interval (beginning of the hour)
    interval_start = start_date + timedelta(days=offset_days)
    interval_start = interval_start.replace(minute=0, second=0, microsecond=0)  # Start of the hour

    # Calculate the end of the interval (one hour later)
    interval_end = interval_start + timedelta(hours=1)

    # Calculate the businessTimestamp as the middle of the hour
    business_timestamp = interval_start + timedelta(minutes=30)

    return {
        "from": interval_start.isoformat(),
        "to": interval_end.isoformat()
    }, business_timestamp.isoformat()

# Function to generate sample data for AECO_FlatList_draft.json
def generate_aeco_sample_data(schema, start_date, offset_days, tso_eic_to_area_code, shared_data, mrID):
    # Randomly select a TSO EIC code and its corresponding Area Code
    owner_code = random.choice(list(tso_eic_to_area_code.keys()))
    area_code = tso_eic_to_area_code[owner_code]

    # Generate a sample JSON object based on the schema
    sample_data = {
        "assessedElementFlatListId": str(uuid.uuid4()),
        "contingencyFlatListId": shared_data["documentId"],  # Cross-reference to CO_Flat_List.documentId
        "businessTimestamp": shared_data["businessTimestamp"],  # Shared with CO_Flat_List
        "cdsId": str(uuid.uuid4()),
        "documentId": str(uuid.uuid4()),
        "gridModelId": str(uuid.uuid4()),
        "ownerCode": owner_code,
        "ownerRole": random.choice(["System Operator", "Grid Manager", "Network Engineer"]),
        "timeHorizon": shared_data["timeHorizon"],  # Shared with CO_Flat_List
        "timeInterval": shared_data["timeInterval"],  # Shared with CO_Flat_List
        "version": random.randint(1, 10),
        "assessedElementList": generate_assessed_element_list(schema, area_code, owner_code, shared_data["contingencyList"], mrID)  # Cross-reference contingencies
    }
    return sample_data

# Helper function to generate a remedial action list
def generate_remedial_action_list(schema):
    return [{
        "enabled": random.choice([True, False]),
        "remedialActionMrid": str(uuid.uuid4()),
        "ruleType": random.choice(["exclude", "include"])
    } for _ in range(random.randint(1, 3))]

# Helper function to generate a limit
def generate_limit(schema):
    return {
        "category": random.choice(["category", "permanent"]),
        "direction": random.choice(["direct", "double", "opposite"]),
        "duration": f"PT{random.randint(1, 60)}M",
        "mrid": str(uuid.uuid4()),
        "type": random.choice(["absolute", "ratio"]),
        "value": round(random.uniform(0, 1000), 2),
        "variable": random.choice(["activePowerMax", "activePowerMin", "apparentPowerMax", "apparentPowerMin", "currentMax", "currentMin", "reactivePowerMax", "reactivePowerMin", "voltageAngleMax", "voltageMax", "voltageMin"])
    }

# Helper function to generate a terminal list
def generate_terminal_list(schema):
    return [{
        "limit": generate_limit(schema),
        "limitMrid": str(uuid.uuid4()),
        "terminalMrid": str(uuid.uuid4())
    } for _ in range(random.randint(1, 3))]

# Helper function to generate an assessed element list
def generate_assessed_element_list(schema, area_code, owner_code, contingency_list, mrID):
    # print(contingency_list)
    return [{
        "appointedMargin": round(random.uniform(0, 100), 2),
        "areaCode": area_code,
        "assessedPowerTransferCorridorCode": str(uuid.uuid4()),
        "assessedSystemOperatorCode": owner_code,
        "conductingEquipmentMrid": str(uuid.uuid4()),
        "conductingEquipmentName": f"Equipment {i+1}" if random.choice([True, False]) else None,
        "contingencyList": [{
            "contingencyMrid": contingency["mrid"],  # Use the mrid from contingency_list
            "enabled": random.choice([True, False]),
            "ruleType": random.choice(["exclude", "include"])
        } for contingency in contingency_list],  # Use the mrid from contingency_list
        "dcTieCorridorCode": str(uuid.uuid4()),
        "description": f"Sample assessed element description {i+1}" if random.choice([True, False]) else None,
        "enabled": random.choice([True, False]),
        "equipmentType": random.choice(["bus", "busbar", "gen", "line", "load", "shuntCompensator", "staticVarCompensator", "switch", "transformer"]),
        "exclusionReason": random.choice(["capacityCalculationRegion", "nonNativeCapacityCalculationRegion", "systemOperator"]),
        "flowReliabilityMargin": round(random.uniform(0, 100), 2),
        "inBaseCase": random.choice([True, False]),
        "isCombinableWithContingency": random.choice([True, False]),
        "isCombinableWithRemedialAction": random.choice([True, False]),
        "isCritical": random.choice([True, False]),
        "isCrossBorderRelevant": random.choice([True, False]),
        "isExcludedAdHoc": random.choice([True, False]),
        "maxFlow": round(random.uniform(0, 1000), 2),
        "maxMarginAdjustment": round(random.uniform(0, 100), 2),
        "mrid": str(uuid.uuid4()),
        "name": f"Assessed Element {i+1}" if random.choice([True, False]) else None,
        "nativeRegionCode": str(uuid.uuid4()),
        "overlappingZoneCode": str(uuid.uuid4()),
        "positiveVirtualMargin": round(random.uniform(0, 100), 2),
        "remedialActionList": generate_remedial_action_list(schema),
        "scannedForRegionCode": str(uuid.uuid4()),
        "scannedThresholdMargin": round(random.uniform(0, 100), 2),
        "securedForRegionCode": str(uuid.uuid4()),
        "targetRemainingAvailableMargin": round(random.uniform(0, 100), 2),
        "terminalList": generate_terminal_list(schema)
    } for i in range(random.randint(1, 5))]  # Iterate based on the length of contingency_list



# Helper function to generate a contingency list for AECO_Flat_List
def generate_aeco_contingency_list(schema):
    return [{
        "contingencyMrid": str(uuid.uuid4()),  # Use contingencyMrid as per AECO schema
        "enabled": random.choice([True, False]),
        "ruleType": random.choice(["exclude", "include"])
    } for _ in range(random.randint(1, 3))]

# Helper function to generate a contingency list for CO_Flat_List
def generate_co_contingency_list(schema, aeco_contingency_mrid):
    # print(aeco_contingency_mrid,"iddd")
    # Generate a contingency list with at least one contingency matching the AECO contingencyMrid
    contingency_list = [{
        "contingencyCondition": random.choice(["design", "environmental", "geographicalLocation", "malfunction", "operation"]) if random.choice([True, False]) else None,
        "contingencyType": random.choice(["exceptional", "ordinary", "outOfRange"]),
        "description": f"Sample contingency description {i+1}" if random.choice([True, False]) else None,
        "equipmentOperatorCode": str(uuid.uuid4()),  # mRID of a SystemOperator
        "groupCode": str(uuid.uuid4()),  # Group code for the contingency
        "mrid": aeco_contingency_mrid if i == 0 else str(uuid.uuid4()),  # Ensure the first contingency matches AECO's contingencyMrid
        "mustStudy": random.choice([True, False]),  # Whether the contingency must be studied
        "name": f"Contingency {i+1}" if random.choice([True, False]) else None,
        "probability": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None  # Probability of the contingency
    } for i in range(random.randint(1, 3))]
    return contingency_list

# Helper function to generate a time interval
def generate_time_interval(start_date, offset_days):
    from_date = start_date + timedelta(days=offset_days)
    to_date = from_date + timedelta(hours=random.randint(1, 24))
    return {
        "from": from_date.isoformat(),
        "to": to_date.isoformat()
    }

# Helper function to generate an equipment list
def generate_equipment_list(schema, area_code):
    return [{
        "areaCode": area_code, # str(uuid.uuid4()),
        "description": f"Sample equipment description {i+1}",
        "equipmentMrid": str(uuid.uuid4()),
        "equipmentType": random.choice(["bus", "busbar", "gen", "line", "load", "shuntCompensator", "staticVarCompensator", "switch", "transformer"]),
        "mrid": str(uuid.uuid4()),
        "name": f"Equipment {i+1}",
    } for i in range(random.randint(1, 3))]

# Helper function to generate a contingency group list
def generate_contingency_group_list(schema, area_code, shared_data):
    return [{
        "equipmentList": generate_equipment_list(schema, area_code),
        "groupCode": contingency["groupCode"], # str(uuid.uuid4())
    } for contingency in shared_data["contingencyList"]]

# Function to generate sample data for CO_Flat_List_Schema_fixed.json
def generate_co_sample_data(schema, start_date, offset_days, tso_eic_to_area_code, aeco_contingency_mrid):
    # Randomly select a TSO EIC code and its corresponding Area Code
    owner_code = random.choice(list(tso_eic_to_area_code.keys()))
    area_code = tso_eic_to_area_code[owner_code]

    # Generate time interval and business timestamp
    time_interval, business_timestamp = generate_time_interval_and_business_timestamp(start_date, offset_days)

    # Generate shared data
    shared_data = {
        "businessTimestamp": business_timestamp,  # Shared with AECO_Flat_List
        "timeHorizon": random.choice(["dayAhead"]),
        "timeInterval": time_interval,
        "documentId": str(uuid.uuid4()),  # Shared with AECO_Flat_List.contingencyFlatListId
        "contingencyList": generate_co_contingency_list(schema, aeco_contingency_mrid)  # Use CO schema's contingency list
    }

    # # Generate shared data
    # shared_data = {
    #     "businessTimestamp": (datetime.now() - timedelta(days=offset_days)).isoformat(),
    #     # "timeHorizon": random.choice(["dayAhead", "intraday", "monthAhead", "twoDaysAhead", "weekAhead", "yearAhead"]),
    #     "timeHorizon": random.choice(["dayAhead"]),
    #     "timeInterval": generate_time_interval(start_date, offset_days),
    #     "documentId": str(uuid.uuid4()),  # Shared with AECO_Flat_List.contingencyFlatListId
    #     "contingencyList": generate_co_contingency_list(schema, aeco_contingency_mrid)  # Use CO schema's contingency list
    # }

    # Generate a sample JSON object based on the schema
    sample_data = {
        "businessTimestamp": shared_data["businessTimestamp"],  # Shared with AECO_Flat_List
        "cdsId": str(uuid.uuid4()),
        "comoDocumentType": "INTERNAL_CO_FLAT_LIST",
        "comoDocumentVersion": "R24Q4V1_0",
        "contingencyGroupList": generate_contingency_group_list(schema, area_code, shared_data),
        "contingencyList": shared_data["contingencyList"],  # Shared with AECO_Flat_List
        "contingencyListId": str(uuid.uuid4()),
        "documentId": shared_data["documentId"],  # Shared with AECO_Flat_List.contingencyFlatListId
        "gridModelId": str(uuid.uuid4()),
        "ownerCode": owner_code,
        "ownerRole": random.choice(["System Operator", "Grid Manager", "Network Engineer"]),
        "timeHorizon": shared_data["timeHorizon"],  # Shared with AECO_Flat_List
        "timeInterval": shared_data["timeInterval"],  # Shared with AECO_Flat_List
        "version": random.randint(1, 10),
        # "areaCode": area_code
    }
    return sample_data, shared_data

# Main function to load schema, generate data, and write to multiple files
def generate_sample_data_files(aeco_schema_path, co_schema_path, output_dir, tso_eic_to_area_code):
    num_samples = 6
    # Load the schemas from the files
    with open(aeco_schema_path, 'r') as f:
        aeco_schema = json.load(f)
    with open(co_schema_path, 'r') as f:
        co_schema = json.load(f)

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Start date for the first sample
    start_date = datetime(2025, 1, 1)

    # Generate and save multiple samples
    for i in range(num_samples):
        offset_days = i
        # Generate a contingencyMrid for AECO_Flat_List
        aeco_contingency_mrid = str(uuid.uuid4())
        # Generate CO_Flat_List data and shared data
        co_sample_data, shared_data = generate_co_sample_data(co_schema, start_date, offset_days, tso_eic_to_area_code, aeco_contingency_mrid)
        # Generate AECO_Flat_List data using shared data
        aeco_sample_data = generate_aeco_sample_data(aeco_schema, start_date, offset_days, tso_eic_to_area_code, shared_data, aeco_contingency_mrid)

        # Save CO_Flat_List sample data
        co_output_file_path = os.path.join(output_dir, f"CO_Flat_List_Schema_fixed_{i+1}.json")
        with open(co_output_file_path, 'w') as f:
            json.dump(co_sample_data, f, indent=4)

        # Save AECO_Flat_List sample data
        aeco_output_file_path = os.path.join(output_dir, f"AECO_FlatList_draft_{i+1}.json")
        with open(aeco_output_file_path, 'w') as f:
            json.dump(aeco_sample_data, f, indent=4)

# Example usage
aeco_schema_path = os.path.join('ae_co_flatlist', 'schema', 'AECO_FlatList_draft.json')
co_schema_path = os.path.join('flat_list', 'schema', 'CO_Flat_List_Schema_fixed.json')
output_dir = os.path.join('combined_aeco_co_flatlist', 'combined_sample_data')
tso_eic_csv_path = os.path.join('csv_files', 'Mapping_TSO_Bidding_Zone_EIC.csv')

# Load TSO EIC codes and corresponding Area Codes from the CSV file
tso_eic_to_area_code = load_tso_eic_and_area_codes(tso_eic_csv_path)

# Generate sample data files
generate_sample_data_files(aeco_schema_path, co_schema_path, output_dir, tso_eic_to_area_code)
