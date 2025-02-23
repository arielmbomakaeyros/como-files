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
        "businessTimestamp": (datetime.now() - timedelta(days=offset_days)).isoformat() if random.choice([True, False]) else None,
        "cdsId": str(uuid.uuid4()),  # Use native UUID
        "comoDocumentType": "INTERNAL_RA_FLAT_LIST",
        "comoDocumentVersion": "R24Q4V1_0",
        "contingencyWithRemedialActionList": generate_contingency_with_remedial_action_list(schema),
        "documentId": str(uuid.uuid4()),  # Use native UUID
        "gridModelId": str(uuid.uuid4()),  # Use native UUID
        "gridStateAlterationRemedialActionList": generate_grid_state_alteration_remedial_action_list(schema),
        "ownerCode": owner_code,  # Use the selected TSO EIC code
        "ownerRole": random.choice(["System Operator", "Grid Manager", "Network Engineer"]),  # Random role
        "powerBidScheduleList": generate_power_bid_schedule_list(schema),
        "powerRemedialActionList": generate_power_remedial_action_list(schema),
        "powerShiftKeyDistributionList": generate_power_shift_key_distribution_list(schema),
        "powerShiftKeyList": generate_power_shift_key_list(schema),
        "remedialActionGroupList": generate_remedial_action_group_list(schema),
        "remedialActionListId": str(uuid.uuid4()),  # Use native UUID
        # "timeHorizon": random.choice(["dayAhead", "intraday", "monthAhead", "twoDaysAhead", "weekAhead", "yearAhead"]),
        "timeHorizon": random.choice(["dayAhead"]),
        "timeInterval": generate_time_interval(start_date, offset_days),
        "version": random.randint(1, 10),
        "areaCode": area_code  # Use the corresponding Area Code
    }
    return sample_data

# Helper functions to generate lists based on the schema
def generate_contingency_with_remedial_action_list(schema):
    if random.choice([True, False]):
        return None
    return [{
        "combinationConstraintKind": random.choice(["considered", "excluded", "included"]),
        "contingencyMrid": str(uuid.uuid4()),
        "enabled": random.choice([True, False]),
        "mrid": str(uuid.uuid4()),
        "remedialActionMrid": str(uuid.uuid4())
    } for _ in range(random.randint(1, 3))]

def generate_grid_state_alteration_remedial_action_list(schema):
    if random.choice([True, False]):
        return None
    return [{
        "available": random.choice([True, False]),
        "description": f"Sample description {i+1}" if random.choice([True, False]) else None,
        "gridStateAlterationList": generate_grid_state_alteration_list(schema),
        "impactThresholdMargin": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "isCrossBorderRelevant": random.choice([True, False]),
        "isManual": random.choice([True, False]),
        "kind": random.choice(["curative", "preventive"]),
        "mrid": str(uuid.uuid4()),
        "name": f"Sample name {i+1}" if random.choice([True, False]) else None,
        "penaltyFactor": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "regionCode": str(uuid.uuid4()),
        "systemOperatorCode": str(uuid.uuid4()) if random.choice([True, False]) else None,
        "timeToImplement": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None
    } for i in range(random.randint(1, 3))]

def generate_grid_state_alteration_list(schema):
    if random.choice([True, False]):
        return None
    return [{
        "actionType": random.choice(["acdcConverterAction", "batteryUnitAction", "biddingZoneAction", "controlFunctionBlockAction", "energySourceAction", "equipmentControllerAction", "equivalentInjectionAction", "externalNetworkInjectionAction", "loadAction", "powerElectronicsConnectionAction", "regulatingControlAction", "rotatingMachineAction", "shuntCompensatorAction", "staticVarCompensatorAction", "tapPositionAction", "topologyAction"]),
        "description": f"Sample description {i+1}" if random.choice([True, False]) else None,
        "enabled": random.choice([True, False]),
        "maximumPerDay": random.randint(1, 24) if random.choice([True, False]) else None,
        "minimumActivation": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "mrid": str(uuid.uuid4()),
        "name": f"Sample name {i+1}" if random.choice([True, False]) else None,
        "powerSystemResourceMrid": str(uuid.uuid4()),
        "propertyReference": str(uuid.uuid4()),
        "rangeConstraintList": generate_range_constraint_list(schema),
        "timePerStage": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None
    } for i in range(random.randint(1, 3))]

def generate_range_constraint_list(schema):
    if random.choice([True, False]):
        return None
    return [{
        "description": f"Sample description {i+1}" if random.choice([True, False]) else None,
        "direction": random.choice(["down", "none", "up", "upAndDown"]) if random.choice([True, False]) else None,
        "mrid": str(uuid.uuid4()),
        "name": f"Sample name {i+1}" if random.choice([True, False]) else None,
        "propertyRangeType": random.choice(["intertemporal", "static"]),
        "propertyReference": str(uuid.uuid4()) if random.choice([True, False]) else None,
        "value": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "valueKind": random.choice(["absolute", "incremental", "incrementalPercentage"]) if random.choice([True, False]) else None
    } for i in range(random.randint(1, 3))]

def generate_power_bid_schedule_list(schema):
    if random.choice([True, False]):
        return None
    return [{
        "currency": random.choice(["USD", "EUR", "GBP"]) if random.choice([True, False]) else None,
        "description": f"Sample description {i+1}" if random.choice([True, False]) else None,
        "direction": random.choice(["down", "none", "up", "upAndDown"]) if random.choice([True, False]) else None,
        "glskBidActionDistributionList": generate_glsk_bid_action_distribution_list(schema),
        "interpolationKind": random.choice(["linear", "next", "none"]),
        "isOffer": random.choice([True, False]),
        "leadTime": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "maximumUpTime": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "minimumActivationP": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "minimumOffTime": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "minimumUpTime": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "mrid": str(uuid.uuid4()),
        "name": f"Sample name {i+1}" if random.choice([True, False]) else None,
        "p": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "powerBidDependencyList": generate_power_bid_dependency_list(schema),
        "powerRemedialActionMrid": str(uuid.uuid4()),
        "price": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "priority": random.randint(1, 10) if random.choice([True, False]) else None,
        "reservePrice": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "shutdownCost": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "startUpCost": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "stepIncrementP": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "totalMaximumEnergy": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "totalMinimumEnergy": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None
    } for i in range(random.randint(1, 3))]

