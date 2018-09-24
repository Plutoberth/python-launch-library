from launchlibrary import Api
from launchlibrary.models import *
from functools import lru_cache


class BaseAsync(BaseModel):
    def __init__(self,  param_translations: dict, api_instance: Api, proper_name: str):
        # Gotta use explicit params for it to work correctly
        super().__init__(param_translations, api_instance, proper_name)

    @classmethod
    async def fetch(cls, api_instance: Api, **kwargs):
        """
        The fetch method implements fetch with an async HTTP GET function.

        :param api_instance: An instance of the api
        :param kwargs: args for the api call
        :return: objects based on BaseAsync
        """

        kwargs = utils.sanitize_input(kwargs)

        json_object = await api_instance.async_send_message(cls._endpoint_name, kwargs)

        classes = cls._create_classes(api_instance, json_object)

        return classes


# All async models should be based on this, and all functions that use fetch should be reimplemented
class AsyncAgencyType(AgencyType, BaseAsync):
    """A class representing an async agency type object."""
    pass


class AsyncAgency(Agency, BaseAsync):
    """A class representing an async agency object."""

    @lru_cache(maxsize=None)
    async def get_type(self) -> list:
        if self.type:
            agency_type = await AsyncAgencyType.fetch(self.api_instance, id=self.type)
        else:
            agency_type = []

        return agency_type[0] if len(agency_type) == 1 else AgencyType.init_from_json(self.api_instance, {})


class AsyncLaunchStatus(LaunchStatus, BaseAsync):
    """A class representing an async launch status object."""
    pass


class AsyncLaunch(Launch, BaseAsync):
    """A class representing an async launch object."""

    @classmethod
    async def next(cls, api_instance: Api, num: int):
        """
        A simple abstraction method to get the next {num} launches.
        :param api_instance: An instance of launchlibrary.Api
        :param num: a number for the number of launches
        """
        return await cls.fetch(api_instance, next=num, status=1)

    @lru_cache(maxsize=None)
    async def get_status(self) -> LaunchStatus:
        """Returns the LaunchStatus model for the corresponding status."""
        if self.status:
            launch_status = LaunchStatus.fetch(self.api_instance, id=self.status)
        else:
            launch_status = []  # to let the ternary init an empty model

        # To avoid attribute errors on the user's side, if the status is not found simply create an empty one.
        return launch_status[0] if len(launch_status) == 1 else LaunchStatus.init_from_json(self.api_instance, {})


class AsyncPad(Pad, BaseAsync):
    """A class representing an async pad object."""
    pass


class AsyncLocation(Location, BaseAsync):
    """A class representing an async Location object."""
    pass


class AsyncRocketFamily(RocketFamily, BaseAsync):
    """A class representing an async rocket family."""
    pass


class AsyncRocket(Rocket, BaseAsync):
    """A class representing an async rocket."""

    @lru_cache(maxsize=None)
    async def get_pads(self) -> List[AsyncPad]:
        """Returns Pad type objects of the pads the rocket uses."""
        pad_objs = []
        if self.default_pads:
            pad_objs = await AsyncPad.fetch(self.api_instance, id=self.default_pads)

        return pad_objs