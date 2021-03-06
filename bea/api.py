"""
This module contains specifics based on the current documentation,
to make calls and consume the data released by the BEA.

Although the BEA (at the time of this writing) supports both XML
and JSON responses; this module does not have XML response support
at this time, only JSON and Python types.

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
from pprint import pprint


class BaseHandler(object):
    """
    This is the super class handler with attributes
    common to all subclassed handlers for BEA requests
    """
    def __init__(self, user_key, result_format='JSON'):
        """

        :param user_key:
        :type user_key:
        :param result_format:
        :type result_format:
        """
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
                                  echo_request=False):
        """
        Takes the request URL and a target node,
        delegating to a few other helper methods to
        unpack and process the response.

        :param url: The target request URL
        :type url: str
        :param target_node: The response node containing the data
        :type target_node: str
        :param echo_request: Whether to echo the request (params, etc.)
            in the response.
        :type echo_request: bool
        :return: The targeted data results as JSON
        :rtype: JSON
        """
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
        """
        Caller to unpack the request node hierarchy, i.e.
        NOT the results node hierarchy.
        Delegates to other helper methods.

        :param response: The JSON response
        :type response: JSON response
        :return: JSON response's request
        :rtype:
        """
        node_hierarchy = self.request_node_hierarchy
        return self._traverse_nodes(response, node_hierarchy)


    def _unpack_results(self, response, target_node):
        """

        :param response:
        :type response:
        :param target_node:
        :type target_node:
        :return:
        :rtype:
        """
        node_hierarchy = self.results_node_hierarchy
        # Target node for results are not static, add target node
        node_hierarchy['target_node'] = target_node
        return self._traverse_nodes(response, node_hierarchy)


    def _traverse_nodes(self, response, node_hierarchy):
        """

        :param response:
        :type response:
        :param node_hierarchy:
        :type node_hierarchy:
        :return:
        :rtype:
        """
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
        """

        :param user_key:
        :type user_key:
        :param result_format:
        :type result_format:
        """
        super().__init__(user_key, result_format)

    # BEA metadata equivalent request methods
    def get_dataset_list(self, target_node='Dataset', echo_request=False):
        """
        Retrieves the BEA datasets list

        :param target_node: The dataset target node
        :type target_node: str
        :param echo_request: Whether to echo the request and params in the response
        :type echo_request: bool
        :return: The targeted data results as JSON
        :rtype: JSON
        """
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
        """

        :param dataset_name:
        :type dataset_name:
        :param target_node:
        :type target_node:
        :param echo_request:
        :type echo_request:
        :return:
        :rtype:
        """
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
        """

        :param dataset_name:
        :type dataset_name:
        :param param_name:
        :type param_name:
        :param target_node:
        :type target_node:
        :param echo_request:
        :type echo_request:
        :return:
        :rtype:
        """
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
        """

        :param dataset_name:
        :type dataset_name:
        :param target_param:
        :type target_param:
        :param table_name:
        :type table_name:
        :param target_node:
        :type target_node:
        :param echo_request:
        :type echo_request:
        :return:
        :rtype:
        """
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

    def create_metadata_dict(self, dataset_name):
        """

        :param dataset_name:
        :type dataset_name:
        :return:
        :rtype:
        """
        metadata_dict = {}
        # Add dataset name to dict and create a params key with an empty dict
        metadata_dict['dataset_name'] = dataset_name
        metadata_dict['parameters'] = {}

        # Get param list for dataset, then get possible
        # param values for each param and add to dict
        param_list = self.get_param_list(dataset_name)
        for d in param_list:
            param_name = d['ParameterName']
            metadata_dict['parameters'][param_name] = {}
            metadata_dict['parameters'][param_name]['param_details'] = d
            param_values = self.get_param_values(dataset_name, param_name)
            metadata_dict['parameters'][param_name]['args'] = param_values
        return metadata_dict




class DataHandler(BaseHandler):

    def __init__(self, user_key, result_format='JSON'):
        """

        :param user_key:
        :type user_key:
        :param result_format:
        :type result_format:
        """
        super().__init__(user_key, result_format)

    def get_data(self, dataset_name, **params):
        """

        :param dataset_name:
        :type dataset_name:
        :param params:
        :type params:
        :return:
        :rtype:
        """
        url = (
            '{}?&'
            'UserID={}&'
            'method=GetData&'
            'datasetname={}&'
            'ResultFormat={}&'.format(
                self.base_url,
                self.user_key,
                dataset_name,
                self.result_format
            )
        )


if __name__=='__main__':

    BEA_API_USER_KEY = ''

    handler = MetadataHandler(BEA_API_USER_KEY)
    my_dict = handler.create_metadata_dict('RegionalIncome')
    pprint(my_dict['parameters']['TableName'])

