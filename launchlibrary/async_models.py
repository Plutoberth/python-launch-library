from launchlibrary import Api
from launchlibrary.models import *
from functools import lru_cache


class BaseAsync(BaseModel):
    def __init__(self, *args):
        super().__init__(args)

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


class asyncAgency(BaseAsync, Agency):
    """A class representing an async agency object."""

    @lru_cache(maxsize=None)
    async def get_type(self) -> list:
        if self.type:
            agency_type = await AsyncAgencyType.fetch(self.api_instance, id=self.type)
        else:
            agency_type = []

        return agency_type[0] if len(agency_type) == 1 else AgencyType.init_from_json(self.api_instance, {})


class AsyncLaunchStatus(BaseAsync, Agency):
    """A class representing an async lauch status object."""
    pass

