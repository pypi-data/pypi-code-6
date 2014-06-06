import factory

from . import content, models


class DummyFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Dummy

    @factory.post_generation
    def content(self, create, extracted, **kwargs):
        if not create:
            return
        Content = models.Dummy.content_type_for(content.TestContent)
        Content.objects.create(parent=self, region='body')
