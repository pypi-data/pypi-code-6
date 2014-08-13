from modeltranslation.translator import translator
from modeltranslation.translator import TranslationOptions

from .models import TeamMember
from .models import Service
from .models import Client
from .models import Country
from .models import Project
from .models import Image
from .models import Team
from .models import Testimonial


class TeamMemberTranslationOptions(TranslationOptions):
    fields = ('position', 'summary', 'strong_skills')


class CountryTranslationOptions(TranslationOptions):
    fields = ('name', )


class ServiceTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


class ClientTranslationOptions(TranslationOptions):
    fields = ('description',)


class ProjectTranslationOptions(TranslationOptions):
    fields = ('description',)


class ImageTranslationOptions(TranslationOptions):
    fields = ('description',)


class TeamTranslationOptions(TranslationOptions):
    fields = ('description', 'name')


class TestimonialTranslationOptions(TranslationOptions):
    fields = ('testimonial',)


translator.register(TeamMember, TeamMemberTranslationOptions)
translator.register(Service, ServiceTranslationOptions)
translator.register(Client, ClientTranslationOptions)
translator.register(Country, CountryTranslationOptions)
translator.register(Project, ProjectTranslationOptions)
translator.register(Image, ImageTranslationOptions)
translator.register(Team, TeamTranslationOptions)
translator.register(Testimonial, TestimonialTranslationOptions)
