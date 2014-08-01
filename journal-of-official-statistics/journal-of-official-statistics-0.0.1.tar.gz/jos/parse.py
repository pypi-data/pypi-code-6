import lxml.html

XPATHS = {
    'issues': 'id("issuesToc")//a/@href',
    'pdfs': '//div[@class="fullContentLink"]/a/@href',
}

def links(response):
    html = lxml.html.fromstring(response.text)
    html.make_links_absolute(response.url)
    return {name: html.xpath(xpath) for name, xpath in XPATHS.items()}
