import requests
import codecs
import sys
from requests import Response
import logging
from logging import StreamHandler
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger('response_analysis.parse_worthy')
logger.setLevel(logging.INFO)
sys.stdin = codecs.getreader('utf-8')(sys.stdin)
sys.stderr = codecs.getwriter('utf-8')(sys.stderr)

def parse_worthy(response, max_parse_size = 2000000, hadoop_reporting = False):

    if not isinstance(response, Response):
        raise Exception("Response must be of type requests.Response")

    if not "content-type" in response.headers:

        if hadoop_reporting:
            logger.info(u"No Content Type header, not parsing " + unicode(response.url))

        return False

    else:

        logger.info(u"Content type is of type " + unicode(response.headers["content-type"]) + u": " + unicode(response.url))
        if not "text" in response.headers["content-type"]:
            if hadoop_reporting:
                logger.info(u"Content type is not of type text" + unicode(ftarget))

            return False

    if "content-length" in response.headers:

        if hadoop_reporting:
            logger.info(u"Content length is " + unicode(response.headers["content-length"]) + u": " + unicode(response.url))

        if int(response.headers["content-length"]) > max_parse_size:

            if hadoop_reporting:
                logger.info(u"Content length is " + unicode(response.headers["content-length"]) + u" NOT parsing: " + unicode(response.url))

            return False

    else:

        logger.info(u"Target %s does not have a content-length header, getting size manually for " % unicode(response.url))
        size = sys.getsizeof(response.content)
        if size > max_parse_size:

            if hadoop_reporting:
                logger.info(u"Response is of size %s for url" % (unicode(size), unicode(response.url)))

            return False

    return True

if __name__ == "__main__":
 
    r = requests.get("http://www.ada.gov/hospcombrprt.pdf")
    print parse_worthy(r)



