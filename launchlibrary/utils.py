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

"""Contains simple utility functions for use within the wrapper."""

ILLEGAL_CHARS = '&=/\\'


def sanitize_input(args: dict) -> dict:
    """
    Gets a dictionary for url params and makes sure it doesn't contain any illegal keywords.
    :param args:
    :return:
    """
    if "mode" in args:
        del args["mode"]  # the mode should always be verbose

    trans = str.maketrans(ILLEGAL_CHARS, ' ' * len(ILLEGAL_CHARS))

    for k, v in args.copy().items():
        if isinstance(v, str):  # we only need to verify v because k will never be entered by a user
            args[k] = v.translate(trans)

    return args
