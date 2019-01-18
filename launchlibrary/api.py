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
import aiohttp

DEFAULT_API_URL = "https://launchlibrary.net"
DEFAULT_VERSION = "1.4"


class Api:
    def __init__(self, api_url: str=DEFAULT_API_URL, version: str=DEFAULT_VERSION, fail_silently: bool=True,
                 retries: int=5, unicode: bool=True):
        """
        The API class for the launchlibrary module.

        :param api_url: The URL of the launchlibrary website.
        :param version: Version of the api
        :param fail_silently: Set to false to raise exceptions when they occur. Useful for debugging.
        :param retries: The maximum amount of retries for requests that time out.
        :param unicode: Set to False to convert unicode characters to ASCII using unidecode.
        """
        # CURRENTLY STUCK ON VERBOSE
        self.mode = "verbose"  # Pick between verbose, list, and summary. Data decreases from verbose to list.

        # These probably shouldn't be changed unless the site changed its address. The wrapper may not work as well
        # with a different version than the default one.
        self.url = "/".join([api_url, version])
        self.fail_silently = fail_silently
        self.retries = retries
        self.unicode = unicode

    def _get_url(self, endpoint, data: dict) -> str:
        """
        Parse the data as GET parameters and return it as a proper request url.

        :param data: A dictionary containing values for the api call.
        :return: A proper GET param string
        """
        params = "?mode={}&".format(self.mode) + "&".join(["{}={}".format(k, v) for k, v in data.items()])
        return "/".join([self.url, endpoint]) + params

    def _dispatch(self, endpoint: str, data: dict) -> dict:
        request_url = self._get_url(endpoint, data)
        try:
            resp = requests.get(request_url)
            if resp.status_code != 200:  # If the request failed for some reason
                raise ll_exceptions.ApiException(
                    "API call to `{}` responded with code `{}`\n"
                    "Complete API response: `{}`".format(request_url, resp.status_code, resp.text)
                )  # raise an api exception
            resp_dict = resp.json()

        except (requests.exceptions.RequestException, json.JSONDecodeError,
                ll_exceptions.ApiException) as e:  # Catch all exceptions from the module

            if isinstance(e, requests.exceptions.ConnectTimeout):
                raise e  # We want to raise this error to allow send_message to retry.

            if self.fail_silently:
                # If it should fail silently, it should just return an empty dictionary.
                resp_dict = {}
            else:
                raise e

        return resp_dict  # Returns a json style object of the response.

    def send_message(self, endpoint: str, data: dict) -> dict:
        """
        A wrapper function for dispatch. Allows us to retry on timeouts.

        :param endpoint:  The api endpoint
        :param data:  A dict containing data for the request
        :return:  response dict.
        """
        attempts = self.retries
        resp = {}

        while attempts >= 1:
            try:
                resp = self._dispatch(endpoint, data)
                break  # It will not reach this line if it gets a ConnectTimeout
            except requests.exceptions.ConnectTimeout:
                attempts -= 1

        return resp

    # I know that having two completely separate functions is messy, but it was necessary.
    async def _async_dispatch(self, endpoint: str, data: dict) -> dict:
        request_url = self._get_url(endpoint, data)
        try:
            async with aiohttp.ClientSession() as sess:
                async with sess.get(request_url) as resp:
                    resp_dict = await resp.json()

            if resp.status != 200:  # If the request failed for some reason
                raise ll_exceptions.ApiException  # raise an api exception

        except (aiohttp.ClientError, json.JSONDecodeError,
                ll_exceptions.ApiException) as e:  # Catch all exceptions from the module

            if isinstance(e, aiohttp.ClientTimeoutError):
                raise e  # We want to raise this error to allow send_message to retry.

            print("Failed while retrieving API details. \nRequest url: {}".format(request_url))
            if self.fail_silently:
                # If it should fail silently, it should just return an empty dictionary.
                resp_dict = {}
            else:
                raise e

        return resp_dict  # Returns a json style object of the response.

    async def async_send_message(self, endpoint: str, data: dict):
        """
        A wrapper function for _async_dispatch. Allows us to retry on timeouts with async.

        :param endpoint:  The api endpoint
        :param data:  A dict containing data for the request
        :return:  response dict.
        """
        attempts = self.retries
        resp = {}

        while attempts >= 1:
            try:
                resp = await self._async_dispatch(endpoint, data)
                break  # It will not reach this line if it gets a ConnectTimeout
            except aiohttp.ClientTimeoutError:
                attempts -= 1

        return resp
