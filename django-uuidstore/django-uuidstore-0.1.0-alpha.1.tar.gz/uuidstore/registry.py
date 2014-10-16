# Django
from django.db.models import signals

registry = {}


class AlreadyRegistered(Exception):
    """
    An attempt was made to register a model more than once.
    """
    pass


class DoesNotMatch(Exception):
    pass


@property
def get_uuid(self):
    if not hasattr(self, '_objectuuid'):
        from .models import ObjectUUID
        obj = ObjectUUID.objects.get_for_instance(self)
        if obj:
            self._objectuuid = obj.uuid
    return getattr(self, '_objectuuid', None)


def pre_save(sender, instance, **kwargs):
    from .models import ObjectUUID

    # Take no action for non-registered models
    if sender not in registry.keys():
        return

    stored = ObjectUUID.objects.get_for_instance(instance)
    if not stored:
        return

    uuid_descriptor = registry[sender].get('uuid_descriptor')
    if uuid_descriptor:
        object_uuid = getattr(instance, uuid_descriptor, None)

        if object_uuid and not str(object_uuid) == str(stored.uuid):
            raise DoesNotMatch(
                "UUIDs do not match for '%s.%s'" % (
                    sender._meta.object_name,
                    uuid_descriptor
                    )
                )


def post_save(sender, instance, created, *args, **kwargs):
    from .models import ObjectUUID

    # Take no action for non-registered models
    if sender not in registry.keys():
        return

    stored = ObjectUUID.objects.get_for_instance(instance)
    if not stored:
        stored = ObjectUUID()
        stored.content_object = instance
        stored.save()

    # What's the attribute name to look for?
    uuid_descriptor = registry[sender].get('uuid_descriptor')

    if uuid_descriptor:
        object_uuid = getattr(instance, uuid_descriptor, None)
        if not object_uuid:
            setattr(instance, uuid_descriptor, stored.uuid)
            instance.save()


def register(model, uuid_descriptor=None):
    """
    Sets the given model class up for working with central UUIDS.
    """

    if model in registry.keys():
        raise AlreadyRegistered(
            "The model '%s' has already been registered".format(
                model._meta.object_name
                )
            )

    # Add model to the registry
    registry[model] = {'uuid_descriptor': uuid_descriptor}

    # Hook up the signals
    signals.post_save.connect(post_save, model)
    signals.pre_save.connect(pre_save, model)

    # Make the uuid available on the model if it hasn't been denormalised
    # This feels more than a little crufty!
    field_names = [field.attname for field in model._meta.fields]
    if uuid_descriptor and uuid_descriptor not in field_names:
        model.add_to_class(uuid_descriptor, get_uuid)
