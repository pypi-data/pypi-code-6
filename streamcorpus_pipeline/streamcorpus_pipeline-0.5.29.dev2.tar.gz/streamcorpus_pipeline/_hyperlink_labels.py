#!/usr/bin/env python
'''
Pipeline stage for extracting hyperlinks to particular domains as
labels generated by the author.

This software is released under an MIT/X11 open source license.

Copyright 2012-2014 Diffeo, Inc.
'''
from __future__ import absolute_import
import re
import sys
import logging

from streamcorpus import add_annotation, Offset, OffsetType, Annotator, Target, Label
from streamcorpus_pipeline._clean_visible import make_clean_visible
from streamcorpus_pipeline.stages import Configured

logger = logging.getLogger(__name__)

anchors_re = re.compile('''(?P<before>(.|\n)*?)''' + \
                        '''(?P<ahref>\<a\s+(.|\n)*?href''' + \
                        '''(?P<preequals>(\s|\n)*)=(?P<postequals>(\s|\n)*)''' + \
                        '''(?P<quote>("|')?)(?P<href>[^"]*)(?P=quote)''' + \
                        '''(?P<posthref>(.|\n)*?)\>)''' + \
                        '''(?P<anchor>(.|\n)*)''', re.I)

def read_to( idx_bytes, stop_bytes=None, run_bytes=None ):
    '''
    iterates through idx_bytes until a byte in stop_bytes or a byte
    not in run_bytes.

    :rtype (int, string): idx of last byte and all of bytes including
    the terminal byte from stop_bytes or not in run_bytes
    '''
    idx = None
    vals = []
    next_b = None
    while 1:
        try:
            idx, next_b = idx_bytes.next()
        except StopIteration:
            ## maybe something going wrong?
            idx = None
            next_b = None
            break
        ## stop when we see any byte in stop_bytes
        if stop_bytes and next_b in stop_bytes:
            break
        ## stop when we see any byte not in run_bytes
        if run_bytes and next_b not in run_bytes:
            break
        ## assemble the ret_val
        vals.append( next_b )

    ## return whatever we have assembled
    return idx, b''.join(vals), next_b


def iter_attrs( idx_bytes ):
    '''
    called when idx_chars is just past "<a " inside an HTML anchor tag
    
    generates tuple(end_idx, attr_name, attr_value)
    '''
    ## read to the end of the "A" tag
    while 1:
        idx, attr_name, next_b = read_to(idx_bytes, ['=', '>'])
        attr_vals = []

        ## stop if we hit the end of the tag, or end of idx_bytes
        if next_b is None or next_b == '>':
            return
        
        idx, space, quote = read_to(idx_bytes, run_bytes = [' ', '\t', '\n', '\r'])
        if quote not in ['"', "'"]:
            ## caught start of the property value
            attr_vals = [quote]
            quote = ' '
        
        idx, attr_val, next_b = read_to(idx_bytes, [quote, '>'])
        ## next_b had better either balance the start quote, end the
        ## tag, or end idx_bytes
        assert next_b in [quote, '>', None], attr_val
        attr_vals.append( attr_val )

        yield idx, attr_name.strip(), b''.join(attr_vals).strip()        


