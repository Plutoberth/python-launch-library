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

from .models import *
from .async_models import *
from .constants import *
from typing import List


class Api:
    def __init__(self, api_url: str = DEFAULT_LL_URL, version: str = DEFAULT_VERSION, unicode: bool = True):
        """
        The API class for the launchlibrary module.

        :param api_url: The URL of the launchlibrary website.
        :param version: Version of the api
        :param unicode: Set to False to convert unicode characters to ASCII using unidecode.
        """

        # These probably shouldn't be changed unless the site changed its address. The wrapper may not work as well
        # with a different version than the default one.
        url = "/".join([api_url, version])
        self.network = Network(url, "verbose")
        self.unicode = unicode

    def fetch_agencytype(self, **kwargs):
        return AgencyType.fetch(self.network, **kwargs)

    def fetch_agency(self, **kwargs):
        return Agency.fetch(self.network, **kwargs)

    def fetch_launch(self, **kwargs):
        return Launch.fetch(self.network, **kwargs)

    def next_launches(self, num: int) -> List[Launch]:
        """
        Get the next {num} launches.

        :param num: a number for the number of launches
        """
        return Launch.next(self.network, num)

    def fetch_launchstatus(self, **kwargs):
        return LaunchStatus.fetch(self.network, **kwargs)

    def fetch_pad(self, **kwargs):
        return Pad.fetch(self.network, **kwargs)

    def fetch_location(self, **kwargs):
        return Location.fetch(self.network, **kwargs)

    def fetch_rocketfamily(self, **kwargs):
        return RocketFamily.fetch(self.network, **kwargs)

    def fetch_rocket(self, **kwargs):
        return Rocket.fetch(self.network, **kwargs)

    # Async fetchers

    async def async_fetch_agencytype(self, **kwargs):
        return AsyncAgencyType.fetch(self.network, **kwargs)

    async def async_fetch_agency(self, **kwargs):
        return AsyncAgency.fetch(self.network, **kwargs)

    async def async_fetch_launch(self, **kwargs):
        return AsyncLaunch.fetch(self.network, **kwargs)

    async def async_next_launches(self, num: int) -> List[AsyncLaunch]:
        """
        Get the next {num} launches.

        :param num: a number for the number of launches
        """
        return await AsyncLaunch.next(self.network, num)

    async def async_fetch_launchstatus(self, **kwargs):
        return AsyncLaunchStatus.fetch(self.network, **kwargs)

    async def async_fetch_pad(self, **kwargs):
        return AsyncPad.fetch(self.network, **kwargs)

    async def async_fetch_location(self, **kwargs):
        return AsyncLocation.fetch(self.network, **kwargs)

    async def async_fetch_rocketfamily(self, **kwargs):
        return AsyncRocketFamily.fetch(self.network, **kwargs)

    async def async_fetch_rocket(self, **kwargs):
        return AsyncRocket.fetch(self.network, **kwargs)
