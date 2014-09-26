# -*- coding: utf-8 -*-
"""
Mod for "djangocms_text_ckeditor", a djangocms plugin to use CKEditor (4.x) instead of the default one

This mod contains some tricks to enabled "django-filebrowser" usage with "image" plugin from CKEditor.

And some contained patches/fixes :

* the codemirror plugin that is not included in djangocms-text-ckeditor;
* Some missed images for the "showblocks" plugin;
* A system to use the "template" plugin (see views.EditorTemplatesListView for more usage details);
* Some patch/overwrites to have content preview and editor more near to Foundation;

Links :

* https://github.com/divio/djangocms-text-ckeditor/
* http://ckeditor.com/
* http://docs.ckeditor.com

Flaws :

* Impossible actuellement d'intégrer Foundation dans l'éditeur parce que F3 force une propriété CSS qui gênent la disposition attendu par l'éditeur, nottement sur le plugin ckeditor magicdiv qui est indispensable;
* Dans les pages CMS, L'éditeur a un mauvais comportement de positionnement : il est bien trop petit, le fullscreen ne sert quasiment à rien et les fenetres modal sont mal positionnés. Le rendu du contenu juste au dessus de l'éditeur doit y être pour quelque chose..
* CKEditor n'aime pas les balises de liens "<a>" qui englobe un ou plusieurs éléments de type "bloc", il les réécrient comme il les aiment. S'il ne le faisait pas cela pourrait gener l'édition.
"""