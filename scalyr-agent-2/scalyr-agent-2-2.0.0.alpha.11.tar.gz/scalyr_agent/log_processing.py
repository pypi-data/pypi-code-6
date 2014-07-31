# Copyright 2014, Scalyr, Inc.
#
# Add appropriate license here.
#
# Abstractions that implement the core of the log reading
# and processing logic for the agent.  These abstractions include:
#     LogFileIterator:  Iterates over the lines in the log file at
#         a single file path.  Also handles noticing log rotations
#         and truncations, correctly returning lines from the previous
#         logs.
#
# author: Steven Czerwinski <czerwin@scalyr.com>

import errno
import glob
import os
import random
import re
import threading
import time

import scalyr_agent.json_lib as json_lib
import scalyr_agent.scalyr_logging as scalyr_logging
import scalyr_agent.util as scalyr_util

from scalyr_agent.agent_status import LogMatcherStatus
from scalyr_agent.agent_status import LogProcessorStatus

from cStringIO import StringIO
from os import listdir
from os.path import isfile, join


# The maximum allowed size for a line when reading from a log file.
# We do not strictly enforce this -- some lines returned by LogFileIterator may be
# longer than this due to some edge cases.
MAX_LINE_SIZE = 5 * 1024

# The number of seconds we are willing to wait when encountering a log line at the end of a log file that does not
# currently end in a new line (referred to as a partial line).  It could be that the full line just hasn't made it
# all the way to disk yet.  After this time though, we will just return the bytes as a line.
LINE_COMPLETION_WAIT_TIME = 5 * 60

# The maximum negative offset relative to the end of a log the log file
# iterator is allowed to become.  If bytes are not being read quickly enough, then
# the iterator will automatically advance so that it is no more than this length
# to the end of the file.  This is essentially the maximum bytes a log file
# is allowed to be caught up when used in copying logs to Scalyr.
MAX_LOG_OFFSET_SIZE = 5 * 1024 * 1024

# The number of bytes to read from a file at a time into the buffer.  This must
# always be greater than the MAX_LINE_SIZE
READ_PAGE_SIZE = 64 * 1024

LOG_DELETION_DELAY = 10 * 60

COPY_STALENESS_THRESHOLD = 15 * 60

log = scalyr_logging.getLogger(__name__)


