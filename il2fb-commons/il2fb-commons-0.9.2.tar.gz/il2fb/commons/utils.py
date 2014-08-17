# -*- coding: utf-8 -*-
import os

from verboselib.factory import TranslationsFactory

here = os.path.abspath(os.path.dirname(__file__))
locale_dir = os.path.join(here, "locale")

translations = TranslationsFactory("il2fb-commons", locale_dir)
