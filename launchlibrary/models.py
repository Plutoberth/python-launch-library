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

from unidecode import unidecode
from dateutil import parser
from dateutil import relativedelta
from functools import lru_cache
import datetime
from typing import List
from launchlibrary import utils
from .network import Network

# Set default dt to the beginning of next month
DEFAULT_DT = datetime.datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0) \
             + relativedelta.relativedelta(months=1)

DO_UNIDECODE = False


class BaseModel:
    """The base model class all models should inherit from. Provides fetch and other utility functionalities.

    :_endpoint_name: The endpoint to use in the api
    :_nested_name:  The name of that will appear in nested results. "Agencies" and the such.

    =========  ===========
    Operation  Description
    ---------  -----------
    x == y     Checks if both objects are of the same type and have the same id.
    =========  ===========
    """

    _endpoint_name = ""
    _nested_name = ""

    def __init__(self, network: Network, param_translations: dict, proper_name: str):
        """
        All launchlibrary models should inherit from this class. Contains utility and fetch functions.

        :param network:  An instance of the Api class.
        :param param_translations:  Translations from API names to pythonic names.
        :param proper_name:  The proper name for use in __repr__
        """

        self.network = network
        # param translations serves both for pythonic translations and default param values
        self._param_translations = param_translations
        self.proper_name = proper_name
        self.param_names = self._param_translations.values()

    @classmethod
    def fetch(cls, network: Network, **kwargs) -> list:
        """
        Initializes a class, or even a list of them from the api using the needed params.

        :param network: An instance of the network class
        :param kwargs: Arguments to include in the GET request
        """

        kwargs = utils.sanitize_input(kwargs)

        json_object = network.send_message(cls._endpoint_name, kwargs)

        classes = cls._create_classes(network, json_object)

        return classes

    @classmethod
    def init_from_json(cls, network: Network, json_object: dict):
        """
        Initializes a class from a json object. Only single classes.

        :param network: launchlibrary.Network
        :param json_object: An object containing the "entry" we want to init.
        :return: cls
        """
        cls_init = cls(network)
        cls_init._set_params_json(json_object)
        cls_init._postprocess()
        return cls_init

    @classmethod
    def _create_classes(cls, network: Network, json_object) -> list:
        """
        Creates the required classes from the json object.

        :param network:
        :param json_object:
        :return:
        """

        classes = []
        for entry in json_object.get(cls._nested_name, []):
            cls_init = cls(network)
            cls_init._set_params_json(entry)
            cls_init._postprocess()
            classes.append(cls_init)

        return classes

    def _set_params_json(self, json_object: dict):
        """Sets the parameters of a class from an object (raw data, not inside "agencies" for example)"""
        self._modelize(json_object)
        for api_name, pythonic_name in self._param_translations.items():
            data = json_object.get(api_name, None)
            # If the data is a string, and the unicode option is set to false
            if isinstance(data, str) and DO_UNIDECODE:
                data = unidecode(data)

            setattr(self, pythonic_name, data)

    def _modelize(self, json_object):
        """Recursively goes over the json object, looking for any compatible models. It's recursive in an indirect
        way (through set_params_json)."""

        for key, val in json_object.items():
            if key in MODEL_LIST_PLURAL.keys():
                if val and isinstance(val, list):
                    if len(val) > 0:
                        json_object[key] = [MODEL_LIST_PLURAL[key].init_from_json(self.network, r) for r in val]
            elif key in MODEL_LIST_SINGULAR.keys():  # if it is a singular
                if val and isinstance(val, dict):
                    if len(val) > 0:
                        json_object[key] = MODEL_LIST_SINGULAR[key].init_from_json(self.network, val)

    def _postprocess(self):
        """Optional method. May be used for model specific operations (like purging times)."""
        pass

    def _get_all_params(self) -> dict:
        return {k: getattr(self, k, None) for k in self.param_names}

    def __repr__(self) -> str:
        subclass_name = self.proper_name
        variables = ",".join("{}={}".format(k, v) for k, v in self._get_all_params().items())
        return "{}({})".format(subclass_name, variables)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(getattr(self, "id", None)) + hash(type(self))

    def __getattr__(self, item):
        """
        This function will allow the user to use the standard, non pythonic api names for the fields returned by the api
        It's possible that the user will want to use API names like infoURLs, instead of info_urls. We can allow this
        using our param_translation dictionaries.
        """
        if item in self._param_translations:
            return getattr(self, self._param_translations[item], None)


