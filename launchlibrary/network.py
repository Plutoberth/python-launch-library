# Copyright 2020 Nir Harel
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
import asyncio

import aiohttp
import aiohttp.web
import requests
from .constants import *
from launchlibrary import exceptions as ll_exceptions


class Network:
    def __init__(self, url=DEFAULT_API_URL, mode="verbose"):
        self.url = url
        self.mode = mode
        self.sess = aiohttp.ClientSession(raise_for_status=True)

    def _get_url(self, endpoint, data: dict) -> str:
        """
        Parse the data as GET parameters and return it as a proper request url.

        :param data: A dictionary containing values for the api call.
        :return: A proper GET param string
        """
        params = "?mode={}&".format(self.mode) + "&".join(["{}={}".format(k, v) for k, v in data.items()])
        return "/".join([self.url, endpoint]) + params

    def send_message(self, endpoint: str, data: dict) -> dict:
        """
        Send synchronous messages

        :param endpoint:  The api endpoint
        :param data:  A dict containing data for the request
        :return:  response dict.
        """
        request_url = self._get_url(endpoint, data)
        try:
            resp = requests.get(request_url)
            resp.raise_for_status()
            resp_dict = resp.json()

        # Don't leak implementation details
        except requests.exceptions.Timeout as e:
            raise ll_exceptions.TimeoutException(str(e))
        except requests.exceptions.HTTPError as e:
            raise ll_exceptions.ApiException(str(e))
        except requests.exceptions.RequestException as e:
            raise ll_exceptions.NetworkException(str(e))

        return resp_dict  # Returns a json style object of the response.

    async def async_send_message(self, endpoint: str, data: dict):
        """
        Send asynchronous messages

        :param endpoint:  The api endpoint
        :param data:  A dict containing data for the request
        :return:  response dict.
        """
        request_url = self._get_url(endpoint, data)
        try:
            async with self.sess.get(request_url) as resp:
                resp_dict = await resp.json()

        # Don't leak implementation details
        except asyncio.TimeoutError as e:
            raise ll_exceptions.TimeoutException(str(e))
        except aiohttp.web.HTTPClientError as e:
            raise ll_exceptions.ApiException(str(e))
        except aiohttp.ClientError as e:
            raise ll_exceptions.NetworkException(str(e))

        return resp_dict  # Returns a json style object of the response.

    # For lru_cache. We're not hashing the sess because it doesn't affect responses
    def __hash__(self):
        return hash((self.url, self.mode))
