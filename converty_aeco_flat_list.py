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
            tso_eic_to_area_code[row['TSO EIC code']] = row['Area Code']
    return tso_eic_to_area_code

# Function to generate sample data based on the schema
def generate_sample_data_final(schema, start_date, offset_days, tso_eic_to_area_code):
    # Randomly select a TSO EIC code and its corresponding Area Code
    owner_code = random.choice(list(tso_eic_to_area_code.keys()))
    area_code = tso_eic_to_area_code[owner_code]

    # Generate a sample JSON object based on the schema
    sample_data = {
        "assessedElementFlatListId": str(uuid.uuid4()),
        "contingencyFlatListId": str(uuid.uuid4()),
        "businessTimestamp": (datetime.now() - timedelta(days=offset_days)).isoformat(),
        "cdsId": str(uuid.uuid4()),
        "documentId": str(uuid.uuid4()),
        "gridModelId": str(uuid.uuid4()),
        "ownerCode": owner_code,
        "ownerRole": random.choice(["System Operator", "Grid Manager", "Network Engineer"]),
        "timeHorizon": random.choice(["dayAhead"]),
        # "timeHorizon": random.choice(["dayAhead", "intraday", "monthAhead", "twoDaysAhead", "weekAhead", "yearAhead"]),
        "timeInterval": generate_time_interval(start_date, offset_days),
        "version": random.randint(1, 10),
        "assessedElementList": generate_assessed_element_list(schema, area_code, owner_code)
    }
    return sample_data

# Helper function to generate an assessed element list
def generate_assessed_element_list(schema, area_code, owner_code):
    if random.choice([True, False]):
        return None
    return [{
        "appointedMargin": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "areaCode": area_code,
        "assessedPowerTransferCorridorCode": str(uuid.uuid4()) if random.choice([True, False]) else None,
        "assessedSystemOperatorCode": str(uuid.uuid4()) if random.choice([True, False]) else None, # owner_code,
        "conductingEquipmentMrid": str(uuid.uuid4()) if random.choice([True, False]) else None,
        "conductingEquipmentName": f"Equipment {i+1}" if random.choice([True, False]) else None,
        "contingencyList": generate_contingency_list(schema),
        "dcTieCorridorCode": str(uuid.uuid4()) if random.choice([True, False]) else None,
        "description": f"Sample assessed element description {i+1}" if random.choice([True, False]) else None,
        "enabled": random.choice([True, False]),
        "equipmentType": random.choice(["bus", "busbar", "gen", "line", "load", "shuntCompensator", "staticVarCompensator", "switch", "transformer"]) if random.choice([True, False]) else None,
        "exclusionReason": random.choice(["capacityCalculationRegion", "nonNativeCapacityCalculationRegion", "systemOperator"]) if random.choice([True, False]) else None,
        "flowReliabilityMargin": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "inBaseCase": random.choice([True, False]),
        "isCombinableWithContingency": random.choice([True, False]),
        "isCombinableWithRemedialAction": random.choice([True, False]),
        "isCritical": random.choice([True, False]),
        "isCrossBorderRelevant": random.choice([True, False]),
        "isExcludedAdHoc": random.choice([True, False]),
        "maxFlow": round(random.uniform(0, 1000), 2) if random.choice([True, False]) else None,
        "maxMarginAdjustment": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "mrid": str(uuid.uuid4()),
        "name": f"Assessed Element {i+1}" if random.choice([True, False]) else None,
        "nativeRegionCode": str(uuid.uuid4()) if random.choice([True, False]) else None,
        "overlappingZoneCode": str(uuid.uuid4()) if random.choice([True, False]) else None,
        "positiveVirtualMargin": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "remedialActionList": generate_remedial_action_list(schema),
        "scannedForRegionCode": str(uuid.uuid4()) if random.choice([True, False]) else None,
        "scannedThresholdMargin": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "securedForRegionCode": str(uuid.uuid4()) if random.choice([True, False]) else None,
        "targetRemainingAvailableMargin": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "terminalList": generate_terminal_list(schema)
    } for i in range(random.randint(1, 5))]