class LogFileIterator(object):
    """Reads the bytes from a log file at a particular path, returning the lines.

    The core abstraction that handles iterating over the lines contained in the
    a log file at a single file path.  If the log file is rotated, then will
    continue returning the lines from the original file until it is exhausted
    and then iterate over the contents in the new file at the file path.  If the
    log file is truncated, assumes it also represents a log rotation and begins
    iterating over the new contents of the file.
    """

    def __init__(self, path, file_system=None, checkpoint=None):
        # The full path of the log file.
        self.__path = path
        # The representation of the iterator is a little tricky.  To handle log rotation, we actually
        # keep a list of pending files that represent the file handles we have to read from (in order) to get
        # all of the log content.  Typically, this should just be a list of one and two at the most (when a log
        # file has been recently rotated).  However, we implement it as a list because it was easier to think about
        # it generically.
        #
        # The abstraction revolves around the notion of mark position (or just usually referred to as position).
        # This represents the place we are currently reading from, relative to the last call to mark().  However, this
        # position goes across files, meaning mark position 500 might be in the first file (the file where the old
        # just recently rotated log is stored) but position 700 might be in the second file (the current file at the
        # file path for the log).  This would be mean the first file only has 699 bytes, so the 700th comes from the
        # next position.
        #
        # So, much of this abstraction is just about mapping which portions of the files map to which mark positions,
        # and corresponding, which portions of the buffered lines match with which mark positions.
        #
        # Oh yes, we actually use a StringIO buffer to temporarily buffer the bytes from the files.  We read them in
        # in chunks of 64K and then just pull the strings out of them.  A single buffer holds the contents from differnt
        # files if needed.

        # The objects of this list are of type LogFileIterator.FileState.  Each object has two important fields
        # position_start and position_end which specify where the contents of the file falls in terms of mark position.
        self.__pending_files = []
        # Roughly, the number of times mark has been invoked.  We use this to help differiente between positions
        # retrieved at different marked points.  We disallow going back to a previous position after mark has been
        # invoked.  At each new mark generation, we reset the mark position to zero.
        self.__mark_generation = 0L
        # The current position we are reading from, in mark position coordinates.
        self.__position = 0L
        # The StringIO buffer holding the bytes to be read.
        self.__buffer = None
        # This is a list of LogFileIterator.BufferEntry which maps which portions of the buffer map to which mark
        # positions.
        self.__buffer_contents_index = None

        # If we are currently not returning a line from the buffer because it is not terminated in a newline, then
        # this records the time when we first decided not return it.  (We wait some amount of time before giving up.)
        self.__partial_line_time = None

        # If there is no longer a file at the log path, then this marks the time when we first noticed it was gone.
        self.__log_deletion_time = None

        # Has closed been called.
        self.__is_closed = False

        # We are at the 'end' if the log file has been deleted.  This is because we always expect more bytes to be
        # written to it if not.
        self.at_end = False

        self.__max_line_length = MAX_LINE_SIZE
        self.__line_completion_wait_time = LINE_COMPLETION_WAIT_TIME
        self.__log_deletion_delay = LOG_DELETION_DELAY
        self.__page_size = READ_PAGE_SIZE

        # Stat just used in testing to verify pages are being read correctly.
        self.page_reads = 0

        # The file system facade that we direct all I/O calls through
        # so that we can insert testing methods in the future if needed.
        self.__file_system = file_system

        if self.__file_system is None:
            self.__file_system = FileSystem()

        if checkpoint is not None:
            need_to_close = True
            try:
                if 'position' in checkpoint:
                    self.__position = checkpoint['position']
                    for state in checkpoint['pending_files']:
                        if not state['is_log_file'] or self.__file_system.trust_inodes:
                            (file_object, file_size, inode) = self.__open_file_by_inode(os.path.dirname(self.__path),
                                                                                        state['inode'])
                        else:
                            (file_object, file_size, inode) = self.__open_file_by_path(self.__path)

                        if file_object is not None:
                            self.__pending_files.append(LogFileIterator.FileState(state, file_object))
                    self.__refresh_pending_files(time.time())
                    need_to_close = False
                else:
                    # Must be a psuedo checkpoint created by the static create_checkpoint method.  This is asking us
                    # to start iterating over the log file at a specific position.
                    self.__position = 0
                    initial_position = checkpoint['initial_position']
                    (file_object, file_size, inode) = self.__open_file_by_path(self.__path)
                    if file_object is not None and file_size >= initial_position:
                        self.__pending_files.append(LogFileIterator.FileState(
                            LogFileIterator.FileState.create_json(0, initial_position, file_size, inode, True),
                            file_object))
                need_to_close = False
            finally:
                if need_to_close:
                    for file_state in self.__pending_files:
                        self.__close_file(file_state)
                    self.__pending_files = []



    def set_parameters(self, max_line_length=None, page_size=None):
        if max_line_length is not None:
            self.__max_line_length = max_line_length

        if page_size is not None:
            self.__page_size = page_size

    def mark(self, current_time=None):
        if current_time is None:
            current_time = time.time()

        # This is a good time to check the state of each of the pending files (seeing if they have grown, shrunk, if
        # the file has rotated, etc.
        self.__refresh_pending_files(current_time)

        new_pending_files = []

        # We throw out any __pending_file entries that are before the current mark position or can no longer be
        # read.
        for pending_file in self.__pending_files:
            if not pending_file.valid or (self.__position >= pending_file.position_end
                                          and not pending_file.is_log_file):
                self.__close_file(pending_file)
            else:
                new_pending_files.append(pending_file)

        # We zero center the mark position.
        for pending_file in new_pending_files:
            pending_file.position_start -= self.__position
            pending_file.position_end -= self.__position

        if self.__buffer is not None:
            for buffer_entry in self.__buffer_contents_index:
                buffer_entry.position_start -= self.__position
                buffer_entry.position_end -= self.__position

        self.__position = 0

        self.__pending_files = new_pending_files
        self.__mark_generation += 1

    def tell(self):
        return LogFileIterator.Position(self.__mark_generation, self.__position)

    def seek(self, position):
        if position.mark_generation != self.__mark_generation:
            raise Exception('Attempt to seek to a position from a previous mark generation')
        buffer_index = self.__determine_buffer_index(position.mark_offset)
        if buffer_index is not None:
            self.__buffer.seek(buffer_index)
        else:
            self.__reset_buffer()

        self.__position = position.mark_offset

    def bytes_between_positions(self, first, second):
        if first.mark_generation != second.mark_generation:
            raise Exception('Attempt to compare positions from two different mark generations')

        return second.mark_offset - first.mark_offset

    def readline(self, current_time=None):
        if current_time is None:
            current_time = time.time()

        if self.__buffer is None or (self.__available_buffer_bytes() < self.__max_line_length and
                                         self.__more_file_bytes_available()):
            self.__fill_buffer(current_time)
        original_buffer_index = self.__buffer.tell()

        # ???
        expected_buffer_index = self.__determine_buffer_index(self.__position)
        if len(self.__buffer_contents_index) > 0 and self.__position != self.__buffer_contents_index[-1].position_end:
            if expected_buffer_index != original_buffer_index:
                self.__emit_state()
                assert expected_buffer_index == original_buffer_index, ('Mismatch between expected index and actual %ld %ld',
                                                                        expected_buffer_index, original_buffer_index)

        result = self.__buffer.readline(self.__max_line_length)
        if len(result) == 0:
            self.__partial_line_time = None
            return result

        # If we have a partial line (doesn't end in a newline) then we should only
        # return it if sufficient time has passed.
        if result[-1] != '\n' and result[-1] != '\r' and len(result) < self.__max_line_length:
            if self.__partial_line_time is None:
                self.__partial_line_time = current_time
            if current_time - self.__partial_line_time < self.__line_completion_wait_time:
                # We aren't going to return it so reset buffer back to the original spot.
                self.__buffer.seek(original_buffer_index)
                return ''
        else:
            self.__partial_line_time = None

        self.__position = self.__determine_mark_position(self.__buffer.tell())

        # ???
        if len(self.__buffer_contents_index) > 0:
            expected_size = self.__buffer_contents_index[-1].buffer_index_end
            actual_size = self.__file_system.get_file_size(self.__buffer)
            if expected_size != actual_size:
                self.__emit_state()
                assert expected_size == actual_size, ('Mismatch between expected and actual size %ld %ld', expected_size,
                                                      actual_size)

        return result

    def advance_to_end(self, current_time=None):
        """Advance the iterator to point at the end of the log file and begin reading from there.

        Returns the number of bytes that were skipped to reach the end."""
        if current_time is None:
            current_time = time.time()

        self.__refresh_pending_files(current_time=current_time)

        skipping = self.available

        for pending in self.__pending_files:
            self.__close_file(pending)
        self.__pending_files = []
        self.__buffer_contents_index = None
        self.__buffer = None
        self.__mark_generation += 1
        self.__position = 0

        self.mark()

        return skipping

    def close(self):
        """Closes all files open for this iterator.  This should be called before it is discarded."""
        for pending in self.__pending_files:
            self.__close_file(pending)
        self.__pending_files = []
        self.__buffer_contents_index = None
        self.__buffer = None
        self.__is_closed = True

    @property
    def available(self):
        if self.__pending_files is not None and len(self.__pending_files) > 0:
            return self.__pending_files[-1].position_end - self.__position
        else:
            return 0

    def __emit_state(self):
        log.warn('Dumping state of iterator')
        if self.__pending_files is not None:
            log.warn('  Pending files:')
            for pending_file in self.__pending_files:
                log.warn('    Pending: (start, end, last_known) %ld %ld %ld', pending_file.position_start, pending_file.position_end,
                         pending_file.last_known_size)
        if self.__buffer is not None:
            log.warn('  Buffer is at %ld with size %ld', self.__buffer.tell(), self.__file_system.get_file_size(self.__buffer))

        if self.__buffer_contents_index is not None:
            log.warn('  Buffer content index')
            for cindex in self.__buffer_contents_index:
                log.warn('    Entry: (buffer start/end, position start/end) %ld %ld %ld %ld',
                         cindex.buffer_index_start, cindex.buffer_index_end, cindex.position_start, cindex.position_end)

        if self.__position is not None:
            log.warn('  Position is %ld', self.__position)
        else:
            log.warn('  No position')
        log.warn('Done dumping')

    def __determine_buffer_index(self, mark_position):
        """Returns the index of the specified position (relative to mark) in the buffer.

        If the buffer does not current hold that position, returns None.  If that position should
        be in the buffer but is not (likely because its file had to be skipped while filling the buffer)
        then it will return the next smallest valid position in the buffer, or None if the end of buffer is reached.
        """
        # Make sure we have filled the buffer.
        if self.__buffer is None or len(self.__buffer_contents_index) == 0:
            return None
        # Make sure the overall range could possibly hold the position.
        if self.__buffer_contents_index[0].position_start > mark_position:
            return None
        if self.__buffer_contents_index[-1].position_end <= mark_position:
            return None

        for entry in self.__buffer_contents_index:
            if entry.position_start <= mark_position < entry.position_end:
                return mark_position - entry.position_start + entry.buffer_index_start
            elif entry.position_start > mark_position:
                return entry.buffer_index_start
        return None

    def __determine_mark_position(self, buffer_index):
        """Returns the position (relative to mark) represented by the specified index in the buffer."""
        # Special case the index representing everything has been read from the buffer to map to the
        # current position end.
        if buffer_index == self.__buffer_contents_index[-1].buffer_index_end:
            return self.__buffer_contents_index[-1].position_end

        for entry in self.__buffer_contents_index:
            if entry.buffer_index_start <= buffer_index < entry.buffer_index_end:
                return entry.position_start + buffer_index - entry.buffer_index_start

        # We should never reach here since the fill_buffer method should construct a buffer_contents_index that
        # spans all the buffer positions.
        assert False, 'Buffer index of %d not found' % buffer_index

    def __available_buffer_bytes(self):
        if self.__buffer is None or len(self.__buffer_contents_index) == 0:
            return 0
        return self.__buffer_contents_index[-1].buffer_index_end - self.__buffer.tell()

    def __more_file_bytes_available(self):
        if self.__pending_files is not None and len(self.__pending_files) > 0:
            if self.__buffer is None or len(self.__buffer_contents_index) == 0:
                return self.__pending_files[-1].position_end > self.__position
            else:
                return self.__pending_files[-1].position_end > self.__buffer_contents_index[-1].position_end
        else:
            return False

    def __reset_buffer(self):
        self.__buffer = None
        self.__buffer_contents_index = None

    def __close_file(self, file_entry):
        self.__file_system.close(file_entry.file_handle)
        file_entry.file_handle = None

    def __add_entry_for_log_path(self, inode, file_size):
        self.__log_deletion_time = None
        if len(self.__pending_files) > 0:
            largest_position = self.__pending_files[-1].position_end
        else:
            largest_position = 0
        (file_handle, file_size, inode) = self.__open_file_by_path(self.__path, starting_inode=inode)

        if file_handle is not None:
            self.__pending_files.append(LogFileIterator.FileState(
                LogFileIterator.FileState.create_json(largest_position, 0, file_size, inode, True), file_handle))

    def __refresh_pending_files(self, current_time):
        """Check to see if __pending_files needs to be adjusted due to log rotation or the
        current log growing."""

        has_no_position = len(self.__pending_files) == 0

        if len(self.__pending_files) > 0 and self.__pending_files[-1].is_log_file:
            current_log_file = self.__pending_files[-1]
        else:
            current_log_file = None

        # First, try to see if the file at the still exists, and if so, what's size and inode is.
        try:
            stat_result = self.__file_system.stat(self.__path)
            inode = stat_result.st_ino
            file_size = stat_result.st_size

            # See if it is rotated by checking out the file handle we last opened to this file path.
            if current_log_file is not None:
                if (current_log_file.last_known_size > stat_result.st_size or
                       self.__file_system.trust_inodes and current_log_file.inode != inode):
                    # Ok, the log file has rotated.  We need to add in a new entry to represent this.
                    # But, we also take this opportunity to see if the current entry we had for the log file has
                    # grown in length since the last time we checked it, which is possible.  This is the last time
                    # we have to check it since theorectically, the file would have been fully rotated before a new
                    # log file was created to take its place.
                    current_log_file.last_known_size = max(
                        current_log_file.last_known_size,
                        self.__file_system.get_file_size(current_log_file.file_handle))
                    current_log_file.is_log_file = False
                    current_log_file.position_end = current_log_file.position_start + current_log_file.last_known_size
                    # Note, we do not yet detect if current_log_file is actually pointing to the same inode as the
                    # log_path.  This could be true if the log file was copied to another location and then truncated
                    # in place (a commom mode of operation used by logrotate).  If this is the case, then the
                    # file_handle in current_log_file will eventually fail since it will seek to a location no longer
                    # in the file.  We handle that fairly cleanly in __fill_buffer so no need to do it here.  However,
                    # if we want to look for the file where the previous log file was copied, this is where we would
                    # do it.  That is a future feature.

                    # Add in an entry for the file content at log_path.
                    self.__add_entry_for_log_path(inode, file_size)
                else:
                    # It has not been rotated.  So we just update the size of the current entry.
                    current_log_file.last_known_size = stat_result.st_size
                    current_log_file.position_end = current_log_file.position_start + stat_result.st_size
            else:
                # There is no entry representing the file at log_path, but it does exist, so we need to add it in.
                self.__add_entry_for_log_path(inode, file_size)
        except OSError, e:
            if e.errno == errno.ENOENT:
                # The file doesn't exist.  See if we think we have a file handle that is for the log path, and if
                # so, update it to reflect it no longer is.
                if current_log_file is not None:
                    current_log_file.is_log_file = False
                    current_log_file.last_known_size = max(current_log_file.last_known_size,
                        self.__file_system.get_file_size(current_log_file.file_handle))
                    current_log_file.position_end = current_log_file.position_start + current_log_file.last_known_size
                if self.__log_deletion_time is None:
                    self.__log_deletion_time = current_time
                self.at_end = current_time - self.__log_deletion_time > self.__log_deletion_delay

            else:
                raise

        if has_no_position and len(self.__pending_files) > 0:
            self.__position = self.__pending_files[-1].position_end

    def __fill_buffer(self, current_time):
        new_buffer = StringIO()
        new_buffer_content_index = []

        # What position we need to read from the files.
        read_position = self.__position

        # Grab whatever is left over in the current buffer.  We first see if the position is even in
        # the buffer.
        buffer_index = self.__determine_buffer_index(self.__position)
        if buffer_index is not None:
            # Copy over the content_index entries.  We have to find where we left off first.
            expected_bytes = 0
            for entry in self.__buffer_contents_index:
                # The easiest way to think about this is that we are shifting the buffer positions of all existing
                # entries by buffer_index.  If that results in a positive end position, then it's still a useful
                # entry.
                entry.buffer_index_start = max(entry.buffer_index_start - buffer_index, 0)
                entry.buffer_index_end -= buffer_index

                if entry.buffer_index_end > 0:
                    new_buffer_content_index.append(entry)
                    expected_bytes += entry.buffer_index_end - entry.buffer_index_start
                    entry.position_start = entry.position_end - (entry.buffer_index_end - entry.buffer_index_start)
                    read_position = entry.position_end

            # Now read the bytes.  We should get the number of bytes we just found in all of the entries.
            tmp = self.__buffer.read()
            new_buffer.write(tmp)
            if expected_bytes != new_buffer.tell():
                self.__emit_state()
                assert expected_bytes == new_buffer.tell(), 'Failed to get the right number of left over bytes %d %d "%s"' % (
                    expected_bytes, new_buffer.tell(), tmp)

        leftover_bytes = new_buffer.tell()

        # Just in case a file has been rotated recently, we refresh our list before we read it.
        self.__refresh_pending_files(current_time)

        # Now we go through the files and get as many bytes as we can.
        for pending_file in self.__pending_files:
            if read_position < pending_file.position_end:
                read_position = max(pending_file.position_start, read_position)
                bytes_left_in_file = pending_file.last_known_size - (read_position - pending_file.position_start)
                content = self.__read_file_chunk(
                    pending_file, read_position,
                    min(self.__page_size - new_buffer.tell(), bytes_left_in_file))
                if content is not None:
                    buffer_start = new_buffer.tell()
                    new_buffer.write(content)
                    buffer_end = new_buffer.tell()
                    new_buffer_content_index.append(LogFileIterator.BufferEntry(read_position,
                                                                                buffer_start,
                                                                                buffer_end - buffer_start))
                read_position = pending_file.position_end
                if new_buffer.tell() >= self.__page_size:
                    break

        self.page_reads += 1
        self.__buffer = new_buffer
        self.__buffer_contents_index = new_buffer_content_index

        if len(self.__buffer_contents_index) > 0:
            # We may not have been able to read the bytes at the current position if those files have become
            # invalidated.  If so, we need to adjust the position to the next legal one according to the
            # buffer map.
            self.__position = self.__buffer_contents_index[0].position_start
        elif len(self.__pending_files) > 0:
            # We only get here if we were not able to read anything into the buffer.  This must mean
            # all of our file content after the current position is gone.  so, just adjust the position to
            # point to the end as we know it.
            self.__position = self.__pending_files[-1].position_end





        # ???
        if len(self.__buffer_contents_index) > 0:
            expected_size = self.__buffer_contents_index[-1].buffer_index_end
            actual_size = self.__buffer.tell()
            if expected_size != actual_size:
                self.__emit_state()
                assert expected_size == actual_size, ('Mismatch between expected and actual size %ld %ld %ld %ld',
                                                      expected_size, actual_size, leftover_bytes,
                                                      new_buffer.tell() - leftover_bytes)

        new_buffer.seek(0)   # ??? Move back up


    def __read_file_chunk(self, file_state, read_position_relative_to_mark, num_bytes):
        if not file_state.valid:
            return None

        offset_in_file = read_position_relative_to_mark - file_state.position_start
        self.__file_system.seek(file_state.file_handle, offset_in_file)
        chunk = self.__file_system.read(file_state.file_handle, num_bytes)
        if chunk is None or len(chunk) != num_bytes:
            file_state.valid = False
            return None

        if self.__file_system.get_file_size(file_state.file_handle) < file_state.last_known_size:
            file_state.valid = False
            return None

        return chunk

    def __open_file_by_path(self, file_path, starting_inode=None):
        pending_file = None
        try:
            attempts_left = 3

            while attempts_left > 0:
                if starting_inode is None:
                    starting_inode = self.__file_system.stat(file_path).st_ino
                pending_file = self.__file_system.open(file_path)
                second_stat = self.__file_system.stat(file_path)

                if not self.__file_system.trust_inodes or starting_inode == second_stat.st_ino:
                    new_file = pending_file
                    pending_file = None
                    return new_file, second_stat.st_size, second_stat.st_ino

                pending_file.close()
                pending_file = None
                attempts_left -= 1
                starting_inode = None
        finally:
            if pending_file is not None:
                pending_file.close()

        return None, None, None

    def __open_file_by_inode(self, dir_path, target_inode):
        if not self.__file_system.trust_inodes:
            return None, None, None

        pending_file = None
        attempts_left = 3

        try:
            while attempts_left > 0:
                found_path = None
                for path in self.__file_system.list_files(dir_path):
                    if self.__file_system.stat(path).st_ino == target_inode:
                        found_path = path
                        break

                if found_path is None:
                    return None, None, None

                (pending_file, file_size, opened_inode) = self.__open_file_by_path(found_path)
                if opened_inode == target_inode:
                    opened_file = pending_file
                    pending_file = None
                    return opened_file, file_size, opened_inode
                pending_file.close()
                pending_file = None
                attempts_left -= 1

            return None, None, None
        finally:
            if pending_file is not None:
                pending_file.close()

    def get_checkpoint(self):
        pending_files = []
        for pending_file in self.__pending_files:
            pending_files.append(pending_file.to_json())
        return {'position': self.__position, 'pending_files': pending_files}

    @staticmethod
    def create_checkpoint(log_path, initial_position, current_time):
        """Returns a checkpoint object that will begin reading the log file from the specified position.

        Arguments:
            log_path: The path of the log file.
            initial_position:  The byte position in the file where copying should begin.
            current_time:  The current time
        """
        # We implement this by creating a psuedo checkpoint that we then detect and handle properly
        # in the constructor.
        return {'initial_position': initial_position}

    def get_open_files_count(self):
        """Returns the number of pending file objects that need to be read to return log content.

        This is only used for tests.
        """
        return len(self.__pending_files)

    class BufferEntry(object):
        def __init__(self, position_start, buffer_index_start, num_bytes):
            self.position_start = position_start
            self.position_end = position_start + num_bytes
            self.buffer_index_start = buffer_index_start
            self.buffer_index_end = buffer_index_start + num_bytes

    class FileState(object):
        def __init__(self, state_json, file_handle):
            self.valid = True
            self.position_start = state_json['position_start']
            self.position_end = state_json['position_end']
            self.file_handle = file_handle
            if 'inode' in state_json:
                self.inode = state_json['inode']
            self.last_known_size = state_json['last_known_size']
            self.is_log_file = state_json['is_log_file']

        def to_json(self):
            result = json_lib.JsonObject(position_start=self.position_start,
                                         position_end=self.position_end,
                                         last_known_size=self.last_known_size,
                                         is_log_file=self.is_log_file)
            if self.inode is not None:
                result['inode'] = self.inode
            return result

        @staticmethod
        def create_json(position_start, initial_offset, file_size, inode, is_log_file):
            result = json_lib.JsonObject(position_start=position_start - initial_offset,
                                         position_end=position_start + file_size - initial_offset,
                                         last_known_size=file_size,
                                         is_log_file=is_log_file)
            if inode is not None:
                result['inode'] = inode
            return result

    class Position(object):
        def __init__(self, mark_generation, position):
            self.mark_offset = position
            self.mark_generation = mark_generation


