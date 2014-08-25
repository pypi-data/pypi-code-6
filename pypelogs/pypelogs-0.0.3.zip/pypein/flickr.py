import logging
import json
import datetime

LOG = logging.getLogger("Flickr")


class Flickr(object):
    """
    Input from the Flickr API.
    """
    def __init__(self, spec):
        # Defer import until we need it
        import flickrapi

        args = spec.split(',')
        creds_fname = args[0]
        if len(args) > 1:
            self.cmds = args[1:]
        else:
            self.cmds = ['interesting']
        # Parse creds file
        with open(creds_fname, "r") as fo:
            creds = eval(fo.read())
        LOG.info("Using creds: %s" % creds)

        self.flickr = flickrapi.FlickrAPI(creds['api_key'], creds['api_secret'], format='json')

    def __iter__(self):
        for cmd in self.cmds:
            n = cmd.find('=')  # (command)=(extras), as in interesting=owner_name,date_upload
            if n > 0:
                args = cmd[n+1:].split(',')
                cmd = cmd[0:n]
            else:
                args = None
            try:
                yielded = 0
                rsp = getattr(self, cmd)(args)
                for e in rsp:
                    yielded += 1
                    yield e
                LOG.info("Method '%s' yielded %s rows" % (cmd, yielded))
            except Exception, err:
                LOG.error("Error-Message: %s", err.message)

    def interesting(self, args=None):
        extras = ','.join(args) if args else 'last_update,geo,owner_name,url_sq'
        page = 1
        while True:
            LOG.info("Fetching page %s" % page)
            rsp = self.load_rsp(self.flickr.interestingness_getList(extras=extras, page=page))
            if rsp["stat"] == "ok":
                photos = rsp["photos"]
                if int(photos["page"]) < page:
                    LOG.info("End of Flickr pages (%s pages with %s per page)" % (photos["pages"], photos["perpage"]))
                    break
                for p in photos["photo"]:
                    if 'lastupdate' in p:
                        p['lastupdate'] = datetime.datetime.fromtimestamp(int(p['lastupdate']))
                    yield p
                page += 1
            else:
                yield [rsp]
                break

    @staticmethod
    def load_rsp(rsp):
        """
        Converts raw Flickr string response to Python dict
        """
        first = rsp.find('(') + 1
        last = rsp.rfind(')')
        return json.loads(rsp[first:last])