class AgencyType(BaseModel):
    """A class representing an agency type object."""
    _nested_name = "types"
    _endpoint_name = "agencytype"

    def __init__(self, network: Network):
        param_translations = {'id': "id", 'name': "name", 'changed': "changed"}

        self.id = None
        self.name = None
        self.changed = None

        proper_name = self.__class__.__name__

        super().__init__(network, param_translations, proper_name)


class Agency(BaseModel):
    """A class representing an agency object."""

    _nested_name = "agencies"
    _endpoint_name = "agency"

    def __init__(self, network: Network):
        param_translations = {'id': 'id', 'name': 'name', 'abbrev': 'abbrev', 'type': 'type',
                              'countryCode': 'country_code', 'wikiURL': 'wiki_url', 'infoURLs': 'info_urls',
                              'islsp': 'is_lsp', 'changed': 'changed'}

        self.id = None
        self.name = None
        self.abbrev = None
        self.type = None
        self.country_code = None
        self.wiki_url = None
        self.info_urls = None
        self.is_lsp = None
        self.changed = None

        proper_name = self.__class__.__name__

        super().__init__(network, param_translations, proper_name)

    @staticmethod
    @lru_cache()
    def _get_type_for_id(network: Network, type_id) -> List[AgencyType]:
        """
        Separated into a different function because we only care about type_id and the version endpoint for caching
        """
        return AgencyType.fetch(network, id=type_id)

    def get_type(self) -> AgencyType:
        if self.type:
            agency_type = Agency._get_type_for_id(self.network, self.type)
        else:
            agency_type = []

        # To avoid attribute errors on the user's side, if the type is not found simply create an empty one.
        return agency_type[0] if len(agency_type) == 1 else AgencyType.init_from_json(self.network, {})


class LaunchStatus(BaseModel):
    """A class representing a launch status object."""

    _nested_name = "types"
    _endpoint_name = "launchstatus"

    def __init__(self, network: Network):
        param_translations = {'id': 'id', 'name': 'name', 'description': 'description', 'changed': 'changed'}

        self.id = None
        self.name = None
        self.description = None
        self.changed = None

        proper_name = self.__class__.__name__

        super().__init__(network, param_translations, proper_name)


class Launch(BaseModel):
    """A class representing a launch object.

    You may use the **'windowstart'**, **'windowend'**, and **'net'** params to access datetime objects of the times.
    They'll be 'None' if the conversion fails.

    The comparison magic methods that are implemented essentially compare the dates of the two objects.

    =========  ===========
    Operation  Description
    ---------  -----------
    x < y      Checks if launch y occurs before launch x.
    x > y      Checks if launch x occurs before launch y.
    =========  ==========="""

    _nested_name = "launches"
    _endpoint_name = "launch"

    def __init__(self, network: Network):
        self.datetime_conversions = {}
        param_translations = {'id': 'id', 'name': 'name', 'tbddate': 'tbddate', 'tbdtime': 'tbdtime',
                              'status': 'status', 'inhold': 'inhold', 'isostart': 'windowstart', 'isoend': 'windowend',
                              'isonet': 'net', 'infoURLs': 'info_urls', 'vidURLs': 'vid_urls',
                              'holdreason': 'holdreason', 'failreason': 'failreason', 'probability': 'probability',
                              'hashtag': 'hashtag', 'lsp': 'agency', 'changed': 'changed', 'location': 'location',
                              'rocket': 'rocket', 'missions': 'missions'}

        self.id = None
        self.name = None
        self.tbddate = None
        self.tbdtime = None
        self.status = None
        self.inhold = None
        self.windowstart = None
        self.windowend = None
        self.net = None
        self.info_urls = None
        self.vid_urls = None
        self.holdreason = None
        self.failreason = None
        self.probability = None
        self.hashtag = None
        self._lsp = None
        self.changed = None
        self.location = None
        self.rocket = None
        self.missions = None

        proper_name = self.__class__.__name__

        super().__init__(network, param_translations, proper_name)

    @classmethod
    def next(cls, network: Network, num: int) -> List["Launch"]:
        """
        A simple abstraction method to get the next {num} launches.

        :param network: An instance of launchlibrary.Api

        :param num: a number for the number of launches
        """
        return cls.fetch(network, next=num, status=1)

    @staticmethod
    @lru_cache()
    def _get_status_for_id(network: Network, status_id) -> List[LaunchStatus]:
        """
        Separating it to a different function allows lru_cache to only care about the network and id parameters.
        These are the only ones that matter for this operation.
        """
        return LaunchStatus.fetch(network, id=status_id)

    def get_status(self) -> LaunchStatus:
        """Returns the LaunchStatus model for the corresponding status."""
        if self.status:
            launch_status = Launch._get_status_for_id(self.network, self.status)
        else:
            launch_status = []  # to let the ternary init an empty model

        # To avoid attribute errors on the user's side, if the status is not found simply create an empty one.
        return launch_status[0] if len(launch_status) == 1 else LaunchStatus.init_from_json(self.network, {})

    def _postprocess(self):
        """Changes times to the datetime format."""
        for time_name in ["windowstart", "windowend", "net"]:
            try:
                # Will need to modify this if we ever implement modes other than verbose
                setattr(self, time_name, parser.parse(getattr(self, time_name, "")))
            except (ValueError, TypeError):
                # The string might not contain a date, so we'll need to handle it with an empty datetime object.
                setattr(self, time_name, None)

    def __lt__(self, other: "Launch") -> bool:
        return self.net < other.net

    def __gt__(self, other: "Launch") -> bool:
        return self.net > other.net


