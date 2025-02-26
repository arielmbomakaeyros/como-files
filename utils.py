import os
import csv
import random
import uuid
from datetime import datetime, timedelta

# Function to load TSO EIC codes and corresponding Area Codes from the CSV file
def load_tso_eic_and_area_codes(csv_file_path):
    tso_eic_to_area_code = {}  # Dictionary to map TSO EIC code to Area Code
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tso_eic_to_area_code[row['TSO EIC code']] = row['Area Code']
    return tso_eic_to_area_code

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

# Helper function to generate a power shift key value
def generate_power_shift_key_value():
    active_power_min = round(random.uniform(0, 100), 2) if random.choice([True, False]) else None
    active_power_max = round(random.uniform(active_power_min + 1, 200), 2) if active_power_min is not None else None

    return {
        "activePowerMax": active_power_max,
        "activePowerMin": active_power_min,
        "blockOrder": random.randint(1, 10) if random.choice([True, False]) else None,
        "participationFactor": round(random.uniform(0, 100), 2) if random.choice([True, False]) else None,
        "shiftDirection": random.choice(["down", "up", "upAndDown"]) if random.choice([True, False]) else None
    }

def generate_range_constraint_list():
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

# Helper function to generate a power shift key list
def generate_power_shift_key_list(area_code):
    if random.choice([True, False]):
        return None
    return [{
        "areaCode": area_code, # str(uuid.uuid4()) if random.choice([True, False]) else None,
        "blockType": random.choice([
            "consumptionsFlat", "consumptionsP", "explicitDistribution", "explicitInstruction",
            "generatorsAndConsumptionsP", "generatorsFlat", "generatorsP", "generatorsPmax",
            "generatorsPmin", "generatorsPriority", "generatorsRemainingCapacity", "generatorsUsedCapacity",
            "nonConformLoadP", "storageFlat", "storageP"
        ]) if random.choice([True, False]) else None,
        "energyGroupMrid": str(uuid.uuid4()) if random.choice([True, False]) else None,
        "resourceMrid": str(uuid.uuid4()) if random.choice([True, False]) else None,
        "resourceType": random.choice([
            "energyConsumer", "energyGroup", "generatingUnit", "hydroPump", "powerElectronicsUnit"
        ]) if random.choice([True, False]) else None,
        "value": generate_power_shift_key_value()
    } for _ in range(random.randint(1, 3))]