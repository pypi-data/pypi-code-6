import os

import jos.download as d
import jos.parse as p

starting_url = 'http://www.degruyter.com/view/j/jos.2014.30.issue-2/issue-files/jos.2014.30.issue-2.xml'

PDF_DIR = os.path.join(os.path.expanduser('~'), '.jos', 'pdfs')
try:
    os.makedirs(PDF_DIR)
except FileExistsError:
    pass

def main():
    issues = set()
    links = {'issues': [starting_url], 'pdfs': []}

    while issues.union(links['issues']) != issues:
        response = None
        for issue in set(links['issues']).difference(issues):
            if response == None:
                response = d.get(issue)
            else:
                response = d.get(issue,
                    headers = {'referer': response.url},
                    cookies = dict(response.cookies))
            if not response.ok:
                raise ValueError('Bad issue response at %s' % response.url)
            issues.add(issue)

            links = p.links(response)
            for pdf in links['pdfs']:
                pdf_response = d.get(pdf,
                    headers = {'referer': response.url},
                    cookies = dict(response.cookies))
                if pdf_response.ok:
                    filename = pdf_response.headers['content-disposition'].split('=')[1]
                    with open(os.path.join(PDF_DIR, filename), 'wb') as fp:
                        fp.write(pdf_response.content)
                else:
                    break
                    raise ValueError('Bad PDF response at %s' % pdf_response.url)
