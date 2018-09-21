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
    def __init__(self, endpoint, param_translations, nested_name, api_instance):
        # Just keeping this here in-case I ever wanna add some base functionality
        self.param_translations = param_translations
        self.endpoint = endpoint
        self.nested_name = nested_name
        self.api_instance = api_instance
        pass

    @classmethod
    def init_from_json(cls, api_instance, json_object):
        cls_init = cls(api_instance)
        nested_name = cls_init.nested_name
        json_object = json_object[nested_name][0]
        for pythonic_name, api_name in cls_init.param_translations.items():
            setattr(cls_init, pythonic_name, json_object.get(api_name, None))

        return cls_init


class Agency(BaseModel):
    def __init__(self, api_instance):
        param_translations = {"id": "id",
                              "name": "name",
                              "abbrev": "abbrev",
                              "type": "type",
                              "country_code": "countryCode",
                              "wiki_url": "wikiURL",
                              "info_urls": "infoURLs",
                              "is_lsp": "islsp",
                              "changed": "changed"}
        nested_name = "agencies"
        self.name_cache = None

        super().__init__("/agency", param_translations, nested_name, api_instance)

    @property
    def type_name(self):
        """Returns the name of the agency type."""
        if self.name_cache is None:
            pass  # Add code to get agency type from the api
        else:
            return self.name_cache
