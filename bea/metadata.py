import requests
import collections
import pandas
from pprint import pprint



BEA_API_ROOT_URL = 'https://www.bea.gov/api/data/'
BEA_API_USER_KEY = '3924A4B4-43A0-4BE6-B131-650F0740C025'


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

        # Only JSON result format, i.e. no XML support
        if result_format != 'JSON':
            raise ValueError("Only 'JSON' responses are supported at this time")
        else:
            self.result_format = result_format

        # The current node hierachies to be used to 'unpack'
        # responses to obtain the target data
        self.request_node_hierarchy = collections.OrderedDict(
            {
                'root_node': 'BEAAPI',
                'request_node': 'Request',
                'target_node': 'RequestParam',
            }
        )
        self.results_node_hierarchy = collections.OrderedDict(
            {
                'root_node': 'BEAAPI',
                'results_node': 'Results',
                'target_node': None
            }
        )
        # Check base_url response to see if API service
        # is available
        response = requests.get(self.base_url)
        if not response.ok:
            raise requests.HTTPError


    # Metadata
    def get_dataset_list(self, target_node='Dataset', echo_request=False):
        url = (
            '{}?&'
            'UserID={}&'
            'method=GetDatasetList&'
            'ResultFormat={}&'.format(
                self.base_url,
                self.user_key,
                self.result_format
            )
        )
        return self._get_and_process_response(url, target_node, echo_request)


    def get_param_list(self, dataset_name, target_node='Parameter',
                       echo_request=False):
        url = (
            '{}?&'
            'UserID={}&'
            'method=GetParameterList&'
            'datasetname={}&'
            'ResultFormat={}&'.format(
                self.base_url,
                self.user_key,
                dataset_name,
                self.result_format
            )
        )
        return self._get_and_process_response(url, target_node, echo_request)


    def get_param_values(self, dataset_name, param_name,
                         target_node='ParamValue', echo_request=False):
        url = (
            '{}?&'
            'UserID={}&'
            'method=GetParameterValues&'
            'datasetname={}&'
            'ParameterName={}&'
            'ResultFormat={}&'.format(
                self.base_url,
                self.user_key,
                dataset_name,
                param_name,
                self.result_format
            )
        )
        return self._get_and_process_response(url, target_node, echo_request)


    def _get_and_process_response(self, url, target_node, echo_request):
        response = requests.get(url)
        if response.ok:
            # Decode JSON response to Python type(s)
            response = response.json()
            # Unpack results
            target_results = self._unpack_results(response, target_node)
            if echo_request:
                # Unpack the request echo in the response,
                # return the echo and results as a tuple
                echo_request_params = self._unpack_request(response)
                return (echo_request_params, target_results)
            else:
                return target_results
        else:
            raise requests.HTTPError


    def _unpack_request(self, response):
        node_hierarchy = self.request_node_hierarchy
        return self._node_traverser(response, node_hierarchy)


    def _unpack_results(self, response, target_node):
        node_hierarchy = self.results_node_hierarchy
        # Target node for results are not static, add target node
        node_hierarchy['target_node'] = target_node
        return self._node_traverser(response, node_hierarchy)


    def _node_traverser(self, response, node_hierarchy):
        try:
            for k, v in node_hierarchy.items():
                response = response[v]
            return response
        except KeyError as e:
            print("The key: {} does not exist in the response"
                  .format(e))
            pprint(response)






def get_param_values_filtered():
    pass



if __name__=='__main__':
    handler = MetaRequestHandle(BEA_API_ROOT_URL, BEA_API_USER_KEY)
    dataset_result = handler.get_dataset_list()
    region_income_params = handler.get_param_values('RegionalIncome', 'GeoFips')
    pprint(region_income_params)



