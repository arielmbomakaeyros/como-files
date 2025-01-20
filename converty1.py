import json
from datetime import datetime, timedelta
import random
import secrets

# Function to generate timestamp with incrementing hours starting from 00:30
def generate_timestamps(base_date, base_time, count, interval_minutes=60):
    timestamps = []
    for i in range(count):
        timestamp = base_date.replace(hour=base_time.hour, minute=base_time.minute) + timedelta(minutes=30 + i * interval_minutes)
        timestamps.append(timestamp.strftime("%Y-%m-%dT%H:%M:%S") + "Z")
    return timestamps

def generate_time_horizon():
    return random.choice(["dayAhead"])

def generate_crosa_version():
    return random.randint(1, 1)

def generate_selected_xnec_result_id():
    return secrets.token_hex(12)

# Generate sample data function
def generate_sample_data(base_date, base_time, count=1):
    # samples = []

    # for _ in range(count):
    business_day = base_date.strftime("%Y-%m-%d")

    # Randomize array length for each iteration
    array_length = random.randint(3, 10)

    # Generate timestamps for array properties
    timestamps_dataPerHour = generate_timestamps(base_date, base_time, array_length)
    timestamps_dataPerXnec = generate_timestamps(base_date, base_time, array_length)
    timestamps_dataPerXnecAndXra = generate_timestamps(base_date, base_time, array_length)
    timestamps_dataPerXra = generate_timestamps(base_date, base_time, array_length)

    sample = {
        "businessDay": business_day,
        "comoDocumentType": "CS_MAPPING_DETAILED_RESULT",
        "comoDocumentVersion": "R24Q4V1_0",
        "crosaVersion": generate_crosa_version(),
        "csProcessVersion": random.randint(1, 5),
        "timeHorizon": generate_time_horizon(),
        "dataPerHour": [
            {
                "aggregatedVolumeDownwardCostlyAnora": round(random.uniform(1000, 5000), 2),
                "aggregatedVolumeUpwardCostlyAnora": round(random.uniform(1000, 5000), 2),
                "averageCostDownwardOraOrAnora": round(random.uniform(100, 500), 2),
                "averageCostUpwardOraOrAnora": round(random.uniform(100, 500), 2),
                "penaltyCostForAnoraVolumes": round(random.uniform(10, 50), 2),
                "timestamp": timestamps_dataPerHour[i],
                "totalCostsAllOras": round(random.uniform(5000, 15000), 2),
                "totalIndividualShare": round(random.uniform(1000, 5000), 2),
                "totalRelativeWeightsAfterRba": round(random.uniform(0.5, 2.0), 2),
                "totalRelativeWeightsBeforeRba": round(random.uniform(0.5, 2.0), 2)
            }
            for i in range(array_length)
        ],
        "dataPerXnec": [
            {
                "deltaMinus": round(random.uniform(0, 100), 2),
                "deltaPlus": round(random.uniform(0, 100), 2),
                "fAfterRao": round(random.uniform(1000, 5000), 2),
                "fLimit": round(random.uniform(1000, 5000), 2),
                "fMax": round(random.uniform(500, 2500), 2),
                "leastCostWeightRi": round(random.uniform(0.5, 1.5), 2),
                "lowerBalancingDualValue": round(random.uniform(10, 100), 2),
                "lowerBalancingSlack": round(random.uniform(10, 100), 2),
                "powerFlowDualValue": round(random.uniform(10, 100), 2),
                "powerFlowSlack": round(random.uniform(10, 100), 2),
                "relativeCostWeightAfterRba": round(random.uniform(0.5, 2.0), 2),
                "relativeCostWeightBeforeRba": round(random.uniform(0.5, 2.0), 2),
                "selectedXnecResultId": generate_selected_xnec_result_id(),
                "shareOfTotalCosts": round(random.uniform(1000, 5000), 2),
                "sumDeltaMinus": round(random.uniform(1000, 5000), 2),
                "sumDeltaPlus": round(random.uniform(1000, 5000), 2),
                "timestamp": timestamps_dataPerXnec[i],
                "totalAdjustedFlow": round(random.uniform(1000, 5000), 2),
                "upperBalancingDualValue": round(random.uniform(10, 100), 2),
                "upperBalancingSlack": round(random.uniform(10, 100), 2),
                "xnecId": generate_selected_xnec_result_id()
            }
            for i in range(array_length)
        ],
        "dataPerXnecAndXra": [
            {
                "timestamp": timestamps_dataPerXnecAndXra[i],
                "value": round(random.uniform(0, 100), 2),
                "valueType": random.choice(["optimizationVariable", "sensitivity"]),
                "xnecId": generate_selected_xnec_result_id(),
                "xraId": generate_selected_xnec_result_id(),
            }
            for i in range(array_length)
        ],
        "dataPerXra": [
            {
                "orderedVolume": round(random.uniform(100, 500), 2),
                "sumAlphaOrBetaOverXnecs": round(random.uniform(1000, 5000), 2),
                "timestamp": timestamps_dataPerXra[i],
                "totalCost": round(random.uniform(5000, 15000), 2),
                "xraId": generate_selected_xnec_result_id(),
            }
            for i in range(array_length)
        ]
    }
 
    # samples.append(sample)
    
    return sample

