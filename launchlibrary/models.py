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

import functools

class BaseModel:
    def __init__(self, endpoint, param_translations, nested_name, api_instance, proper_name):
        # param translations serves both for pythonic translations and default param values
        self.param_translations = param_translations
        self.endpoint = endpoint
        self.nested_name = nested_name
        self.api_instance = api_instance
        self.proper_name = proper_name
        self.param_names = self.param_translations.keys()

    @classmethod
    def fetch(cls, api_instance, **kwargs):
        """Initializes a class, or even a list of them from the api using the needed params."""
        cls_init = cls(api_instance)
        json_object = api_instance.send_message(cls_init.endpoint, kwargs)

        classes = []
        print(json_object)

        for entry in json_object.get(cls_init.nested_name, []):
            cls_init = cls(api_instance)
            cls_init.set_params_json(entry)
            classes.append(cls_init)

        return classes

    @classmethod
    def init_from_json(cls, api_instance, json_object):
        """
        Initializes a class from a json object. Only singular classes.
        :param api_instance: launchlibrary.Api
        :param json_object: An object containing the "entry" we want to init.
        :return: cls
        """
        cls_init = cls(api_instance)
        cls_init.set_params_json(json_object)
        return cls_init

    def set_params_json(self, json_object):
        """Sets the parameters of a class from an object (raw data, not inside "agenices" for example)"""
        for pythonic_name, api_name in self.param_translations.items():
            setattr(self, pythonic_name, json_object.get(api_name, None))

    def __repr__(self):
        subclass_name = self.proper_name
        variables = ",".join(f"{k}={getattr(self, k)}" for k in self.param_translations.keys())

        return "{}({})".format(subclass_name, variables)


class Agency(BaseModel):
    def __init__(self, api_instance):
        param_translations = dict(id="id", name="name", abbrev="abbrev", type="type", country_code="countryCode"
                                  , wiki_url="wikiURL", info_urls="infoURLs", is_lsp="islsp", changed="changed")
        proper_name = self.__class__.__name__
        nested_name = "agencies"
        endpoint_name = "agency"

        super().__init__(endpoint_name, param_translations, nested_name, api_instance, proper_name)

    @functools.lru_cache(maxsize=None)
    def get_type(self):
        """Returns the name of the agency type."""
        agency_type = AgencyType.fetch(self.api_instance, id=self.type)
        return agency_type[0] if len(agency_type) == 1 else None


class AgencyType(BaseModel):
    def __init__(self, api_instance):
        param_translations = dict(id="id", name="name", changed="changed")
        proper_name = self.__class__.__name__
        nested_name = "types"
        endpoint_name = "agencytype"

        super().__init__(endpoint_name, param_translations, nested_name, api_instance, proper_name)


class Launch(BaseModel):
    def __init__(self, api_instance):
        param_translations = dict(id="id", name="name", net="net", tbddate="tbddate", tbdtime="tbdtime", status="status"
                                  , inhold="inhold", windowstart="windowstart", windowend="windowend",
                                  isostart="isostart"
                                  , isoend="isoend", isonet="isonet", wsstamp="wsstamp", westamp="westamp",
                                  netstamp="netstamp", info_urls="infoURLs", vid_urls="vidURLs", holdreason="holdreason"
                                  , failreason="failreason", probability="probability", hashtag="hashtag", lsp="lsp",
                                  changed="changed", location="location", rocket="rocket", missions="missions")
        proper_name = self.__class__.__name__
        nested_name = "launches"
        endpoint_name = "launch"

        super().__init__(endpoint_name, param_translations, nested_name, api_instance, proper_name)

    def get_agency(self):
        """Gets the Agency model of the launch service provider either from json or from the server."""
        if self.api_instance.mode == "verbose" and self.lsp is not None:
            lsp = Agency.init_from_json(self.api_instance, self.lsp)
        else:
            lsp = Agency.fetch(self.api_instance, id=self.lsp)
            if len(lsp) > 0:
                lsp = lsp[0]

        return lsp
