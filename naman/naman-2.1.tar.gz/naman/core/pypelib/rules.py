import logging

from naman.core.pypelib import RuleTable

from naman.core.mappings import get_mappings
from naman.core.models import Rule
from django.conf import settings


def evaluate(machine):

    mappings = get_mappings()
    table = RuleTable(
        "Decide tunned temp",
        mappings,
        "RegexParser",
        #rawfile,
        "RAWFile",
        None)

    table.setPolicy(False)

    table.addRule("if heater_manual = 1  then accept do tune_to_confort")

    for rule in Rule.objects.filter(active=True, thermostat=True).order_by("pk"):
        table.addRule(rule.to_pypelib())

    if settings.DEBUG:
        table.dump()

    metaObj = {}

    try:
        table.evaluate(metaObj)
    except Exception:
        mappings["tune_to_economic"]()

    table1 = RuleTable(
        "Decide flame status",
        mappings,
        "RegexParser",
        #rawfile,
        "RAWFile",
        None)
    table1.addRule("if heater_on = 0 then deny")
    table1.addRule("if current_internal_temperature < tuned_temperature then accept")
    if settings.DEBUG:
        table1.dump()
        
    try:
        table1.evaluate(metaObj)
        try:
            mappings["start_flame"]()
        except Exception, ex:
            logging.error("ERROR: Cant start flame: %s" % ex)
    except Exception as e:
        try:
            mappings["stop_flame"]()
        except Exception, ex:
            logging.error("ERROR: Cant stop flame: %s" % ex)

