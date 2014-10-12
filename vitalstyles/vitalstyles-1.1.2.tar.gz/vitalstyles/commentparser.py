import re
import textwrap

from . import markdownparser
from . import settings


class Comment(object):
    newlinepattern = re.compile(r'\n|\r|\r\n')
    def __init__(self, comment):
        self.comment = self._clean(comment)
        self.unparsed_comment = comment

    def _clean(self, comment):
        whitespacenormalized = textwrap.dedent(comment).rstrip()
        if len(whitespacenormalized) > 1 and whitespacenormalized[0] == '*':
            lines = self.newlinepattern.split(whitespacenormalized)
            starlines = [line[1:] for line in lines if line.startswith('*')]
            if len(starlines) == len(lines):
                return textwrap.dedent('\n'.join(starlines))
        else:
            return whitespacenormalized

    def __str__(self):
        return str(unicode(self).encode('ascii', 'ignore'))

    def __unicode__(self):
        return self.comment

    def to_html(self, settingsobject=None):
        settingsobject = settingsobject or settings.Settings()
        return markdownparser.to_html(self.comment, settingsobject)


class Parse(object):
    """
    Parses the given ``text`` looking for comments matching one of the following styles::

        /**
        A comment.
        */
       
       /**
        * A comment.
        */
       
    This does NOT work::

        /** A comment */
    """

    commentpattern = re.compile(r'(?<=/\*\*)[ \t]*(?:\n|\r|\r\n)(.*?)(?=\*/)', re.DOTALL)

    def __init__(self, text):
        """
        Parameters:
            text (unicode): The text to parse.
        """
        self.text = text
        self.commentbodies = self.commentpattern.findall(self.text)

    def __getitem__(self, index):
        return Comment(self.commentbodies[index])

    def __len__(self):
        return len(self.commentbodies)

    def __iter__(self):
        for commentbody in self.commentbodies:
            yield Comment(commentbody)

    def unicodelist(self):
        return map(lambda c: unicode(c), self)