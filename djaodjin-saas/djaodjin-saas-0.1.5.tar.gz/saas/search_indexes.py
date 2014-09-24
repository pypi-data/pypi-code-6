# Copyright (c) 2014, DjaoDjin inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from haystack import indexes
from saas.utils import datetime_or_now
from saas.models import Charge, Organization, Transaction


class ChargeIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Haystack search index for charges
    """
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='customer__full_name')
    pub_date = indexes.DateTimeField(model_attr='created_at')

    def get_model(self):
        return Charge

    def index_queryset(self, using=None):
        """
        Used when the entire index for model is updated.
        """
        return self.get_model().objects.filter(
            created_at__lte=datetime_or_now())


class OrganizationIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Haystack search index for organizations
    """
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='full_name')
    pub_date = indexes.DateTimeField(model_attr='created_at')

    def get_model(self):
        return Organization

    def index_queryset(self, using=None):
        """
        Used when the entire index for model is updated.
        """
        return self.get_model().objects.filter(
            created_at__lte=datetime_or_now())


class TransactionIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Haystack search index for transactions
    """
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='orig_organization__full_name')
    pub_date = indexes.DateTimeField(model_attr='created_at')

    def get_model(self):
        return Transaction

    def index_queryset(self, using=None):
        """
        Used when the entire index for model is updated.
        """
        return self.get_model().objects.filter(
            created_at__lte=datetime_or_now())