# Helper function to generate a contingency list
def generate_contingency_list(schema):
    if random.choice([True, False]):
        return None
    return [{
        "contingencyMrid": str(uuid.uuid4()),
        "enabled": random.choice([True, False]),
        "ruleType": random.choice(["exclude", "include"])
    } for _ in range(random.randint(1, 3))]

# Helper function to generate a remedial action list
def generate_remedial_action_list(schema):
    if random.choice([True, False]):
        return None
    return [{
        "enabled": random.choice([True, False]),
        "remedialActionMrid": str(uuid.uuid4()),
        "ruleType": random.choice(["exclude", "include"])
    } for _ in range(random.randint(1, 3))]

# Helper function to generate a terminal list
def generate_terminal_list(schema):
    if random.choice([True, False]):
        return None
    return [{
        "limit": generate_limit(schema) if random.choice([True, False]) else None,
        "limitMrid": str(uuid.uuid4()) if random.choice([True, False]) else None,
        "terminalMrid": str(uuid.uuid4())
    } for _ in range(random.randint(1, 3))]

# Helper function to generate a limit
def generate_limit(schema):
    return {
        "category": random.choice(["category", "permanent"]) if random.choice([True, False]) else None,
        "direction": random.choice(["direct", "double", "opposite"]) if random.choice([True, False]) else None,
        "duration": f"PT{random.randint(1, 60)}M" if random.choice([True, False]) else None,
        "mrid": str(uuid.uuid4()),
        "type": random.choice(["absolute", "ratio"]) if random.choice([True, False]) else None,
        "value": round(random.uniform(0, 1000), 2),
        "variable": random.choice(["activePowerMax", "activePowerMin", "apparentPowerMax", "apparentPowerMin", "currentMax", "currentMin", "reactivePowerMax", "reactivePowerMin", "voltageAngleMax", "voltageMax", "voltageMin"])
    }

# Helper function to generate a time interval
def generate_time_interval(start_date, offset_days):
    if random.choice([True, False]):
        return None
    from_date = start_date + timedelta(days=offset_days)
    to_date = from_date + timedelta(hours=random.randint(1, 24))
    return {
        "from": from_date.isoformat(),
        "to": to_date.isoformat()
    }

# Main function to load schema, generate data, and write to multiple files
def generate_sample_data_files(schema_file_path, output_dir, output_file_prefix, tso_eic_to_area_code):
    num_samples = 10
    # Load the schema from the file
    with open(schema_file_path, 'r') as f:
        schema = json.load(f)

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Start date for the first sample
    start_date = datetime(2024, 1, 1)

    # Generate and save multiple samples
    for i in range(num_samples):
        offset_days = i
        sample_data = generate_sample_data_final(schema, start_date, offset_days, tso_eic_to_area_code)
        output_file_path = os.path.join(output_dir, f"{output_file_prefix}_{i+1}.json")
        with open(output_file_path, 'w') as f:
            json.dump(sample_data, f, indent=4)

# Example usage
baseFileName = "AECO_FlatList_draft"
schema_file_path = os.path.join('ae_co_flatlist', 'schema', 'AECO_FlatList_draft.json')

# Path to the output directory (2 levels down)
output_dir = os.path.join('ae_co_flatlist', 'AECO_FlatList_draft_sample_data')

# Path to the TSO EIC codes CSV file
tso_eic_csv_path = os.path.join('csv_files', 'Mapping_TSO_Bidding_Zone_EIC.csv')

# Load TSO EIC codes and corresponding Area Codes from the CSV file
tso_eic_to_area_code = load_tso_eic_and_area_codes(tso_eic_csv_path)

# Generate sample data files
output_file_prefix = f'{baseFileName}_file'
generate_sample_data_files(schema_file_path, output_dir, output_file_prefix, tso_eic_to_area_code)