def generate_glsk_bid_action_distribution_list(schema):
    if random.choice([True, False]):
        return None
    return [{
        "description": f"Sample description {i+1}" if random.choice([True, False]) else None,
        "energyBlockOrderMrid": str(uuid.uuid4()) if random.choice([True, False]) else None,
        "energyConsumerMrid": str(uuid.uuid4()) if random.choice([True, False]) else None,
        "energyGroupMrid": str(uuid.uuid4()) if random.choice([True, False]) else None,
        "generatingUnitMrid": str(uuid.uuid4()) if random.choice([True, False]) else None,
        "glskScheduleMrid": str(uuid.uuid4()),
        "hydroPumpMrid": str(uuid.uuid4()) if random.choice([True, False]) else None,
        "mrid": str(uuid.uuid4()),
        "name": f"Sample name {i+1}" if random.choice([True, False]) else None,
        "participationFactor": round(random.uniform(0, 100), 2),
        "powerElectronicsUnitMrid": str(uuid.uuid4()) if random.choice([True, False]) else None,
        "scheduleResourceMrid": str(uuid.uuid4()) if random.choice([True, False]) else None
    } for i in range(random.randint(1, 3))]

def generate_power_bid_dependency_list(schema):
    if random.choice([True, False]):
        return None
    return [{
        "delay": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "dependentPowerGridScheduleMrid": str(uuid.uuid4()),
        "kind": random.choice(["exclusive", "inclusive", "restrictive"]),
        "mrid": str(uuid.uuid4())
    } for i in range(random.randint(1, 3))]

def generate_power_remedial_action_list(schema):
    if random.choice([True, False]):
        return None
    return [{
        "available": random.choice([True, False]),
        "biddingZoneCode": str(uuid.uuid4()),
        "description": f"Sample description {i+1}" if random.choice([True, False]) else None,
        "glskStrategy": random.choice(["explicitInstruction", "explicitSchedule", "generatorFlat", "generatorPmax", "loadFlat", "proportionalForGenerator", "proportionalForGeneratorAndLoad", "proportionalForLoad", "proportionalForRemainingCapacity"]) if random.choice([True, False]) else None,
        "impactThresholdMargin": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "isCrossBorderRelevant": random.choice([True, False]),
        "isManual": random.choice([True, False]),
        "kind": random.choice(["curative", "preventive"]),
        "maxEconomicP": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "maxRegulatingDown": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "maxRegulatingUp": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "minEconomicP": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "mrid": str(uuid.uuid4()),
        "name": f"Sample name {i+1}" if random.choice([True, False]) else None,
        "penaltyFactor": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "powerRemedialActionType": random.choice(["countertrade", "redispatch"]),
        "regionCode": str(uuid.uuid4()),
        "shiftMethod": random.choice(["priority", "shared"]) if random.choice([True, False]) else None,
        "systemOperatorCode": str(uuid.uuid4()) if random.choice([True, False]) else None,
        "timeToImplement": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None
    } for i in range(random.randint(1, 3))]

def generate_power_shift_key_distribution_list(schema):
    if random.choice([True, False]):
        return None
    return [{
        "description": f"Sample description {i+1}" if random.choice([True, False]) else None,
        "mrid": str(uuid.uuid4()),
        "name": f"Sample name {i+1}" if random.choice([True, False]) else None,
        "powerBidScheduleMrid": str(uuid.uuid4()),
        "resourceMrid": str(uuid.uuid4())
    } for i in range(random.randint(1, 3))]

def generate_power_shift_key_list(schema):
    if random.choice([True, False]):
        return None
    return [{
        "areaCode": str(uuid.uuid4()) if random.choice([True, False]) else None,
        "blockType": random.choice(["consumptionsFlat", "consumptionsP", "explicitDistribution", "explicitInstruction", "generatorsAndConsumptionsP", "generatorsFlat", "generatorsP", "generatorsPmax", "generatorsPmin", "generatorsPriority", "generatorsRemainingCapacity", "generatorsUsedCapacity", "nonConformLoadP", "storageFlat", "storageP"]),
        "energyGroupMrid": str(uuid.uuid4()) if random.choice([True, False]) else None,
        "resourceMrid": str(uuid.uuid4()) if random.choice([True, False]) else None,
        "resourceType": random.choice(["energyConsumer", "energyGroup", "generatingUnit", "hydroPump", "powerElectronicsUnit"]) if random.choice([True, False]) else None,
        "value": generate_power_shift_key_value(schema)
    } for i in range(random.randint(1, 3))]

def generate_power_shift_key_value(schema):
    return {
        "activePowerMax": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "activePowerMin": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "blockOrder": random.randint(1, 10) if random.choice([True, False]) else None,
        "participationFactor": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "shiftDirection": random.choice(["down", "up", "upAndDown"]) if random.choice([True, False]) else None
    }

def generate_remedial_action_group_list(schema):
    if random.choice([True, False]):
        return None
    return [{
        "description": f"Sample description {i+1}" if random.choice([True, False]) else None,
        "maxRegulatingDown": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "maxRegulatingUp": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "mrid": str(uuid.uuid4()),
        "name": f"Sample name {i+1}" if random.choice([True, False]) else None,
        "remedialActionDependencyList": generate_remedial_action_dependency_list(schema)
    } for i in range(random.randint(1, 3))]

def generate_remedial_action_dependency_list(schema):
    if random.choice([True, False]):
        return None
    return [{
        "enabled": random.choice([True, False]),
        "kind": random.choice(["exclusive", "inclusive", "none", "restrictive"]),
        "mrid": str(uuid.uuid4()),
        "remedialActionMrid": str(uuid.uuid4())
    } for i in range(random.randint(1, 3))]

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
    num_samples=10
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
baseFileName = "RA_FlatList_fixed"
schema_file_path = os.path.join('ra_flat_list', 'schema', 'RA_FlatList_fixed.json')

