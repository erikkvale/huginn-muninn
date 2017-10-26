"""
BEA API:

This module contains specifics based on the current documentation,
to make calls and consume the data released by the BEA.
"""
import requests
import json
import collections
import pandas
from pprint import pprint




def request_and_unpack_json(request_url, node_hierarchy):
    """
    Attempts to return a "narrowed" json response, by
    unpacking the initial response by traversing the
    input node hierarchy.
    --------------
    Parameters
    --------------
    request_url: <str>, url to resource
    node_hierarchy: <OrderedDict>,
        Example:
        {
            'root_node':'name',
            'child_node_<1>': 'name',
            ...
            'child_node_<n>:''}
        }
    """
    json_response = requests.get(request_url).json()
    for k, v in node_hierarchy.items():
        json_response = json_response[v]
    return json.dumps(json_response)


def json_to_excel(output_file_path, output_spreadsheet_name,
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


def build_url(settings):
    try:
        request_url = '{0}?&UserID={1}&method={2}&datasetname={3}&ResultFormat={4}&'.format(
            settings['base_url'],
            settings['api_key'],
            settings['method'],
            settings['datasetname'],
            settings['result_format'],
        )
        return request_url
    except KeyError as e:
        print('Key Error:{}, trying alternative....'.format(e))
        request_url = '{0}?&UserID={1}&method={2}&ResultFormat={3}&'.format(
            settings['base_url'],
            settings['api_key'],
            settings['method'],
            settings['result_format'],
        )
        print("Alternative successful.")
        return request_url




if __name__=='__main__':

    # Settings and initial configuration
    GET_DATASET_LIST_SETTINGS = {
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


    GET_DATASET_PARAMS_SETTINGS = {
        'api_key': '3924A4B4-43A0-4BE6-B131-650F0740C025',
        'base_url': 'https://www.bea.gov/api/data/',
        'method': 'getparameterlist',
        'datasetname': 'GETDATASETLIST',
        'result_format': 'JSON',
        'node_hierarchy': collections.OrderedDict({
            'root_node': 'BEAAPI',
            'child_node_one': 'Results',
            'child_node_two': 'Parameter',
        })
    }

    url = build_url(settings=GET_DATASET_LIST_SETTINGS)
    response = requests.get(url).json()

    # Calls
    json_response = request_and_unpack_json(
        request_url=url,
        node_hierarchy=GET_DATASET_LIST_SETTINGS['node_hierarchy']
    )

    dataset_list = [dataset.get('DatasetName') for dataset in json_response]
    print(dataset_list)
    # json_to_excel(
    #     output_file_path=r'C:\Users\eirik\Desktop\metadata.xlsx',
    #     output_spreadsheet_name=bea_request_settings['datasetname'],
    #     json_data=json_response,
    #     json_orientation='records'
    # )