class LogFileProcessor(object):
    """Performs all processing on a single log file (identified by a path) including return which lines are ready
    to be sent to the server, along with applying any sampling and redaction rules.
    """

    def __init__(self, file_path, log_attributes=None, file_system=None, checkpoint=None):
        if file_system is None:
            file_system = FileSystem()
        if log_attributes is None:
            log_attributes = {}

        self.__path = file_path
        self.__log_file_iterator = LogFileIterator(file_path, file_system=file_system, checkpoint=checkpoint)
        self.__is_closed = False

        self.__log_attributes = log_attributes
        self.__redacter = LogLineRedacter(file_path)
        self.__sampler = LogLineSampler(file_path)

        self.__total_bytes_copied = 0L
        self.__total_bytes_skipped = 0L
        self.__total_bytes_failed = 0L
        self.__total_bytes_dropped_by_sampling = 0L
        self.__total_bytes_pending = 0L

        self.__total_lines_copied = 0L
        self.__total_lines_dropped_by_sampling = 0L

        self.__total_redactions = 0L

        self.__last_processing_time = None

        self.__lock = threading.Lock()

        self.__copy_staleness_threshold = COPY_STALENESS_THRESHOLD
        self.__max_log_offset_size = MAX_LOG_OFFSET_SIZE

        self.__last_success = None

    def generate_status(self):
        try:
            self.__lock.acquire()
            result = LogProcessorStatus()
            result.log_path = self.__path
            result.last_scan_time = self.__last_processing_time

            result.total_bytes_copied = self.__total_bytes_copied
            result.total_bytes_pending = self.__total_bytes_pending

            result.total_bytes_skipped = self.__total_bytes_skipped
            result.total_bytes_failed = self.__total_bytes_failed
            result.total_bytes_dropped_by_sampling = self.__total_bytes_dropped_by_sampling
            result.total_lines_copied = self.__total_lines_copied
            result.total_lines_dropped_by_sampling = self.__total_lines_dropped_by_sampling
            result.total_redactions = self.__total_redactions
            result.total_bytes_skipped = self.__total_bytes_skipped

            return result
        finally:
            self.__lock.release()

    def is_closed(self):
        self.__lock.acquire()
        result = self.__is_closed
        self.__lock.release()
        return result

    @property
    def log_path(self):
        # TODO:  Change this to just a regular property?
        return self.__path

    def perform_processing(self, add_events_request, current_time=None):
        """Scans the available lines from the log file, processes them using the configured redacters and samplers
         and appends the final lines to add_events_message.

        TODO:
        """

        if current_time is None:
            current_time = time.time()

        if self.__last_success is None:
            self.__last_success = current_time

        self.__lock.acquire()
        self.__last_processing_time = current_time
        self.__lock.release()

        self.__log_file_iterator.mark(current_time=current_time)

        # Check to see if we haven't had a success in enough time.  If so, then we just skip ahead.
        if current_time - self.__last_success > self.__copy_staleness_threshold:
            self.skip_to_end('Too long since last success.  Last success was \'%s\'' % scalyr_util.format_time(
                self.__last_success), 'skipForStaleness', current_time=current_time)
        # Also make sure we are at least within 5MB of the tail of the log.  If not, then we skip ahead.
        elif self.__log_file_iterator.available > self.__max_log_offset_size:
            self.skip_to_end(
                'Too far behind end of log.  Num of bytes to end is %ld' % self.__log_file_iterator.available,
                'skipForTooFarBehind', current_time=current_time)

        original_position = self.__log_file_iterator.tell()
        original_events_position = add_events_request.position()

        try:
            bytes_read = 0L
            lines_read = 0L
            bytes_copied = 0L
            lines_copied = 0L
            total_redactions = 0L
            lines_dropped_by_sampling = 0L
            bytes_dropped_by_sampling = 0L

            buffer_filled = False

            while True:
                position = self.__log_file_iterator.tell()

                line = self.__log_file_iterator.readline(current_time=current_time)

                if len(line) == 0:
                    break

                bytes_read += len(line)
                lines_read += 1L

                sample_result = self.__sampler.process_line(line)
                if sample_result is None:
                    lines_dropped_by_sampling += 1L
                    bytes_dropped_by_sampling += len(line)
                    continue

                (line, redacted) = self.__redacter.process_line(line)

                if len(line) > 0:
                    if not add_events_request.add_event(self.__create_events_object(line, sample_result)):
                        self.__log_file_iterator.seek(position)
                        buffer_filled = True
                        break

                if redacted:
                    total_redactions += 1L
                bytes_copied += len(line)
                lines_copied += 1

            final_position = self.__log_file_iterator.tell()

            def completion_callback(success):
                try:
                    self.__lock.acquire()
                    if success:
                        self.__total_bytes_copied += bytes_copied
                        self.__total_bytes_skipped += self.__log_file_iterator.bytes_between_positions(
                            original_position, final_position) - bytes_read

                        self.__total_bytes_dropped_by_sampling += bytes_dropped_by_sampling
                        self.__total_bytes_pending = self.__log_file_iterator.available
                        self.__total_lines_copied += lines_copied
                        self.__total_lines_dropped_by_sampling += lines_dropped_by_sampling
                        self.__total_redactions += total_redactions
                        self.__last_success = current_time

                        self.__log_file_iterator.mark(current_time)
                        if self.__log_file_iterator.at_end:
                            self.__log_file_iterator.close()
                            self.__is_closed = True
                            return True
                        else:
                            return False
                    else:
                        self.__total_bytes_pending = self.__log_file_iterator.available
                        self.__total_bytes_failed += bytes_read

                        return False
                finally:
                    self.__lock.release()

            return completion_callback, buffer_filled
        except Exception:
            log.exception('Failed to copy lines from \'%s\'.  Will re-attempt lines.', self.__path,
                          error_code='logCopierFailed')
            self.__log_file_iterator.seek(original_position)
            add_events_request.set_position(original_events_position)

            return None, False

    def skip_to_end(self, message, error_code, current_time=None):
        if current_time is None:
            current_time = time.time()
        skipped_bytes = self.__log_file_iterator.advance_to_end()
        self.__log_file_iterator.mark(current_time=current_time)

        self.__lock.acquire()
        self.__total_bytes_skipped += skipped_bytes
        self.__lock.release()

        log.warn('Skipped copying %ld bytes in \'%s\' due to: %s', skipped_bytes, self.__path, message,
            error_code=error_code)

    def add_sampler(self, match_expression, sampling_rate):
        """Adds a new sampling rule that will be applied after all previously added sampling rules.

        Args:
            match_expression:  The regular expression that must match any portion of a log line
            sampling_rate:  The rate to include any line that matches the expression in the results sent to the
                server.
        """
        self.__sampler.add_rule(match_expression, sampling_rate)

    def add_redacter(self, match_expression, replacement):
        """Adds a new redaction rule that will be applied after all previously added redaction rules.

        Args:
            match_expression:  The regular expression that must match the portion of the log line that will be redacted.
            replacement:  The text to replace the matched expression with.  You may use \1, \2, etc to use sub
                expressions from the match regular expression.
        """
        self.__redacter.add_redaction_rule(match_expression, replacement)

    def __create_events_object(self, event_message, sampling_rate):
        """Returns the events object that can be sent to the server for this log to insert the specified message.

        Arguments:
            event_message:  The contents of the event, to be placed in attrs.message.

        Returns:
            A dict containing the correct fields that when serialized to JSON and added to an addEvents request
            will insert the specified event along with any log attributes associated with this log.  In particular,
            it will contain a 'attrs' field.  The ts (timestamp) field is not set because the AddEventRequest object
            will set its value.  The attrs field will be another dict containing all of the log attributes for this
            log as well as a 'message' field containing event_message.
        """
        attrs = self.__log_attributes.copy()
        attrs['message'] = event_message
        if sampling_rate != 1.0:
            attrs['sample_rate'] = sampling_rate
        return {
            'attrs': attrs,
        }

    def get_checkpoint(self):
        return self.__log_file_iterator.get_checkpoint()

    @staticmethod
    def create_checkpoint(log_path, initial_position, current_time):
        """Returns a checkpoint object that will begin reading the log file from the specified position.

        Arguments:
            log_path:  The path of the log file
            initial_position:  The byte position in the file where copying should begin.
            current_time:  The current time
        """
        return LogFileIterator.create_checkpoint(log_path, initial_position, current_time)


