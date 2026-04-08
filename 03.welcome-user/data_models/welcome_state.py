# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class WelcomeState:
    def __init__(self, did_welcome: bool = False):
        self.did_welcome_user = did_welcome
