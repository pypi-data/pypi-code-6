from django.db.models.signals import post_save
from django.dispatch import receiver
from hacore.models import Device
from hautomation_gpio.cmds import set_to_output
from hautomation_gpio.utils import is_output


@receiver(post_save, sender=Device)
def post_save_gpio_device(sender, instance, **kwargs):
    if instance.protocol.name == "GPIO" and not is_output(instance.did):
        set_to_output(instance.did)


