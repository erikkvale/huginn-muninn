"""
BEA API:

This module contains specifics based on the current documentation,
to make calls and consume the data released by the BEA.
"""
import requests
import json
import pandas
from pprint import pprint
from settings import DATASET_LIST_SETTINGS



def request_and_unpack_json(request_url, node_hierarchy, return_json=True):
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
    if return_json:
        return json.dumps(json_response)
    else:
        return json_response


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


    url = build_url(settings=DATASET_LIST_SETTINGS)
    response = requests.get(url).json()

    # Calls
    json_response = request_and_unpack_json(
        request_url=url,
        node_hierarchy=DATASET_LIST_SETTINGS['node_hierarchy'],
        return_json=False
    )
    dataset_list = [item['DatasetName'] for item in json_response]

    
    # pprint(json.loads(json_response))
    # json_to_excel(
    #     output_file_path=r'C:\Users\eirik\Desktop\metadata.xlsx',
    #     output_spreadsheet_name=bea_request_settings['datasetname'],
    #     json_data=json_response,
    #     json_orientation='records'
    # )
