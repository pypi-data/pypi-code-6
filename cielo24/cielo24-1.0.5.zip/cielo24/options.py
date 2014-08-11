from re import compile

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
    def __init__(self,
                 characters_per_caption_line = None,
                 elementlist_version = None,
                 emit_speaker_change_token_as = None,
                 mask_profanity = None,
                 remove_sounds_list = None,
                 remove_sound_references = None,
                 replace_slang = None,
                 sound_boundaries = None):
        self.characters_per_caption_line = characters_per_caption_line
        self.elementlist_version = elementlist_version
        self.emit_speaker_change_token_as = emit_speaker_change_token_as
        self.mask_profanity = mask_profanity
        self.remove_sounds_list = remove_sounds_list
        self.remove_sound_references = remove_sound_references
        self.replace_slang = replace_slang
        self.sound_boundaries = sound_boundaries


class TranscriptionOptions(CommonOptions):
    def __init__(self,
                 create_paragraphs = None,
                 newlines_after_paragraph = None,
                 newlines_after_sentence = None,
                 timecode_every_paragraph = None,
                 timecode_format = None,
                 time_code_interval = None,
                 timecode_offset = None):
        self.create_paragraphs = create_paragraphs
        self.newlines_after_paragraph = newlines_after_paragraph
        self.newlines_after_sentence = newlines_after_sentence
        self.timecode_every_paragraph = timecode_every_paragraph
        self.timecode_format = timecode_format
        self.time_code_interval = time_code_interval
        self.timecode_offset = timecode_offset


class CaptionOptions(CommonOptions):
    def __init__(self,
                 build_url = None,
                 caption_words_min = None,
                 caption_by_sentence = None,
                 dfxp_header = None,
                 disallow_dangling = None,
                 display_effects_speaker_as = None,
                 display_speaker_id = None,
                 force_case = None,
                 include_dfxp_metadata = None,
                 layout_target_caption_length_ms = None,
                 line_break_on_sentence = None,
                 line_ending_format = None,
                 lines_per_caption = None,
                 maximum_caption_duration = None,
                 merge_gap_interval = None,
                 minimum_caption_length_ms = None,
                 minimum_gap_between_captions_ms = None,
                 minimum_merge_gap_interval = None,
                 qt_seamless = None,
                 silence_max_ms = None,
                 single_speaker_per_caption = None,
                 sound_threshold = None,
                 sound_tokens_by_caption = None,
                 sound_tokens_by_line = None,
                 sound_tokens_by_caption_list = None,
                 sound_tokens_by_line_list = None,
                 speaker_on_new_line = None,
                 srt_format = None,
                 srt_print = None,
                 strip_square_brackets = None,
                 utf8_mark = None):
        self.build_url = build_url
        self.caption_words_min = caption_words_min
        self.caption_by_sentence = caption_by_sentence
        self.dfxp_header = dfxp_header
        self.disallow_dangling = disallow_dangling
        self.display_effects_speaker_as = display_effects_speaker_as
        self.display_speaker_id = display_speaker_id
        self.force_case = force_case
        self.include_dfxp_metadata = include_dfxp_metadata
        self.layout_target_caption_length_ms = layout_target_caption_length_ms
        self.line_break_on_sentence = line_break_on_sentence
        self.line_ending_format = line_ending_format
        self.lines_per_caption = lines_per_caption
        self.maximum_caption_duration = maximum_caption_duration
        self.merge_gap_interval = merge_gap_interval
        self.minimum_caption_length_ms = minimum_caption_length_ms
        self.minimum_gap_between_captions_ms = minimum_gap_between_captions_ms
        self.minimum_merge_gap_interval = minimum_merge_gap_interval
        self.qt_seamless = qt_seamless
        self.silence_max_ms = silence_max_ms
        self.single_speaker_per_caption = single_speaker_per_caption
        self.sound_threshold = sound_threshold
        self.sound_tokens_by_caption = sound_tokens_by_caption
        self.sound_tokens_by_line = sound_tokens_by_line
        self.sound_tokens_by_caption_list = sound_tokens_by_caption_list
        self.sound_tokens_by_line_list = sound_tokens_by_line_list
        self.speaker_on_new_line = speaker_on_new_line
        self.srt_format = srt_format
        self.srt_print = srt_print
        self.strip_square_brackets = strip_square_brackets
        self.utf8_mark = utf8_mark

class PerformTranscriptionOptions(BaseOptions):
    def __init__(self,
                 customer_approval_steps = None,
                 customer_approval_tool = None,
                 custom_metadata = None,
                 notes = None,
                 return_iwp = None,
                 speaker_id = None):
        self.customer_approval_steps = customer_approval_steps
        self.customer_approval_tool = customer_approval_tool
        self.custom_metadata = custom_metadata
        self.notes = notes
        self.return_iwp = return_iwp
        self.speaker_id = speaker_id