# Main function to load schema, generate data, and write to multiple files
def generate_sample_data_files(schema_file_path, output_file_prefix, num_samples=10):
    # Load the schema from the file
    with open(schema_file_path, 'r') as f:
        schema = json.load(f)

    # Start date for the first sample
    start_date = datetime(2024, 10, 1)

    # Base time for timestamps
    base_time = datetime.strptime("00:00", "%H:%M")

    # Generate and save multiple samples
    for i in range(num_samples):
        # Increment base date for each file
        current_base_date = start_date + timedelta(days=i)
        sample_data = generate_sample_data(current_base_date, base_time)
        output_file_path = f"{output_file_prefix}_{i+1}.json"
        with open(output_file_path, 'w') as f:
            json.dump(sample_data, f, indent=4)

baseFineName = "MappingDetailedResults"
schema_file_path = 'MappingDetailedResults_Schema_fixed.json'
output_file_prefix = f'{baseFineName}_file'
generate_sample_data_files(schema_file_path, output_file_prefix)



















# import json
# from datetime import datetime, timedelta
# import random
# import secrets

# # Function to generate timestamp with incrementing hours
# def generate_timestamps(base_date, base_time, count, interval_minutes=30):
#     timestamps = []
#     for i in range(count):
#         timestamp = base_date.replace(hour=base_time.hour, minute=base_time.minute) + timedelta(minutes=i * interval_minutes)
#         timestamps.append(timestamp.strftime("%Y-%m-%dT%H:%M:%S") + "Z")
#     return timestamps

# def generate_time_horizon():
#     return random.choice(["dayAhead"])

# def generate_crosa_version():
#     return random.randint(1, 1)

# def generate_selected_xnec_result_id():
#     return secrets.token_hex(12)

# # Generate sample data function
# def generate_sample_data(base_date, base_time, count=10):
#     samples = []

#     for _ in range(count):
#         business_day = base_date.strftime("%Y-%m-%d")

#         # Randomize array length for each iteration
#         array_length = random.randint(3, 10)

#         # Generate timestamps for array properties
#         timestamps_dataPerHour = generate_timestamps(base_date, base_time, array_length)
#         timestamps_dataPerXnec = generate_timestamps(base_date, base_time, array_length)
#         timestamps_dataPerXnecAndXra = generate_timestamps(base_date, base_time, array_length)
#         timestamps_dataPerXra = generate_timestamps(base_date, base_time, array_length)