# Path to the output directory (2 levels down)
output_dir = os.path.join('ra_flat_list', 'RA_FlatList_fixed_sample_data')

# Path to the TSO EIC codes CSV file
tso_eic_csv_path = os.path.join('csv_files', 'Mapping_TSO_Bidding_Zone_EIC.csv')

# Load TSO EIC codes and corresponding Area Codes from the CSV file
tso_eic_to_area_code = load_tso_eic_and_area_codes(tso_eic_csv_path)

# Generate sample data files
output_file_prefix = f'{baseFileName}_file'
generate_sample_data_files(schema_file_path, output_dir, output_file_prefix, tso_eic_to_area_code)












































# import json
# import secrets
# import random
# from datetime import datetime, timedelta
# from random import choice
# import uuid
# # from faker import Faker
# import os
# import pandas as pd
# import re

# # fake = Faker()

# directory = '.'  # The directory where the file is located
# filename = 'Bidding_zone_EIC_code.csv'
# filename2 = 'TSO_EIC_CODE.csv'

# # Enum values for ValueFlowComponentType
# ValueFlowComponentType = [
#     "allocatedFlow",
#     "internalFlow",
#     "loopFlow",
#     "loopFlowOutsideCore",
#     "pstFlow"
# ]


# # Helper function to generate a random value
# def get_random_value():
#     return round(random.uniform(0, 1), 2)

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

# def getBiddingZoneCode():
#     return extract_bidding_zone_codes(directory, filename, 'Bidding Area EIC Code')
#     # return random.choice(bidding_zones)

# def generateBiddingZoneCode():
#     bidding_zones = extract_bidding_zone_codes(directory, filename, 'Bidding Area EIC Code')
#     return random.choice(bidding_zones)

# def generateTsoEicCodes():
#     tso_eic_codes = extract_bidding_zone_codes(directory, filename2, 'TS0 EIC code')
#     return random.choice(tso_eic_codes)

# # Generate biddingZoneList with random values
# def generate_bidding_zone_list(size):
#     bidding_zone_list = []
#     for _ in range(size):
#         bidding_zone_list.append({
#             "biddingZoneCode": generateBiddingZoneCode(),
#             "value": get_random_value()
#         })
#     return bidding_zone_list

# # Calculate the sum of values in biddingZoneList
# def calculate_sum(bidding_zone_list):
#     return round(sum(zone["value"] for zone in bidding_zone_list), 2)

# # get percentage of a value
# def calculate_percentage(value, total):
#     """
#     Calculate the percentage of a value with respect to a total.

#     :param value: The part value
#     :param total: The total value
#     :return: Percentage as a float
#     """
#     if total == 0:
#         raise ValueError("Total cannot be zero.")
#     return (value * total) / 100

# # Function to generate component flows
# def generate_component_flows(bidding_zone_list):
#     component_flows = []
#     sum_value = abs(calculate_sum(bidding_zone_list))  # Calculate sum once for loopFlow

#     for component_type in ValueFlowComponentType:
#         # value = sum_value  # Use sum for loopFlow
#         # bidding_zone_list_copy = bidding_zone_list  # Use original biddingZoneList
#         if component_type == "loopFlow":
#             # value = sum_value  # Use sum for loopFlow
#             value = max(sum_value, 0)  # Ensure value is non-negative
#             bidding_zone_list_copy = bidding_zone_list  # Use original biddingZoneList
        
#         # THIS ELSE PORTION MAKES SURE THAT WE SUM UP EACH bidding_zone IN THE LIST AND GIVE THE SUM AS A FLOW TYPE VALUE FOR ALL NON LOOPFLOW 
#         else:
#             # For other types, create a distinct value
#             offset = round(random.uniform(0.1, 0.5), 2)  # Random offset for uniqueness
#             value = round(sum_value + offset, 2)  # Apply offset to the sum
#             value = max(value, 0)  # Ensure value is non-negative
            
#             # Create a new biddingZoneList that sums to the same total
#             bidding_zone_list_copy = []
#             total_adjusted = 0  # To keep track of the adjusted total
            
#             for zone in bidding_zone_list:
#                 # Generate a unique random value for each zone
#                 unique_value = round(abs(zone["value"] + random.uniform(0.01, 0.1)), 2)
#                 bidding_zone_list_copy.append({
#                     "biddingZoneCode": zone["biddingZoneCode"],
#                     "value": unique_value
#                 })
#                 total_adjusted += unique_value

#             # Adjust the last zone's value to ensure the sum remains the same
#             last_zone_value = round(value - (total_adjusted - bidding_zone_list_copy[-1]["value"]), 2)
#             last_zone_value = max(last_zone_value, 0)  # Ensure last_zone_value is non-negative
#             bidding_zone_list_copy[-1]["value"] = last_zone_value

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

#     precision = 3

#     total_flow = round(sum(obj["value"] for obj in component_list), precision)
#     # total_flow = sum(obj["value"] for obj in component_list)

#     return {
#         "adjustedFmax": calculate_percentage(25, total_flow), # total_flow - 3, # round(random.uniform(150, 200), 2),
#         "componentList": component_list,
#         "convertedXnecId": str(uuid.uuid4()),
#         "totalFlow": total_flow, # round(random.uniform(0, 100), 2)
#     }

# def generate_comp_list():
#     bidding_zone_list = generate_bidding_zone_list(size=random.randint(2, 5))
#     return generate_component_flows(bidding_zone_list)

# # Helper functions to generate sample data for each property
# def generate_business_day(start_date, offset_days):
#     business_day = start_date + timedelta(days=offset_days)
#     return business_day.strftime("%Y-%m-%d")

# def generate_business_timestamp(business_day):
#     random_hour = random.randint(0, 23)
#     random_minute = random.randint(0, 59)
#     random_second = random.randint(0, 59)
#     return f"{business_day}T{random_hour:02}:{random_minute:02}:{random_second:02}Z"

# def generate_crosa_version():
#     # return random.randint(1, 5)
#     return random.randint(1, 1)

