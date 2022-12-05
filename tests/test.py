import sys
sys.path.append(".")
from src.main import RooftopAPI, check, main
import unittest
import json
import random
from unittest import mock
import sys


ordered_blocks = ["f319", "46ec", "c1c7", "3720", "c7df", "c4ea", "4e3e", "80fd"]


def mocked_requests_get(*args, **kwargs):

    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    shuffled_blocks = list(ordered_blocks)
    random.shuffle(shuffled_blocks)
    shuffled_blocks.remove("f319")
    shuffled_blocks.insert(0, "f319")

    return MockResponse({"data": shuffled_blocks}, 200)

def mocked_requests_post(*args, **kwargs):

    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
            

        def json(self):
            return self.json_data

    #check if contiguos
    if "blocks" in kwargs['data']:
        blocks = json.loads(kwargs['data'])['blocks']

        for i in range(len(ordered_blocks) - 1):
            if ordered_blocks[i] == blocks[0] and ordered_blocks[i+1] == blocks[1]:
                return MockResponse({"message": True}, 200)

        return MockResponse({"message": False}, 200)

    elif "encoded" in kwargs['data']:
        concatenated_blocks = json.loads(kwargs['data'])['encoded']

        if concatenated_blocks == ''.join(ordered_blocks):
            return MockResponse({"message": True}, 200)
        else:
            return MockResponse({"message": False}, 400)
    else:
        return MockResponse({"message": False}, 400)

    

class RooftopChallengeTestCase(unittest.TestCase):

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def testThatCheckFunctionSortsTheBlocksCorrectly(self, mock_get, mock_post):
        
        token = "aToken"
        rooftopAPI = RooftopAPI(token)

        blocks = rooftopAPI.getBlocks()
        sorted_blocks = check(blocks, token)

        assert sorted_blocks == ordered_blocks

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def testThatMainProgramDeliversTheSolutionInTheCorrectFormat(self, mock_get, mock_post):
    
        sys.argv[1] = "aToken"
        result = main()

        assert result == True

if __name__ == '__main__':
    unittest.main()