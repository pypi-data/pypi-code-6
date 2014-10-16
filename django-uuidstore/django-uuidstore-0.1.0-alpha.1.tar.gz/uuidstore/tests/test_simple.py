from django.test import TestCase
from uuidstore.tests.models import (
    ModelWithDetatchedUUID,
    ModelWithMonkeyPatchedUUID,
    )
from uuidstore.models import ObjectUUID
import uuid


class SimpleTestClient(TestCase):

    def test_model_with_detatched_uuid(self):
        obj = ModelWithDetatchedUUID.objects.create(title='Test')
        stored = ObjectUUID.objects.get_for_instance(obj)

        # We're talking about the same object?
        self.assertEqual(obj, stored.content_object)

        try:
            id = uuid.UUID(stored.uuid)  # noqa
        except ValueError:
            msg = "'{}' is not a valid UUID.".format(stored.uuid)
            self.fail(msg)

    def test_model_with_monkey_patched_uuid(self):
        obj = ModelWithMonkeyPatchedUUID.objects.create(title='Test')

        stored = ObjectUUID.objects.get_for_instance(obj)

        # We're talking about the same object?
        self.assertEqual(obj, stored.content_object)

        # ... and it matches the one on the object?
        self.assertEqual(stored.uuid, obj.uuid)

        try:
            id = uuid.UUID(obj.uuid)  # noqa
        except ValueError:
            msg = "'{}' is not a valid UUID.".format(obj.uuid)
            self.fail(msg)
