import requests
from django_thermostat import settings
from hautomation_restclient.cmds import pl_switch
from django_thermostat.models import Context, Thermometer
from django.core.urlresolvers import reverse
from time import strftime, localtime, mktime, strptime
import os, logging, simplejson


def current_external_temperature(mo=None):
    try:
        print "entering external"

        if not settings.LIST_THERMOMETERS_API is None:
            ret = requests.get("http://localhost%stemperatures=True" % reverse("temperatures"))
            therms = ret.json()
        else:
            therms = simplejson.loads(read_temperatures())
        print "los termometros:%s" % therms
        for therm in therms:
            data = therms[therm]

            if data["is_external"]:
                print "external: %s" % float(data["temp"]["celsius"])
                return float(data["temp"]["celsius"])
    except Exception as et:
        print "EXXXXXXXXXXXXXXXXXXXXXXXXXXXX:%s" % et


def current_internal_temperature(mo=None):
    try:
        print "entering internal"    

        if not settings.LIST_THERMOMETERS_API is None:
            ret = requests.get("http://localhost%stemperatures=True" % reverse("temperatures"))
            therms = ret.json()
        else:
            therms = simplejson.loads(read_temperatures())
        print "los termometros:%s" % therms
        for therm in therms:
            data = therms[therm]
      
            if data["is_internal"]:
                print "internal: %s" % float(data["temp"]["celsius"])
                return float(data["temp"]["celsius"])
    except Exception as et:
        print "EXXXXXXXXXXXXXXXXXXXXXXXXXXXX:%s" % et
    

def confort_temperature(mo=None):
    ctxt = Context.objects.get()
    if ctxt.flame:
        return float(ctxt.confort_temperature) + settings.HEATER_MARGIN
    return ctxt.confort_temperature


def economic_temperature(mo=None):
    ctxt = Context.objects.get()
    if ctxt.flame:
        return float(ctxt.economic_temperature) + settings.HEATER_MARGIN
    return ctxt.economic_temperature


def tuned_temperature(mo=None):
    ctxt = Context.objects.get()
    if ctxt.flame:
        return float(ctxt.tuned_temperature) + settings.HEATER_MARGIN
    return ctxt.tuned_temperature


def tune_to_confort(mo=None):
    #print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Tunning to confort"
    logging.debug("Tunning to confort")
    ctxt = Context.objects.get()
    ctxt.tuned_temperature = ctxt.confort_temperature
    ctxt.save()


def tune_to_economic(mo=None):
    #print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Tuning to economic"
    logging.debug("Tunning to economic")
    ctxt = Context.objects.get()
    
    ctxt.tuned_temperature = ctxt.economic_temperature
    ctxt.save()
    


def heater_manual(mo=None):
    return int(Context.objects.get().manual)


def heater_on(mo=None):
    return int(Context.objects.get().heat_on)


def set_heater_on(no=None):
    ctxt = Context.objects.get()
    ctxt.heat_on = True
    ctxt.save()


def set_heater_off(no=None):
    ctxt = Context.objects.get()
    ctxt.heat_on = False
    ctxt.save()


def flame_on():
    return 1 if Context.objects.get().flame else 0


def log_flame_stats(new_state):
    if settings.FLAME_STATS: 
        with open(settings.FLAME_STATS_PATH, "a") as stats:
            t = localtime()      
            st = strftime(settings.FLAME_STATS_DATE_FORMAT, t)
            stats.write("%s - %s - %f\n" % (
                "ON" if new_state else "OFF", 
                st, 
                mktime(strptime(st, settings.FLAME_STATS_DATE_FORMAT))))
            
def start_flame():
    #print "Starting flame"
    
    ctxt = Context.objects.get()
    if ctxt.flame:
        logging.debug("Not starting flame, because its already started")
        return
 
    pl_switch(
        settings.HEATER_PROTOCOL,
        settings.HEATER_DID,
        "on",
        settings.HEATER_API,
        settings.HEATER_USERNAME,
        settings.HEATER_PASSWORD)

    ctxt.flame = True
    ctxt.save()

    logging.debug("Flame started")
    log_flame_stats(True)


def stop_flame():
    ctxt = Context.objects.get()
    if not ctxt.flame:
        logging.debug("Not stopping flame, because its already stopped")
        return

    pl_switch(
        settings.HEATER_PROTOCOL,
        settings.HEATER_DID,
        "off",
        settings.HEATER_API,
        settings.HEATER_USERNAME,
        settings.HEATER_PASSWORD)

    ctxt.flame = False
    ctxt.save()

    logging.debug("Flame stopped")
    log_flame_stats(False)
    #print "%s flame stopped" % strftime("%d.%m.%Y %H:%M:%S", localtime())


mappings = [
    current_internal_temperature,
    current_external_temperature,
    confort_temperature,
    economic_temperature,
    start_flame,
    stop_flame,
    heater_manual,
    heater_on,
    flame_on,
    tune_to_confort,
    tune_to_economic,
    tuned_temperature,
    set_heater_off,
    set_heater_on,
    ]
