
from tracking import settings
import re

IP_RE = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')


# private static final String[] HEADERS_TO_TRY = {
#     "X-Forwarded-For",
#     "Proxy-Client-IP",
#     "WL-Proxy-Client-IP",
#     "HTTP_X_FORWARDED_FOR",
#     "HTTP_X_FORWARDED",
#     "HTTP_X_CLUSTER_CLIENT_IP",
#     "HTTP_CLIENT_IP",
#     "HTTP_FORWARDED_FOR",
#     "HTTP_FORWARDED",
#     "HTTP_VIA",
#     "REMOTE_ADDR" };
#
# public static String getClientIpAddress(HttpServletRequest request) {
#     for (String header : HEADERS_TO_TRY) {
#         String ip = request.getHeader(header);
#         if (ip != null && ip.length() != 0
#             && !"unknown".equalsIgnoreCase(ip)) {
#             return ip;
#         }
#     }
#     return request.getRemoteAddr();
# }

def get_ip(request):
    """
    Retrieves the remote IP address from the request data.  If the user is
    behind a proxy, they may have a comma-separated list of IP addresses, so
    we need to account for that.  In such a case, only the first IP in the
    list will be retrieved.  Also, some hosts that use a proxy will put the
    REMOTE_ADDR into HTTP_X_FORWARDED_FOR.  This will handle pulling back the
    IP from the proper place.
    """

    # if neither header contain a value, just use local loopback
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR',
                                  request.META.get('REMOTE_ADDR', '127.0.0.1'))
    if ip_address:
        # make sure we have one and only one IP
        try:
            ip_address = IP_RE.match(ip_address)
            if ip_address:
                ip_address = ip_address.group(0)
            else:
                # no IP, probably from some dirty proxy or other device
                # throw in some bogus IP
                ip_address = settings.TRACKING_BOGUS_IP
        except IndexError:
            pass

    return ip_address
