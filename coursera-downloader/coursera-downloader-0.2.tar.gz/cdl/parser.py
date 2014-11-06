import os
import urllib
import string
from urlparse import urlparse

from pyquery import PyQuery as pq


def parse(html):
    res = []
    for i in pq(html)('.course-item-list-header'):
        div = pq(i)
        chapter = div('h3').text().strip()
        section = []
        for j in div.nextAll('ul').eq(0).find('li'):
            li = pq(j)
            a = li.find('a.lecture-link')
            lecture = a.text().strip()
            links = [pq(k).attr('href') for k in a.nextAll(
                '.course-lecture-item-resource').eq(0).find('a')]
            section.append((lecture, tuple(links)))
        res.append((chapter, section))
    return res


def esc(s):
    from_ = string.punctuation + string.whitespace
    to = '_' * len(from_)
    trans = string.maketrans(from_, to)
    return string.translate(s, trans)


def generate_download_script(res):
    def wget(href, fname):
        return '''if [ ! -e '%s' ]; then
  wget --no-cookies --header "Cookie: $(cat cookie)" '%s' -O '%s'
fi''' % (fname, href, fname)

    for chapter, content in res:
        path = esc(chapter.encode('utf8'))
        yield "mkdir '%s'" % path

        for lecture, links in content:
            name = os.path.join(path, esc(lecture.encode('utf8')))
            if not links:
                break

            video = links[-1]
            _, ext = os.path.splitext(urlparse(video).path)
            vname = name + ext
            yield wget(video, vname)

            if len(links) >= 2:
                script = links[-2]
                if script.find('srt') > 0:
                    sname = name + '.srt'
                    yield wget(script, sname)

            if len(links) >= 2:
                pdf = [link for link in links if link.endswith('.pdf')]
                if pdf:
                    pdf = pdf[0]
                    pname = os.path.basename(urlparse(pdf).path)
                    pname = urllib.unquote(pname)
                    pname = os.path.join(path, pname)
                    yield wget(pdf, pname)
