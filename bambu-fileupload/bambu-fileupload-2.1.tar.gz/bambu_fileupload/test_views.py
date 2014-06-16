from django.contrib.auth.models import User, AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.utils.http import urlencode
from bambu_fileupload import DEFAULT_HANDLERS
from bambu_fileupload.models import FileUploadContext
from bambu_fileupload.views import upload
from os import path
from uuid import uuid4
import json

class FileUploadViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = upload

    @override_settings(FILEUPLOAD_HANDLERS = DEFAULT_HANDLERS)
    def test_authenticated(self):
        guid = unicode(uuid4())
        user = User.objects.create_user(
            username = 'test',
            password = 'test',
            email = 'test@example.com'
        )

        with open(
            path.join(
                path.dirname(__file__),
                'static', 'fileupload', 'img', 'filetypes', '_blank.png'
            ),
            'rb'
        ) as image:
            request = self.factory.post(
                '/fileupload/?%s' % urlencode(
                    dict(
                        handler = 'attachments',
                        params = urlencode(
                            dict(
                                guid = guid
                            )
                        )
                    )
                ),
                data = {
                    'fileupload[]': image
                }
            )

            request.user = user
            SessionMiddleware().process_request(request)
            MessageMiddleware().process_request(request)
            request.session.save()
            response = upload(request)
            content = json.loads(response.content)

            self.assertEqual(
                len(content), 1
            )

            self.assertEqual(
                content[0]['size'], 446
            )

            self.assertEqual(
                content[0]['type'], 'image/png'
            )

            self.assertEqual(
                content[0]['name'], '_blank.png'
            )

            context = FileUploadContext.objects.get(
                uuid = guid
            )

            self.assertEqual(
                context.attachments.count(),
                1
            )

            context.attachments.all().delete()
