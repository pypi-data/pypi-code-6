# coding: utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from urlparse import urlparse
from .models import FlickrLink


class FlickrLinkForm(forms.ModelForm):

    class Meta:
        model = FlickrLink

    def clean_url(self):
        url = self.cleaned_data['url']

        if u"/player" in url:
            url = url[:url.rindex(u"/player")]

        url_parsed = urlparse(url)
        path = url_parsed.path.split(u"/")

        if not u"flickr.com" in url_parsed.netloc or len(path) != 5 or \
                path[1] != "photos" or path[3] != "sets":
            raise forms.ValidationError(_(u"Incorrect URL format."))
        return url

    def save(self, commit=True):
        instance = super(FlickrLinkForm, self).save(commit=False)
        


        if commit:
            instance.save()
        return instance
