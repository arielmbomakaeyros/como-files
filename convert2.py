import json

# Load JSON data from files
with open('W49_costDistributionResult.json', 'r') as file1, open('CostDistribution_Schema_CSV.json', 'r') as file2:
    w49_data = json.load(file1)
    schema_data = json.load(file2)

# Extract relevant fields from W49_costDistributionResult.json
business_day = w49_data['businessDay']
business_timestamp = w49_data['businessTimestamp']
crosa_version = w49_data['crosaVersion']
cs_process_version = w49_data['csProcessVersion']
flow_decomposition_id = w49_data['flowDecompositionId']
result_id = w49_data['id']
mapping_result_id = w49_data['mappingResultId']
selected_xnec_result_id = w49_data['selectedXnecResultId']
time_horizon = w49_data['timeHorizon']

# Extract the first elements from xnecCostList
xnec_cost = w49_data['xnecCostList'][0]
bidding_zone_cost = xnec_cost['biddingZoneCostList'][0]
flow_component = xnec_cost['flowComponentList'][0]
threshold_application = None

# Find the first non-empty appliedThresholdList
for component in xnec_cost['flowComponentList']:
    if component.get('appliedThresholdList'):
        threshold_application = component['appliedThresholdList'][0]
        break

tso_cost = xnec_cost['tsoCostList'][0]

# Build the new JSON structure
new_json = {
    "businessDay": business_day,
    "businessTimestamp": business_timestamp,
    "crosaVersion": crosa_version,
    "csProcessVersion": cs_process_version,
    "flowDecompositionId": flow_decomposition_id,
    "id": result_id,
    "mappingResultId": mapping_result_id,
    "selectedXnecResultId": selected_xnec_result_id,
    "timeHorizon": time_horizon,
    "biddingZoneCost": bidding_zone_cost,
    "flowComponent": flow_component,
    "thresholdApplication": threshold_application,
    "tsoCost": tso_cost,
    "xnecCost": {
        "convertedXnecId": xnec_cost['convertedXnecId'],
        "cost": xnec_cost['cost'],
        "volumeOverload": xnec_cost['volumeOverload'],
        # "flowComponentList": xnec_cost['flowComponentList']
    }
}

# Save the newly generated JSON to a file
with open('new_generated_file2.json', 'w') as output_file:
    json.dump(new_json, output_file, indent=4)

print("New JSON file has been created as 'new_generated_file.json'.")










# import json

# # Load JSON data from files
# with open('W49_costDistributionResult.json', 'r') as file1, open('CostDistribution_Schema_CSV.json', 'r') as file2:
#     w49_data = json.load(file1)
#     schema_data = json.load(file2)

# # Extract relevant fields from W49_costDistributionResult.json
# business_day = w49_data['businessDay']
# business_timestamp = w49_data['businessTimestamp']
# crosa_version = w49_data['crosaVersion']
# cs_process_version = w49_data['csProcessVersion']
# flow_decomposition_id = w49_data['flowDecompositionId']
# result_id = w49_data['id']
# mapping_result_id = w49_data['mappingResultId']
# selected_xnec_result_id = w49_data['selectedXnecResultId']
# time_horizon = w49_data['timeHorizon']

# # Extract the first elements from xnecCostList
# xnec_cost = w49_data['xnecCostList'][0]
# bidding_zone_cost = xnec_cost['biddingZoneCostList'][0]
# flow_component = xnec_cost['flowComponentList'][0]
# threshold_application = None

# # Find the first non-empty appliedThresholdList
# for component in xnec_cost['flowComponentList']:
#     if component.get('appliedThresholdList'):
#         threshold_application = component['appliedThresholdList'][0]
#         break

# tso_cost = xnec_cost['tsoCostList'][0]

# # Build the new JSON structure
# new_json = {
#     "businessDay": business_day,
#     "businessTimestamp": business_timestamp,
#     "crosaVersion": crosa_version,
#     "csProcessVersion": cs_process_version,
#     "flowDecompositionId": flow_decomposition_id,
#     "id": result_id,
#     "mappingResultId": mapping_result_id,
#     "selectedXnecResultId": selected_xnec_result_id,
#     "timeHorizon": time_horizon,
#     "definition": {
#         "biddingZoneCost": bidding_zone_cost,
#         "flowComponent": flow_component,
#         "thresholdApplication": threshold_application,
#         "tsoCost": tso_cost,
#         "xnecCost": {
#             "convertedXnecId": xnec_cost['convertedXnecId'],
#             "cost": xnec_cost['cost'],
#             "volumeOverload": xnec_cost['volumeOverload'],
#             # "flowComponentList": xnec_cost['flowComponentList']
#         }
#     }
# }

# # Save the newly generated JSON to a file
# with open('new_generated_file.json', 'w') as output_file:
#     json.dump(new_json, output_file, indent=4)

# print("New JSON file has been created as 'new_generated_file.json'.")