class LogLineSampler(object):
    """Encapsulates all of the configured sampling rules to perform on lines from a single log file.

    It contains a list of filters, specified as regular expressions and a corresponding pass rate
    (a number between 0 and 1 inclusive) for each filter.  When a line is processed, each filter
    regular expression is matched against the line in order.  If a expression matches any portion of the
    line, then its pass rate is used to determine if that line should be included in the output.  A random number
    is generated and if it is greater than the filter's pass rate, then the line is included.  The first filter that
    matches a line is used.
    """

    def __init__(self, log_file_path):
        """Initializes an instance for a single file.

        Args:
            log_file_path:  The full path for the log file that the sampler will be applied to.
        """
        self.__log_file_path = log_file_path
        self.__sampling_rules = []
        self.total_passes = 0L

    def process_line(self, input_line):
        """Performs all configured sampling operations on the input line and returns whether or not it should
        be kept.  If it should be kept, then a float is returned indicating the sampling rate of the rule that
        allowed it to be included.  Otherwise, None.

        See the class description for the algorithm that determines which lines are returned.

        Args:
            input_line:  The input line.

        Returns:
            A float between 0 and 1 if the input line should be kept, the sampling rate of the rule that allowed
            it to be included.  Otherwise, None.
        """

        if len(self.__sampling_rules) == 0:
            self.total_passes += 1L
            return 1.0

        sampling_rule = self.__find_first_match(input_line)
        if sampling_rule is None:
            return 1.0
        else:
            sampling_rule.total_matches += 1L
            if self.__flip_biased_coin(sampling_rule.sampling_rate):
                sampling_rule.total_passes += 1L
                self.total_passes += 1L
                return sampling_rule.sampling_rate
        return None

    def add_rule(self, match_expression, sample_rate):
        """Appends a new sampling rule.  Any line that contains a match for match expression will be sampled with
        the specified rate.

        Args:
            match_expression:  The regular expression that much match any part of a line to activie the rule.
            sample_rate:  The sampling rate, expressed as a number between 0 and 1 inclusive.
        """
        self.__sampling_rules.append(SamplingRule(match_expression, sample_rate))

    def __find_first_match(self, line):
        """Returns the first sampling rule to match the line, if any.

        Args:
            line: The input line to match against.

        Returns:
            The first sampling rule to match any portion of line.  If none
            match, then returns None.
        """
        for sampling_rule in self.__sampling_rules:
            if sampling_rule.match_expression.search(line) is not None:
                return sampling_rule
        return None

    def __flip_biased_coin(self, bias):
        if bias == 0:
            return False
        elif bias == 1:
            return True
        else:
            return self._get_next_random() < bias

    def _get_next_random(self):
        """Returns a random between 0 and 1 inclusive.

        This is used for testing.
        """
        return random.random()


