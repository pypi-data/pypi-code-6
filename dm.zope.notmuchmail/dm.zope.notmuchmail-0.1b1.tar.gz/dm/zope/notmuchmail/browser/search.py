# Copyright (C) 2012-2014 by Dr. Dieter Maurer <dieter@handshake.de>
# All rights resevered -- see "LICENSE.txt" for details.
"""Email search and result presentation."""
from email.header import decode_header, make_header
from email import message_from_file
from itertools import islice
from datetime import datetime

from zope.interface import Interface
from zope.component import getUtility
from zope.schema import TextLine
from zope.i18nmessageid import MessageFactory
from zope.formlib.form import Fields, action
from ZTUtils import make_query
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from five.formlib.formbase import PageForm, SubPageForm

from dm.zope.notmuchmail.interfaces import \
     INotMuchDatabase, IAdditionalHeaderItems

_ = MessageFactory('dm_zope_notmuchmail')


class ISimpleSearchParams(Interface):
  search_terms = TextLine(
    title=_(u"search_terms_title",
            u"Search terms",
            ),
    description=_(
      u"search_terms_description",
      u"""\
       The  search  terms  can  consist of free-form text (and quoted phrases)
       which  will  match  all  messages  that  contain  all  of   the   given
       terms/phrases in the body, the subject, or any of the sender or recipient headers.

       As a special case, a search  string  consisting  of  exactly  a  single
       asterisk ("*") will match all messages.

       In  addition  to free text, the following prefixes can be used to force
       terms to match against specific portions of an email, (where <brackets>
       indicate user-supplied values):

            from:<name-or-address>

            to:<name-or-address>

            subject:<word-or-quoted-phrase>

            attachment:<word>

            tag:<tag> (or is:<tag>)

            id:<message-id>

            thread:<thread-id>

            folder:<directory-path>

       The  from: prefix is used to match the name or address of the sender of
       an email message.

       The to: prefix is used to match the names or addresses of any recipient
       of an email message, (whether To, Cc, or Bcc).

       Any  term  prefixed with subject: will match only text from the subject
       of an email. Searching for a phrase in  the  subject  is  supported  by
       including quotation marks around the phrase, immediately following subject:.

       The attachment: prefix can be used to search for specific filenames (or
       extensions) of attachments to email messages.

       For  tag:  and is: valid tag values include inbox and unread by default
       for new messages added by notmuch new as well as any other  tag  values
       added manually with notmuch tag.

       For  id:, message ID values are the literal contents of the Message-ID:
       header of email messages, but without the '<', '>' delimiters.

       The thread: prefix can be used with the thread ID values that are  generated  internally  by  notmuch  (and do not appear in email messages).
       These thread ID values can be seen in the first column of  output  from
       notmuch search

       The  folder:  prefix can be used to search for email message files that
       are contained within particular directories within the mail store. Only
       the  directory  components  below  the top-level mail database path are
       available to be searched.

       In addition to individual terms, multiple terms can  be  combined  with
       Boolean  operators  ( and, or, not , etc.). Each term in the query will
       be implicitly connected by a logical AND if  no  explicit  operator  is
       provided,  (except  that  terms with a common prefix will be implicitly
       combined with OR until we get Xapian defect #402 fixed).

       Parentheses can also be used to control the combination of the  Boolean
       operators.

       Finally, results can be restricted to only messages within a particular
       time range, (based on the Date: header) with a syntax of:

            <initial-timestamp>..<final-timestamp>

       Each timestamp is a number representing the  number  of  seconds  since
       1970-01-01  00:00:00  UTC.  This  is  not  the most convenient means of
       expressing date ranges, but until notmuch is fixed  to  accept  a  more
       convenient  form, one can use the date program to construct timestamps.
       For example, with the bash shell the following syntax would  specify  a
       date range to return messages from 2009-10-01 until the current time:

            $(date +%s -d 2009-10-01)..$(date +%s)
       """
      )
    )


class SimpleSearch(PageForm):
  label = _(u"simple_search", u"Simple email search")
  form_fields = Fields(ISimpleSearchParams)

  OVERVIEW_NAME = "email_search_threads" # can be overridden

  @action(_(u"action_search", u"Search"))
  def search(self, action, data): self.do_search(data["search_terms"])

  def do_search(self, search_terms):
    r = self.request
    r.response.redirect(
      r["URL1"] + "/@@" + self.OVERVIEW_NAME + "?" +
      make_query(search_terms=search_terms)
      )


class ViewBase(BrowserView):
  """Base class for search result related views."""

  def nm_db(self):
    return getUtility(INotMuchDatabase)

  _jqui = None

  def jqui(self):
    jqui = self._jqui
    if jqui is None:
      from .interfaces import IJqUi
      jqui = self._jqui = IJqUi.providedBy(self.context)
    return jqui


