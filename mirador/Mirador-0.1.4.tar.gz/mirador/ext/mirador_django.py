from __future__ import absolute_import
from ..errors import MiradorException
from ..client import MiradorClient

try:
    import django.db
    import django.db.models
    from django.db.models.signals import pre_save
    from django.dispatch import receiver
except ImportError:
    print "error: failed to import django"
    raise

# only want to expose moderate_field
# when someone goes after the whole package
__all__ = (
    'moderate_field'
)


def get_model_image(instance, image_field_name):
    "retrieve the image object from the model safely"

    if not instance:
        return None

    if image_field_name not in instance:
        raise MiradorException(
            "field '%s' not in instance" % image_field_name)

    image = instance[image_field_name]

    if not image or not getattr(image, 'read', None):
        return None

    return image


def classify_file(client, file, output_type=float):
    "use the mirador client to classify the file, parse result"

    result = client.classify_files(file)
    if not result:
        return None

    return result.value if output_type == float else result.safe


def moderate_field(model=None, image_field_name=None,
                   moderation_field_name=None,
                   moderation_field_type=float,
                   on_moderation=None, api_key=''):
    """
    Attach to a model's `pre_save` hook, updating the
    `moderation_field_name` with the value of the Mirador
    API result. This field is a float by default, but can also
    be a boolean indicating flagging (based on our threshold).
    For asynchronous results, provide a callback for `on_moderation`
    instead of a `moderation_field.` This will be called with the following
    parameters::
        def on_moderation_cb(model_instance, is_safe, value):
            "is_safe - boolean, value - float"
    """

    print "attaching hook"

    @receiver(pre_save, sender=model)
    def on_presave_signal(sender, **kwargs):

        if not 'instance' in kwargs:
            return None


        instance = kwargs['instance']
        image = get_model_image(
            instance, image_field_name)

        print "received instance: {}".format(instance)

        if not instance or not image:
            return None

        mirador_client = MiradorClient(api_key)

        # if the user has passed in a callback, use this by default
        # and do not update the original model. This will use an
        # asynchronous request in `requests`.
        if on_moderation is not None:

            def moderation_cb_wrapper(results):
                if not results or len(results) != 1:
                    return on_moderation(image, None, None)

                on_moderation(instance, results[0].safe, results[0].value)

            mirador_client.async_classify_files([image], moderation_cb_wrapper)
            return None

        print "classifying image: {}".format(image)

        # if this fails, the output will be `None`
        col_data = classify_file(
            mirador_client, image, moderation_field_type)

        # put the data onto the instance; will be saved in the db
        instance[moderation_field_name] = col_data
        return col_data
