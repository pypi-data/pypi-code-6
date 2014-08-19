"""Cobertura aggregation runner"""
import argparse
import imp
from cli_tools import argument
from base import CoberturaXMLAggregator, CoberturaJSONAggregator


@argument('--config', type=str, help="Path to aggregator configuration file")
def run(config):
    """runner"""
    settings_mod = imp.load_source('SETTINGS', config)
    settings_dict = settings_mod.SETTINGS

    # Convert to use python argparse built in
    api_agg = CoberturaJSONAggregator()
    xml_agg = CoberturaXMLAggregator()
    for name, settings in settings_dict.iteritems():
        agg_type = settings.get(CoberturaXMLAggregator.TYPE_KEY)
        if agg_type == 'xml':
            aggregator = xml_agg
        elif agg_type == 'jenkins_api':
            aggregator = api_agg

        aggregator.set_settings(name, settings)
        aggregator.generate_report()
        aggregator.print_report()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str)
    args = parser.parse_args()
    run(args.config)
