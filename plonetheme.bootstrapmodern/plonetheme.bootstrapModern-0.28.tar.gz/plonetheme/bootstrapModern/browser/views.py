from plone.app.layout.viewlets.common import FooterViewlet
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five import BrowserView
from AccessControl import getSecurityManager
from Products.CMFPlone.PloneBatch import Batch
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.interfaces import IColumn
from zope.interface import Interface
from plone.portlets.interfaces import IPortletManager
from plone.memoize.instance import memoize
from zope.component import getMultiAdapter
from collective.portletpage.browser.portletpage import TwoColumns
from plone.portlet.collection import collection as base
from plone.app.search.browser import Search
from plone.app.layout.viewlets.common import GlobalSectionsViewlet
try:
    from Products.PloneGetPaid.interfaces import IBuyableMarker
    from Products.PloneGetPaid.interfaces import PayableMarkerMap
    from Products.PloneGetPaid.interfaces import IPayableMarker
    GETPAID_EXISTS = True
except ImportError:
    GETPAID_EXISTS = False

class CommonBrowserView(BrowserView):
    """
    Common utilities for all the other views
    """
    nxt = None
    prv = None
    
    def cacheNextPrev(self):
        """
        Caches the values for next and prev
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog.queryCatalog({"portal_type": "Media Event",
                                 "sort_on": "start",
                                 "hasMedia": True,
                                 "review_state": "published"})
        
        for i in range(0, len(results)):
            if results[i].UID == self.context.UID():
                if i < len(results) - 2:
                    self.nxt = results[i +1]
    
                if i > 0:
                    self.prv = results[i -1]
    
    """Base class for index page views
    """
    @memoize
    def plone_view(self):
        return getMultiAdapter((self.context, self.request), name=u"plone")

    def getNextEvent(self):
        """
        Gets the next event in chronological order.
        """
        if self.nxt is None:
            self.cacheNextPrev()
        
        return self.nxt
    
    def getPrevEvent(self):
        """
        Gets the previous event in chronological order
        """
        if self.prv is None:
            self.cacheNextPrev()
        
        return self.prv
    
    def showManageButton(self):
        secman = getSecurityManager()
        if not secman.checkPermission('Portlets: Manage portlets', self.context):
            return False
        else:
            return True
        
    def addPaypalButton(self, label, name, price):
        return """
            <form action="https://www.paypal.com/cgi-bin/webscr" method="post" onSubmit="return Arnolfini.trackEcommerce('%(name)s', '%(price).2f', 'Book')">
                <input name="business" type="hidden" value="general@intk.com" />
                <input name="amount" type="hidden" value="%(price).2f" />
                <input name="item_name" type="hidden" value="%(name)s" />
                <input name="no-shipping" type="hidden" value="1" />
                <input name="currency_code" type="hidden" value="GBP" />
                <input name="cpp_header_image" type="hidden" value="http://new.arnolfini.org.uk/++resource++plonetheme.arnolfini.images/arnolfiniLogo.png" />
                <input name="return" type="hidden" value="http://www.arnolfini.org.uk/purchase/thank-you/" />
                <input name="cmd" type="hidden" value="_xclick" />
                <input type="submit" value="%(label)s" />
            </form>
        """%{"price": price, "name": name, "label": label}
    
    def payable(self, item):
        """Return the payable (shippable) version of the context.
        """
        if GETPAID_EXISTS:
            iface = PayableMarkerMap.get(IBuyableMarker, None)
            if iface is None:
                print("Something is badly wrong here.")
                return None
            return iface( item )
        else:
            return none
        
    def checkPermission(self, item, permission):
        secman = getSecurityManager()
        return secman.checkPermission(permission, item)
    
    def getTagsAsClass(self, item):
        
        classes = []
        
        if not hasattr(item, 'getURL'):
            catalog = getToolByName(self.context, 'portal_catalog')
            brains = catalog.queryCatalog({"UID": item.UID()})
            item = brains[0]
        
        for tag in item.Subject:
            classes.append("tag_%s"%tag.replace(" ", "_"))
        
        return " ".join(classes)
    
    def slideshow(self, parent):
        """
        Creates a slideshow with the media from parent
        """
        parentURL = parent.absolute_url()
        structure = """
        <div class="embededMediaShow">
            <a  href="%s?recursive=true">slideshow</a>
        </div>
        """%parentURL
        
        return structure
    
    def checkYoutubeLink(self, link):
        """
        Check if a URL is a youtube video
        """
        isYoutube = link.find("youtube") != -1
        youtubeId = ""
        amp = link.find("&")
    
        if isYoutube and amp != -1:
            youtubeId = link[link.find("?v=")+3:amp]
        elif isYoutube and amp == -1:
            youtubeId = link[link.find("?v=")+3:]
    
        return isYoutube, youtubeId
        
    def checkVimeoLink(self, link):
        """
        Check if URL is a vimeo video
        """
        isVimeo = link.find("vimeo") != -1
        vimeoId = ""
        
        if isVimeo:
            vimeoId = link.split("vimeo.com/")[1]
            
        return isVimeo, vimeoId
    
    def getLeadMediaTag(self, item, scale="large"):
        catalog = getToolByName(self.context, 'portal_catalog')
        if item.portal_type == 'Link':
            isYoutube, youtubeId = self.checkYoutubeLink(item.getRemoteUrl)
            isVimeo, vimeoId = self.checkVimeoLink(item.getRemoteUrl)
            embed = ""
            
            if isYoutube:
                return '<iframe id="'+youtubeId+'" width="100%" height="393" src="http://www.youtube.com/embed/'+youtubeId+'?rel=0&enablejsapi=1" frameborder="0" allowfullscreen></iframe>'
            elif isVimeo:
                return '<iframe src="http://player.vimeo.com/video/'+vimeoId+'?title=0&amp;byline=0&amp;portrait=0" width="100%" height="393" frameborder="0"></iframe>'

        if item.portal_type == 'Image':
            if hasattr(item, 'getURL'):
                lead = item.getURL()
            else:
                lead = item.absolute_url()
        elif hasattr(item, 'leadMedia'):
            leadUID = item.leadMedia
            #print leadUID
            leadBrain = catalog.queryCatalog({"UID": leadUID})
            if len(leadBrain) != 0:
                lead = leadBrain[0].getURL()
            else:
                lead = None

        else:
            brains = catalog.queryCatalog({"UID": item.UID()})
            #print brains
            if len(brains) != 0:
                leadUID = brains[0].leadMedia
                leadBrain = catalog.queryCatalog({"UID": leadUID})
                if len(leadBrain) != 0:
                    lead = leadBrain[0].getURL()
                else:
                    lead = None
            else:
                lead = None

        if lead is not None:
            crop = ""
            if hasattr(item, 'getURL'):
                return '<img src="%(url)s" alt="%(title)s" title="%(title)s" />%(crop)s'%{'url': "%s/image_%s"%(lead, scale), 'title':item.Title, 'crop':crop}
            else:
                return '<img src="%(url)s" alt="%(title)s" title="%(title)s" />%(crop)s'%{'url': "%s/image_%s"%(lead, scale), 'title':item.Title(), 'crop':crop}
        else:
            return ""

    def containsMedia(self, item):
        if item.portal_type == "Collection":
            return len(self.getCollectionMedia(item)) > 0
        
        if hasattr(item, 'hasMedia'):
            return item.hasMedia
        else:
            catalog = getToolByName(self.context, 'portal_catalog')
            brains = catalog.queryCatalog({"UID": item.UID()})
            if len(brains) != 0:
                return brains[0].hasMedia
            else:
                return False
    
    def getPressKit(self, item):
        if item.restrictedTraverse('@@plone').isStructuralFolder():
            catalog = getToolByName(self.context, 'portal_catalog')
            plone_utils = getToolByName(self.context, 'plone_utils')
                
            path = '/'.join(item.getPhysicalPath())
            sm = getSecurityManager() 
            
            results = catalog.searchResults(path = {'query' : path}, portal_type = 'Press Kit')
            
            for result in results:
                if sm.checkPermission('View', result):
                    return result
            
            return None
        else:
            return None
    
    def trimText(self, text, limit, strip=False):
        if strip:
            text = self.stripTags(text)
    
        if len(text) > limit: 
            res = text[0:limit]
            lastspace = res.rfind(" ")
            res = res[0:lastspace] + " ..."
            return res
        else:
            return text
            
    def stripTags(self, text):
        return re.sub('<[^<]+?>', '', text)
    
    def getTwoWayRelatedContent(self):
        """
        Gets all the manually related content both related items of the current context and items where the current context is marked as related.
        """
        filtered = []
        related = []
        related = self.context.getRefs()
        backRelated = self.context.getBRefs()
        
        related.extend(backRelated)
        
        result = self._uniq(related);
        
        for res in result:
            if self.checkPermission(res, 'View'):
                filtered.append(res)
                
        return filtered
        
    def getContentAsLinks(self, content):
        """
        A commodity, this formats a content list as an HTML structure of titles with links. Comma separated. Used to list the artists related to an exhibition.
        """
        result = []
        workflow = getToolByName(self.context,'portal_workflow')
        sortedContent = sorted(content, key=lambda res: res.portal_type == 'Media Person' and self._normalizePersonName(res.title) or res.title)
        for res in sortedContent:
            if self.checkPermission(res, 'View'):
                if res.portal_type == 'Media Person':
                    result.append('<a href="%(link)s" class="%(state_class)s">%(title)s</a>'%{'link':res.absolute_url(), 'title':self._normalizePersonName(res.title), 'state_class': 'state-' + queryUtility(IIDNormalizer).normalize(workflow.getInfoFor(res,'review_state'))})
                else:
                    result.append('<a href="%(link)s" class="%(state_class)s">%(title)s</a>'%{'link':res.absolute_url(), 'title':res.title, 'state_class': 'state-' + queryUtility(IIDNormalizer).normalize(workflow.getInfoFor(res,'review_state'))})               
        
        return ", ".join(result)
    
    def getTwoWayRelatedContentOfType(self, typeList):
        result = []
        for res in self.getTwoWayRelatedContent():
            if res.portal_type in typeList:
                result.append(res)
                
        return result
    
    def _normalizePersonName(self, person):
        names = person.split(",")
        if len(names) == 2:
            return "%s %s"%(names[1], names[0])
        else:
            return person
          
    def isEventPast(self, event):
        """
        Checks if the event is already past
        """
        if event.portal_type != 'Event' and event.portal_type != 'Media Event':
            return False
        else:
            t = DateTime(time.time())
            if event.end() is not None:
                end = DateTime(event.end())
                return end.year() < t.year() or (end.year() == t.year() and end.month() < t.month()) or(end.year() == t.year() and end.month() == t.month() and end.day() < t.day())
            else:
                start = DateTime(event.start())
                return start.year() < t.year() or (start.year() == t.year() and start.month() < t.month()) or(start.year() == t.year() and start.month() == t.month() and start.day() < t.day())
            
    
    def getCurrentTime(self):
        """
        Utility, returns a current DateTime object.
        """
        return DateTime()
    
    def getFormattedEventDate(self, event):
        """
        Formats the start and end dates properly and marks the event as past or future
        """
        if event.portal_type != 'Event' and event.portal_type != 'Media Event':
            return ""
        
        if event.start() is None or event.end() is None:
            if event.start() is None and event.end() is None:
                return ""
            else:
                samedate = True
        else:
            samedate = event.start().strftime('%d - %m - %Y') == event.end().strftime('%d - %m - %Y')
            
        exceptions = ""
        
        if hasattr(event, 'exceptions'):
            exceptions = event.exceptions
            
        finalDatesFmt = '<div class="dates %(class)s"><span class="dateText">%(dates)s%(hours)s %(exceptions)s</span></div>'
        
        dates = "%s"%(samedate and (event.start() is not None and event.start().strftime('%A %d %B %Y') or event.end().strftime('%A %d %B %Y')) or "%s to %s"%(event.start().strftime('%A %d %B %Y'), event.end().strftime('%A %d %B %Y')))
        
        openingHour = event.start() is not None and event.start().strftime('%H:%M') or ""
        closingHour = event.end() is not None and event.end().strftime('to %H:%M') or ""
        hoursExist = 'to %s'%openingHour != closingHour
        
        hours = hoursExist and '<span class="hours">, %s %s</span>'%(openingHour, closingHour) or '<span class="hours">, %s</span>'%openingHour
        
        finalDates = finalDatesFmt%{'class': self.isEventPast(event) and 'past' or 'future', 'dates': dates, 'hours': hours, 'exceptions':exceptions}
        
        return finalDates
            
    def isBuyable(self, item):
        """
        Check if an item is buyable with PloneGetPaid
        """
        if not GETPAID_EXISTS:
            return False
        else:
            return IBuyableMarker.providedBy(item)
    
    def getEventBookingLink(self, event):
        """
        Check if the booking information is a link or just a code. return a full url
        """
        if not event.getBooking():
            return ""
        else:
            if event.getLink().find("http://") != -1:
                return event.getLink()
            else:
                return 'http://purchase.tickets.com/buy/TicketPurchase?agency=ARNOLFINI&organ_val=26385&schedule=list&event_val=%s'%event.getLink()
      
    def _uniq(self, alist):    # Fastest order preserving
        set = {}
        return [set.setdefault(e,e) for e in alist if e not in set]

class SearchView(CommonBrowserView, Search):
    """
    Adding to Search view
    """
    
class PagePortletView(ViewletBase):
    """
    helper classes for pagePortlet
    """
    def showManageButton(self):
        secman = getSecurityManager()
        if not secman.checkPermission('Portlets: Manage portlets', self.context):
            return False
        else:
            return True

class FooterView(FooterViewlet):
    """
    helper classes for footer
    """
    def showManageButton(self):
        secman = getSecurityManager()
        if not secman.checkPermission('Portlets: Manage portlets', self.context):
            return False
        else:
            return True

class FolderListing(CommonBrowserView):
    """'
    Override of folder_listing view
    """
    def results(self, batch=True, b_start = 0, pagesize=10, only_documented=False):
        results = []
        
        #print "FOLDER LISTING"
        if self.context.portal_type  == 'Collection':
            brains = self.context.queryCatalog(batch=False)
            if only_documented:
                final_res = []
                for res in brains:
                    if res.hasMedia:
                        final_res.append(res)
            else:
                final_res = list(brains)
            if batch:
               results = Batch(final_res, pagesize, start=b_start)
            else:
                return final_res
        elif self.context.portal_type  in ['Folder', 'Press Kit']:
            brains = self.context.getFolderContents()
            if only_documented:
                final_res = []
                for res in brains:
                    if res.hasMedia:
                        final_res.append(res)
            else:
                final_res = list(brains)
            if batch:
                results = Batch(final_res, pagesize, start=b_start)
            else:
                return final_res
        
        return results

class CollectionPortlet(base.Renderer, FolderListing):
    """
        Extend portlet base renderer
    """
    _template = ViewPageTemplateFile("alternative_templates/portletcollection.pt")
    render = _template


class SectionsViewlet(GlobalSectionsViewlet):
    """
    helper classes for sections
    """