class SamplingRule(object):
    """Encapsulates all data for one sampling rule."""

    def __init__(self, match_expression, sampling_rate):
        self.match_expression = re.compile(match_expression)
        self.sampling_rate = sampling_rate
        self.total_matches = 0
        self.total_passes = 0


class LogLineRedacter(object):
    """Encapsulates all of the configured redaction rules to perform on lines from a single log file.

    It contains a list of redaction filters, specified as regular expressions, that are applied against
    all lines being processed, in order.  If a redaction filter's regular expression matches any portion
    of the line, the matched text is replaced with the text specified by the redaction rule, which may
    include portions of the matched text using the $1, etc operators from the regular expression.

    Redaction rules can match each line multiple times.
    """

    def __init__(self, log_file_path):
        """Initializes an instance for a single file.

        Args:
            log_file_path:  The full path for the log file that the sampler will be applied to.
        """
        self.__log_file_path = log_file_path
        self.__redaction_rules = []
        self.total_redactions = 0

    def process_line(self, input_line):
        """Performs all configured redaction rules on the input line and returns the results.

        See the class description for the algorithm that determines how the rules are applied.

        Args:
            input_line:  The input line.

        Returns:
            A sequence of two elements, the line with the redaction applied (if any) and True or False
            indicating if a redaction was applied.
        """

        if len(self.__redaction_rules) == 0:
            return input_line, False

        modified_it = False

        for redaction_rule in self.__redaction_rules:
            (input_line, redaction) = self.__apply_redaction_rule(input_line, redaction_rule)
            modified_it = modified_it or redaction

        return input_line, modified_it

    def add_redaction_rule(self, redaction_expression, replacement_text):
        """Appends a new redaction rule to this instance.

        Args:
            redaction_expression:  The regular expression that must match some portion of the line.
            replacement_text:  The text to replace the matched text with.  May include \1 etc to
                use a portion of the matched text.
        """
        self.__redaction_rules.append(RedactionRule(redaction_expression, replacement_text))

    def __apply_redaction_rule(self, line, redaction_rule):
        """Applies the specified redaction rule on line and returns the result.

        Args:
            line: The input line
            redaction_rule:  The redaction rule.

        Returns:
            A sequence of two elements, the line with the redaction applied (if any) and True or False
            indicating if a redaction was applied.
        """
        (result, matches) = redaction_rule.redaction_expression.subn(
            redaction_rule.replacement_text, line)
        if matches > 0:
            self.total_redactions += 1
            redaction_rule.total_lines += 1
            redaction_rule.total_redactions += matches
        return result, matches > 0


