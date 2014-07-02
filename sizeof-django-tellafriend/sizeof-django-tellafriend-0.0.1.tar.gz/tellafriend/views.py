# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Copyright (c) 2010-2014 Mariusz Smenzyk <mariusz.smenzyk@sizeof.pl>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""

@author: Mariusz Smenzyk
@license: MIT License
@contact: mariusz.smenzyk@sizeof.pl
"""
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.contrib.sites.models import Site
from django.views.generic import CreateView, TemplateView
from tellafriend.forms import TellAFriendForm


class TellafriendView(CreateView):
    """
    Displays the tell-a-friend form and sends out the e-mail
    """
    form_class = TellAFriendForm
    template_name = 'tellafriend/tellafriend.html'

    def get_context_data(self, **kwargs):
        context = super(TellafriendView, self).get_context_data(**kwargs)
        url = self.request.REQUEST['url'] if self.request.REQUEST.has_key('url') else ''
        full_url = 'http://%s%s' % (Site.objects.get_current().domain, url)
        context.update({'url': url, 'tellafriend_url': url, 'tellafriend_full_url': full_url})
        return context

    def get_initial(self):
        context = self.get_context_data()
        return {'url': context['url']}

    def get_success_url(self):
        return reverse('tellafriend_success')

    def form_valid(self, form):
        context = self.request.POST.copy()
        context.update(self.get_context_data())

        text = render_to_string('tellafriend/email.txt', context, context_instance=RequestContext(self.request))
        html = render_to_string('tellafriend/email.html', context, context_instance=RequestContext(self.request))
        msg = EmailMultiAlternatives(_("Recommendation by %s" % self.request.POST.get('email_sender')), text,
                                     settings.EMAIL_SENDER, [self.request.POST.get('email_recipient')])
        msg.attach_alternative(html, "text/html")
        msg.send()

        # Save additional data
        form.instance.user_agent = self.request.META.get('HTTP_USER_AGENT', '')[:255]
        if not self.request.user.is_anonymous():
            form.instance.user = self.request.user
        form.instance.save()

        return super(TellafriendView, self).form_valid(form)


class TellafriendSuccesView(TemplateView):
    template_name = 'tellafriend/success.html'
