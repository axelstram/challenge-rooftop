import requests
import json
import sys

class RooftopAPI():

    def __init__(self, token):
        self.token = token
        self.headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

    def getBlocks(self):
        url = "https://rooftop-career-switch.herokuapp.com/blocks?token="
        response = requests.get(url + self.token)
        blocks = response.json()["data"]
        
        if response.status_code != 200:
            raise Exception(f"blocks endpoint failed with code {response.status_code}")

        return blocks

    def checkIfBlocksAreContiguous(self, first_block, second_block):
        url = "https://rooftop-career-switch.herokuapp.com/check?token="
        payload = {"blocks": [first_block, second_block]}
        response = requests.post(url + self.token, data=json.dumps(payload), headers=self.headers)
        blocks_are_contiguous = response.json()["message"]

        if response.status_code != 200:
            raise Exception(f"check endpoint failed with code {response.status_code}")

        return blocks_are_contiguous

    def checkIfBlocksAreCorrectlySorted(self, blocks):
        url = "https://rooftop-career-switch.herokuapp.com/check?token="
        payload = {"encoded": blocks}
        response = requests.post(url + self.token, data=json.dumps(payload), headers=self.headers)
        is_correct = response.json()["message"]

        if response.status_code != 200:
            raise Exception(f"check endpoint failed with code {response.status_code}")

        return is_correct


def generateCache(blocks, token):
    #if "a" and "b" are contiguous, it will store "a" as key and "b" as value. 
    #last block has "FINAL" as value
    rooftopAPI = RooftopAPI(token)
    cache = {}
    total_api_calls = 0

    #Call "check" endpoint and fill the cache.
    for i in range(len(blocks)):
        first_block = blocks[i]

        #First block is already in the correct position, so it will never be the contiguous block of any other block.
        for j in range(1, len(blocks)):
            if i != j:
                second_block = blocks[j]

                if second_block in cache.values():
                    continue

                blocks_are_contiguous = rooftopAPI.checkIfBlocksAreContiguous(first_block, second_block)
                total_api_calls += 1

                if blocks_are_contiguous:
                    cache[first_block] = second_block
                    break
                
                #If it made it to the end, then first_block has no contiguous block, therefore it's the last one.
                cache[first_block] = "FINAL"

    print(f"Total API calls: {total_api_calls}")

    return cache


def check(blocks, token):
    cache = generateCache(blocks, token)

    ordered_blocks = []
    ordered_blocks.append(blocks[0]) #First one already in the correct order.

    for i in range(1, len(blocks)):
        next_block_in_order = cache[ordered_blocks[-1]]
        ordered_blocks.append(next_block_in_order)

    return ordered_blocks
    


def main():

    if len(sys.argv) > 1:
        token = sys.argv[1]
    else:
        raise Exception("A token needs to be provided")

    rooftopAPI = RooftopAPI(token)

    blocks = rooftopAPI.getBlocks()
    sorted_blocks = check(blocks, token)
    sorted_blocks_appended = ''.join(sorted_blocks)
    result = rooftopAPI.checkIfBlocksAreCorrectlySorted(sorted_blocks_appended)

    print(f"Blocks were sorted in order: {result}")

    return result

if __name__ == '__main__':
    main()