#         sample = {
#             "businessDay": business_day,
#             "crosaVersion": generate_crosa_version(),
#             "csProcessVersion": random.randint(1, 5),
#             "timeHorizon": generate_time_horizon(),
#             "dataPerHour": [
#                 {
#                     "aggregatedVolumeDownwardCostlyAnora": round(random.uniform(1000, 5000), 2),
#                     "aggregatedVolumeUpwardCostlyAnora": round(random.uniform(1000, 5000), 2),
#                     "averageCostDownwardOraOrAnora": round(random.uniform(100, 500), 2),
#                     "averageCostUpwardOraOrAnora": round(random.uniform(100, 500), 2),
#                     "penaltyCostForAnoraVolumes": round(random.uniform(10, 50), 2),
#                     "timestamp": timestamps_dataPerHour[i],
#                     "totalCostsAllOras": round(random.uniform(5000, 15000), 2),
#                     "totalIndividualShare": round(random.uniform(1000, 5000), 2),
#                     "totalRelativeWeightsAfterRba": round(random.uniform(0.5, 2.0), 2),
#                     "totalRelativeWeightsBeforeRba": round(random.uniform(0.5, 2.0), 2)
#                 }
#                 for i in range(array_length)
#             ],
#             "dataPerXnec": [
#                 {
#                     "deltaMinus": round(random.uniform(0, 100), 2),
#                     "deltaPlus": round(random.uniform(0, 100), 2),
#                     "fAfterRao": round(random.uniform(1000, 5000), 2),
#                     "fLimit": round(random.uniform(1000, 5000), 2),
#                     "fMax": round(random.uniform(500, 2500), 2),
#                     "leastCostWeightRi": round(random.uniform(0.5, 1.5), 2),
#                     "lowerBalancingDualValue": round(random.uniform(10, 100), 2),
#                     "lowerBalancingSlack": round(random.uniform(10, 100), 2),
#                     "powerFlowDualValue": round(random.uniform(10, 100), 2),
#                     "powerFlowSlack": round(random.uniform(10, 100), 2),
#                     "relativeCostWeightAfterRba": round(random.uniform(0.5, 2.0), 2),
#                     "relativeCostWeightBeforeRba": round(random.uniform(0.5, 2.0), 2),
#                     "selectedXnecResultId": generate_selected_xnec_result_id(),
#                     "shareOfTotalCosts": round(random.uniform(1000, 5000), 2),
#                     "sumDeltaMinus": round(random.uniform(1000, 5000), 2),
#                     "sumDeltaPlus": round(random.uniform(1000, 5000), 2),
#                     "timestamp": timestamps_dataPerXnec[i],
#                     "totalAdjustedFlow": round(random.uniform(1000, 5000), 2),
#                     "upperBalancingDualValue": round(random.uniform(10, 100), 2),
#                     "upperBalancingSlack": round(random.uniform(10, 100), 2),
#                     "xnecId": generate_selected_xnec_result_id()
#                 }
#                 for i in range(array_length)
#             ],
#             "dataPerXnecAndXra": [
#                 {
#                     "timestamp": timestamps_dataPerXnecAndXra[i],
#                     "value": round(random.uniform(0, 100), 2),
#                     "valueType": random.choice(["optimizationVariable", "sensitivity"]),
#                     "xnecId": generate_selected_xnec_result_id(),
#                     "xraId": generate_selected_xnec_result_id(),
#                 }
#                 for i in range(array_length)
#             ],
#             "dataPerXra": [
#                 {
#                     "orderedVolume": round(random.uniform(100, 500), 2),
#                     "sumAlphaOrBetaOverXnecs": round(random.uniform(1000, 5000), 2),
#                     "timestamp": timestamps_dataPerXra[i],
#                     "totalCost": round(random.uniform(5000, 15000), 2),
#                     "xraId": generate_selected_xnec_result_id(),
#                 }
#                 for i in range(array_length)
#             ]
#         }

#         samples.append(sample)
    
#     return samples

# # Main function to load schema, generate data, and write to multiple files
# def generate_sample_data_files(schema_file_path, output_file_prefix, num_samples=10):
#     # Load the schema from the file
#     with open(schema_file_path, 'r') as f:
#         schema = json.load(f)

#     # Start date for the first sample
#     start_date = datetime(2024, 10, 1)

#     # Base time for timestamps
#     base_time = datetime.strptime("00:00", "%H:%M")

#     # Generate and save multiple samples
#     for i in range(num_samples):
#         # Increment base date for each file
#         current_base_date = start_date + timedelta(days=i)
#         sample_data = generate_sample_data(current_base_date, base_time)
#         output_file_path = f"{output_file_prefix}_{i+1}.json"
#         with open(output_file_path, 'w') as f:
#             json.dump(sample_data, f, indent=4)

# baseFineName = "MappingDetailedResults"
# schema_file_path = 'MappingDetailedResults_Schema_fixed.json'
# output_file_prefix = f'{baseFineName}_file'
# generate_sample_data_files(schema_file_path, output_file_prefix)



























# import json
# from datetime import datetime, timedelta
# import random
# import secrets

# # Create base_date
# new_date = datetime.strptime("2024-10-01", "%Y-%m-%d")

# # Generate a random number of days to add (between -15 and +15)
# random_days = random.randint(-15, 15)

# # Calculate the base date
# base_date = new_date + timedelta(days=random_days)

# # Set base time
# base_time = datetime.strptime("00:00", "%H:%M")

# # Function to generate timestamp with incrementing hours
# def generate_timestamps(base_date, base_time, count, interval_hours=1):
#     timestamps = []
#     for i in range(count):
#         timestamp = base_date.replace(hour=base_time.hour, minute=base_time.minute) + timedelta(hours=i * interval_hours)
#         timestamps.append(timestamp.strftime("%Y-%m-%dT%H:%M:%S") + "Z")
#     return timestamps

