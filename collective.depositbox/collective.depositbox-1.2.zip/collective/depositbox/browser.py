import csv
from AccessControl import Unauthorized
from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFCore.utils import _checkPermission
from StringIO import StringIO
from collective.depositbox.interfaces import IDepositBox


class DepositBoxView(BrowserView):
    """Simple browser view that knows how to interact with the deposit box.

    Simply a front end for the adapter really.
    """

    # Character set to use for exporting to csv.  Possibly iso-8859-1
    # is nicer for Excel.
    export_charset = 'utf-8'

    def put(self, value, token=None):
        context = aq_inner(self.context)
        box = IDepositBox(context)
        secret = box.put(value, token=token)
        return secret

    def confirm(self, secret, token=None):
        context = aq_inner(self.context)
        box = IDepositBox(context)
        confirmed = box.confirm(secret, token=token)
        return confirmed

    def get(self, secret, token=None):
        context = aq_inner(self.context)
        box = IDepositBox(context)
        stored = box.get(secret, token=token)
        return stored

    def pop(self, secret, token=None):
        context = aq_inner(self.context)
        box = IDepositBox(context)
        stored = box.pop(secret, token=token)
        return stored

    def edit(self, secret, value, token=None):
        context = aq_inner(self.context)
        box = IDepositBox(context)
        box.edit(secret, value, token=token)

    def get_all_confirmed(self, raise_exceptions=True):
        context = aq_inner(self.context)
        if not _checkPermission("collective.depositbox: View Data", context):
            if raise_exceptions:
                raise Unauthorized("Not allowed to get confirmed data.")
            return []
        box = IDepositBox(context)
        return box.get_all_confirmed()

    def confirmed_as_csv(self):
        out = StringIO()
        writer = csv.writer(out, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for values in self.get_all_confirmed():
            decoded = []
            for value in values:
                if isinstance(value, str):
                    value = value.decode(self.export_charset, 'replace')
                decoded.append(value)
            writer.writerow(values)
        response = self.request.response
        response.setHeader('content-type',
                           'application/vnd.ms-excel; charset=%s' %
                           self.export_charset)
        filename = 'deposit-box-data.csv'
        response.setHeader('content-disposition',
                           'attachment; filename=%s' % filename)
        return out.getvalue()
