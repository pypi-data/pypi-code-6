from re import compile, match

class BaseOptions:

    def get_dict(self):
        return dict((k, v) for k, v in vars(self).iteritems() if v)

    def to_query(self):
        dict = self.get_dict()
        array = list()
        for k, v in dict.iteritems():
            array.append(k + "=" + self.__get_string_value(v))
        return "&".join(array)

    def __get_string_value(self, value):
        if isinstance(value, bool):
            return str(value).lower()
        else:
            return str(value)

    def populate_from_key_value_pair(self, key, value):
        # Iterate over instance variables
        for k, v in vars(self).iteritems():
            if k == key:
                setattr(self, key, value)
                break

    def populate_from_list(self, list):
        pattern = compile("([^?=&]+)(=([^&]*))?")
        if list is None:
            return
        for item in list:
            match = pattern.match(item)
            self.populate_from_key_value_pair(match.group(1), match.group(3))


class CommonOptions(BaseOptions):
    def __init__(self):
        self.characters_per_caption_line = None
        self.elementlist_version = None
        self.emit_speaker_change_token_as = None
        self.mask_profanity = None
        self.remove_sounds_list = None
        self.remove_sound_references = None
        self.replace_slang = None
        self.sound_boundaries = None


class TranscriptionOptions(CommonOptions):
    def __init__(self):
        self.create_paragraphs = None
        self.newlines_after_paragraph = None
        self.newlines_after_sentence = None
        self.timecode_every_paragraph = None
        self.timecode_format = None
        self.time_code_interval = None
        self.timecode_offset = None


class CaptionOptions(CommonOptions):
    def __init__(self):
        self.build_url = None
        self.caption_words_min = None
        self.caption_by_sentence = None
        self.dfxp_header = None
        self.disallow_dangling = None
        self.display_effects_speaker_as = None
        self.display_speaker_id = None
        self.force_case = None
        self.include_dfxp_metadata = None
        self.layout_target_caption_length_ms = None
        self.line_break_on_sentence = None
        self.line_ending_format = None
        self.lines_per_caption = None
        self.maximum_caption_duration = None
        self.merge_gap_interval = None
        self.minimum_caption_length_ms = None
        self.minimum_gap_between_captions_ms = None
        self.minimum_merge_gap_interval = None
        self.qt_seamless = None
        self.silence_max_ms = None
        self.single_speaker_per_caption = None
        self.sound_threshold = None
        self.sound_tokens_by_caption = None
        self.sound_tokens_by_line = None
        self.sound_tokens_by_caption_list = None
        self.sound_tokens_by_line_list = None
        self.speaker_on_new_line = None
        self.srt_format = None
        self.srt_print = None
        self.strip_square_brackets = None
        self.utf8_mark = None

class PerformTranscriptionOptions(BaseOptions):
    def __init__(self):
        self.customer_approval_steps = None
        self.customer_approval_tool = None
        self.custom_metadata = None
        self.notes = None
        self.return_iwp = None
        self.speaker_id = None