# def generate_time_horizon():
#     return random.choice(["dayAhead"])

# def generate_crosa_version():
#     return random.randint(1, 1)

# def generate_selected_xnec_result_id():
#     return secrets.token_hex(12)

# # Generate sample data function
# def generate_sample_data(count=10, base_date=None):
#     samples = []

#     for _ in range(count):
#         if base_date is None:
#             business_day = datetime.now().strftime("%Y-%m-%d")
#         else:
#             business_day = base_date.strftime("%Y-%m-%d")

#         # Randomize array length for each iteration
#         array_length = random.randint(3, 10)

#         # Generate timestamps for array properties
#         timestamps_dataPerHour = generate_timestamps(base_date, base_time, array_length)
#         timestamps_dataPerXnec = generate_timestamps(base_date, base_time, array_length)
#         timestamps_dataPerXnecAndXra = generate_timestamps(base_date, base_time, array_length)
#         timestamps_dataPerXra = generate_timestamps(base_date, base_time, array_length)

#         sample = {
#             "businessDay": business_day,
#             "crosaVersion": generate_crosa_version(),
#             "csProcessVersion": random.randint(1, 5),
#             "timeHorizon": generate_time_horizon(),
#             "dataPerHour": [
#                 {
#                     "aggregatedVolumeDownwardCostlyAnora": round(random.uniform(1000, 5000), 2),
#                     "aggregatedVolumeUpwardCostlyAnora": round(random.uniform(1000, 5000), 2),
#                     "averageCostDownwardOraOrAnora": round(random.uniform(100, 500), 2),
#                     "averageCostUpwardOraOrAnora": round(random.uniform(100, 500), 2),
#                     "penaltyCostForAnoraVolumes": round(random.uniform(10, 50), 2),
#                     "timestamp": timestamps_dataPerHour[i],
#                     "totalCostsAllOras": round(random.uniform(5000, 15000), 2),
#                     "totalIndividualShare": round(random.uniform(1000, 5000), 2),
#                     "totalRelativeWeightsAfterRba": round(random.uniform(0.5, 2.0), 2),
#                     "totalRelativeWeightsBeforeRba": round(random.uniform(0.5, 2.0), 2)
#                 }
#                 for i in range(array_length)
#             ],
#             "dataPerXnec": [
#                 {
#                     "deltaMinus": round(random.uniform(0, 100), 2),
#                     "deltaPlus": round(random.uniform(0, 100), 2),
#                     "fAfterRao": round(random.uniform(1000, 5000), 2),
#                     "fLimit": round(random.uniform(1000, 5000), 2),
#                     "fMax": round(random.uniform(500, 2500), 2),
#                     "leastCostWeightRi": round(random.uniform(0.5, 1.5), 2),
#                     "lowerBalancingDualValue": round(random.uniform(10, 100), 2),
#                     "lowerBalancingSlack": round(random.uniform(10, 100), 2),
#                     "powerFlowDualValue": round(random.uniform(10, 100), 2),
#                     "powerFlowSlack": round(random.uniform(10, 100), 2),
#                     "relativeCostWeightAfterRba": round(random.uniform(0.5, 2.0), 2),
#                     "relativeCostWeightBeforeRba": round(random.uniform(0.5, 2.0), 2),
#                     "selectedXnecResultId": generate_selected_xnec_result_id(),
#                     "shareOfTotalCosts": round(random.uniform(1000, 5000), 2),
#                     "sumDeltaMinus": round(random.uniform(1000, 5000), 2),
#                     "sumDeltaPlus": round(random.uniform(1000, 5000), 2),
#                     "timestamp": timestamps_dataPerXnec[i],
#                     "totalAdjustedFlow": round(random.uniform(1000, 5000), 2),
#                     "upperBalancingDualValue": round(random.uniform(10, 100), 2),
#                     "upperBalancingSlack": round(random.uniform(10, 100), 2),
#                     "xnecId": generate_selected_xnec_result_id()
#                 }
#                 for i in range(array_length)
#             ],
#             "dataPerXnecAndXra": [
#                 {
#                     "timestamp": timestamps_dataPerXnecAndXra[i],
#                     "value": round(random.uniform(0, 100), 2),
#                     "valueType": random.choice(["optimizationVariable", "sensitivity"]),
#                     "xnecId": generate_selected_xnec_result_id(),
#                     "xraId": generate_selected_xnec_result_id(),
#                 }
#                 for i in range(array_length)
#             ],
#             "dataPerXra": [
#                 {
#                     "orderedVolume": round(random.uniform(100, 500), 2),
#                     "sumAlphaOrBetaOverXnecs": round(random.uniform(1000, 5000), 2),
#                     "timestamp": timestamps_dataPerXra[i],
#                     "totalCost": round(random.uniform(5000, 15000), 2),
#                     "xraId": generate_selected_xnec_result_id(),
#                 }
#                 for i in range(array_length)
#             ]
#         }

