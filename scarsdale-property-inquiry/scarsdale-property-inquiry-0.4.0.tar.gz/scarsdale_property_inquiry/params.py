def url():
    return 'http://www.scarsdale.com/Home/Departments/InformationTechnology/PropertyInquiry.aspx'

def headers(user_agent):
    return {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'User-Agent': user_agent,
        'Referer': url(),
        'Content-Encoding': 'gzip',
    }

def data(publickeytoken, viewstate, eventvalidation, eventtarget, value):
    return [
        ('StylesheetManager_TSSM', ''),
        ('ScriptManager_TSM', ';;System.Web.Extensions, Version=3.5.0.0, Culture=neutral, PublicKeyToken=' + publickeytoken),
        ('__EVENTTARGET', eventtarget),
        ('__EVENTARGUMENT', ''),
        ('__LASTFOCUS', ''),
        ('__VIEWSTATE', viewstate),
        ('__EVENTVALIDATION', eventvalidation),
        ('dnn$SEARCH1$Search', 'SiteRadioButton'),
        ('dnn$SEARCH1$txtSearch', ''),
        (eventtarget, value),
        ('dnn$dnnSEARCH$Search', 'SiteRadioButton'),
        ('dnn$dnnSEARCH$txtSearch', ''),
        ('ScrollTop', 73), # how far the page is scrolled
        ('__dnnVariable', '{"__scdoff":"1"}'),
    ]

def house_data(publickeytoken, viewstate, eventvalidation, house_id):
#   eventtarget = 'dnn$ctr1398$ViewHelloWorld$lstboxAddresses'
    eventtarget = 'dnn$ctr1398$ViewHelloWorld$txtProperty'
    result = data(publickeytoken, viewstate, eventvalidation, eventtarget, house_id)
    return result

def street_data(publickeytoken, viewstate, eventvalidation, street_id):
    eventtarget = 'dnn$ctr1398$ViewHelloWorld$lstboxStreets'
    result = data(publickeytoken, viewstate, eventvalidation, eventtarget, street_id)
    i = result.index(("dnn$dnnSEARCH$Search", "SiteRadioButton"))
    result.insert(i, ('dnn$ctr1398$ViewHelloWorld$txtProperty', ''))
    return result
