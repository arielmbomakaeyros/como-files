import os
import json
import csv
import uuid
from datetime import datetime, timedelta
import random

from utils import generate_range_constraint_list, load_tso_eic_and_area_codes, generate_time_interval, generate_power_shift_key_list, generate_power_shift_key_value, generate_time_interval_and_business_timestamp


# Function to generate sample data based on the schema
def generate_sample_data_final(schema, start_date, offset_days, tso_eic_to_area_code):
    # Randomly select a TSO EIC code and its corresponding Area Code
    owner_code = random.choice(list(tso_eic_to_area_code.keys()))
    area_code = tso_eic_to_area_code[owner_code]

    # Generate time interval and business timestamp
    time_interval, business_timestamp = generate_time_interval_and_business_timestamp(start_date, offset_days)

    remedialActionGroupList = generate_remedial_action_group_list(schema)

    # Accessing the first item
    item_0 = remedialActionGroupList[0]

    # Accessing remedialActionDependencyList
    remedial_action_dependency_list = item_0["remedialActionDependencyList"]

    # Generate a sample JSON object based on the schema
    sample_data = {
        "businessTimestamp": business_timestamp, # (datetime.now() - timedelta(days=offset_days)).isoformat(), # if random.choice([True, False]) else None,
        "documentId": str(uuid.uuid4()),  # Use native UUID
        "ownerCode": owner_code,  # Use the selected TSO EIC code
        "ownerRole": random.choice(["System Operator", "Grid Manager", "Network Engineer"]),  # Random role
        "timeHorizon": random.choice(["dayAhead"]),
        "cdsId": str(uuid.uuid4()),  # Use native UUID
        "comoDocumentType": "INTERNAL_RA_FLAT_LIST",
        "comoDocumentVersion": "R24Q4V1_0",
        "gridModelId": str(uuid.uuid4()),  # Use native UUID
        "remedialActionListId": str(uuid.uuid4()),  # Use native UUID
        "timeInterval": time_interval, # generate_time_interval(start_date, offset_days),
        # "version": random.randint(1, 10),
        "version": random.randint(1, 1),
        "remedialActionGroupList": remedialActionGroupList, #generate_remedial_action_group_list(schema),
        "gridStateAlterationRemedialActionList": generate_grid_state_alteration_remedial_action_list(schema, remedial_action_dependency_list),
        "powerRemedialActionList": generate_power_remedial_action_list(schema),
        "contingencyWithRemedialActionList": generate_contingency_with_remedial_action_list(schema),

        "powerBidScheduleList": generate_power_bid_schedule_list(schema),
        "powerShiftKeyDistributionList": generate_power_shift_key_distribution_list(schema),
        "powerShiftKeyList": generate_power_shift_key_list(schema, area_code),
        # "areaCode": area_code  # Use the corresponding Area Code
        # "timeHorizon": random.choice(["dayAhead", "intraday", "monthAhead", "twoDaysAhead", "weekAhead", "yearAhead"]),
    }
    return sample_data

# Helper functions to generate lists based on the schema
def generate_contingency_with_remedial_action_list(schema):
    # if random.choice([True, False]):
    #     return None
    return [{
        "combinationConstraintKind": random.choice(["considered", "excluded", "included"]),
        "contingencyMrid": str(uuid.uuid4()),
        "enabled": random.choice([True, False]),
        "mrid": str(uuid.uuid4()),
        "remedialActionMrid": str(uuid.uuid4())
    } for _ in range(random.randint(1, 3))]

def generate_grid_state_alteration_remedial_action_list(schema, remedialActionDependencyList):
    # if random.choice([True, False]):
    #     return None
    return [{
        "available": random.choice([True, False]),
        "description": f"Sample description", # if random.choice([True, False]) else None,
        "gridStateAlterationList": generate_grid_state_alteration_list(schema),
        "impactThresholdMargin": round(random.uniform(0, 100), 2), # if random.choice([True, False]) else None,
        "isCrossBorderRelevant": random.choice([True, False]),
        "isManual": random.choice([True, False]),
        "kind": random.choice(["curative", "preventive"]),
        "mrid": remedialActionDep["remedialActionMrid"], # str(uuid.uuid4()),
        "name": f"Sample name", # if random.choice([True, False]) else None,
        "penaltyFactor": round(random.uniform(0, 100), 2), # if random.choice([True, False]) else None,
        "regionCode": str(uuid.uuid4()),
        "systemOperatorCode": str(uuid.uuid4()), # if random.choice([True, False]) else None,
        "timeToImplement": round(random.uniform(0, 100), 2), # if random.choice([True, False]) else None
    } for remedialActionDep in remedialActionDependencyList]
    # for i in range(random.randint(1, 3))

