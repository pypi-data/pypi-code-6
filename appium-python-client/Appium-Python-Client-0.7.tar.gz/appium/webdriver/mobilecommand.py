#!/usr/bin/env python

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class MobileCommand(object):
    CONTEXTS = 'getContexts',
    GET_CURRENT_CONTEXT = 'getCurrentContext',
    SWITCH_TO_CONTEXT = 'switchToContext'
    TOUCH_ACTION = 'touchAction'
    MULTI_ACTION = 'multiAction'
    OPEN_NOTIFICATIONS = 'openNotifications'

    # Appium Commands
    GET_APP_STRINGS = 'getAppStrings'
    PRESS_KEYCODE = 'pressKeyCode'
    # TODO: remove when new Appium is out
    KEY_EVENT = 'keyEvent'
    LONG_PRESS_KEYCODE = 'longPressKeyCode'
    GET_CURRENT_ACTIVITY = 'getCurrentActivity'
    SET_IMMEDIATE_VALUE = 'setImmediateValue'
    PULL_FILE = 'pullFile'
    PUSH_FILE = 'pushFile'
    COMPLEX_FIND = 'complexFind'
    BACKGROUND = 'background'
    IS_APP_INSTALLED = 'isAppInstalled'
    INSTALL_APP = 'installApp'
    REMOVE_APP = 'removeApp'
    LAUNCH_APP = 'launchApp'
    CLOSE_APP = 'closeApp'
    END_TEST_COVERAGE = 'endTestCoverage'
    LOCK = 'lock'
    SHAKE = 'shake'
    RESET = 'reset'
    HIDE_KEYBOARD = 'hideKeyboard'