class RedactionRule(object):
    """Encapsulates all data for one redaction rule."""

    def __init__(self, redaction_expression, replacement_text):
        self.redaction_expression = re.compile(redaction_expression)
        self.replacement_text = replacement_text
        self.total_lines = 0
        self.total_redactions = 0

class LogMatcher(object):
    def __init__(self, log_entry_config):
        self.__log_entry_config = log_entry_config
        self.log_path = self.__log_entry_config['path']
        self.__is_glob = '*' in self.log_path or '?' in self.log_path or '[' in self.log_path
        self.__last_check = None
        self.__processors = []
        self.__lock = threading.Lock()

    def generate_status(self):
        try:
            self.__lock.acquire()
            self.__removed_closed_processors()

            result = LogMatcherStatus()
            result.log_path = self.log_path
            result.is_glob = self.__is_glob
            result.last_check_time = self.__last_check

            for processor in self.__processors:
                result.log_processors_status.append(processor.generate_status())

            return result
        finally:
            self.__lock.release()

    def find_matches(self, existing_processors, previous_state, copy_at_index_zero=False):
        if not self.__is_glob and self.log_path in existing_processors:
            return []

        self.__lock.acquire()
        self.__last_check = time.time()
        self.__removed_closed_processors()
        self.__lock.release()

        result = []
        for matched_file in glob.glob(self.__log_entry_config['path']):
            if not matched_file in existing_processors:
                checkpoint_state = None
                if matched_file in previous_state:
                    checkpoint_state = previous_state[matched_file]
                    del previous_state[matched_file]
                elif copy_at_index_zero:
                    # If we don't have a checkpoint and we are suppose to start copying the file at index zero,
                    # then create a checkpoint to represent that.
                    checkpoint_state = LogFileProcessor.create_checkpoint(matched_file, 0, self.__last_check)

                # Be sure to add in an entry for the logfile name to include in the log attributes.  We only do this
                # if the field or legacy field is not present.  Maybe we should override this regardless because the
                # user could get it wrong.. but for now, we just let them screw it up if they want to.
                log_attributes = dict(self.__log_entry_config['attributes'])
                if 'logfile' not in log_attributes and 'filename' not in log_attributes:
                    log_attributes['logfile'] = matched_file

                # Create the processor to handle this log.
                new_processor = LogFileProcessor(matched_file, log_attributes, checkpoint=checkpoint_state)
                for rule in self.__log_entry_config['redaction_rules']:
                    new_processor.add_redacter(rule['match_expression'], rule['replacement'])
                for rule in self.__log_entry_config['sampling_rules']:
                    new_processor.add_sampler(rule['match_expression'], rule['sampling_rate'])
                result.append(new_processor)
                self.__lock.acquire()
                self.__processors.append(new_processor)
                self.__lock.release()

        return result

    def __removed_closed_processors(self):
        new_list = []
        for processor in self.__processors:
            if not processor.is_closed():
                new_list.append(processor)
        self.__processors = new_list

