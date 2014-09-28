from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Pronoun(models.Model):
    name = models.CharField(max_length='30')
    description = models.CharField(max_length=256)

    subject = models.CharField(max_length='10', help_text="He, she, it")
    object = models.CharField(max_length='10', help_text="Her, him, it")
    reflexive = models.CharField(max_length='15', help_text="Itself, himself, herself")
    possessive_pronoun = models.CharField(max_length='10', help_text="Hers, his, its")
    possessive_determiner = models.CharField(max_length='10', help_text="His, her, its")

    def em(self):
        return self.subject
    she_he = em
    he_she = em

    def ey(self):
        return self.object
    him_her = ey
    her_him = ey

    def emself(self):
        return self.reflexive
    herself_himself = emself
    himself_herself = emself

    def eir(self):
        return self.possessive_pronoun
    his_hers = eir
    hers_his = eir

    def eirs(self):
        return self.possessive_determiner
    his_her = eirs
    her_his = eirs

    def __str__(self):
        return self.name
