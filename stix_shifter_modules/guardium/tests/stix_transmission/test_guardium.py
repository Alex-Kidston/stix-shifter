from stix_shifter_modules.guardium.entry_point import EntryPoint
from stix_shifter_modules.guardium.stix_transmission.api_client import ClientResponse
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import Status
from stix_shifter.stix_transmission import stix_transmission
from tests.utils.async_utils import get_mock_response

from unittest.mock import patch
import unittest


class TestGuardiumConnection(unittest.TestCase, object):
    def test_is_async(self):
        entry_point = EntryPoint()
        check_async = entry_point.is_async()

        assert not check_async

    @patch('stix_shifter_modules.guardium.stix_transmission.api_client.APIClient.create_search', autospec=True)
    @patch('stix_shifter_modules.guardium.stix_transmission.api_client.APIClient.get_token', autospec=True)
    def test_query_response(self, mock_get_token_response, mock_query_response):
        # mock_get_token_response = None
        # mock_api_client.return_value = None
        mocked_return_value = '{"search_id": "108cb8b0-0744-4dd9-8e35-ea8311cd6211"}'
        respObj = ClientResponse()
        respObj.status_code = 200
        respObj._content = mocked_return_value
        mock_query_response.return_value = respObj
        mock_get_token_response.return_value = get_mock_response(200, mocked_return_value)

        config = {
            "auth": {
                "username": "admin",
                "password": "12345678"
            }
        }
        connection = {
            "client_id": 'WHO',
            "client_secret": "57695f99-fe23-4bb4-5116-4b7985c8532b",
            "host": "where.ibm.com",
            "port": 22,
            "selfSignedCert": False
        }

        query = '[x-ibm-finding:database_name=\'ggg\' AND  ipv4-addr:dst_ip=\'10.0.0.2\']'
        transmission = stix_transmission.StixTransmission('guardium',  connection, config)
        query_response = transmission.query(query)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == "108cb8b0-0744-4dd9-8e35-ea8311cd6211"

    @patch('stix_shifter_modules.guardium.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_status_response(self, mock_status_response):
        mocked_return_value = '{"search_id": "108cb8b0-0744-4dd9-8e35-ea8311cd6211", "status": "COMPLETED", "progress": "100"}'
        mock_status_response.return_value = get_mock_response(200, mocked_return_value)

        config = {
            "auth": {
                "username": "admin",
                "password": "12345678"
            }
        }
        connection = {
            "client_id": 'WHO',
            "client_secret": "57695f99-fe23-4bb4-5116-4b7985c8532b",
            "host": "where.ibm.com",
            "port": 22,
            "selfSignedCert": False
        }
        
        search_id = "108cb8b0-0744-4dd9-8e35-ea8311cd6211"
        transmission = stix_transmission.StixTransmission('guardium',  connection, config)
        status_response = transmission.status(search_id)

        assert status_response['success']
        assert status_response is not None
        assert 'status' in status_response
        assert status_response['status'] == Status.COMPLETED.value