# def generate_tso_code():
#     # return random.choice(["dayAhead", "weekAhead", "monthAhead", "Intraday"])
#     return random.choice(["CEPS", "APG", "PSE", "MAVIR", "Transelectrica"]),

# def generate_cs_process_version():
#     return random.randint(1, 5)
#     # return random.randint(1, 1)

# def generate_flow_decomposition_id():
#     return secrets.token_hex(12)

# def generate_id():
#     return secrets.token_hex(12)

# def generate_mapping_result_id():
#     return secrets.token_hex(12)

# def generate_selected_xnec_result_id():
#     return secrets.token_hex(12)

# def generate_time_horizon():
#     # return random.choice(["dayAhead", "weekAhead", "monthAhead", "Intraday"])
#     return random.choice(["dayAhead"])



# def generate_flow_component_list():
#     return [generate_flow_component() for _ in range(random.randint(1, 3))]

# def generate_flow_component():
#     return {
#         "appliedThresholdList": generate_applied_threshold_list(),
#         "burdeningFlow": random.uniform(200, 500),
#         "commonThreshold": random.uniform(0, 100),
#         "contribution": random.uniform(0, 1),
#         "stackingOrder": random.randint(1, 10),
#         "type": random.choice(["allocatedFlow", "internalFlow", "loopFlow", "loopFlowOutsideCore", "pstFlow"])
#     }

# def generate_applied_threshold_list():
#     if random.choice([True, False]):
#         return []
#     return [generate_applied_threshold() for _ in range(random.randint(1, 5))]

# def generate_applied_threshold():
#     return {
#         # "biddingZoneCode": random.choice(["EIC_DE", "EIC_SI", "EIC_PL", "EIC_SK", "EIC_RO"]),
#         "biddingZoneCode": random.choice([generateBiddingZoneCode()]),
#         "burdeningFlow": random.uniform(0, 100),
#         "flowAboveThreshold": random.uniform(0, 100),
#         "flowBelowThreshold": random.uniform(0, 100),
#         "individualThreshold": random.uniform(10, 20)
#     }

# def generate_tso_cost_list():
#     return [generate_tso_cost() for _ in range(random.randint(1, 3))]

# def generate_tso_cost():
#     return {
#         "contribution": random.uniform(0, 1),
#         "cost": random.uniform(20000, 50000),
#         "tsoCode": generateTsoEicCodes (),
#         # "tsoCode": random.choice(["CEPS", "APG", "PSE", "MAVIR", "Transelectrica"]),
#         "tsoShare": random.uniform(0, 1)
#     }

# def generate_volume_overload():
#     return random.uniform(200, 300)


# def generate_bidding_zone_cost_list():
#     # bidding_zones = ["EIC_DE", "EIC_SI", "EIC_NL", "EIC_FR", "EIC_PL", "EIC_SK", "EIC_RO"]
#     bidding_zones = random.sample(getBiddingZoneCode (), 5)

#     cost_list = []
#     # for _ in range(random.randint(1, 3)):
#     for zone in bidding_zones:
#         item = {
#             # "biddingZoneCode": generateBiddingZoneCode(),
#             "biddingZoneCode": zone,
#             "contribution": random.uniform(0, 1),
#             "cost": random.uniform(0, 25000)
#         }
#         cost_list.append(item)
#     return cost_list

# def generate_xnec_cost():
#     bidding_zone_cost_list = generate_bidding_zone_cost_list()

#     total_cost = sum(item["cost"] for item in bidding_zone_cost_list)
#     return {
#         "biddingZoneCostList": bidding_zone_cost_list,
#         # "convertedXnecId": f"ID{random.randint(1, 100)}",
#         "convertedXnecId": str(uuid.uuid4()),
#         "cost": total_cost,
#         "flowComponentList": generate_flow_component_list(),
#         "tsoCostList": generate_tso_cost_list(),
#         "volumeOverload": generate_volume_overload()
#     }

# cumulative_costs_ora = 0
# cumulative_costs_pst = 0

# def generate_string_off_dat ():
#     # Generate a random date within the past year
#     start = datetime.now() - timedelta(days=365)  # One year ago from today
#     end = datetime.now()
#     random_date = start + (end - start) * random.random()

#     # Randomly choose either 01:30 or 02:30 for the time
#     hour = random.choice([1, 2])
#     random_date = random_date.replace(hour=hour, minute=30, second=0, microsecond=0)

#     # Format the date and timestamp
#     business_day = random_date.strftime('%Y-%m-%d')
#     # business_timestamp = random_date.isoformat()
#     business_timestamp = random_date.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'  # Add 'Z' for UTC

#     # Step 1: Extract the date part and remove hyphens
#     date_part = business_timestamp.split("T")[0].replace("-", "")

#     # Step 2: Define the static middle part
#     middle_part = "_DA_CROSA_ORA_"

#     # Step 3: Generate a random 4-digit number
#     random_value = random.randint(1000, 9999)  # Random 4-digit number

#     # Construct the final string
#     final_string = f"{date_part}{middle_part}{random_value}"  # Pad with zeros to make it 4 digits
#     return final_string

# def generate_ra_data(final_string):
#     # Generate a random positive real number
#     return {
#         "costsOra": round(random.uniform(150, 200), 2),
#         "costsOraVariable": round(random.uniform(150, 200), 2),
#         "hourlyCostsAfterFixedCosts": round(random.uniform(150, 200), 2),
#         "hourlyCostsAfterReallocation": round(random.uniform(150, 200), 2),
#         "hourlyCostsFiltered": round(random.uniform(0, 100), 2),
#         "raId": final_string, # str(uuid.uuid4()),
#         "variableCostFinal": round(random.uniform(150, 200), 2),
#         "variableCostIntermediate": round(random.uniform(150, 200), 2)
#     }

# def generate_pst_data():
#     # Generate a random positive real number
#     return {
#         "costsPst": round(random.uniform(150, 200), 2),
#         "pstId": str(uuid.uuid4()),
#         "tapAfter": round(random.uniform(0, 100), 2),
#         "tapBefore": round(random.uniform(150, 200), 2)
#     }

