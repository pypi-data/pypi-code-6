# Copyright 2014, Scalyr, Inc.
# Add appropriate license here.
#
#
# author: Steven Czerwinski <czerwin@scalyr.com>

import os
import threading
import time
import sys

import scalyr_agent.scalyr_logging as scalyr_logging
import scalyr_agent.util as scalyr_util

from scalyr_agent import json_lib
from scalyr_agent.util import Util
from scalyr_agent.util import StoppableThread
from scalyr_agent.log_processing import LogMatcher, LogFileProcessor
from scalyr_agent.agent_status import CopyingManagerStatus

log = scalyr_logging.getLogger(__name__)


class SendEventsTask(object):
    def __init__(self, add_events_request, total_bytes, completion_callback):
        self.add_events_request = add_events_request
        self.total_bytes = total_bytes
        self.completion_callback = completion_callback


class CopyingParameters(object):
    def __init__(self, configuration):
        self.max_allowed_request_size = configuration.max_allowed_request_size
        self.min_allowed_request_size = configuration.min_allowed_request_size

        self.min_request_spacing_interval = configuration.min_request_spacing_interval
        self.max_request_spacing_interval = configuration.max_request_spacing_interval
        self.max_error_request_spacing_interval = configuration.max_error_request_spacing_interval

        self.low_water_bytes_sent = configuration.low_water_bytes_sent
        self.low_water_request_spacing_adjustment = configuration.low_water_request_spacing_adjustment
        self.high_water_bytes_sent = configuration.high_water_bytes_sent
        self.high_water_request_spacing_adjustment = configuration.high_water_request_spacing_adjustment

        self.failure_request_spacing_adjustment = configuration.failure_request_spacing_adjustment

        self.request_too_large_adjustment = configuration.request_too_large_adjustment

        self.current_bytes_allowed_to_send = configuration.max_allowed_request_size
        self.current_sleep_interval = configuration.max_request_spacing_interval

    def update_params(self, result, bytes_sent):
        if result == 'success':
            max_request_spacing_interval = self.max_request_spacing_interval
            if bytes_sent < self.low_water_bytes_sent:
                self.current_sleep_interval *= self.low_water_request_spacing_adjustment
            elif bytes_sent > self.high_water_bytes_sent:
                self.current_sleep_interval *= self.high_water_request_spacing_adjustment
        else:
            self.current_sleep_interval *= self.failure_request_spacing_adjustment
            max_request_spacing_interval = self.max_error_request_spacing_interval

        if result == 'success':
            self.current_bytes_allowed_to_send = self.max_allowed_request_size
        elif result == 'requestTooLarge':
            self.current_bytes_allowed_to_send = int(bytes_sent * self.request_too_large_adjustment)

        self.current_bytes_allowed_to_send = self.__ensure_within(self.current_bytes_allowed_to_send,
                                                                  self.min_allowed_request_size,
                                                                  self.max_allowed_request_size)

        self.current_sleep_interval = self.__ensure_within(self.current_sleep_interval,
                                                           self.min_request_spacing_interval,
                                                           max_request_spacing_interval)

    def __ensure_within(self, value, min_value, max_value):
        if value < min_value:
            value = min_value
        elif value > max_value:
            value = max_value
        return value


LATEST_USED_TIMESTAMP = None


