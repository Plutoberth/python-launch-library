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

# Unused at the moment. Will add exceptions later.


class ApiException(Exception):
    def __init__(self, message: str = "There was an unknown issue with the API. Please reevaluate your call."):
        super().__init__(message)


class NetworkException(Exception):
    """Some type of network failure unrelated to the request, like the connection timing out"""

    def __init__(self, message: str):
        super().__init__(message)


class TimeoutException(Exception):
    """All timeout failures, both during the initial connection and subsequent messages"""

    def __init__(self, message: str = ""):
        super().__init__(message)
