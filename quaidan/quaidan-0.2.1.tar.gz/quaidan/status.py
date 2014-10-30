"""Domain model of the blancer manager page. This module contains a parser
that creates the model from the page's HTML, too.
"""

from collections import namedtuple
from lxml.html import fragments_fromstring
import re

Status = namedtuple('Status', 'clusters')
Cluster = namedtuple('Cluster', 'name members')
Member = namedtuple(
    'Member', 'worker_url route route_redirect load_factor lb_set \
    ignore_errors draining_mode enabled hot_standby elected busy load \
    transferred read'
)

def parse_balancer_manager_page(html):
    """Parse the balancer manager page and create an object with the
    information found on the page.

    :param html: The raw HTML of the balancer manager page.
    :returns: an Status object with the information found on the page.
    """
    clusters = __extract_clusters_from_html(html)
    return Status(clusters)

def __extract_clusters_from_html(html):
    """Parse the clusters of a balancer manager page.

    :param html: The raw HTML of the balancer manager page.
    :returns: a list of clusters.
    """
    clusters = []
    for section in re.findall('(<h3>.+?)<hr />', html.replace('\n', '')):
        cluster = _parse_cluster(section)
        clusters.append(cluster)
    return clusters

def _parse_cluster(html):
    """Parse the HTML of a single cluster.

    :param html: The raw HTML of a single cluster. This is the HTML that \
        starts with the ``h3`` tag and ends before the ``<hr />`` tag.
    :returns: a cluster.
    """
    first_table_processed = False
    for element in fragments_fromstring(html):
        if element.tag == 'h3':
            href = element.find('a').get('href')
            name = re.findall('b=(.*?)&', href)[0]
        elif element.tag == 'table':
            if first_table_processed:
                members = _parse_members(element)
            else:
                first_table_processed = True
    return Cluster(name, members)

def _parse_members(element):
    """Parse the member table node of a single cluster.

    :param html: The table node of a single cluster that contains the \
        information about the members.
    :returns: a list of members.
    """
    members = []
    for index, row in enumerate(element.findall('tr')):
        if index != 0:
            member = _parse_member(row)
            members.append(member)
    return members

def _parse_member(element):
    """Parse the table row node of a single member.

    :param html: The table row node of a single member.
    :returns: a member.
    """
    cells = element.findall('td')
    status = cells[5].text
    ignore_errors = "Ign" in status
    draining_mode = "Drn" in status
    enabled = "Ok" in status
    hot_standby = "Stby" in status
    return Member(
        cells[0].find('a').text, cells[1].text, cells[2].text,
        int(cells[3].text), int(cells[4].text), ignore_errors,
        draining_mode, enabled, hot_standby, int(cells[6].text),
        int(cells[7].text), int(cells[8].text), cells[9].text.strip(),
        cells[10].text.strip()
    )