# # Function to generate an array of random objects and calculate cumulative costsOra
# def generate_random_objects_and_cumulative_ra_cost(final_string):
#     # Generate a random number of objects between 1 and 5
#     num_objects = random.randint(1, 5)
    
#     # Generate the array of objects
#     raData = [generate_ra_data(final_string) for _ in range(num_objects)]
    
#     # Calculate the cumulative value of costsOra
#     cumulative_costs_ora = sum(obj["costsOra"] for obj in raData)
    
#     return {
#         "raData": raData, 
#         "cumulative_costs_ora": cumulative_costs_ora
#     }

# # Function to generate an array of random objects and calculate cumulative costsOra
# def generate_random_objects_and_cumulative_pst_cost():
#     # Generate a random number of objects between 1 and 5
#     num_objects = random.randint(1, 5)
    
#     # Generate the array of objects
#     raData = [generate_pst_data() for _ in range(num_objects)]

#     # Calculate the cumulative value of costsOra
#     cumulative_costs_pst = sum(obj["costsPst"] for obj in raData)

#     return {
#         "pstData": raData, 
#         "cumulative_costs_pst": cumulative_costs_pst
#     }

# def basic_psdf_data ():
#     # Generate a random positive real number
#     positive_real = abs(random.random() * random.randint(1, 10_000))
#     precision = 3
#     random_decimal = round(positive_real, precision)
#     return {
#         "convertedXnecId": str(uuid.uuid4()),
#         "pstId": generate_string_off_dat (), #str(uuid.uuid4()),
#         "sensitivity": random_decimal,
#     }

# def generate_psdf_data(final_string):
#     num_objects = random.randint(1, 5)
#     # Generate a random positive real number
#     psdf_data = [basic_psdf_data() for _ in range(num_objects)]
#     return psdf_data

# def basic_ptdf_data ():
#     # Generate a random positive real number
#     # Generate a random decimal between 0 and 1 (3 decimal)
#     random_decimal = random.uniform(0, 1)

#     # Specify the number of decimal places (e.g., 2 decimal places)
#     precision = 3
#     random_decimal = round(random_decimal, precision)
#     return {
#         "convertedXnecId": str(uuid.uuid4()),
#         "raId": generate_string_off_dat (),
#         "sensitivity": random_decimal,
#     }

# def generate_ptdf_data(final_string):
#     num_objects = random.randint(1, 5)
#     # Generate a random positive real number
#     psdf_data = [basic_ptdf_data() for _ in range(num_objects)]
#     return psdf_data


# def generate_xnec_cost_list():
#     return [generate_xnec_cost() for _ in range(random.randint(1, 5))]



# def resolve_ref(schema, ref):
#     """Resolve a $ref within the schema."""
#     parts = ref.lstrip('#/').split('/')
#     ref_obj = schema
#     for part in parts:
#         ref_obj = ref_obj.get(part)
#         if ref_obj is None:
#             return None
#     return ref_obj

# pattern = r'^(xnec.*Id|.*xnecId)$'
# patternXra = r'^(xra.*Id|.*xraId)$'
# offset_days = ""
# start_date = datetime(2024, 1, 1)



# def resolve_reference(schema, ref):
#     """Resolve a reference within the JSON schema."""
#     ref_path = ref.replace("#/", "").split("/")
#     ref_schema = schema
#     for part in ref_path:
#         ref_schema = ref_schema.get(part, {})
#     return ref_schema


# # GENERATE SAMPLE DATA
# def generate_sample_data(schema, root_schema):
#     """Generate sample data based on the provided JSON schema."""
#     start = datetime.now() - timedelta(days=365)  # One year ago from today
#     end = datetime.now()
#     random_date = start + (end - start) * random.random()

#     # Randomly choose either 01:30 or 02:30 for the time
#     hour = random.choice([1, 2])
#     random_date = random_date.replace(hour=hour, minute=30, second=0, microsecond=0)

#     # Format the date and timestamp
#     business_day = random_date.strftime('%Y-%m-%d')

#     # Detect and handle `oneOf` property
#     if 'oneOf' in schema:
#         # Randomly select one of the schemas from `oneOf`
#         chosen_schema = random.choice(schema['oneOf'])
#         return generate_sample_data(chosen_schema, root_schema)
#         # return generate_sample_data_final(chosen_schema, root_schema, start_date, offset_days)
    
#     # # If neither condition matches, handle as needed (optional)
#     # raise ValueError("Chosen schema does not match expected cases.")

#     # Determine the type of the schema
#     schema_type = schema.get('type')
#     if isinstance(schema_type, list):
#         # If type is an array, handle the types that exist in the array
#         if 'null' in schema_type:
#             # Randomly decide if we should return None (null)
#             if random.choice([True, False]):
#                 return None
#         # Set schema_type to first non-null type
#         schema_type = next(t for t in schema_type if t != 'null')

#     # Check if the schema has a 'const' property and return its value if so
#     if 'const' in schema:
#         return schema['const']

#     # Handle each type accordingly
#     if schema_type == 'string':
#         if 'enum' in schema:
#             return random.choice(schema['enum'])
#         if 'format' in schema and schema['format'] == 'date-time':
#             return business_day
#         return generate_selected_xnec_result_id()

#     elif schema_type == 'integer':
#         return random.randint(1, 100)

#     elif schema_type == 'number':
#         return round(random.uniform(1.0, 100.0), 2)

#     elif schema_type == 'boolean':
#         return random.choice([True, False])

#     elif schema_type == 'array':
#         items_schema = schema.get('items', {})
#         # return [generate_sample_data_final(items_schema, root_schema, start_date, offset_days)]
#         return [generate_sample_data(items_schema, root_schema) for _ in range(random.randint(1, 3))]

#     elif schema_type == 'object':
#         properties = schema.get('properties', {})
#         obj = {}
#         for key, prop_schema in properties.items():
#             if '$ref' in prop_schema:
#                 # Resolve the reference and generate sample for it
#                 resolved_schema = resolve_reference(root_schema, prop_schema['$ref'])
#                 obj[key] = generate_sample_data(resolved_schema, root_schema)
#             else:
#                 obj[key] = generate_sample_data(prop_schema, root_schema)
#         return obj

