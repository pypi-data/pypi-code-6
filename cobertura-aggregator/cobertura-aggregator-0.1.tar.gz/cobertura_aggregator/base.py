"""Cobertura report aggregator for a given set of TARGETS"""
import base64
import calendar
import logging
import simplejson
import time
import urllib2
import xml.etree.ElementTree as ET
from tabulate import tabulate

LOGGER = logging.getLogger()


class CoberturaAggregator(object):
    """Cobertura aggregation base class"""
    REPORT_PATH_KEY = 'REPORT_PATH'
    TARGETS_KEY = 'TARGETS'
    TYPE_KEY = 'TYPE'

    def __init__(self, name=None, settings={}):
        self._name = name
        self._report_path = settings.get(self.REPORT_PATH_KEY, '')
        self._targets = settings.get(self.TARGETS_KEY, [])
        self._report = []
        self._target_stats = {}
        for target in self._targets:
            self._target_stats[target] = {
                'lines': 0,
                'lines_missed': 0,
                'cond': 0,
                'cond_missed': 0,
                'line_coverage': float(0),
                'cond_coverage': float(0),
            }

        if self._report_path and self._report_path[-1] != '/':
            self._report_path = '{}/'.format(self._report_path)

        # /path/to/file/1387487334_cobertura_agg.txt
        self._report_file = '{}{}_cobertura_agg.txt'.format(
            self._report_path,
            calendar.timegm(time.gmtime())
            )

    def set_settings(self, name, settings):
        """Reset instance settings"""
        self.__init__(name, settings)

    def get_report_file(self):
        """Get report file path"""
        return self._report_file

    def print_report(self):
        """Print the report"""
        headers = ['Target', 'Line%', 'Branch%']
        table = tabulate(self._report, headers)
        print """

---------
{} REPORT
---------
""".format(self._name)
        print table

        if self._report_path:
            with open(self._report_file, 'w+') as report_file:
                report_file.write(table)

    def generate_report(self):
        """Each aggregator needs to implement this"""
        raise NotImplementedError

    def _get_stats(self, **kwargs):
        """Search for target aggregations"""
        raise NotImplementedError

    def _get_target_stats(self, target, classes):
        """Update target aggregation"""
        raise NotImplementedError

    def _dump_stats(self):
        """Dump aggregations into a useable list for tabulate"""
        for target in self._targets:
            stats = self._target_stats[target]
            self._report.append([
                target,
                "{:.2f}%".format(stats['line_coverage']),
                "{:.2f}%".format(stats['cond_coverage'])
                ]
            )

    def _update_target_stats(self,
                             target,
                             lines_covered,
                             total_lines,
                             branches_covered,
                             total_branches
                             ):
        """Update target stats"""
        stats = self._target_stats[target]
        stats['lines'] += total_lines
        stats['lines_missed'] += (total_lines - lines_covered)
        if total_lines:
            perc = float(stats['lines_missed']) / float(stats['lines'])
            stats['line_coverage'] = 100 - (perc * 100)
        else:
            stats['line_coverage'] = stats['line_coverage'] or float(100)

        stats['cond'] += total_branches
        stats['cond_missed'] += (total_branches - branches_covered)
        if total_branches:
            perc = float(stats['cond_missed']) / float(stats['cond'])
            stats['cond_coverage'] = 100 - (perc * 100)
        else:
            stats['cond_coverage'] = stats['line_coverage'] or float(100)
        self._target_stats[target] = stats


