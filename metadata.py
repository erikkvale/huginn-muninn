import requests
from pprint import pprint



BEA_API_ROOT_URL = 'https://www.bea.gov/api/data/'
BEA_API_USER_KEY = '3924A4B4-43A0-4BE6-B131-'


METADATA_METHODS_AND_URLS = {
    'GetDatasetList':
        '{}?&'
        'UserID={}&'
        'method=GetDatasetList&'
        'ResultFormat={}&',
    'GetParameterList':
        '{}?&'
        'UserID={}&'
        'method=GetParameterList&'
        'datasetname={}&'
        'ResultFormat={}&',
    'GetParameterValues':
        '{}?&'
        'UserID={}&'
        'method=GetParameterValues&'
        'datasetname={}&'
        'ParameterName={}&'
        'ResultFormat={}&',
    'GetParameterValuesFiltered':
        '{}?&'
        'UserID={}&'
        'method=GetParameterValuesFiltered&'
        'datasetname={}&'
        'TargetParameter={}&'
        'TableName={}'
        'ResultFormat={}&',
}

class MetaRequestHandle:

    def __init__(self, base_url, user_key,
                 result_format='JSON'):
        self.base_url = base_url
        self.user_key = user_key

        if result_format != 'JSON':
            raise ValueError
        else:
            self.result_format = result_format

# Metadata
def get_dataset_list(base_url, user_key, result_format):
    pass

def get_param_list(base_url, user_key, result_format):
    pass

def get_param_values(base_url, user_key, result_format):
    pass

def get_param_values_filtered(dataset_name, target_param, table_name):
    pass



if __name__=='__main__':
    ds = get_dataset_list(BEA_API_ROOT_URL, BEA_API_USER_KEY, 'JSON')
    pprint(ds)


