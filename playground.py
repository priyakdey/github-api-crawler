# Script to test things
import time
from datetime import datetime

import requests
from ratelimit import limits, sleep_and_retry

# Testing ratelimit
# Create mock response from : https://designer.mocky.io/
mock_url = "https://run.mocky.io/v3/e0372b06-9050-444d-83eb-754b0a7cdc05"


def send_request(i):
    response = requests.get(mock_url)
    print("Request No:", i, "Received at:", datetime.now(), "Data received: ", response.json())
    time.sleep(5)  # So per minute ~ 12 requests should go through


@sleep_and_retry
@limits(calls=2, period=30)
def send_limited_request(i):
    response = requests.get(mock_url)
    print("Request No:", i, "Received at:", datetime.now(), "Data received: ", response.json())
    # So per minute ~ 12 requests should go through, but since limited, only 2 calls per 30 seconds can go
    time.sleep(5)


def main():
    for i in range(1, 21):
        # send_request(i)
        send_limited_request(i)


main()
