# Copyright 2018 Nir Harel
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
# limitations under the License.

import requests
import json
from launchlibrary import exceptions as ll_exceptions

DEFAULT_API_URL = "https://launchlibrary.net"
DEFAULT_VERSION = "1.4"


class Api:
    def __init__(self, api_url=DEFAULT_API_URL, version=DEFAULT_VERSION, fail_silently=True, retries=5):
        """
        :param api_url: The URL of the launchlibrary website.
        :param version: Version of the api
        :param fail_silently: Set to false to raise exceptions when they occur.
        :param retries: The maximum amount of retries for requests that timed out.
        """
        # CURRENTLY STUCK ON VERBOSE
        self.mode = "verbose"  # Pick between verbose, list, and summary. Data decreases from verbose to list.

        # These probably shouldn't be changed unless the site changed its address. The wrapper may not work as well
        # with a different version than the default one.
        self.url = "/".join([api_url, version])

        self.fail_silently = fail_silently

    def parse_data(self, data: dict) -> str:
        """
        Parse data as get parameters.
        :param data: A dictionary containing key value pairs
        :return
        """
        return "?mode={}&".format(self.mode) + "&".join([f"{k}={v}" for k, v in data.items()])

    def send_message(self, endpoint, data):
        request_url = "/".join([self.url, endpoint]) + self.parse_data(data)
        try:
            resp = requests.get(request_url)
            if resp.status_code == '404':  # If it didn't find anything
                raise ll_exceptions.ApiException  # raise an api exception
            resp_dict = resp.json()

        except (requests.exceptions.RequestException, json.JSONDecodeError,
                ll_exceptions.ApiException) as e:  # Catch all exceptions from the module
            print(f"Failed while retrieving API details. \nRequest url: {request_url}")
            if not self.fail_silently:
                raise e
            else:  # If it fails silently, it should just return an empty dictionary.
                resp_dict = {}

        return resp_dict  # Returns a json style object of the response.
