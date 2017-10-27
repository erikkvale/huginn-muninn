import collections

# Settings and initial configuration
DATASET_LIST_SETTINGS = {
    'api_key': '3924A4B4-43A0-4BE6-B131-650F0740C025',
    'base_url': 'https://www.bea.gov/api/data/',
    'method': 'GETDATASETLIST',
    'result_format': 'JSON',
    'node_hierarchy': collections.OrderedDict({
        'root_node': 'BEAAPI',
        'child_node_one': 'Results',
        'child_node_two': 'Dataset',
    })
}


DATASET_PARAMS_SETTINGS = {
    'api_key': '3924A4B4-43A0-4BE6-B131-650F0740C025',
    'base_url': 'https://www.bea.gov/api/data/',
    'method': 'getparameterlist',
    'datasetname': [],  # Populated from dataset list
    'result_format': 'JSON',
    'node_hierarchy': collections.OrderedDict({
        'root_node': 'BEAAPI',
        'child_node_one': 'Results',
        'child_node_two': 'Parameter',
    })
}