class Threads(ViewBase):
  """Threads overview for search result.

  This view has parameters `search_terms` (unicode string)
  and optionally `b_start` (int).
  """

  # how many threads should be presented per batch
  BATCH_SIZE = 100

  def info(self):
    """a mapping describing a threads batch.

    The mapping contains keys:

     `batch`
       the batch

     `b_start`
       the batch start index

     `b_next`, `b_prev`
       the index for the next or previous batch (or `None`).

     `b_url`
       the base url to construct links to the next/previous batch.

     `b_size`
       the batch size

     `b_range`
       `None` when no batching is necessary; otherwise
       the range of thread numbers represented by `batch`.
    """
    r = self.request; terms = r["search_terms"]
    bs = self.BATCH_SIZE
    threads = self.nm_db().create_query(terms).search_threads()
    b_start = r.get("b_start", 0)
    batch = map(self.preprocess, islice(threads, b_start, b_start + bs))
    if b_start > 0: b_prev = max(b_start - bs, 0)
    else: b_prev = None
    b_next = len(batch) == bs and b_start + bs or None
    return dict(
      search_terms=terms,
      batch=batch,
      b_start=b_start,
      b_next=b_next,
      b_prev=b_prev,
      b_url=r["URL"] + "?" + make_query(search_terms=terms),
      b_size=bs,
      b_range=(b_next or b_prev) is not None and "%d -- %d" % (b_start+1, b_start + len(batch))
      )

  def preprocess(self, t):
    """preprocess thread *t*."""
    return dict(
      thread=t,
      id=t.get_thread_id(),
      msgnos="%d/%d" % (t.get_matched_messages(), t.get_total_messages()),
      authors=t.get_authors(),
      subject=t.get_subject(),
      dates="%s -- %s" % (mkdate(t.get_oldest_date()), mkdate(t.get_newest_date())),
      tags=", ".join(t.get_tags()),
      url="@@email_search_thread?" + make_query(
        tid=t.get_thread_id(),
        search_terms=self.request["search_terms"],
        ),
      )

class SimpleSearchCombined(SimpleSearch, Threads, SubPageForm):
  """Page representing both the form as well as the search results (if available).
  """
  template = ViewPageTemplateFile("combined.pt")
  form_template = SubPageForm.template

  def do_search(self, search_terms):
    self.request.form["search_terms"] = search_terms
    return self.template()
    

  
  
class Thread(ViewBase):
  """Single thread in search result.

  This view has parameters `search_terms` (unicode string)
  and `tid` (the thread id).

  It provides an hierarchical view on the messages in the thread.
  """

  def info(self):
    r = self.request
    tid = r["tid"]; terms = r.get("search_terms")
    qt = u"thread:" + tid
    q = terms and "(%s) AND %s" % (terms, qt) or qt
    th = self.nm_db().create_query(q).search_threads().next()
    return dict(
      tid=tid,
      search_terms=terms,
      msgs=map(self.process_message, th.get_toplevel_messages())
      )

  STD_HEADERS = "From To CC Subject Date".split()

  def process_message(self, msg):
    r = self.request
    gh = msg.get_header
    msgid = msg.get_message_id()
    return dict(
      tid=r["tid"],
      search_terms=r.get("search_terms", ""),
      msgid=msgid,
      header_items=[(name, gh(name.lower())) for name in self.STD_HEADERS]
                   + list(IAdditionalHeaderItems(msg, ())),
      matched=msg.get_flag(msg.FLAG.MATCH),
      tags=", ".join(msg.get_tags()),
      msgs=map(self.process_message, msg.get_replies()),
      url="@@email_search_message?" + make_query(
        tid=r["tid"], search_terms=r.get("search_terms", ""), msgid=msgid,
        ),
      file=msg.get_filename(),
      )



class Message(Thread):
  """Single message in single thread in search result.

  This view has parameters `msgid` (the message's message id),
  search_terms` (unicode string) and `tid` (the thread id).

  It shows the text/plain part of the message together with
  thread navigation.
  """

  def info(self):
    msgid = self.request["msgid"]
    thread_info = super(Message, self).info()
    def lookup(msgs, parent):
      """lookup *msgid* in *msgs*, return mapping describing the message or `None`."""
      for i, msg in enumerate(msgs):
        if msg["msgid"] == msgid:
          msg["parent"] = parent
          msg["prev"] = i and msgs[i-1]
          msg["next"] = i < len(msgs) - 1 and msgs[i + 1]
          return msg
        msg = lookup(msg["msgs"], msg)
        if msg is not None: return msg
    msg = lookup(thread_info["msgs"], None)
    m = message_from_file(open(msg["file"], "rt"))
    while m.is_multipart() and m.get_content_type() != "multipart/alternative":
      m = m.get_payload()[0]
    if m.get_content_type() == "multipart/alternative":
      for p in m.get_payload():
        if p.get_content_type() == "text/plain": m = p; break
    if m.get_content_type() == "text/plain":
      msg["body"] = m.get_payload(decode=True)
    else: msg["body"] = None
    return msg
      

def mkdate(ts):
  """date from timestamp *ts*."""
  return datetime.fromtimestamp(ts)


# should not be necessary ("notmuch" converts automatically to unicode
#  -- for correct "encoded-word" according to RFC2047
def decode_msg_header(hv):
  """decode message header value *hv* to unicode."""
  try: hv = str(hv)
  except UnicodeError: return hv # hopefully already decoded
  return unicode(make_header(decode_header(hv)))