class Pad(BaseModel):
    """A class representing a pad object."""

    _nested_name = "pads"
    _endpoint_name = "pad"

    def __init__(self, network: Network):
        param_translations = {'id': 'id', 'name': 'name', 'padType': 'pad_type', 'latitude': 'latitude',
                              'longitude': 'longitude', 'mapURL': 'map_url', 'retired': 'retired',
                              'locationid': 'locationid', 'agencies': 'agencies',
                              'wikiURL': 'wiki_url', 'infoURLs': 'info_urls'}

        self.id = None
        self.name = None
        self.pad_type = None
        self.latitude = None
        self.longitude = None
        self.map_url = None
        self.retired = None
        self.locationid = None
        self.agencies = None
        self.wiki_url = None
        self.info_urls = None

        proper_name = self.__class__.__name__

        super().__init__(network, param_translations, proper_name)


class Location(BaseModel):
    """A class representing a location object."""

    _nested_name = "locations"
    _endpoint_name = "location"

    def __init__(self, network: Network):
        param_translations = {'id': 'id', 'name': 'name', 'countrycode': 'country_code',
                              'wikiURL': 'wiki_url', 'infoURLs': 'info_urls', 'pads': 'pads'}
        # pads might be included w/ launch endpoint

        self.id = None
        self.name = None
        self.country_code = None
        self.wiki_url = None
        self.info_urls = None
        self.pads = None

        proper_name = self.__class__.__name__

        super().__init__(network, param_translations, proper_name)


class RocketFamily(BaseModel):
    """A class representing a rocket family object."""

    _nested_name = "RocketFamilies"
    _endpoint_name = "rocketfamily"

    def __init__(self, network: Network):
        param_translations = {'id': 'id', 'name': 'name', 'agencies': 'agencies', 'changed': 'changed'}

        self.id = None
        self.name = None
        self.agencies = None
        self.changed = None

        proper_name = self.__class__.__name__

        super().__init__(network, param_translations, proper_name)


class Rocket(BaseModel):
    """A class representing a rocket object."""

    _nested_name = "rockets"
    _endpoint_name = "rocket"

    def __init__(self, network: Network):
        param_translations = {'id': 'id', 'name': 'name', 'defaultPads': 'default_pads', 'family': 'family',
                              'wikiURL': 'wiki_url', 'infoURLs': 'info_urls', 'imageURL': 'image_url',
                              'imageSizes': 'image_sizes'}

        self.id = None
        self.name = None
        self.default_pads = None
        self.family = None
        self.wiki_url = None
        self.info_urls = None
        self.image_url = None
        self.image_sizes = None

        proper_name = self.__class__.__name__

        super().__init__(network, param_translations, proper_name)

    @staticmethod
    @lru_cache()
    def _get_pads_for_id(network: Network, pads: str):
        return Pad.fetch(network, id=pads)

    def get_pads(self) -> List[Pad]:
        """Returns Pad type objects of the pads the rocket uses."""
        pad_objs = []
        if self.default_pads:
            pad_objs = Rocket._get_pads_for_id(self.network, self.default_pads)

        return pad_objs


# putting it at the end to load the classes first
MODEL_LIST_PLURAL = {"agencies": Agency, "pads": Pad, "locations": Location
    , "rockets": Rocket, "families": RocketFamily}
MODEL_LIST_SINGULAR = {"agency": Agency, "pad": Pad, "location": Location, "rocket": Rocket, "family": RocketFamily,
                       "lsp": Agency}
