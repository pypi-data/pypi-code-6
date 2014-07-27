# pylint: disable=W0105, W0403, R0201
"""
This module provides an API for managing and processing a virtual
representation of a disk image file.
"""
# Standard library imports
import os
import re

# LaZy_NT module imports
import config
import carve_object

class DiskImage(object):
    """
    Represent the state of a disk image file that is in the process of
    being examined.
    """
    def __init__(self, image_id, filename):
        """Instantiate a disk image file representation."""
        self.compression_state = ""
        """
        (bool): Indicate whether this chunk of the disk image file is being
        processed as compressed data.
        """
        self.filename = filename
        """(str): Fully qualified path to the disk image file"""
        self.image_id = image_id
        """(int): A numeric identifier for the disk image file."""
        self.image_size = os.path.getsize(filename)
        """(int): Size of the disk image file, in bytes."""
        self.mm = None
        """
        (`mmap` object): Handle to a memory map of this disk image file.
        """
        self.carve_objects = []
        """
        (list): Contains all of the `CarveObject`s that have been instantiated
        by this `LaZy_NT.disk_image.DiskImage`.
        """
        self.volume_length = 0
        """
        (int): Size of the NTFS file system volume found within the disk
        image file, as reported by the Master Boot Record, if one exists.
        """
        self.__abs_offset = 0
        self.__cluster_offset = 0
        self.__comp_header = ""
        self.__decompressed_stream = ""
        self.__tag_byte = ""
        self.__wait_for_zeroes = True
        self.__wait_for_ASCII = True
        self.__working_cluster = ""

    def analyze_chunk(self):
        """
        Analyze a chunk of the image file, stored in the private
        `__working_cluster` attribute, for file signatures or 'interesting'
        raw data sequences. Instantiate `vFile`s and set processing flags.
        """
        file_found = False
        # If an entire chunk of data is zeroes, finish any in-process vFiles
        # (except .bmp) then return immediately - don't analyze for signatures
        if self.__working_cluster == chr(0x00) * config.options['chunk_size']:
            if self.inprocess_carve_objects() > 0:
                self.finish_inprocess_vFiles(flush=True)
            self.__wait_for_zeroes = False
            return
        # Treat any valid/signed MBRs as special files to carve.
        if ((self.__working_cluster[3:7] == 'NTFS' or
             self.__working_cluster[3:8] == 'MSDOS') and
                self.__working_cluster[510:512] == chr(0x55) + chr(0xAA)):
            self.__comp_header = '_MBR'
            # Only if this is the first file we've found (ie: Sector 0)
            if self.carve_objects == []:
                # Process the MBR to decode volume length
                if self.__working_cluster[3:7] == 'NTFS':
                    for i in range(47, 39, -1):
                        self.volume_length <<= 8
                        self.volume_length += ord(self.__working_cluster[i])
                if self.__working_cluster[3:8] == 'MSDOS':
                    for i in range(35, 31, -1):
                        self.volume_length <<= 8
                        self.volume_length += ord(self.__working_cluster[i])
            # Otherwise just create a new vFile object
            self.compression_state = False
            self.__instantiate_vFile('_MBR', self.__abs_offset)
            return
        # For each of the three 'normal' starting offsets, try to match
        # against each file signature
        for offset in [0, 2, 3]:
            for sig in config.signatures:
                # Files in uncompressed volumes only start on offset 0
                if config.options['unc_image'] and not offset == 0:
                    continue
                # If we find a signature match (new file detected)
                if (self.__working_cluster[offset:
                                           offset + len(sig.signature)]
                        == sig.signature):
                    file_found = True
                    # Finalize other vFiles in-process
                    if (self.inprocess_carve_objects() > 0 and
                            not config.options['no_carve']):
                        self.finish_inprocess_vFiles(flush=True)
                    if offset == 0:
                        self.__comp_header = ""
                        self.compression_state = False
                    else:
                        self.compression_state = True
                    # Create a new vFile object and add it to the list
                    self.__instantiate_vFile(
                        sig.file_type,
                        self.__abs_offset,
                        stop_sig=sig.stop_sig,
                        bmp_offset=offset)
                    break # If a match is found break inner loop, skips continue
            else:
                continue # If no match found, try the next signature
            break # After inner break, immediately break outer loop

        # Attempt a signatureless carving, but only if deep carving is enabled,
        # no file was found this chunk, no vFiles are in-process and we're not
        # blocked waiting for a zero-chunk state reset
        if (config.options['deep_carve'] and not file_found and
                self.inprocess_carve_objects('vFile') == 0 and
                not self.__wait_for_zeroes):
            if self.__signatureless_id():
                if self.__sanity_check_compression_meta(
                        self.__working_cluster[0:4]):
                    self.compression_state = True
                else:
                    self.__comp_header = ""
                    self.compression_state = False
                self.__instantiate_vFile('_deepcarve_raw', self.__abs_offset)
        else:
            return

    def finish_inprocess_vFiles(self, flush=False, force=False):
        """ Finalize all `vFile`s currently in 'Processing' status.

        ### Args:
        * **flush (bool):** Indicates whether or not the private
        `__decompressed_stream` attribute should be flushed.
        * **force (bool):** Indicates whether or not all `vFile`s should be
        forced to finalize, even if special optimizations might have allowed
        some to ignore this operation.
        """
        for obj in self.carve_objects:
            # Accuracy of bitmap carving is increased on uncompressed volumes
            # by *not* breaking on a zero-chunk. However this breaks processing
            # of compressed files in general, so we only allow it in '-u' mode.
            if (obj.status == "Processing" and
                    (force or
                     (not obj.type == 'bmp' or
                      not config.options['unc_image']))):
                obj.to_file()
        if flush:
            self.__decompressed_stream = ""

    def increment_abs_offset(self):
        """
        Increment the private `__abs_offset` attribute by the length of
        the `__working_cluster`.
        """
        self.__abs_offset += len(self.__working_cluster)

    def inprocess_carve_objects(self, subtype='All'):
        """
        Determine the number of `CarveObjects` that are curretly in
        'Processing' status. Can be optionally restricted to only count
        `CarveObjects` of a specific sub type.

        ### Args:
        * **subtype (str):** Specific subclass type of `CarveObject` to be
        counted. Objects belonging to a different subclass are ignored.

        ### Returns:
        * **count (int):** The number of matching `CarveObjects` that are in
        'Processing' status.
        """
        count = 0
        if subtype == 'All':
            for obj in self.carve_objects:
                if obj.status == 'Processing':
                    count += 1
            return count
        else:
            for obj in self.carve_objects:
                if obj.status == 'Processing' and obj.subclass == subtype:
                    count += 1
            return count

    def process_comp_stream(self):
        """
        Follow a compressed data stream from the beginning of this chunk,
        stored in the `__working_cluster`. Decompress the stream into the
        `__decompressed_stream`, then send the data to all `CarveObject`s in
        the 'Processing' state.
        """
        self.__comp_header = self.__working_cluster[0:2]
        # 0x0000 header indicates the end of this compression stream
        while not (self.__comp_header[0] == chr(0x00) and
                   self.__comp_header[1] == chr(0x00)):
            # Otherwise decode the header to determine this segment's length
            header_decode = ((ord(self.__comp_header[1]) << 8) +
                             ord(self.__comp_header[0]))
            header_len = int((header_decode & 0x0FFF) + 1)
            if (header_decode & 0x8000) == 0x8000:
                header_cbit = True
            else:
                header_cbit = False
            # Grab the data length indicated, plus the next two-byte header
            self.read_bytes(header_len + 4, seek=self.__abs_offset)
            decompressed_offset = len(self.__decompressed_stream)
            # Uncompressed data in the stream can be copied directly into
            # the decompressed stream (minus the two headers)
            if not header_cbit:
                self.__decompressed_stream = "".join(
                    [self.__decompressed_stream, self.__working_cluster[2:-2]])
                for obj in self.carve_objects:
                    if obj.status == "Processing":
                        obj.in_bytes(
                            self.__decompressed_stream[decompressed_offset:])
                if config.options['deep_carve']:
                    self.__double_carve(decompressed_offset)
                # Move abs_offset, extract the next header and repeat
                self.__abs_offset += len(self.__working_cluster) - 2
                self.__comp_header = (self.__working_cluster[-2] +
                                      self.__working_cluster[-1])
                continue
            # Compressed data in the stream must be decompressed first
            else:
                rel_offset = 2 # account for the 2 byte tag we already passed
                # For the length of this segment (until you hit the next header)
                while rel_offset < len(self.__working_cluster) - 2:
                    # Extract and decode the next tag byte
                    self.__tag_byte = self.__working_cluster[rel_offset]
                    rel_offset += 1
                    tag_byte_decode = format(ord(self.__tag_byte), '008b')
                    # For of the 8 bits in the tag byte
                    for i in range(7, -1, -1):
                        # Safely handle a 'partial' tag byte at end of segment
                        if rel_offset >= len(self.__working_cluster) - 2:
                            continue
                        # '0' bit indicates an uncompressed byte
                        if tag_byte_decode[i] == '0':
                            self.__decompressed_stream = "".join(
                                [self.__decompressed_stream,
                                 self.__working_cluster[rel_offset]])
                            rel_offset += 1
                        # '1' bit indicates a compression tuple
                        else:
                            comp_tuple = ord(
                                self.__working_cluster[rel_offset + 1])
                            comp_tuple = (comp_tuple << 8) + \
                                         ord(self.__working_cluster[rel_offset])
                            # Tuple decoding changes based on offset within
                            # the orignal 4K cluster (now dec_stream length)
                            len_mask = 0x0FFF
                            shift_amt = 12
                            rel_cluster_offset = len(
                                self.__decompressed_stream) % 4096 - 1
                            while rel_cluster_offset >= 16:
                                rel_cluster_offset >>= 1
                                len_mask >>= 1
                                shift_amt -= 1
                            # Decode the tuple into backref and length
                            tuple_len = (comp_tuple & len_mask) + 3
                            tuple_backref = (
                                ((len_mask ^ 0xFFFF) & comp_tuple)
                                >> shift_amt) + 1
                            # Locate the backref starting offset
                            backref_start = (len(self.__decompressed_stream) -
                                             tuple_backref)
                            # Is the stream long enough to fulfill the length?
                            if (backref_start + tuple_len <=
                                    len(self.__decompressed_stream)):
                                self.__decompressed_stream = "".join(
                                    [self.__decompressed_stream,
                                     self.__decompressed_stream[
                                         backref_start:
                                         backref_start + tuple_len]])
                            # If not, we have to repeat bytes to meet length
                            else:
                                backref_len = (len(self.__decompressed_stream) -
                                               backref_start)
                                remainder_len = tuple_len % backref_len
                                if not remainder_len == 0:
                                    backref_remainder = \
                                        self.__decompressed_stream[
                                            backref_start:
                                            backref_start + remainder_len]
                                else:
                                    backref_remainder = ""
                                temp_stream = self.__decompressed_stream[
                                    backref_start:
                                    len(self.__decompressed_stream)] * \
                                    (tuple_len // backref_len)
                                self.__decompressed_stream = "".join(
                                    [self.__decompressed_stream,
                                     temp_stream, backref_remainder])
                            rel_offset += 2
                # Finished with this compression header
                for obj in self.carve_objects:
                    if obj.status == "Processing":
                        obj.in_bytes(
                            self.__decompressed_stream[decompressed_offset:])
                if config.options['double_carve']:
                    self.__double_carve(decompressed_offset)
                if config.options['ascii']:
                    self.__ascii_extract(decompressed_offset)
                self.__decompressed_stream = ""
                # Move abs_offset, extract the next header and repeat
                self.__abs_offset += len(self.__working_cluster) - 2
                self.__comp_header = (self.__working_cluster[-2] +
                                      self.__working_cluster[-1])
                continue
        # Found 0x0000 header - this stream is finished.
        rel_offset = self.__abs_offset % 4096
        if rel_offset == 0:
            return
        # Re-align abs_offset to the next 4K cluster boundary. If this
        # file isn't fragmented, its stream will continue there...
        else:
            rel_offset = 4096 - rel_offset - 1
            self.__abs_offset += rel_offset
            self.read_bytes(1, seek=self.__abs_offset)
            self.__abs_offset += 1
            return

    def process_unc_chunk(self):
        """
        Send known-uncompressed data from the `__working_cluster` directly
        to all `CarveObject`s in the 'Processing' state.
        """
        # Carve the MBR if it was found in this cluster.
        if self.__comp_header == '_MBR':
            if not config.options['no_carve']:
                for obj in self.carve_objects:
                    if (obj.type == '_MBR' and
                            obj.status == "Processing"):
                        obj.in_bytes(self.__working_cluster)
            self.__abs_offset += config.options['chunk_size']
            return
        # 0xFF3F on a 4K cluster boundary indicates an uncompressed cluster
        # withing a compressed CU. Switch to comp. state and follow stream,
        # unless we've been told this is an uncompressed volume
        if (self.__working_cluster[0:2] == chr(0xFF) + chr(0x3F) and
                self.__abs_offset % 4096 == 0 and
                not config.options['unc_image']):
            self.compression_state = True
            self.__comp_header = self.__working_cluster[0:2]
            self.__tag_byte = ""
        # Otherwise, copy this uncompressed chunk to the decompressed stream
        # and all in-process vFiles
        else:
            if not config.options['no_carve']:
                decompressed_offset = len(self.__decompressed_stream)
                self.__decompressed_stream = "".join(
                    [self.__decompressed_stream, self.__working_cluster])
                for obj in self.carve_objects:
                    if obj.status == "Processing":
                        obj.in_bytes(
                            self.__decompressed_stream[decompressed_offset:])
                if config.options['double_carve']:
                    self.__double_carve(decompressed_offset)
                if config.options['ascii']:
                    self.__ascii_extract(decompressed_offset)
            self.__abs_offset += config.options['chunk_size']
        return

    def read_bytes(self, length, seek=""):
        """
        Attempt to read data bytes from the disk image file into the
        `__working_cluster`.

        ### Args:
        * **length (int):** Number of bytes to read from the disk image file.
        * **seek (int, optional):** Specifies the absolute offset within
        the disk image file to seek to before reading.

        ### Returns:
        * **True** if *any* bytes were read from the disk image, even if
        the full `length` request was not satisfied.
        * **False** if zero bytes were read.
        """
        if not seek == "":
            self.mm.seek(seek)
        self.__working_cluster = self.mm.read(length)
        if not self.__working_cluster:
            return False
        return True

    def __ascii_extract(self, stream_offset):
        """
        Perform a second analysis of data in the `__decompressed_stream`.
        Identify ASCII data and parse it for `StringTemplates`. Instantiate
        `vStrings` and raw ASCII `vFiles`.

        ### Args:
        * **stream_offset (int):** An absolute offset within the
        decompressed stream from where to begin the analysis.
        """
        for item in config.templates:
            pattern = item.start + item.body
            for match in re.finditer(
                    pattern, self.__decompressed_stream[stream_offset:]):
                # Create a new vString and capture it's ID
                new_id = len(self.carve_objects)
                self.__instantiate_vString(
                    item.type,
                    self.__abs_offset,
                    item.stop)
                # For only that ID, stream in the data from the match
                # offset to the end of the decompressed stream
                for obj in self.carve_objects:
                    if obj.id == new_id:
                        obj.in_bytes(
                            self.__decompressed_stream[
                                stream_offset + match.start() + 1:])
        # If the wait flag was set, return immediately
        if self.__wait_for_ASCII:
            self.__wait_for_ASCII = False
            return
        # If we have any 'ASCII-like' vFiles in process, set the wait
        # flag and return. If raw files are not being preserved, return
        for obj in self.carve_objects:
            if (obj.subclass == 'vFile' and
                    obj.status == "Processing" and obj.ASCII_flag):
                self.__wait_for_ASCII = True
                return
        if not config.options['keep_raw']:
            return
        # Otherwise, perform generic ASCII text matching
        min_len = min([64, config.options['chunk_size'] / 2])
        pattern = r'[\x09\x0A\x0D\x20-\x7E]{' + str(min_len) + ',}'
        for match in re.finditer(
                pattern, self.__decompressed_stream[stream_offset:]):
            # Create a new vFile and capture it's ID
            new_id = len(self.carve_objects)
            self.__instantiate_vFile('_ASCII_raw', self.__abs_offset)
            # For only that ID, stream in the data from the match offset
            # to the end of the decompressed stream
            for obj in self.carve_objects:
                if obj.id == new_id:
                    obj.in_bytes(
                        self.__decompressed_stream[
                            stream_offset + match.start():])

    def __double_carve(self, stream_offset):
        """
        Perform a second analysis of data in the `__decompressed_stream`.
        Identify file signatures that were previously undetectable due to
        being stored compressed or not on a `chunk_size` boundary, and
        instantiate `vFiles`.

        ### Args:
        * **stream_offset (int):** An absolute offset within the
        decompressed stream from where to begin the analysis.
        """
        for sig in config.signatures:
            assert sig.deep_flag in [True, False, 'NoDupe', 'List']
            # Don't operate on signatures that have deep carving disabled
            if not sig.deep_flag:
                continue
            cont = False
            for obj in self.carve_objects:
                # 'NoDupe' signatures won't be processed if a vFile of the
                # same type is already being processed
                if (sig.deep_flag == 'NoDupe' and
                        obj.type == sig.file_type and
                        obj.status == "Processing"):
                    cont = True
                    break
                # 'NoList' signatures won't be processed if a vFile type in
                # their list is already being processed
                if (sig.deep_flag == 'List' and
                        (obj.type in sig.deep_list or
                         obj.type[:-1] in sig.deep_list) and
                        obj.status == "Processing"):
                    cont = True
                    break
            if cont:
                continue # Try the next signature
            # Look for a signature somewhere other than the chunk boundary
            found_offset = self.__decompressed_stream[
                stream_offset + 1:].find(sig.signature)
            if not found_offset == -1:
                # Create a new vFile and capture it's ID
                new_id = len(self.carve_objects)
                self.__instantiate_vFile(
                    sig.file_type + '_',
                    self.__abs_offset,
                    stop_sig=sig.stop_sig,
                    bmp_offset=found_offset)
                # For only that ID, stream in the data from the signature
                # to the end of the decompressed stream
                for obj in self.carve_objects:
                    if obj.id == new_id:
                        obj.in_bytes(
                            self.__decompressed_stream[
                                stream_offset + found_offset + 1:])
            continue # Allow multiple signatures to match - no break

    def __instantiate_vFile(self, filetype, start_offset, stop_sig="",
                            bmp_offset=0):
        """
        Create a new `vFile` object.

        ### Args:
        * **file_type (str):** The extension/type of file, or one of the
        special types '_deepcarve_raw' or '_ASCII_raw'.
        * **start_offset (int):** The offset of a chunk of the disk image file
        within which this file was found.
        * **stop_sig (str, optional):** The footer bytes that will indicate
        the end of the file if later discovered in the data stream.
        * **bmp_offset (int, optional):** Indicates the relative offset
        from a cluster boundary where a 'bmp' file was found. Unused for other
        file types.
        """
        if filetype == '_MBR':
            self.carve_objects.append(
                carve_object.vFile(
                    self.image_id,
                    self.filename,
                    len(self.carve_objects),
                    '_MBR',
                    start_offset,
                    max_bytes=512,
                    compressed=False))
            return
        # For all other non-.bmps, create a vFile with default max length
        if not filetype == 'bmp':
            self.carve_objects.append(
                carve_object.vFile(
                    self.image_id,
                    self.filename,
                    len(self.carve_objects),
                    filetype,
                    start_offset,
                    stop_sig=stop_sig,
                    compressed=self.compression_state))
        # .bmp lengths are extracted from the header, but we need
        # to make sure the header didn't get compressed...
        else:
            # If this chunk is not compressed, no problem.
            if bmp_offset == 0 or bmp_offset == 2:
                len_bytes = 0
                for i in range(bmp_offset + 5, bmp_offset + 1, -1):
                    len_bytes <<= 8
                    len_bytes += ord(self.__working_cluster[i])
                self.carve_objects.append(
                    carve_object.vFile(
                        self.image_id,
                        self.filename,
                        len(self.carve_objects),
                        'bmp',
                        start_offset,
                        max_bytes=len_bytes,
                        compressed=False))
            else:
                # If it passes a sniff test for compression, use default max_len
                if self.__sanity_check_compression_meta(
                        self.__working_cluster[bmp_offset - 3:bmp_offset], 6):
                    self.carve_objects.append(
                        carve_object.vFile(
                            self.image_id,
                            self.filename,
                            len(self.carve_objects),
                            'bmp',
                            start_offset,
                            compressed=self.compression_state))
                else:
                    # Otherwise assume no compression and extract length
                    len_bytes = 0
                    for i in range(bmp_offset + 5, bmp_offset + 1, -1):
                        len_bytes <<= 8
                        len_bytes += ord(self.__working_cluster[i])
                    self.carve_objects.append(
                        carve_object.vFile(
                            self.image_id,
                            self.filename,
                            len(self.carve_objects),
                            'bmp',
                            start_offset,
                            max_bytes=len_bytes,
                            compressed=self.compression_state))
        return

    def __instantiate_vString(self, type_, start_offset, stop=""):
        """
        Create a new `vString` object.

        ### Args:
        * **type_ (str):** The type of ASCII string object, ie: 'email' or
        'CCN'.
        * **start_offset (int):** The offset of a chunk of the disk image file
        within which this string was found.
        * **stop (str):** The set of disallowed characters that will end this
        string if later discovered in the data stream.
        """
        self.carve_objects.append(
            carve_object.vString(
                self.image_id,
                self.filename,
                len(self.carve_objects),
                type_,
                start_offset,
                stop,
                compressed=self.compression_state))

    def __sanity_check_compression_meta(self, three_bytes, sig_len=4):
        """
        Determine whether a set of bytes could plausibly represent a
        compression header and tag byte metadata.

        ### Args:
        * **three_bytes (str):** The three bytes to be evaluated.
        * **sig_len (int, optional):** Length of the file signature found
        immediately following the suspect three bytes. Used to bias the
        determination of plausibility.

        ### Returns:
        **True** if the input could plausibly indicate compressed data
        following
        **False** otherwise.
        """
        header_decode = (ord(three_bytes[1]) << 8) + ord(three_bytes[0])
        header_len = int((header_decode & 0x0FFF) + 1)
        sanity_mask = 1
        mask_shift = sig_len - 1
        while mask_shift >= 1:
            mask_shift -= 1
            sanity_mask <<= 1
        # Is this a plausible compression bit, stream length and tag byte
        if ((header_decode & 0x8000) == 0x8000 and
                header_len in range(256, 3073, 1) and
                (ord(three_bytes[2]) & sanity_mask) == 0x00):
            return True
        else:
            return False

    def __signatureless_id(self):
        """
        Determine whether non-Zero data in this chunk of the image file
        should be considered interesting and deep carved for additional
        processing, or ignored.

        ### Returns:
        * **True** if the data in this chunk is interesting
        * **False** otherwise.
        """
        # Many meta-structures are stored in unicode format which looks like
        # null-delimited ASCII. Also rejects solid fills.
        every_other_byte = self.__working_cluster[1]
        for offset in range(3, 16, 2):
            if self.__working_cluster[offset] == every_other_byte:
                self.__wait_for_zeroes = True
                return False
        # Reject known NTFS MFT structures and the FAT FSinfo sector
        for bad_sig in ['FILE0', 'RCRD(', 'INDX(', 'RSTR', 'RRaA']:
            if not self.__working_cluster[0:16].find(bad_sig) == -1:
                self.__wait_for_zeroes = True
                return False
        # Reject FAT tables
        if (self.__working_cluster[0:3] == chr(0xF8) + chr(0xFF) + chr(0xFF) and
                (self.__working_cluster[3] == chr(0xFF) or
                 self.__working_cluster[3] == chr(0x7F) or
                 self.__working_cluster[3] == chr(0x0F))):
            self.__wait_for_zeroes = True
            return False
        # Reject 'signed' FAT32 structures
        if config.options['chunk_size'] >= 512:
            if self.__working_cluster[510:512] == chr(0x55) + chr(0xAA):
                self.__wait_for_zeroes = True
                return False
        return True