#     if '$ref' in schema:
#         # Resolve reference and generate sample
#         resolved_schema = resolve_reference(root_schema, schema['$ref'])
#         return generate_sample_data(resolved_schema, root_schema)

#     return None


# def generate_random_number ():
#     return random.randint(1000, 9999)

# xneMrid_assessedElementMrid = ""
# xneName_assessedElementName = ""

# contingencyMrid=""
# contingencyName=""
# hasCostlyRa=""
# raMrid=""
# iBefore=""
# iAfter=""
# iMax=""
# fBefore=""
# fAfter=""
# fMax=""

# def generate_original_xnec1 (contingencyMrid, contingencyName, fAfter, fBefore, fMax, hasCostlyRa, iAfter, iBefore, iMax, raMrid):
#     xneMrid_assessedElementMrid = generate_selected_xnec_result_id ()
#     xneName_assessedElementName = generate_selected_xnec_result_id ()

#     zone_code_tso_code = generateBiddingZoneCode()

#     return {
#         "assessedElementMrid": xneMrid_assessedElementMrid,
#         "assessedElementName": xneName_assessedElementName,
#         "biddingZoneCode": zone_code_tso_code,
#         "conductingEquipmentMrid": secrets.token_hex(12), 
#         "contingencyMrid": contingencyMrid, #
#         "contingencyName": contingencyName, #
#         "fAfter": fAfter, #
#         "fBefore": fBefore, #
#         "fMax": fMax, #
#         "hasCostlyRa": hasCostlyRa, #
#         "iAfter": iAfter, #
#         "iBefore": iBefore, #
#         "iMax": iMax, #
#         "id": secrets.token_hex(12),
#         "raMrid": raMrid, #
#         # "tsoCode": random.choice(["CEPS", "APG", "PSE", "MAVIR", "Transelectrica"]),
#         "tsoCode": zone_code_tso_code,
#         "xneMrid": xneMrid_assessedElementMrid,
#         "xneName": xneName_assessedElementName
#     }

# def generate_original_xnec2 (contingencyMrid, contingencyName, fAfter, fBefore, fMax, hasCostlyRa, iAfter, iBefore, iMax, raMrid):
#     xneMrid_assessedElementMrid = generate_selected_xnec_result_id ()
#     xneName_assessedElementName = generate_selected_xnec_result_id ()
#     zone_code_tso_code = generateBiddingZoneCode()

#     return {
#         "assessedElementMrid": xneMrid_assessedElementMrid,
#         "assessedElementName": xneName_assessedElementName,
#         "biddingZoneCode": zone_code_tso_code,
#         "conductingEquipmentMrid": secrets.token_hex(12), 
#         "contingencyMrid": contingencyMrid, #
#         "contingencyName": contingencyName, #
#         "fAfter": fAfter, #
#         "fBefore": fBefore, #
#         "fMax": fMax, #
#         "hasCostlyRa": hasCostlyRa, #
#         "iAfter": iAfter, #
#         "iBefore": iBefore, #
#         "iMax": iMax, #
#         "id": secrets.token_hex(12),
#         "raMrid": raMrid, #
#         # "tsoCode": random.choice(["CEPS", "APG", "PSE", "MAVIR", "Transelectrica"]),
#         "tsoCode": zone_code_tso_code,
#         "xneMrid": xneMrid_assessedElementMrid,
#         "xneName": xneName_assessedElementName
#     }


# # ===============================================
# # Function to generate a timestamp starting from 2024-03-03T01:30:00Z and incrementing by 1 hour
# def generate_timestamp(base_time, offset):
#     return (base_time + timedelta(hours=offset)).strftime("%Y-%m-%dT%H:%M:%SZ")

# # Generate dataPerXnec
# def generate_data_per_xnec(timestamp):
#     xnec_id = str(uuid.uuid4())
#     return {
#         "deltaMinus": round(random.uniform(0, 100), 2),
#         "deltaPlus": round(random.uniform(0, 100), 2),
#         "fAfterRao": round(random.uniform(2000, 3000), 2),
#         "fLimit": round(random.uniform(2000, 3000), 2),
#         "fMax": round(random.uniform(500, 1000), 2),
#         "leastCostWeightRi": round(random.uniform(0, 2), 2),
#         "lowerBalancingDualValue": round(random.uniform(0, 50), 2),
#         "lowerBalancingSlack": round(random.uniform(0, 50), 2),
#         "powerFlowDualValue": round(random.uniform(0, 20), 2),
#         "powerFlowSlack": round(random.uniform(0, 20), 2),
#         "relativeCostWeightAfterRba": round(random.uniform(0, 2), 2),
#         "relativeCostWeightBeforeRba": round(random.uniform(0, 2), 2),
#         "selectedXnecResultId": str(uuid.uuid4()),
#         "shareOfTotalCosts": round(random.uniform(4000, 5000), 2),
#         "sumDeltaMinus": round(random.uniform(4000, 5000), 2),
#         "sumDeltaPlus": round(random.uniform(4000, 5000), 2),
#         "timestamp": timestamp,
#         "totalAdjustedFlow": round(random.uniform(200, 400), 2),
#         "upperBalancingDualValue": round(random.uniform(50, 100), 2),
#         "upperBalancingSlack": round(random.uniform(50, 100), 2),
#         "xnecId": xnec_id
#     }

# # Generate dataPerXra
# def generate_data_per_xra(timestamp):
#     xra_id = str(uuid.uuid4())
#     return {
#         "orderedVolume": round(random.uniform(0, 100), 2),
#         "sumAlphaOrBetaOverXnecs": round(random.uniform(0, 100), 2),
#         "timestamp": timestamp,
#         "totalCost": round(random.uniform(0, 100), 2),
#         "xraId": xra_id
#     }

# def generate_data_per_xnec_and_xra(xnec_id, xra_id, timestamp, value_type, value):

