from launchlibrary.models import *
from async_lru import alru_cache
from .network import Network


class BaseAsync(BaseModel):
    def __init__(self, network: Network, param_translations: dict, proper_name: str):
        # Gotta use explicit params for it to work correctly
        super().__init__(network, param_translations, proper_name)

    @classmethod
    async def fetch(cls, network: Network, **kwargs):
        """
        The fetch method implements fetch with an async HTTP GET function.

        :param network: A network instance
        :param kwargs: args for the api call
        :return: objects based on BaseAsync
        """

        kwargs = utils.sanitize_input(kwargs)

        json_object = await network.async_send_message(cls._endpoint_name, kwargs)

        classes = cls._create_classes(network, json_object)
        return classes


# All async models should be based on this, and all functions that use fetch should be reimplemented
class AsyncAgency(Agency, BaseAsync):
    """A class representing an async agency object."""


class AsyncLaunch(Launch, BaseAsync):
    """A class representing an async launch object."""

    @classmethod
    async def next(cls, network: Network, num: int):
        """
        Get the next {num} launches.

        :param network: A network instance

        :param num: a number for the number of launches
        """
        return await cls.fetch(network, next=num, status=1)


class AsyncPad(Pad, BaseAsync):
    """A class representing an async pad object."""
    pass


class AsyncLocation(Location, BaseAsync):
    """A class representing an async Location object."""
    pass


class AsyncRocket(Rocket, BaseAsync):
    """A class representing an async rocket."""

    @staticmethod
    @alru_cache()
    async def _get_pads_for_id(network: Network, pads: str):
        return await AsyncPad.fetch(network, id=pads)

    async def get_pads(self) -> List[AsyncPad]:
        """Returns Pad type objects of the pads the rocket uses."""
        pad_objs = []
        if self.default_pads:
            pad_objs = await AsyncRocket._get_pads_for_id(self.network, self.default_pads)

        return pad_objs