#         samples.append(sample)
    
#     return samples


# # Main function to load schema, generate data, and write to multiple files
# def generate_sample_data_files(schema_file_path, output_file_prefix, num_samples=10):
#     # Load the schema from the file
#     with open(schema_file_path, 'r') as f:
#         schema = json.load(f)

#     # Generate and save multiple samples
#     for i in range(num_samples):
#         # Randomly generate a base date for each sample
#         random_days = random.randint(-15, 15)
#         base_date = new_date + timedelta(days=random_days)

#         sample_data = generate_sample_data(base_date=base_date)
#         output_file_path = f"{output_file_prefix}_{i+1}.json"
#         with open(output_file_path, 'w') as f:
#             json.dump(sample_data, f, indent=4)

# baseFineName = "MappingDetailedResults"
# schema_file_path = 'MappingDetailedResults_Schema_fixed.json'

# output_file_prefix = f'{baseFineName}_file'
# generate_sample_data_files(schema_file_path, output_file_prefix)

















# import json
# from datetime import datetime, timedelta
# import random
# import secrets

# # Create base_date
# new_date = datetime.strptime("2024-10-01", "%Y-%m-%d")

# # Generate a random number of days to add (between -15 and +15)
# random_days = random.randint(-15, 15)

# # Calculate the new date
# base_date = new_date + timedelta(days=random_days)

# # Set base date and time
# # base_date = datetime.strptime("2024-10-01", "%Y-%m-%d")
# base_time = datetime.strptime("01:30", "%H:%M")

# # Function to generate timestamp with incrementing hours
# def generate_timestamps(base_date, base_time, count, interval_hours=1):
#     timestamps = []
#     for i in range(count):
#         timestamp = base_date.replace(hour=base_time.hour, minute=base_time.minute) + timedelta(hours=i * interval_hours)
#         timestamps.append(timestamp.strftime("%Y-%m-%dT%H:%M:%S") + "Z")
#     return timestamps

# def generate_time_horizon():
#     # return random.choice(["dayAhead", "weekAhead", "monthAhead", "Intraday"])
#     return random.choice(["dayAhead"])

# def generate_crosa_version():
#     # return random.randint(1, 5)
#     return random.randint(1, 1)

# def generate_selected_xnec_result_id():
#     return secrets.token_hex(12)

# # Generate sample data function
# def generate_sample_data(count=10):
#     samples = []

#     for _ in range(count):
#         business_day = base_date.strftime("%Y-%m-%d")

#         # Randomize array length for each iteration
#         array_length = random.randint(3, 10)

#         # Generate timestamps for array properties
#         timestamps_dataPerHour = generate_timestamps(base_date, base_time, array_length)
#         timestamps_dataPerXnec = generate_timestamps(base_date, base_time, array_length)
#         timestamps_dataPerXnecAndXra = generate_timestamps(base_date, base_time, array_length)
#         timestamps_dataPerXra = generate_timestamps(base_date, base_time, array_length)

