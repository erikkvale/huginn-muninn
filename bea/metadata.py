import requests
import collections
from pprint import pprint


class BaseHandler(object):
    """
    This is the super class handler with attributes
    common to all subclassed handlers for BEA requests
    """
    def __init__(self, user_key, result_format='JSON'):
        # The current base URL for the BEA's API
        self.base_url = 'https://www.bea.gov/api/data/'
        self.user_key = user_key

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

        # Only JSON result format, i.e. no XML support
        if result_format != 'JSON':
            raise ValueError("Only 'JSON' responses are supported at this time")
        else:
            self.result_format = result_format

        # Check base_url response to see if API service
        # is available
        response = requests.get(self.base_url)
        if not response.ok:
            raise requests.HTTPError

    # Helper methods
    def _get_and_process_response(self, url, target_node,
                                  echo_request):
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
        return self._traverse_nodes(response, node_hierarchy)


    def _unpack_results(self, response, target_node):
        node_hierarchy = self.results_node_hierarchy
        # Target node for results are not static, add target node
        node_hierarchy['target_node'] = target_node
        return self._traverse_nodes(response, node_hierarchy)


    def _traverse_nodes(self, response, node_hierarchy):
        try:
            for k, v in node_hierarchy.items():
                response = response[v]
            return response
        except KeyError as e:
            print("The key: {} does not exist in the response"
                  .format(e))
            pprint(response)



class MetadataHandler(BaseHandler):

    def __init__(self, user_key, result_format='JSON'):
        super().__init__(user_key, result_format)

    # BEA metadata equivalent request methods
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
        return super()._get_and_process_response(
            url,
            target_node,
            echo_request
        )


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
        return super()._get_and_process_response(
            url,
            target_node,
            echo_request
        )


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
        return super()._get_and_process_response(
            url,
            target_node,
            echo_request
        )


    def get_param_values_filtered(self, dataset_name, target_param,
                                  table_name, target_node='ParamValue',
                                  echo_request=False):
        url = (
            '{}?&'
            'UserID={}&'
            'method=GetParameterValuesFiltered&'
            'datasetname={}&'
            'TargetParameter={}&'
            'TableName={}'
            'ResultFormat={}&'.format(
                self.base_url,
                self.user_key,
                dataset_name,
                target_param,
                table_name,
                self.result_format
            )
        )
        return super()._get_and_process_response(
            url,
            target_node,
            echo_request
        )

class DataHandler(BaseHandler):

    def __init__(self, user_key, result_format='JSON'):
        super().__init__(user_key, result_format)

    def get_data(self, dataset_name, **params):
        pass


if __name__=='__main__':

    BEA_API_USER_KEY = '3924A4B4-43A0-4BE6-B131-650F0740C025'

    handler = MetadataHandler(BEA_API_USER_KEY)
    ds = handler.get_dataset_list()
    pprint(ds)


