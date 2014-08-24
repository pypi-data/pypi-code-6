"""Download species names in a given language from Avibase."""

import lxml.html
import urllib2

from csvkit import CSVKitWriter


synonyms = {
    "English": "EN",
    "Czech": "CS",
    "German": "DE",
    "Danish": "DA",
    "Spanish": "ES",
    "Finnish": "FI",
    "French": "FR",
    "Icelandic": "IS",
    "Italian": "IT",
    "Japanese": "JP",
    "Dutch": "NL",
    "Norwegian": "NO",
    "Polish": "PL",
    "Portuguese": "PT",
    "Brasilian": "PTBR",
    "Russian": "RU",
    "Slovak": "SK",
    "Swedish": "SV",
    "Chinese": "ZH",
    "Galician": "GL",
}


def run(*args):

    avibase_index = 'http://avibase.bsc-eoc.org/checklist.jsp?list=eBird'
    list_name = args[0]
    language = synonyms[args[1]]

    response = urllib2.urlopen(avibase_index)
    html = lxml.html.fromstring(response.read())
    links = html.cssselect('.AVBregions td a')

    names = []

    for link in links:
        if link.text == list_name:
            checklist_url = 'http://avibase.bsc-eoc.org/' + link.attrib['href']
            if language != 'EN':
                checklist_url += '&synlang=%s' % language
            response = urllib2.urlopen(checklist_url)
            html = lxml.html.fromstring(response.read())

            for row in html.cssselect('.AVBlist tr.highlight1'):
                cells = row.cssselect('td')
                scientific_name = cells[1].cssselect('i')[0].text
                if language == 'EN':
                    common_name = cells[0].text
                else:
                    common_name = cells[2].text
                if common_name:
                    common_name = common_name.encode('latin_1').decode('utf-8')
                else:
                    common_name = scientific_name
                names.append((scientific_name, common_name))

    suffix = language.lower()

    with open('species_names_%s.csv' % suffix, 'wb') as fp:
        writer = CSVKitWriter(fp)
        writer.writerow(('scientific_name', 'common_name_%s' % suffix))
        for name in names:
            writer.writerow(name)
