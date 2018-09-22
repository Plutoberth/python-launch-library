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
    def __init__(self, endpoint, param_translations, nested_name, api_instance, proper_name, kwargs):
        # Just keeping this here in-case I ever wanna add some base functionality
        self.param_translations = param_translations
        self.endpoint = endpoint
        self.nested_name = nested_name
        self.api_instance = api_instance
        self.proper_name = proper_name

    @classmethod
    def fetch(cls, api_instance, **kwargs):
        """Initializes a class, or even a list of them from the api using the needed params."""
        cls_init = cls(api_instance)
        json_object = api_instance.send_message(cls_init.endpoint, kwargs)

        cls_init = cls(api_instance)
        classes = []
        for entry in json_object[cls_init.nested_name]:
            cls_init = cls(api_instance)
            cls_init.set_params_json(entry)
            classes.append(cls_init)

        return classes

    def set_params_json(self, json_object):
        """Sets the parameters of a class from an object (raw data, not inside "agenices" for example)"""
        for pythonic_name, api_name in self.param_translations.items():
            setattr(self, pythonic_name, json_object.get(api_name, None))

    def __repr__(self):
        subclass_name = self.proper_name
        variables = ",".join(f"{k}={getattr(self, k)}" for k, v in self.param_translations.items())

        return "{}({})".format(subclass_name, variables)


class Agency(BaseModel):
    def __init__(self, api_instance, **kwargs):
        param_translations = {"id": "id",
                              "name": "name",
                              "abbrev": "abbrev",
                              "type": "type",
                              "country_code": "countryCode",
                              "wiki_url": "wikiURL",
                              "info_urls": "infoURLs",
                              "is_lsp": "islsp",
                              "changed": "changed"}
        proper_name = "Agency"
        nested_name = "agencies"
        self.name_cache = None

        super().__init__("/agency", param_translations, nested_name, api_instance, proper_name, kwargs)

    @property
    def type_name(self):
        """Returns the name of the agency type."""
        if self.name_cache is None:
            pass  # Add code to get agency type from the api
        else:
            return self.name_cache