class FileSystem(object):
    """A facade through which file system calls can be made.

    This abstraction is really in place for future testing.  It centralizes all
    of the I/O methods so that they can be stubbed or mocked out if needed.  However,
    for now, the only implementation of this class uses the real file system.

    Attributes:
        trust_inodes:  True if inodes are trusted on this file system.  This is a place
            holder since Scalyr only supports systems (like Linux and MacOS X) that do have
            valid inodes.
    """

    def __init__(self):
        self.trust_inodes = True

    def open(self, file_path):
        """Returns a file object to read the file at file_path.

        Args:
            file_path:  The path of the file to open

        Returns:
            The file object
        """
        return open(file_path, 'r')

    def readlines(self, file_object, max_bytes=None):
        """Reads lines from the file_object, up to max_bytes bytes.

        Args:
            file_object:  The file.
            max_bytes:  The maximum number of bytes to read.

        Returns:
            A list of lines read.
        """
        if max_bytes is None:
            return file_object.readlines()
        else:
            return file_object.readlines(max_bytes)

    def readline(self, file_object, max_bytes=None):
        """Reads a single lines from the file_object, up to max_bytes bytes.

        Args:
            file_object:  The file.
            max_bytes:  The maximum number of bytes to read.

        Returns:
            The line read.
        """
        if max_bytes is None:
            return file_object.readline()
        else:
            return file_object.readline(max_bytes)

    def read(self, file_object, size):
        """Reads bytes from file_object, up to max_bytes bytes.

        Args:
            file_object:  The file.
            max_bytes:  The maximum number of bytes to read.

        Returns:
            A string containing the bytes.
        """
        return file_object.read(size)

    def stat(self, file_path):
        """Performs a stat on the file at file_path and returns the result.

        Args:
            file_path:  The path of the file to stat.

        Returns:
            The stat object for the file (see os.stat)
        """
        return os.stat(file_path)

    def close(self, file_object):
        """Closes the file.

        Args:
            file_object:  The file to close
        """
        file_object.close()

    def tell(self, file_object):
        """Returns the current position of the file object.

        Args:
            file_object:  The file.
        """
        return file_object.tell()

    def seek(self, file_object, position):
        """Changes the current read position of the file.

        Args:
            file_object:  The file.
            position:  The position of the next bytes to read.
        """
        file_object.seek(position)

    def list_files(self, directory_path):
        """Returns the list of files in the specified directory.  Does not include directories.

        Args:
            directory_path:  The path of the directory

        Returns:
            A list of string containing the full path name of the files (not directories) present in the directory.
        """
        result = []
        for f in listdir(directory_path):
            full_path = join(directory_path, f)
            if isfile(full_path):
                result.append(full_path)
        return result

    def get_file_size(self, file_object):
        original_position = None
        try:
            original_position = file_object.tell()
            file_object.seek(0, 2)
            return file_object.tell()
        finally:
            if original_position is not None:
                file_object.seek(original_position)