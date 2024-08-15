"""
CST8333 Programming Language Research Project
Practical Project Part 02
Student Name: Ka Yan Ieong
Student No.: 041070033

This py file is for unit testing.
"""

import pytest
from src.data_model import TrafficDataModel, TrafficVolumesData

# Mock data for reading records unit testing
mock_headers = ['Header1', 'Header2', 'Header3']
mock_data = [
    TrafficVolumesData(mock_headers, {'Header1': 'Value1', 'Header2': 'Value2', 'Header3': 'Value3'}),
    TrafficVolumesData(mock_headers, {'Header1': 'Value4', 'Header2': 'Value5', 'Header3': 'Value6'}),
    TrafficVolumesData(mock_headers, {'Header1': 'Value7', 'Header2': 'Value8', 'Header3': 'Value9'})
]


@pytest.fixture
def traffic_data_model_parse_data_to_object():
    # mock the headers retrieval operation
    model = TrafficDataModel(file_path='dummy.csv')
    # parse the mock data list as object list
    model.objects_list = mock_data
    return model


def test_read_by_row_number_valid(traffic_data_model_parse_data_to_object):
    model = traffic_data_model_parse_data_to_object
    result = model.read_by_row_numbers('1')
    assert result[0].header1 == 'Value1'
    assert result[0].header2 == 'Value2'
    assert result[0].header3 == 'Value3'
    print('test_read_by_row_number_valid passed')
    print('Test is done by Ka Yan Ieong - 041070033')


def test_read_by_row_number_invalid(traffic_data_model_parse_data_to_object):
    model = traffic_data_model_parse_data_to_object
    result = model.read_by_row_numbers('4')
    assert result == []
    print('test_read_by_row_number_invalid passed')
    print('Test is done by Ka Yan Ieong - 041070033')


def test_read_by_row_number_boundary(traffic_data_model_parse_data_to_object):
    model = traffic_data_model_parse_data_to_object
    result = model.read_by_row_numbers('3')
    assert result[0].header1 == 'Value7'
    assert result[0].header2 == 'Value8'
    assert result[0].header3 == 'Value9'
    print('test_read_by_row_number_boundary passed')
    print('Test is done by Ka Yan Ieong - 041070033')

def test_read_two_rows(traffic_data_model_parse_data_to_object):
    model = traffic_data_model_parse_data_to_object
    result = model.read_by_row_numbers('1', '2')
    assert len(result) == 2  # Ensure that two rows are returned
    assert result[0].header1 == 'Value1'
    assert result[0].header2 == 'Value2'
    assert result[0].header3 == 'Value3'
    assert result[1].header1 == 'Value4'
    assert result[1].header2 == 'Value5'
    assert result[1].header3 == 'Value6'
    print('test_read_two_rows passed')
    print('Test is done by Ka Yan Ieong - 041070033')