# What this guy needs to do:
#  - Take in a JsonObject representing the configuration.
#  - Has a list of LogFileMatchers
#  - Has a list of LogFileProcessors
#  - Has a ScalyrClient
#
class CopyingManager(StoppableThread):
    def __init__(self, scalyr_client, configuration, logs_initial_positions):
        StoppableThread.__init__(self, name='log copier thread')
        self.__config = configuration
        self.__log_matchers = []
        self.__log_processors = []
        self.__log_paths_being_processed = {}
        self.__lock = threading.Lock()
        self.__pending_send_events_task = None
        self.__sleep_interval = 1
        self.__current_processor = 0

        self.__scalyr_client = scalyr_client
        self.__last_new_file_scan_time = 0
        self.__log_matchers = configuration.logs

        self.__last_attempt_time = None
        self.__last_success_time = None
        self.__last_attempt_size = None
        self.__last_response = None
        self.__last_response_status = None
        self.__total_bytes_uploaded = 0
        self.__total_errors = 0
        self.__logs_initial_positions = logs_initial_positions

        # A semaphore that we increment when this object has begun copying files (after first scan).
        self.__copying_semaphore = threading.Semaphore()

    @staticmethod
    def build_log(log_config):
        return LogMatcher(log_config)

    def run(self):
        # So the scanning.. every scan:
        #   - See if any of the loggers have new files that are being matched
        #   - Update the file length counts of all current scanners:
        #   - Then pick up where you left off, getting X bytes as determined that abstraction
        #   - Send it to the client
        #   - determine success or not.. if success, update it.
        #   - sleep
        try:
            current_time = time.time()
            checkpoints_state = self.__read_checkpoint_state()
            if (checkpoints_state is not None and
                    current_time - checkpoints_state['time'] < self.__config.max_allowed_checkpoint_age):
                self.__scan_for_new_logs_if_necessary(current_time=current_time,
                                                      checkpoints=checkpoints_state['checkpoints'])

            elif checkpoints_state is not None:
                log.warn('The current checkpoint is too stale (written at "%s").  Ignoring it.  All log files will be '
                         'copied starting at their current end.', scalyr_util.format_time(
                        checkpoints_state['time']), error_code='staleCheckpointFile')
                self.__scan_for_new_logs_if_necessary(current_time=current_time,
                                                      logs_initial_positions=self.__logs_initial_positions)
            else:
                log.info('The checkpoints could not be read.  All logs will be copied starting at their current end')
                self.__scan_for_new_logs_if_necessary(current_time=current_time,
                                                      logs_initial_positions=self.__logs_initial_positions)

            copying_params = CopyingParameters(self.__config)

            last_success = time.time()

            # We are about to start copying.  We can tell waiting threads.
            self.__copying_semaphore.release()

            while self._run_state.is_running():
                current_time = time.time()
                try:
                    if current_time - last_success > self.__config.max_retry_time:
                        if self.__pending_send_events_task is not None:
                            self.__pending_send_events_task.completion_callback(False)
                            self.__pending_send_events_task = None
                        # Tell all of the processors to the end of the current log file.  We will start copying from
                        # there.
                        for processor in self.__log_processors:
                            processor.skip_to_end('Too long since last successful request to server.',
                                                  'skipNoServerSuccess', current_time=current_time)

                    # Check for new logs.  If we do detect some new log files, they must have been created since our
                    # last scan.  In this case, we start copying them from byte zero instead of the end of the file.
                    self.__scan_for_new_logs_if_necessary(current_time=current_time, copy_at_index_zero=True)

                    if self.__pending_send_events_task is None:
                        self.__pending_send_events_task = self.__get_next_send_events_task(
                            copying_params.current_bytes_allowed_to_send)

                    if self.__pending_send_events_task is not None:
                        (result, bytes_sent, full_response) = self.__send_events(self.__pending_send_events_task)

                        if result == 'success' or 'discardBuffer' in result:
                            self.__pending_send_events_task.completion_callback(result == 'success')
                            self.__pending_send_events_task = None
                            self.__write_checkpoint_state()

                        if result == 'success':
                            last_success = current_time
                    else:
                        result = 'failedReadingLogs'
                        bytes_sent = 0
                        full_response = ''

                        log.error('Failed to read logs for copying.  Will re-try')

                    self.__lock.acquire()
                    copying_params.update_params(result, bytes_sent)
                    self.__last_attempt_time = current_time
                    self.__last_success_time = last_success
                    self.__last_attempt_size = bytes_sent
                    self.__last_response = full_response
                    self.__last_response_status = result
                    if result == 'success':
                        self.__total_bytes_uploaded += bytes_sent
                    self.__lock.release()

                except Exception:
                    log.exception('Failed while attempting to scan and transmit logs')
                    self.__lock.acquire()
                    self.__last_attempt_time = current_time
                    self.__total_errors += 1
                    self.__lock.release()

                self._run_state.sleep_but_awaken_if_stopped(copying_params.current_sleep_interval)
        except Exception:
            # If we got an exception here, it is caused by a bug in the program, so let's just terminate.
            log.exception('Log copying failed due to exception')
            sys.exit(1)

    def wait_for_copying_to_begin(self):
        """Block the current thread until this instance has finished its first scan and has begun copying.

        It is good to wait for the first scan to finish before possibly creating new files to copy because
        if the first scan has not completed, the copier will just begin copying at the end of the file when
        it is first noticed.  However, if the first scan has completed, then the copier will know that the
        new file was just newly created and should therefore have all of its bytes copied to Scalyr.

        TODO:  Make it so that this thread does not block indefinitely if the copying never starts.  However,
        we do not do this now because the CopyManager's run method will sys.exit if the copying fails to start.
        """
        self.__copying_semaphore.acquire(True)

    def generate_status(self):
        try:
            self.__lock.acquire()

            result = CopyingManagerStatus()
            result.total_bytes_uploaded = self.__total_bytes_uploaded
            result.last_success_time = self.__last_success_time
            result.last_attempt_time = self.__last_attempt_time
            result.last_attempt_size = self.__last_attempt_size
            result.last_response = self.__last_response
            result.last_response_status = self.__last_response_status
            result.total_errors = self.__total_errors

            for entry in self.__log_matchers:
                result.log_matchers.append(entry.generate_status())

        finally:
            self.__lock.release()

        return result

    def __read_checkpoint_state(self):
        file_path = os.path.join(self.__config.agent_data_path, 'checkpoints.json')

        if not os.path.isfile(file_path):
            log.info('The log copying checkpoint file "%s" does not exist, skipping.' % file_path)
            return None

        try:
            return Util.read_file_as_json(file_path)
        except Exception:
            log.exception('Could not read checkpoint file due to error.', error_code='failedCheckpointRead')
            return None

    def __write_checkpoint_state(self):
        checkpoints = {}
        state = {
            'time': time.time(),
            'checkpoints': checkpoints,
        }

        for processor in self.__log_processors:
            checkpoints[processor.log_path] = processor.get_checkpoint()

        # We write to a temporary file and then rename it to the real file name to make the write more atomic.
        # We have had problems in the past with corrupted checkpoint files due to failures during write.
        file_path = os.path.join(self.__config.agent_data_path, 'checkpoints.json')
        tmp_path = os.path.join(self.__config.agent_data_path, 'checkpoints.json~')
        fp = None
        try:
            fp = open(tmp_path, 'w')
            fp.write(json_lib.serialize(state))
            fp.close()
            fp = None
            os.rename(tmp_path, file_path)
        except Exception:
            if fp is not None:
                fp.close()
            log.exception('Could not write checkpoint file due to error', error_code='failedCheckpointWrite')

    def __get_next_send_events_task(self, bytes_allowed_to_send):
        num_bytes = 0
        all_callbacks = {}
        logs_processed = 0
        first_processor = self.__current_processor

        current_processor = self.__current_processor

        buffer_filled = False

        add_events_request = self.__scalyr_client.add_events_request(session_info=self.__config.server_attributes,
                                                                     max_size=bytes_allowed_to_send)

        while not buffer_filled and logs_processed < len(self.__log_processors):
            (callback, buffer_filled) = self.__log_processors[current_processor].perform_processing(
                add_events_request)

            if callback is None:
                for key in all_callbacks:
                    all_callbacks[key](False)
                return None

            all_callbacks[current_processor] = callback
            logs_processed += 1

            if not buffer_filled or current_processor == first_processor:
                self.__current_processor += 1
                if self.__current_processor >= len(self.__log_processors):
                    self.__current_processor = 0
                current_processor = self.__current_processor
            else:
                break

        def handle_completed_callback(success):
            processor_list = self.__log_processors[:]
            self.__log_processors = []
            self.__log_paths_being_processed = {}
            add_events_request.close()

            for i in range(0, len(processor_list)):
                processor = processor_list[i]
                if i in all_callbacks:
                    keep_it = not all_callbacks[i](success)
                else:
                    keep_it = True
                if keep_it:
                    self.__log_processors.append(processor)
                    self.__log_paths_being_processed[processor.log_path] = True

        return SendEventsTask(add_events_request, num_bytes, handle_completed_callback)

    def __send_events(self, send_events_task):
        return self.__scalyr_client.send(send_events_task.add_events_request)

    def __advance_all_logs_to_end(self):
        return None

    def __scan_for_new_logs_if_necessary(self, current_time=None, checkpoints=None, logs_initial_positions=None,
                                         copy_at_index_zero=False):
        if current_time is None:
            current_time = time.time()

        if (self.__last_new_file_scan_time is None or
                current_time - self.__last_new_file_scan_time < self.__config.max_new_log_detection_time):
            return

        self.__last_new_file_scan_time = current_time

        if checkpoints is None:
            checkpoints = {}

            if logs_initial_positions is not None:
                for log_path in logs_initial_positions:
                    checkpoints[log_path] = self.__create_checkpoint_with_initial_position(
                        log_path, logs_initial_positions[log_path], current_time)

        for matcher in self.__log_matchers:
            for new_processor in matcher.find_matches(self.__log_paths_being_processed, checkpoints,
                                                      copy_at_index_zero=copy_at_index_zero):
                self.__log_processors.append(new_processor)
                self.__log_paths_being_processed[new_processor.log_path] = True

    def __create_checkpoint_with_initial_position(self, log_path, position, current_time):
        return LogFileProcessor.create_checkpoint(log_path, position, current_time)

    @staticmethod
    def __get_next_timestamps(num_timestamps):
        if num_timestamps == 0:
            return []

        global LATEST_USED_TIMESTAMP

        base_timestamp = long(time.time() * 1000000000L)
        if LATEST_USED_TIMESTAMP is not None and base_timestamp <= LATEST_USED_TIMESTAMP:
            base_timestamp = LATEST_USED_TIMESTAMP + 1L

        result = []
        for i in range(num_timestamps):
            result.append(base_timestamp + i)
        LATEST_USED_TIMESTAMP = result[-1]

        return result
