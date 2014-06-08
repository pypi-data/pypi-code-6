import base64
import functools
from io import BytesIO
import time

from selenium.common.exceptions import WebDriverException
from ._webdriver import EyesScreenshot

from applitools.errors import EyesError
from applitools.geometry import Region, Point

# noinspection PyProtectedMember
from .utils._image_utils import png_image_from_bytes


class MatchWindowTask(object):
    """
    Handles matching of output with the expected output (including retry and 'ignore mismatch'
    when needed).
    """
    _MATCH_INTERVAL = 0.5

    def __init__(self, eyes, agent_connector, running_session, driver, max_window_load_time):
        self._eyes = eyes
        self._agent_connector = agent_connector
        self._running_session = running_session
        self._driver = driver
        self._max_window_load_time = max_window_load_time
        self._screenshot = None
    
    def _get_screenshot(self, force_full_page_screenshot):
        if force_full_page_screenshot:
            current_screenshot = self._driver.get_full_page_screenshot()
            return EyesScreenshot.create_from_image(current_screenshot, self._driver)
        current_screenshot64 = self._driver.get_screenshot_as_base64()
        return EyesScreenshot.create_from_base64(current_screenshot64, self._driver)
        
    def _prepare_match_data_for_window(self, tag, force_full_page_screenshot, user_inputs,
                                       ignore_mismatch=False):
        title = self._eyes.get_title()
        self._screenshot = self._get_screenshot(force_full_page_screenshot)
        app_output = {'title': title, 'screenshot64': self._screenshot.get_base64()}
        return dict(appOutput=app_output, userInputs=user_inputs, tag=tag,
                    ignoreMismatch=ignore_mismatch)

    def _prepare_match_data_for_region(self, region, tag, force_full_page_screenshot, user_inputs,
                                       ignore_mismatch=False):
        title = self._eyes.get_title()
        self._screenshot = self._get_screenshot(force_full_page_screenshot)\
                               .get_sub_screenshot_by_region(region)
        app_output = {'title': title, 'screenshot64': self._screenshot.get_base64()}
        return dict(appOutput=app_output, userInputs=user_inputs, tag=tag,
                    ignoreMismatch=ignore_mismatch)

    def _prepare_match_data_for_element(self, element, tag, force_full_page_screenshot, user_inputs,
                                        ignore_mismatch=False):
        title = self._eyes.get_title()
        self._screenshot = self._get_screenshot(force_full_page_screenshot)
        self._screenshot = self._screenshot.get_sub_screenshot_by_element(element)
        app_output = {'title': title, 'screenshot64': self._screenshot.get_base64()}
        return dict(appOutput=app_output, userInputs=user_inputs, tag=tag,
                    ignoreMismatch=ignore_mismatch)

    def _run_with_intervals(self, prepare_action, total_run_time):
        """
        Includes retries in case the screenshot does not match.
        """
        # We intentionally take the first screenshot before starting the timer, to allow the page
        # just a tad more time to stabilize.
        data = prepare_action(ignore_mismatch=True)
        # Start the timer.
        start = time.time()
        match_retry = total_run_time
        as_expected = self._agent_connector.match_window(self._running_session, data)
        while (not as_expected) and (match_retry > 0):
            time.sleep(self._MATCH_INTERVAL)
            data = prepare_action(ignore_mismatch=True)
            as_expected = self._agent_connector.match_window(self._running_session, data)
            if as_expected:
                return {"as_expected": True, "screenshot": self._screenshot}
            match_retry -= (time.time() - start)
        # If needed, one last try
        if not as_expected:
            data = prepare_action()
            as_expected = self._agent_connector.match_window(self._running_session, data)
        return {"as_expected": as_expected, "screenshot": self._screenshot}

    def _run(self, prepare_action, run_once_after_wait=False):
        if run_once_after_wait or not self._max_window_load_time:
            # If the load time is 0, the sleep would immediately return anyway.
            time.sleep(self._max_window_load_time)
            data = prepare_action()
            as_expected = self._agent_connector.match_window(self._running_session, data)
            result = {"as_expected": as_expected, "screenshot": self._screenshot}
        else:
            result = self._run_with_intervals(prepare_action, self._max_window_load_time)
        return result

    def match_window(self, tag, force_full_page_screenshot, user_inputs,
                     run_once_after_wait=False):
        """
        Performs a match for a given region.
        """
        prepare_action = functools.partial(self._prepare_match_data_for_window, tag,
                                           force_full_page_screenshot, user_inputs)
        return self._run(prepare_action, run_once_after_wait)

    def match_region(self, region, tag, force_full_page_screenshot, user_inputs,
                     run_once_after_wait=False):
        """
        Performs a match for a given region.
        """
        prepare_action = functools.partial(self._prepare_match_data_for_region, region, tag,
                                           force_full_page_screenshot, user_inputs)
        return self._run(prepare_action, run_once_after_wait)

    def match_element(self, element, tag, force_full_page_screenshot, user_inputs,
                      run_once_after_wait=False):
        """
        Performs a match for a given element.
        """
        prepare_action = functools.partial(self._prepare_match_data_for_element, element,
                                           tag, force_full_page_screenshot, user_inputs)
        return self._run(prepare_action, run_once_after_wait)