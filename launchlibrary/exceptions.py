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


class LlException(Exception):
    """The base class for all exceptions emitted by the library"""
    def __init__(self, message: str = "There was an unspecified exception regarding the LaunchLibrary wrapper."):
        super().__init__(message)


class ApiException(LlException):
    """An exception related to the API's response"""
    def __init__(self, message: str = "There was an unknown issue with the API. Please reevaluate your call."):
        super().__init__(message)


class NetworkException(LlException):
    """Some network failure that's unrelated to the request, like a dropped connection"""

    def __init__(self, message: str):
        super().__init__(message)


class TimeoutException(LlException):
    """All timeout failures, both during the initial connection and subsequent messages"""

    def __init__(self, message: str = ""):
        super().__init__(message)
