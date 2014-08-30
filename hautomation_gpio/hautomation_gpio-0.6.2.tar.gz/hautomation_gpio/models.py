
from hautomation_gpio.cmds import set_to_output
from hautomation_gpio.utils import is_output
import logging

logger = logging.getLogger("driver")
try:
    from django.conf import settings
except:
    import hautomation_gpio.settings

logger.setLevel(settings.LOG_LEVEL)


try:
    from django.db.models.signals import post_save
    from django.dispatch import receiver
    from hacore.models import Device
    #TODO test without django installed
    @receiver(post_save, sender=Device)
    def post_save_gpio_device(sender, instance, **kwargs):
        if instance.protocol.name == "GPIO" and not is_output(instance.did):
            logger.debug("Just saved GPIO device not OUT-configured, changing it to OUT...")
            set_to_output(instance.did)
except Exception:
    logger.debug("No suppor for Django detected, thus not activating hacore.models.Device post_save signal")
    pass


