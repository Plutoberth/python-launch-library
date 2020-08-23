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
class AsyncAgencyType(AgencyType, BaseAsync):
    """A class representing an async agency type object."""
    pass


class AsyncAgency(Agency, BaseAsync):
    """A class representing an async agency object."""

    @staticmethod
    @alru_cache()
    async def _get_type_for_id(network: Network, type_id):
        """
        Separated into a different function because we only care about type_id and the version endpoint for caching
        """
        return await AsyncAgencyType.fetch(network, id=type_id)

    async def get_type(self) -> list:
        if self.type:
            agency_type = await AsyncAgency._get_type_for_id(self.network, self.type)
        else:
            agency_type = []

        return agency_type[0] if len(agency_type) == 1 else AgencyType.init_from_json(self.network, {})


class AsyncLaunchStatus(LaunchStatus, BaseAsync):
    """A class representing an async launch status object."""
    pass


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

    @staticmethod
    @alru_cache()
    async def _get_status_for_id(network: Network, status_id):
        """
        Separating it to a different function allows lru_cache to only care about the network and id parameters.
        These are the only ones that matter for this operation.
        """
        return await AsyncLaunchStatus.fetch(network, id=status_id)

    async def get_status(self) -> AsyncLaunchStatus:
        """Returns the LaunchStatus model for the corresponding status."""
        if self.status:
            launch_status = await AsyncLaunch._get_status_for_id(self.network, self.status)
        else:
            launch_status = []  # to let the ternary init an empty model

        # To avoid attribute errors on the user's side, if the status is not found simply create an empty one.
        return launch_status[0] if len(launch_status) == 1 else AsyncLaunchStatus.init_from_json(self.network, {})


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
