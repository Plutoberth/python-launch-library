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

        global DO_UNIDECODE
        # I know that this is super hacky, but it'll work for almost all users.
        # Fix it and submit a PR if you care.
        DO_UNIDECODE = unicode

    def fetch_agencytype(self, **kwargs):
        """Fetch from the AgencyType endpoint"""
        return AgencyType.fetch(self.network, **kwargs)

    def fetch_agency(self, **kwargs):
        """Fetch from the Agency endpoint"""
        return Agency.fetch(self.network, **kwargs)

    def fetch_launch(self, **kwargs):
        """Fetch from the Launch endpoint"""
        return Launch.fetch(self.network, **kwargs)

    def next_launches(self, num: int) -> List[Launch]:
        """
        Get the next {num} launches.

        :param num: a number for the number of launches
        """
        return Launch.next(self.network, num)

    def fetch_launchstatus(self, **kwargs):
        """Fetch from the LaunchStatus endpoint"""
        return LaunchStatus.fetch(self.network, **kwargs)

    def fetch_pad(self, **kwargs):
        """Fetch from the Pad endpoint"""
        return Pad.fetch(self.network, **kwargs)

    def fetch_location(self, **kwargs):
        """Fetch from the Location endpoint"""
        return Location.fetch(self.network, **kwargs)

    def fetch_rocketfamily(self, **kwargs):
        """Fetch from the RocketFamily endpoint"""
        return RocketFamily.fetch(self.network, **kwargs)

    def fetch_rocket(self, **kwargs):
        """Fetch from the Rocket endpoint"""
        return Rocket.fetch(self.network, **kwargs)

    # Async fetchers

    async def async_fetch_agencytype(self, **kwargs):
        """Fetch from the AgencyType endpoint"""
        return await AsyncAgencyType.fetch(self.network, **kwargs)

    async def async_fetch_agency(self, **kwargs):
        """Fetch from the Agency endpoint"""
        return await AsyncAgency.fetch(self.network, **kwargs)

    async def async_fetch_launch(self, **kwargs):
        """Fetch from the Launch endpoint"""
        return await AsyncLaunch.fetch(self.network, **kwargs)

    async def async_next_launches(self, num: int) -> List[AsyncLaunch]:
        """
        Get the next {num} launches.

        :param num: a number for the number of launches
        """
        return await AsyncLaunch.next(self.network, num)

    async def async_fetch_launchstatus(self, **kwargs):
        """Fetch from the LaunchStatus endpoint"""
        return await AsyncLaunchStatus.fetch(self.network, **kwargs)

    async def async_fetch_pad(self, **kwargs):
        """Fetch from the Pad endpoint"""
        return await AsyncPad.fetch(self.network, **kwargs)

    async def async_fetch_location(self, **kwargs):
        """Fetch from the Location endpoint"""
        return await AsyncLocation.fetch(self.network, **kwargs)

    async def async_fetch_rocketfamily(self, **kwargs):
        """Fetch from the RocketFamily endpoint"""
        return await AsyncRocketFamily.fetch(self.network, **kwargs)

    async def async_fetch_rocket(self, **kwargs):
        """Fetch from the Rocket endpoint"""
        return await AsyncRocket.fetch(self.network, **kwargs)