def generate_grid_state_alteration_list(schema):
    # if random.choice([True, False]):
    #     return None
    return [{
        "actionType": random.choice(["acdcConverterAction", "batteryUnitAction", "biddingZoneAction", "controlFunctionBlockAction", "energySourceAction", "equipmentControllerAction", "equivalentInjectionAction", "externalNetworkInjectionAction", "loadAction", "powerElectronicsConnectionAction", "regulatingControlAction", "rotatingMachineAction", "shuntCompensatorAction", "staticVarCompensatorAction", "tapPositionAction", "topologyAction"]),
        "description": f"Sample description {i+1}", # if random.choice([True, False]) else None,
        "enabled": random.choice([True, False]),
        "maximumPerDay": random.randint(1, 24), # if random.choice([True, False]) else None,
        "minimumActivation": round(random.uniform(0, 100), 2), # if random.choice([True, False]) else None,
        "mrid": str(uuid.uuid4()),
        "name": f"Sample name {i+1}", # if random.choice([True, False]) else None,
        "powerSystemResourceMrid": str(uuid.uuid4()),
        "propertyReference": str(uuid.uuid4()),
        "rangeConstraintList": generate_range_constraint_list(),
        "timePerStage": round(random.uniform(0, 100), 2), # if random.choice([True, False]) else None
    } for i in range(random.randint(1, 3))]

def generate_power_bid_schedule_list(schema):
    # if random.choice([True, False]):
    #     return None
    return [{
        "currency": random.choice(["USD", "EUR", "GBP"]), # if random.choice([True, False]) else None,
        "description": f"Sample description {i+1}", # if random.choice([True, False]) else None,
        "direction": random.choice(["down", "none", "up", "upAndDown"]), # if random.choice([True, False]) else None,
        "glskBidActionDistributionList": generate_glsk_bid_action_distribution_list(schema),
        "interpolationKind": random.choice(["linear", "next", "none"]),
        "isOffer": random.choice([True, False]),
        "leadTime": round(random.uniform(0, 100), 2), # if random.choice([True, False]) else None,
        "maximumUpTime": round(random.uniform(0, 100), 2), # if random.choice([True, False]) else None,
        "minimumActivationP": round(random.uniform(0, 100), 2), # if random.choice([True, False]) else None,
        "minimumOffTime": round(random.uniform(0, 100), 2), # if random.choice([True, False]) else None,
        "minimumUpTime": round(random.uniform(0, 100), 2), # if random.choice([True, False]) else None,
        "mrid": str(uuid.uuid4()),
        "name": f"Sample name {i+1}", # if random.choice([True, False]) else None,
        "p": round(random.uniform(0, 100), 2), # if random.choice([True, False]) else None,
        "powerBidDependencyList": generate_power_bid_dependency_list(schema),
        "powerRemedialActionMrid": str(uuid.uuid4()),
        "price": round(random.uniform(0, 100), 2), # if random.choice([True, False]) else None,
        "priority": random.randint(1, 10), # if random.choice([True, False]) else None,
        "reservePrice": round(random.uniform(0, 100), 2), # if random.choice([True, False]) else None,
        "shutdownCost": round(random.uniform(0, 100), 2), # if random.choice([True, False]) else None,
        "startUpCost": round(random.uniform(0, 100), 2), # if random.choice([True, False]) else None,
        "stepIncrementP": round(random.uniform(0, 100), 2), # if random.choice([True, False]) else None,
        "totalMaximumEnergy": round(random.uniform(0, 100), 2), # if random.choice([True, False]) else None,
        "totalMinimumEnergy": round(random.uniform(0, 100), 2), # if random.choice([True, False]) else None
    } for i in range(random.randint(1, 3))]

def generate_glsk_bid_action_distribution_list(schema):
    # if random.choice([True, False]):
    #     return None
    return [{
        "description": f"Sample description {i+1}", # if random.choice([True, False]) else None,
        "energyBlockOrderMrid": str(uuid.uuid4()), # if random.choice([True, False]) else None,
        "energyConsumerMrid": str(uuid.uuid4()), # if random.choice([True, False]) else None,
        "energyGroupMrid": str(uuid.uuid4()), # if random.choice([True, False]) else None,
        "generatingUnitMrid": str(uuid.uuid4()), # if random.choice([True, False]) else None,
        "glskScheduleMrid": str(uuid.uuid4()),
        "hydroPumpMrid": str(uuid.uuid4()), # if random.choice([True, False]) else None,
        "mrid": str(uuid.uuid4()),
        "name": f"Sample name {i+1}", # if random.choice([True, False]) else None,
        "participationFactor": round(random.uniform(0, 100), 2),
        "powerElectronicsUnitMrid": str(uuid.uuid4()), # if random.choice([True, False]) else None,
        "scheduleResourceMrid": str(uuid.uuid4()), # if random.choice([True, False]) else None
    } for i in range(random.randint(1, 3))]

def generate_power_bid_dependency_list(schema):
    # if random.choice([True, False]):
    #     return None
    return [{
        "delay": round(random.uniform(0, 100), 2), # if random.choice([True, False]) else None,
        "dependentPowerGridScheduleMrid": str(uuid.uuid4()),
        "kind": random.choice(["exclusive", "inclusive", "restrictive"]),
        "mrid": str(uuid.uuid4())
    } for i in range(random.randint(1, 3))]

