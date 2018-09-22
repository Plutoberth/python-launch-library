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


DEFAULT_API_URL = "https://launchlibrary.net"
DEFAULT_VERSION = "1.4"

import requests


class Api:
    def __init__(self, mode="verbose", api_url=DEFAULT_API_URL, version=DEFAULT_VERSION):
        self.mode = mode  # Pick between verbose, list, and summary. Data decreases from verbose to summary.

        # These probably shouldn't be changed unless the site changed its address. The wrapper may not work as well
        # with a different version than the default one.
        self.url = "/".join([api_url, version])

    @staticmethod
    def parse_data(data: dict) -> str:
        """
        Parse data as get parameters.
        :param data: A dictionary containing key value pairs
        :return
        """
        return "?" + "?".join([f"{k}={v}" for k, v in data.items()])

    def send_message(self, endpoint, data):
        request_url = "/".join([self.url, endpoint]) + self.parse_data(data)
        print(request_url)
        try:
            resp = requests.get(request_url)
        except requests.exceptions.RequestException as e:  # Catch all exceptions from the module
            print(f"Failed with requests exception {e}. \nUrl: {request_url}")
            raise e

        return resp.json()  # Returns a json style object of the response.


