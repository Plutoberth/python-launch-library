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


class BaseModel:
    def __init__(self, endpoint, param_translations, nested_name, api_instance, proper_name):
        # param translations contains translations from non-pythonic to pythonic names
        self.param_translations = param_translations
        self.endpoint = endpoint
        self.nested_name = nested_name
        self.api_instance = api_instance
        self.proper_name = proper_name
        self.param_names = []  # for use in repr, locals doesn't work for some reason

    @classmethod
    def fetch(cls, api_instance, **kwargs):
        """Initializes a class, or even a list of them from the api using the needed params."""
        cls_init = cls(api_instance)
        json_object = api_instance.send_message(cls_init.endpoint, kwargs)

        cls_init = cls(api_instance)
        classes = []
        print(json_object)
        for entry in json_object.get(cls_init.nested_name, []):
            cls_init = cls(api_instance)
            cls_init.set_params_json(entry)
            classes.append(cls_init)

        return classes

    def set_params_json(self, json_object):
        """Sets the parameters of a class from an object (raw data, not inside "agenices" for example)"""
        for api_name, value in json_object.items():
            setattr(self, self.param_translations.get(api_name, api_name), value)
            self.param_names.append(self.param_translations.get(api_name, api_name))

    def __repr__(self):
        subclass_name = self.proper_name
        variables = ",".join(f"{k}={getattr(self, k)}" for k in self.param_names)

        return "{}({})".format(subclass_name, variables)


class Agency(BaseModel):
    def __init__(self, api_instance):
        param_translations = dict(country_code="countryCode", wiki_url="wikiURL", info_urls="infoURLs", is_lsp="islsp")
        proper_name = self.__class__.__name__
        nested_name = "agencies"
        endpoint_name = "agency"

        self.name_cache = None

        super().__init__(endpoint_name, param_translations, nested_name, api_instance, proper_name)

    @property
    def type_name(self):
        """Returns the name of the agency type."""
        if self.name_cache is None:
            pass  # Add code to get agency type from the api
        else:
            return self.name_cache


class Launch(BaseModel):
    def __init__(self, api_instance):
        param_translations = dict(wiki_url="wikiURL", info_urls="infoURLs", vid_urls="vidURLs")
        proper_name = self.__class__.__name__
        nested_name = "launches"
        endpoint_name = "launch"

        super().__init__(endpoint_name, param_translations, nested_name, api_instance, proper_name)