class hyperlink_labels(Configured):
    '''Creates document labels from hyperlinks in ``body.clean_html``.

    The labels are attached to the stream item body with an annotator
    ID of ``author``.  Any HTML ``<a href="...">`` matching the selection
    criteria will be turned into a label.

    You generally must set either ``all_domains`` or
    ``domain_substrings``.  A typical configuration will look like:

    .. code-block:: yaml

        streamcorpus_pipeline:
          incremental_transforms: [ ..., hyperlink_labels, ... ]
          hyperlink_labels:
            require_abs_url: true
            domain_substrings: [ "trec-kba.org" ]

    Configuration options:

    .. code-block:: yaml

        all_domains: false
        domain_substrings: [ 'trec-kba.org' ]

    A label will only be produced if ``all_domains`` is true, or if
    the hostname part of the URL has one of ``domain_substrings`` as a
    substring.  Note that the default configuration is ``all_domains``
    false and an empty ``domain_substrings`` list, so no labels will
    be produced without additional configuration.

    .. code-block:: yaml

        require_abs_url: true

    Only produce labels for fully-qualified ``http://...`` URLs.  False
    by default.

    .. code-block:: yaml

        offset_types: [BYTES]

    A list containing at least one of ``BYTES`` and ``LINES``
    indicating what sort of document offset should be attached to the
    label.  Only the first value is used.  ``LINES`` is not
    recommended.

    .. code-block:: yaml

        require_clean_html: true

    Cannot be changed.

    '''
    config_name = 'hyperlink_labels'
    default_config = {
        'require_clean_html': True,
        'require_abs_url': False,
        'all_domains': False,
        'domain_substrings': [],
        'offset_types': ['BYTES'],
    }

    def __init__(self, *args, **kwargs):
        super(hyperlink_labels, self).__init__(*args, **kwargs)
        self.offset_type = getattr(OffsetType, self.config['offset_types'][0])
        if self.offset_type != OffsetType.BYTES:
            logger.warn('using offset_type other than BYTES: %r' % self.offset_type)

    def href_filter(self, href):
        '''
        Test whether an href string meets criteria specified by
        configuration parameters 'require_abs_url', which means "does
        it look like it is probably an absolute URL?" and
        'domain_substrings'.  It searches for each of the
        domain_substrings in the href individually, and if any match,
        then returns True.

        :param: href string
        :returns bool:
        '''
        if self.config['require_abs_url']:
            if not href.lower().startswith('http://'):
                return False
        if self.config['all_domains']:
            ## blanket accept all domains as labels
            return True

        if self.config['domain_substrings']:
            parts = href.split('/')
            if len(parts) < 3:
                return False
            domain = parts[2].lower()
            for substring in self.config['domain_substrings']:
                if substring in domain:
                    return True            

    def line_href_anchors(self):
        '''
        simple, regex-based extractor of anchor tags, so we can
        compute LINE offsets for anchor texts and associate them with
        their href.
        
        Generates tuple(href_string, first_byte, byte_length, anchor_text)

        Also, this mangles the body.clean_html so that LINE offsets
        uniquely identify tokens in anchor tags -- quite a kludge.
        '''
        idx = 0
        new_clean_html = ''
        newlines_added = 0
        ## split doc up into pieces that end on an anchor tag
        parts = self.clean_html.split('</a>')
        assert len('</a>'.join(parts) ) == len(self.clean_html)
        for i in range(len(parts)):
            part = parts[i]

            ## try to get an A tag out:
            m = anchors_re.match(part)

            ## if not, then just keep going
            if not m:
                new_clean_html += part
                if i < len(parts) - 1:
                    new_clean_html += '</a>'
                continue

            before = m.group('before')
            ahref = m.group('ahref')

            ## construct a text containing bytes up to the anchor text
            pre_anchor_increment = before + ahref

            ## increment the index to get line number for the anchor
            idx += len( pre_anchor_increment.splitlines() )
            first = idx

            ## usually this will be one, but it could be more than
            ## that when an anchor text contains newlines
            length = len(m.group('anchor').split('\n'))

            ## construct new clean_html with these newlines inserted
            new_clean_html += pre_anchor_increment + '\n' + m.group('anchor') + '\n</a>'

            newlines_added += 2

            ## update the index for the next loop
            idx += length - 1

            yield m.group('href'), first, length, m.group('anchor')

        ## replace clean_html with our new one that has newlines inserted
        assert len(self.clean_html) == len(new_clean_html) - newlines_added
        self.clean_html = new_clean_html

    def byte_href_anchors(self, chars=False):
        '''
        simple, regex-based extractor of anchor tags, so we can
        compute BYTE offsets for anchor texts and associate them with
        their href.
        
        Generates tuple(href_string, first_byte, byte_length, anchor_text)
        '''
        input_buffer = self.clean_html
        if chars:
            input_buffer = input_buffer.decode('utf8')
        idx = 0
        ## split doc up into pieces that end on an anchor tag
        parts = input_buffer.split('</a>')
        assert len('</a>'.join(parts) ) == len(input_buffer)
        for part in parts:
            ## try to get an A tag out:
            m = anchors_re.match(part)

            if not m:
                idx += len(part) + 4
                continue

            before = m.group('before')
            ahref = m.group('ahref')

            ## increment the index to get line number for the anchor
            idx += len(before) + len(ahref)
            first = idx

            ## usually this will be one, but it could be more than
            ## that when an anchor text contains newlines
            length = len(m.group('anchor'))

            ## update the index for the next loop
            # include anchor plus the </a>
            idx += length + 4

            yield m.group('href'), first, length, m.group('anchor')

        assert idx - 4 == len(input_buffer)

    def byte_href_anchors_state_machine(self):
        '''
        byte-based state machine extractor of anchor tags, so we can
        compute byte offsets for anchor texts and associate them with
        their href.
        
        Generates tuple(href_string, first_byte, byte_length, anchor_text)
        '''
        tag_depth = 0
        a_tag_depth = 0
        vals = []
        href = None
        idx_bytes = enumerate( self.clean_html )
        while 1:
            end_idx, val, next_b = read_to( idx_bytes, '<' )
            tag_depth += 1

            if href:
                ## must be inside an anchor tag, so accumulate the
                ## whole anchor
                assert a_tag_depth > 0, (href, self.clean_html)
                vals.append(val)

            ## figure out if start of an "A" anchor tag or close
            ## of a previous tag
            idx, next_b1 = idx_bytes.next()
            if next_b1.lower() == 'a':
                ## could be start of "A" tag
                idx, next_b2 = idx_bytes.next()
                if next_b2 == ' ':
                    a_tag_depth += 1

                    href = None
                    for idx, attr_name, attr_val in iter_attrs( idx_bytes ):
                        if attr_name.lower() == 'href':
                            href = attr_val
                        if idx is None:
                            ## doc ended mid tag, so invalid HTML--> just bail
                            return

                    first = idx + 1

                    ## if we got an href, then we want to keep the
                    ## first byte idx of the anchor:
                    if href:
                        ## Someone could nest an A tag inside another
                        ## A tag, which is invalid (even in HTML5), so
                        ## vals could be nonempty.  We only generate
                        ## the leaf-level A tags in these rare cases
                        ## of nested A tags, so reset it:
                        vals = []

            elif next_b1 == '/':
                idx, next_b1 = idx_bytes.next()
                if next_b1 == 'a':
                    ## could be end of "A" tag
                    idx, next_b2 = idx_bytes.next()
                    if next_b2 == '>':
                        a_tag_depth -= 1
                        if href:
                            ## join is much faster than using += above
                            anchor = b''.join(vals)
                            length = len(anchor)

                            ## yield the data
                            yield href, first, len(anchor), anchor

                            ## reset, no yield again in a nested A tag
                            href = None

            else:
                ## the next_b was not part of </a> or a nested <a tag,
                ## so keep it in the output
                vals.append(next_b)


    def make_labels(self, clean_html, clean_visible=None):
        '''
        Make a list of Labels for 'author' and the filtered hrefs &
        anchors
        '''
        if   self.offset_type == OffsetType.BYTES:
            parser = self.byte_href_anchors

        elif self.offset_type == OffsetType.LINES:
            parser = self.line_href_anchors

        labels = []
        ## make clean_html accessible as a class property so we can 
        self.clean_html = clean_html
        for href, first, length, value in parser():
            if self.href_filter(href):
                '''
                if clean_visible:
                    _check_html = self.clean_html.splitlines()[first-10:10+first+length]
                    _check_visi =   clean_visible.splitlines()[first:first+length]
                    if not make_clean_visible(_check_html) == _check_visi:
                        print len(self.clean_html.splitlines())
                        print len(clean_visible.splitlines())

                        print href
                        print '\t html: %r' % _check_html
                        print '\t visi: %r' % _check_visi
                '''
                ## add a label for every href
                label = Label(
                    annotator = Annotator(annotator_id = 'author'),
                    target = Target(target_id = href),
                    )
                ## the offset type is specified by the config
                label.offsets[self.offset_type] = Offset(
                    first=first, length=length, 
                    value=value,
                    ## the string name of the content field, not the
                    ## content itself :-)
                    content_form='clean_html')
                labels.append(label)

        return labels

    def __call__(self, stream_item, context):
        '''
        Act as an incremental transform in the kba.pipeline
        '''
        ## right now, we only do clean_html
        assert self.config.get('require_clean_html', True)

        if stream_item.body and stream_item.body.clean_html:
            labels = self.make_labels(stream_item.body.clean_html,
                                      stream_item.body.clean_visible)
            if labels:
                if self.offset_type == OffsetType.LINES:
                    ## for LINES-type labels, must replace clean_html
                    ## with a new one that has newlines inserted
                    stream_item.body.clean_html = self.clean_html

                ## Remove any previous author labels
                stream_item.body.labels['author'] = []

                ## also add the new labels
                add_annotation(stream_item.body, *labels)
        return stream_item

if __name__ == '__main__':
    clean_html = sys.stdin.read()
    for m in anchors_re.finditer(clean_html):
        print m.group('href'), m.group('anchor')
