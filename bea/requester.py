"""
BEA API:

This module contains specifics based on the current documentation,
to make calls and consume the data released by the BEA.

--------------------
API Calling Limits
--------------------
The API has default calling limits as shown below. These limits are meant
to protect BEA’s API and webserver infrastructure from activity that may be
detrimental to that infrastructure and/or unfairly impede other API users.

• 1000 API calls per minute, and/or
• 30 errors per minute, and/or
• 50 MB (raw data) per minute.

Any user that exceeds the above calling limits will receive an explanatory
error message for each API call until the per-minute cause has expired.
The best way to avoid such errors is to design your application to call
the API within these limits, e.g., programmatically regulate the
frequency/size of API calls.
"""

import requests
import collections
import json
import pandas
from pprint import pprint


BEA_API_ROOT_URL = 'https://www.bea.gov/api/data/'
BEA_API_USER_KEY = '3924A4B4-43A0-4BE6-B131-650F0740C025'
BEA_API_RESULTS_NODE_HIERARCHY = collections.OrderedDict(
    {
        'root_node': 'BEAAPI',
        'results_node': 'Results',
    }
)


class BeaRequestHandler:

    def __init__(self, root_url, user_key,
                 root_node_hierarchy):
        self.root_url = root_url
        self.user_key = user_key
        self.root_node_hierarchy = root_node_hierarchy


    def get_dataset_list(self, target_node_name='Dataset', method='GetDatasetList',
                         result_format='JSON', return_json=True):
        request_url = '{0}?&UserID={1}&method={2}&ResultFormat={3}&'.format(
            self.root_url,
            self.user_key,
            method,
            result_format
        )
        dataset_node_hierarchy = self.root_node_hierarchy
        dataset_node_hierarchy['data_node'] = target_node_name
        response = self._request_and_unpack_json(
            request_url=request_url,
            node_hierarchy=dataset_node_hierarchy,
            return_json=return_json
        )
        return response


    def get_dataset_params(self, dataset_name, target_node_name='Parameter',
                           method='GetParameterList', result_format='JSON',
                           return_json=False):
        request_url = ('{0}?&UserID={1}&method={2}&datasetname={3}'
                       '&ResultFormat={4}&'.format(
            self.root_url,
            self.user_key,
            method,
            dataset_name,
            result_format
        ))
        param_node_hierarchy = self.root_node_hierarchy
        param_node_hierarchy['data_node'] = target_node_name
        response = self._request_and_unpack_json(
            request_url=request_url,
            node_hierarchy=node_hierarchy,
            return_json=return_json
        )
        return response


    def _request_and_unpack_json(self, request_url, node_hierarchy,
                                 return_json=True):
        """
        Attempts to return a "narrowed" json response, by
        unpacking the initial response by traversing the
        input node hierarchy.
        --------------
        Parameters
        --------------
        request_url: <str>
            -URL to resource
        node_hierarchy: <OrderedDict>
            -Example:
                collection.OrderedDict({
                    'root_node':'name',
                    'child_node_<1>': 'name',
                    ...
                    'child_node_<n>:''}
                })
        return_json: <bool>
            -If true then returns a JSON formatted string object, else a
             Python object
        """
        response = requests.get(request_url).json()
        for k, v in node_hierarchy.items():
            response = response[v]
        if return_json:
            return json.dumps(response)
        else:
            return response


    def json_to_excel(self, output_file_path, output_spreadsheet_name,
                      json_data, json_orientation='records'):
        """
        Attempts to read json data into Pandas dataframe, then
        write that data out to a specified Excel workbook and
        spreadsheet.
        """
        writer = pandas.ExcelWriter(path=output_file_path,
                                    engine='xlsxwriter')
        df = pandas.read_json(json_data, orient=json_orientation)
        df.to_excel(writer, output_spreadsheet_name)
        writer.save()


if __name__=='__main__':
    import os
    handler = BeaRequestHandler(BEA_API_ROOT_URL,
                                BEA_API_USER_KEY,
                                BEA_API_RESULTS_NODE_HIERARCHY)
    datasets = handler.get_dataset_list(return_json=False)
    print(datasets)
    print(os.getcwd())