#         sample = {
#             "businessDay": business_day,
#             "crosaVersion": generate_crosa_version (),
#             "csProcessVersion": random.randint(1, 5),
#             "timeHorizon": generate_time_horizon (),
#             "dataPerHour": [
#                 {
#                     "aggregatedVolumeDownwardCostlyAnora": round(random.uniform(1000, 5000), 2),
#                     "aggregatedVolumeUpwardCostlyAnora": round(random.uniform(1000, 5000), 2),
#                     "averageCostDownwardOraOrAnora": round(random.uniform(100, 500), 2),
#                     "averageCostUpwardOraOrAnora": round(random.uniform(100, 500), 2),
#                     "penaltyCostForAnoraVolumes": round(random.uniform(10, 50), 2),
#                     "timestamp": timestamps_dataPerHour[i],
#                     "totalCostsAllOras": round(random.uniform(5000, 15000), 2),
#                     "totalIndividualShare": round(random.uniform(1000, 5000), 2),
#                     "totalRelativeWeightsAfterRba": round(random.uniform(0.5, 2.0), 2),
#                     "totalRelativeWeightsBeforeRba": round(random.uniform(0.5, 2.0), 2)
#                 }
#                 for i in range(array_length)
#             ],
#             "dataPerXnec": [
#                 {
#                     "deltaMinus": round(random.uniform(0, 100), 2),
#                     "deltaPlus": round(random.uniform(0, 100), 2),
#                     "fAfterRao": round(random.uniform(1000, 5000), 2),
#                     "fLimit": round(random.uniform(1000, 5000), 2),
#                     "fMax": round(random.uniform(500, 2500), 2),
#                     "leastCostWeightRi": round(random.uniform(0.5, 1.5), 2),
#                     "lowerBalancingDualValue": round(random.uniform(10, 100), 2),
#                     "lowerBalancingSlack": round(random.uniform(10, 100), 2),
#                     "powerFlowDualValue": round(random.uniform(10, 100), 2),
#                     "powerFlowSlack": round(random.uniform(10, 100), 2),
#                     "relativeCostWeightAfterRba": round(random.uniform(0.5, 2.0), 2),
#                     "relativeCostWeightBeforeRba": round(random.uniform(0.5, 2.0), 2),
#                     "selectedXnecResultId": generate_selected_xnec_result_id (),
#                     "shareOfTotalCosts": round(random.uniform(1000, 5000), 2),
#                     "sumDeltaMinus": round(random.uniform(1000, 5000), 2),
#                     "sumDeltaPlus": round(random.uniform(1000, 5000), 2),
#                     "timestamp": timestamps_dataPerXnec[i],
#                     "totalAdjustedFlow": round(random.uniform(1000, 5000), 2),
#                     "upperBalancingDualValue": round(random.uniform(10, 100), 2),
#                     "upperBalancingSlack": round(random.uniform(10, 100), 2),
#                     "xnecId": generate_selected_xnec_result_id ()
#                 }
#                 for i in range(array_length)
#             ],
#             "dataPerXnecAndXra": [
#                 {
#                     "timestamp": timestamps_dataPerXnecAndXra[i],
#                     "value": round(random.uniform(0, 100), 2),
#                     "valueType": random.choice(["optimizationVariable", "sensitivity"]),
#                     "xnecId": generate_selected_xnec_result_id (),
#                     "xraId": generate_selected_xnec_result_id (), 
#                 }
#                 for i in range(array_length)
#             ],
#             "dataPerXra": [
#                 {
#                     "orderedVolume": round(random.uniform(100, 500), 2),
#                     "sumAlphaOrBetaOverXnecs": round(random.uniform(1000, 5000), 2),
#                     "timestamp": timestamps_dataPerXra[i],
#                     "totalCost": round(random.uniform(5000, 15000), 2),
#                     "xraId": generate_selected_xnec_result_id (), 
#                 }
#                 for i in range(array_length)
#             ]
#         }

#         samples.append(sample)
    
#     return samples


# # Main function to load schema, generate data, and write to multiple files
# def generate_sample_data_files(schema_file_path, output_file_prefix, num_samples=10):
#     # Load the schema from the file
#     with open(schema_file_path, 'r') as f:
#         schema = json.load(f)

#     # Start date for the first sample
#     start_date = datetime(2024, 1, 1)

#     # Generate and save multiple samples
#     for i in range(num_samples):
#         sample_data = generate_sample_data()
#         output_file_path = f"{output_file_prefix}_{i+1}.json"
#         with open(output_file_path, 'w') as f:
#             json.dump(sample_data, f, indent=4)

# baseFineName = "MappingDetailedResults"
# schema_file_path = 'MappingDetailedResults_Schema_fixed.json'
# # baseFineName = "Flow_Decomposition"
# # schema_file_path = 'Flow_Decomposition_Schema_fixed.json'
# # baseFineName = "CostDistribution"
# # schema_file_path = 'CostDistribution_Schema_fixed.json'

# # Flow_Decomposition_Schema_fixed.json
# output_file_prefix = f'{baseFineName}_file'
# generate_sample_data_files(schema_file_path, output_file_prefix)


# # # Generate 10 samples
# # sample_data = generate_sample_data(); 

# # # Save to JSON file
# # with open("sample_data.json", "w") as f:
# #     json.dump(sample_data, f, indent=4)

# # print("Sample data generated with randomized array lengths and saved to sample_data.json.")


