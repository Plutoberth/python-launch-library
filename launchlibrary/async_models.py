from launchlibrary import Api
from launchlibrary.models import *


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
        pass


# All async models should be based on this, and all functions that use fetch should be reimplemented
class AgencyType(BaseAsync, AgencyType):
    def __init__(self, api_instance: Api):
        super().__init__(api_instance)