def generate_power_remedial_action_list(schema):
    # if random.choice([True, False]):
    #     return None
    return [{
        "available": random.choice([True, False]),
        "biddingZoneCode": str(uuid.uuid4()),
        "description": f"Sample description {i+1}", # if random.choice([True, False]) else None,
        "glskStrategy": random.choice(["explicitInstruction", "explicitSchedule", "generatorFlat", "generatorPmax", "loadFlat", "proportionalForGenerator", "proportionalForGeneratorAndLoad", "proportionalForLoad", "proportionalForRemainingCapacity"]), # if random.choice([True, False]) else None,
        "impactThresholdMargin": round(random.uniform(0, 100), 2), # if random.choice([True, False]) else None,
        "isCrossBorderRelevant": random.choice([True, False]),
        "isManual": random.choice([True, False]),
        "kind": random.choice(["curative", "preventive"]),
        "maxEconomicP": round(random.uniform(0, 100), 2), # if random.choice([True, False]) else None,
        "maxRegulatingDown": round(random.uniform(0, 100), 2), # if random.choice([True, False]) else None,
        "maxRegulatingUp": round(random.uniform(0, 100), 2), # if random.choice([True, False]) else None,
        "minEconomicP": round(random.uniform(0, 100), 2), # if random.choice([True, False]) else None,
        "mrid": str(uuid.uuid4()),
        "name": f"Sample name {i+1}", # if random.choice([True, False]) else None,
        "penaltyFactor": round(random.uniform(0, 100), 2), # if random.choice([True, False]) else None,
        "powerRemedialActionType": random.choice(["countertrade", "redispatch"]),
        "regionCode": str(uuid.uuid4()),
        "shiftMethod": random.choice(["priority", "shared"]), # if random.choice([True, False]) else None,
        "systemOperatorCode": str(uuid.uuid4()), # if random.choice([True, False]) else None,
        "timeToImplement": round(random.uniform(0, 100), 2), # if random.choice([True, False]) else None
    } for i in range(random.randint(1, 3))]

def generate_power_shift_key_distribution_list(schema):
    # if random.choice([True, False]):
    #     return None
    return [{
        "description": f"Sample description {i+1}", # if random.choice([True, False]) else None,
        "mrid": str(uuid.uuid4()),
        "name": f"Sample name {i+1}", # if random.choice([True, False]) else None,
        "powerBidScheduleMrid": str(uuid.uuid4()),
        "resourceMrid": str(uuid.uuid4())
    } for i in range(random.randint(1, 3))]

def generate_power_shift_key_list(schema, area_code):
    # if random.choice([True, False]):
    #     return None
    return [{
        "areaCode": area_code, # str(uuid.uuid4()), # if random.choice([True, False]) else None,
        "blockType": random.choice(["consumptionsFlat", "consumptionsP", "explicitDistribution", "explicitInstruction", "generatorsAndConsumptionsP", "generatorsFlat", "generatorsP", "generatorsPmax", "generatorsPmin", "generatorsPriority", "generatorsRemainingCapacity", "generatorsUsedCapacity", "nonConformLoadP", "storageFlat", "storageP"]),
        "energyGroupMrid": str(uuid.uuid4()), # if random.choice([True, False]) else None,
        "resourceMrid": str(uuid.uuid4()), # if random.choice([True, False]) else None,
        "resourceType": random.choice(["energyConsumer", "energyGroup", "generatingUnit", "hydroPump", "powerElectronicsUnit"]), # if random.choice([True, False]) else None,
        "value": generate_power_shift_key_value()
    } for i in range(random.randint(1, 3))]

def generate_remedial_action_group_list(schema):
    # if random.choice([True, False]):
    #     return None
    return [{
        "description": f"Sample description {i+1}", # if random.choice([True, False]) else None,
        "maxRegulatingDown": round(random.uniform(0, 100), 2), # if random.choice([True, False]) else None,
        "maxRegulatingUp": round(random.uniform(0, 100), 2), # if random.choice([True, False]) else None,
        "mrid": str(uuid.uuid4()),
        "name": f"Sample name {i+1}", # if random.choice([True, False]) else None,
        "remedialActionDependencyList": generate_remedial_action_dependency_list(schema)
    } for i in range(random.randint(1, 1))]

def generate_remedial_action_dependency_list(schema):
    # if random.choice([True, False]):
    #     return None
    return [{
        "enabled": random.choice([True, False]),
        "kind": random.choice(["exclusive", "inclusive", "none", "restrictive"]),
        "mrid": str(uuid.uuid4()),
        "remedialActionMrid": str(uuid.uuid4())
    } for i in range(random.randint(1, 3))]

# Main function to load schema, generate data, and write to multiple files
def generate_sample_data_files(schema_file_path, output_dir, output_file_prefix, tso_eic_to_area_code):
    num_samples=10
    # Load the schema from the file
    with open(schema_file_path, 'r') as f:
        schema = json.load(f)

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Start date for the first sample
    start_date = datetime(2025, 1, 1)

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