class CoberturaJSONAggregator(CoberturaAggregator):
    """Cobertura REST JSON aggregator"""
    USERNAME_KEY = 'USERNAME'
    API_TOKEN_KEY = 'API_TOKEN'
    DOMAIN_KEY = 'DOMAIN'
    JOBS_KEY = 'JOBS'

    _LINES_KEY = 'Lines'
    _CONDITIONALS_KEY = 'Conditionals'
    _NUMERATOR_KEY = 'numerator'
    _DENOMINATOR_KEY = 'denominator'

    def __init__(self, name=None, settings={}):
        super(CoberturaJSONAggregator, self).__init__(name, settings)
        self._username = settings.get(self.USERNAME_KEY)
        self._api_token = settings.get(self.API_TOKEN_KEY)
        self._domain = settings.get(self.DOMAIN_KEY)
        self._jobs = settings.get(self.JOBS_KEY, [])

        coverage_uri = "lastSuccessfulBuild/cobertura/api/json?depth=4"
        self._cobertura_urls = []
        for job in self._jobs:
            self._cobertura_urls.append(
                "{}/job/{}/{}".format(self._domain, job, coverage_uri)
                )

    def generate_report(self):
        for cobertura_url in self._cobertura_urls:
            auth_header = 'Basic: ' + base64.b64encode('%s:%s' % (
                self._username,
                self._api_token
                )
            ).strip()
            headers = {'Authorization': auth_header}
            request = urllib2.Request(
                cobertura_url,
                headers=headers
            )

            try:
                resp = urllib2.urlopen(request, timeout=5)
                cobertura_json = resp.read()
                cobertura_report = simplejson.loads(cobertura_json)
            except urllib2.HTTPError as e:
                LOGGER.error("{}\nHTTP error: {}".format(cobertura_url, e))
                continue
            except urllib2.URLError as e:
                LOGGER.error("{}\nURL error: {}".format(
                    cobertura_url,
                    e.reason
                    )
                )
                continue
            except simplejson.scanner.JSONDecodeError as e:
                LOGGER.error(
                    "{}\nCobertura URL did not return valid json: {}".format(
                        resp.read(),
                        e
                    )
                )
                continue

            # Drill down to what we care about...
            results = cobertura_report.get('results')
            children = results.get('children')
            for child in children:
                self._get_stats(child.get('children'))

        self._dump_stats()

    def _get_stats(self, children):
        for child in children:
            for target in self._targets:
                if target in child.get('name'):
                    self._get_target_stats(target, child)

    def _get_target_stats(self, target, child):
        lines_covered = 0
        total_lines = 0
        branches_covered = 0
        total_branches = 0

        for element in child.get('elements'):
            name = element.get('name')
            if name == self._LINES_KEY:
                total_lines += element.get(self._DENOMINATOR_KEY)
                lines_covered += element.get(self._NUMERATOR_KEY)
            elif name == self._CONDITIONALS_KEY:
                total_branches += element.get(self._DENOMINATOR_KEY)
                branches_covered += element.get(self._NUMERATOR_KEY)

        self._update_target_stats(**{
            'target': target,
            'lines_covered': lines_covered,
            'total_lines': total_lines,
            'branches_covered': branches_covered,
            'total_branches': total_branches

        })


class CoberturaXMLAggregator(CoberturaAggregator):
    """Cobertura XML aggregator"""
    XML_FILES_KEY = 'XML_FILES'

    def __init__(self, name=None, settings={}):
        super(CoberturaXMLAggregator, self).__init__(name, settings)
        self._cobertura_xml = settings.get(self.XML_FILES_KEY, [])
        self._xml_tree = None

    def generate_report(self):
        for cobertura_report in self._cobertura_xml:
            xml_tree = ET.parse(cobertura_report)

            root = xml_tree.getroot()
            for classes in root.iter('classes'):
                self._get_stats(classes)

        self._dump_stats()

    def _get_stats(self, classes):
        """Search for target aggregations"""
        cobertura_class = classes.find('class')
        class_fn = cobertura_class.get('filename')
        for target in self._targets:
            if class_fn.find(target) == 0:
                self._get_target_stats(target, classes)

    def _get_target_stats(self, target, classes):
        """Update target aggregation"""
        lines_covered = 0
        total_lines = 0
        branches_covered = 0
        total_branches = 0

        for line in classes.iter('line'):
            total_lines += 1
            if int(line.get('hits')) > 0:
                lines_covered += 1

            if line.get('branch') == "true":
                branch_stats = line.get('condition-coverage')
                b_covered, \
                    b_total = self._parse_branch_stats(branch_stats)
                branches_covered += b_covered
                total_branches += b_total

        self._update_target_stats(**{
            'target': target,
            'lines_covered': lines_covered,
            'total_lines': total_lines,
            'branches_covered': branches_covered,
            'total_branches': total_branches

        })

    @staticmethod
    def _parse_branch_stats(s):
        """Parse branch string from XML: condition-coverage="50% (1/2)" """
        covered = 0
        total = 0
        branch_stats = s[s.find("(")+1:s.find(")")]
        covered, total = branch_stats.split('/')
        return int(covered), int(total)