#     return {
#         "timestamp": timestamp,  # Same timestamp for all entries
#         "value": value,
#         "valueType": value_type,
#         "xnecId": xnec_id,
#         "xraId": xra_id
#     }

# def generate_sample_data_final(schema, full_schema, start_date, offset_days):

#     # Generate a random date within the past year
#     start = datetime.now() - timedelta(days=365)  # One year ago from today
#     end = datetime.now()
#     random_date = start + (end - start) * random.random()

#     # Randomly choose either 01:30 or 02:30 for the time
#     hour = random.choice([1, 2])
#     random_date = random_date.replace(hour=hour, minute=30, second=0, microsecond=0)

#     # Format the date and timestamp
#     business_day = random_date.strftime('%Y-%m-%d')
#     business_timestamp = random_date.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'  # Add 'Z' for UTC

#     # Step 1: Extract the date part and remove hyphens
#     date_part = business_timestamp.split("T")[0].replace("-", "")

#     # Step 2: Define the static middle part
#     middle_part = "_DA_CROSA_ORA_"

#     obj = {}

#     # Generate dataPerXnec, dataPerXra, and dataPerXnecAndXra ONLY if they exist in the schema
#     if 'properties' in schema:
#         if 'dataPerXnec' in schema['properties']:
#             base_time = datetime.strptime(business_timestamp, '%Y-%m-%dT%H:%M:%SZ')
#             num_xnec = random.randint(3, 5)  # Randomly generate between 3 to 5 dataPerXnec
#             data_per_xnec = [generate_data_per_xnec(generate_timestamp(base_time, i)) for i in range(num_xnec)]
#             obj["dataPerXnec"] = data_per_xnec
#         else:
#             data_per_xnec = []

#         if 'dataPerXra' in schema['properties']:
#             base_time = datetime.strptime(business_timestamp, '%Y-%m-%dT%H:%M:%SZ')
#             num_xra = random.randint(3, 5)  # Randomly generate between 3 to 5 dataPerXra
#             # Ensure num_xra is always less than or equal to num_xnec
#             if 'dataPerXnec' in obj:
#                 num_xra = min(num_xra, len(obj["dataPerXnec"]))
#             data_per_xra = [generate_data_per_xra(generate_timestamp(base_time, i)) for i in range(num_xra)]
#             obj["dataPerXra"] = data_per_xra
#         else:
#             data_per_xra = []

#         if 'dataPerXnecAndXra' in schema['properties']:
#             if data_per_xnec and data_per_xra:  # Ensure dataPerXnec and dataPerXra are generated first
#                 xnec_ids = [xnec["xnecId"] for xnec in data_per_xnec]
#                 xra_ids = [xra["xraId"] for xra in data_per_xra]

#                 data_per_xnec_and_xra = []
#                 min_length = min(len(xnec_ids), len(xra_ids))

#                 # Generate pairs for matching timestamps
#                 for i in range(min_length):
#                     timestamp = generate_timestamp(base_time, i)
#                     xnec_id = xnec_ids[i]
#                     xra_id = xra_ids[i]

#                     # Generate sensitivity value (random between -1 and 1)
#                     sensitivity_value = round(random.uniform(-1, 1), 2)
#                     data_per_xnec_and_xra.append(generate_data_per_xnec_and_xra(
#                         xnec_id, xra_id, timestamp, "sensitivity", sensitivity_value
#                     ))

#                     # Generate optimizationVariable value (random between 0 and 100)
#                     optimization_value = round(random.uniform(0, 100), 2)
#                     data_per_xnec_and_xra.append(generate_data_per_xnec_and_xra(
#                         xnec_id, xra_id, timestamp, "optimizationVariable", optimization_value
#                     ))

#                 obj["dataPerXnecAndXra"] = data_per_xnec_and_xra

#     if 'const' in schema:
#         return schema['const']

#     for prop, prop_schema in schema.get('properties', {}).items():
#         # Check if the property has an enum and select a random value from it
#         if prop in ["dataPerXnec", "dataPerXra", "dataPerXnecAndXra"]:
#             continue  # Skip, as we've already handled these
#         else: 
#             if 'const' in prop_schema:
#                 obj[prop] = prop_schema['const']
#             if 'enum' in prop_schema:
#                 obj[prop] = random.choice(prop_schema['enum'])
#             elif re.search(r'businessDay', prop, re.IGNORECASE):
#                 # obj[prop] = generate_business_day(start_date, offset_days)
#                 obj[prop] = business_day
#             elif re.search(r'businessTimestamp', prop, re.IGNORECASE):
#                 # obj[prop] = generate_business_timestamp(obj.get('businessDay'))
#                 obj[prop] = business_timestamp
#             elif re.search(r'crosaVersion', prop, re.IGNORECASE):
#                 obj[prop] = generate_crosa_version()
#             elif re.search(r'csProcessVersion', prop, re.IGNORECASE):
#                 obj[prop] = generate_cs_process_version()
#             elif re.search(r'flowDecompositionId', prop, re.IGNORECASE):
#                 obj[prop] = generate_flow_decomposition_id()
#             elif re.search(r'^id$', prop, re.IGNORECASE):
#                 obj[prop] = generate_id()
#             elif re.search(r'timestamp', prop, re.IGNORECASE):
#                 obj[prop] = business_timestamp
#             elif re.search(r'mappingResultId', prop, re.IGNORECASE):
#                 obj[prop] = generate_mapping_result_id()
#             elif re.search(r'selectedXnecResultId', prop, re.IGNORECASE):
#                 obj[prop] = generate_selected_xnec_result_id()
#             elif re.search(r'timeHorizon', prop, re.IGNORECASE):
#                 obj[prop] = generate_time_horizon()
#             elif re.search(pattern, prop, re.IGNORECASE):
#                 obj[prop] = generate_selected_xnec_result_id()
#             elif prop == "biddingZoneCode":
#                 obj[prop] = generateBiddingZoneCode()
#             # elif prop == "componentList":
#             #     obj[prop] = generate_comp_list()
#             elif re.search(r'xnecList', prop, re.IGNORECASE):
#                 obj[prop] = generate_xnec_flow_component ()
#             elif re.search(patternXra, prop, re.IGNORECASE):
#                 obj[prop] = generate_selected_xnec_result_id()
#             elif re.search(r'xnecCostList', prop, re.IGNORECASE):
#                 obj[prop] = generate_xnec_cost_list()
#             elif re.search(r'tsoCode', prop, re.IGNORECASE):
#                 obj[prop] = random.choice(["CEPS", "APG", "PSE", "MAVIR", "Transelectrica"])
#             elif re.search(r'convertedXnecId', prop, re.IGNORECASE):
#                 obj[prop] = generate_selected_xnec_result_id()
#             elif re.search(r'ptdfData', prop, re.IGNORECASE):
#                 obj[prop] = generate_ptdf_data (f"{date_part}{middle_part}{generate_random_number ()}")
#             elif re.search(r'psdfData', prop, re.IGNORECASE):
#                 obj[prop] = generate_psdf_data (f"{date_part}{middle_part}{generate_random_number ()}")
#             elif re.search(r'raData', prop, re.IGNORECASE):
#                 result = generate_random_objects_and_cumulative_ra_cost (f"{date_part}{middle_part}{generate_random_number ()}")
#                 cumulative_costs_ora = result ["cumulative_costs_ora"]
#                 obj[prop] = result ["raData"]
#             elif re.search(r'pstData', prop, re.IGNORECASE):
#                 result = generate_random_objects_and_cumulative_pst_cost ()
#                 cumulative_costs_pst = result ["cumulative_costs_pst"]
#                 obj[prop] = result ["pstData"]
#             # elif re.search(r'totalCostsAllOras', prop, re.IGNORECASE):
#             #     obj[prop] = cumulative_costs_ora
#             elif re.search(r'totalCostsAllPsts', prop, re.IGNORECASE):
#                 obj[prop] = cumulative_costs_pst
#             elif re.search(r'assessedElementMrid', prop, re.IGNORECASE):
#                 xneMrid_assessedElementMrid = generate_selected_xnec_result_id ()
#                 obj[prop] = xneMrid_assessedElementMrid
#             elif re.search(r'xneMrid', prop, re.IGNORECASE):
#                 obj[prop] = xneMrid_assessedElementMrid
#             elif re.search(r'assessedElementName', prop, re.IGNORECASE):
#                 xneName_assessedElementName = generate_selected_xnec_result_id ()
#                 obj[prop] = xneName_assessedElementName
#             elif re.search(r'xneName', prop, re.IGNORECASE):
#                 obj[prop] = xneName_assessedElementName
#             elif re.search(r'originalXnec1', prop, re.IGNORECASE):
#                 hasCostlyRa = random.choice([True, False])
#                 generate_number = random.randint(1, 100)
#                 contingencyMrid = secrets.token_hex(12)
#                 contingencyName = secrets.token_hex(12)
#                 raMrid = secrets.token_hex(12)
#                 iBefore = random.randint(1, 100)
#                 iAfter = random.randint(1, 100)
#                 iMax = random.randint(1, 100)
#                 fBefore = generate_number
#                 fAfter = generate_number - 6
#                 fMax = generate_number - 2
#                 obj[prop] = generate_original_xnec1 (contingencyMrid, contingencyName, fAfter, fBefore, fMax, hasCostlyRa, iAfter, iBefore, iMax, raMrid)
#             elif re.search(r'originalXnec2', prop, re.IGNORECASE):
#                 obj[prop] = generate_original_xnec2 (contingencyMrid, contingencyName, fAfter, fBefore, fMax, hasCostlyRa, iAfter, iBefore, iMax, raMrid)
#             else:
#                 if '$ref' in prop_schema:
#                     ref_schema = resolve_ref(full_schema, prop_schema['$ref'])
#                     if ref_schema:
#                         obj[prop] = generate_sample_data_final(ref_schema, full_schema, start_date, offset_days)
#                         # obj[prop] = generate_sample_data(ref_schema, full_schema)
#                     else:
#                         obj[prop] = None
#                 elif ('array' in prop_schema.get('type', []) if isinstance(prop_schema.get('type'), list) else prop_schema.get('type') == 'array') and 'items' in prop_schema:
#                     items_schema = prop_schema['items']
#                     if '$ref' in items_schema:
#                         ref_schema = resolve_ref(full_schema, items_schema['$ref'])
#                         if ref_schema:
#                             obj[prop] = [generate_sample_data_final(ref_schema, full_schema, start_date, offset_days)]
#                         else:
#                             obj[prop] = None
#                     else:
#                         obj[prop] = [generate_sample_data_final(items_schema, full_schema, start_date, offset_days)]
#                 else:
#                     obj[prop] = generate_sample_data(prop_schema, full_schema)

#     return obj


# # Main function to load schema, generate data, and write to multiple files
# def generate_sample_data_files(schema_file_path, output_dir, output_file_prefix): 

#     num_samples=10
#     # Load the schema from the file
#     with open(schema_file_path, 'r') as f:
#         schema = json.load(f)

#     # Start date for the first sample
#     start_date = datetime(2024, 1, 1)

#     # Generate and save multiple samples
#     for i in range(num_samples):
#         offset_days = i
#         sample_data = generate_sample_data_final(schema, schema, start_date, i)
#         # output_file_path = f"{output_file_prefix}_{i+1}.json"
#         output_file_path = os.path.join(output_dir, f"{output_file_prefix}_{i+1}.json")
#         with open(output_file_path, 'w') as f:
#             json.dump(sample_data, f, indent=4)

# baseFineName = "CO_Flat_List_Schema_fixed"
# schema_file_path = os.path.join('flat_list', 'schema', 'CO_Flat_List_Schema_fixed.json')

# # Path to the output directory (2 levels down)
# output_dir = os.path.join('flat_list', 'CO_Flat_List_Schema_fixed_sample_data')


# # Flow_Decomposition_Schema_fixed.json
# output_file_prefix = f'{baseFineName}_file'
# generate_sample_data_files(schema_file_path, output_dir, output_file_prefix)






























