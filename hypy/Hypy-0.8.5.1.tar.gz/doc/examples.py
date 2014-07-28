import sys
sys.path.insert(0, '/home/cdodt/wc/Hypy')
from hypy import *

INDEX = 'breakfast/'
db = HDatabase()
db.open(INDEX, 'w') # create it, destroying old one if it exists
db.close()
db.open(INDEX, 'a')

doc = HDocument(uri=u'http://estraier.gov/example.txt')
doc.addText(u"Hello there, this is my text.")
db.putDoc(doc)

# db = HDatabase(autoflush=True)  ## or ...
db.autoflush = True
# turning on autoflush does not immediately flush, so do that.
db.flush()

doc2 = HDocument(uri=u'http://estraier.gov/pricelist.txt')
doc2.addText(u"""Coffee: $2.00
Toast: $1.00
Eggs (2, any style): $3.00          Eggs (9, any style): $13.50
Eggs (3, any style): $4.50          Eggs (10, any style): $15.00
Eggs (4, any style): $6.00          Eggs (11, any style): $16.50
Eggs (5, any style): $7.50          Eggs (12, any style): $18.00
Eggs (6, any style): $9.00          Eggs (13, any style): $19.50
Eggs (7, any style): $10.50         Eggs (14, any style): $21.00
Eggs (8, any style): $12.00         Eggs (15, any style): $22.50
...
with apologies to the New Yorker for this joke""")
doc2[u'maxprice'] = u'22.50'
doc2[u'minprice'] = u'1.00'
db.putDoc(doc2)

if 0:
    print doc[u'@id']
    ## prints 1
    print doc[u'@uri']
    ## prints http://estraier.gov/example.txt

db.remove(id=1)  
db.putDoc(doc) # put it back so we can remove it again :)
db.remove(doc)
db.putDoc(doc) # and again..
db.remove(uri=u'http://estraier.gov/example.txt')

if 0:
    # n.b. the document gets a NEW ID each time we put it in..
    print doc[u'@id']
    ## prints 4

    print len(db)
    ## prints 1

    print db[u'http://estraier.gov/pricelist.txt']

    print doc2.encode('utf-16')


doc5 = HDocument(u'http://estraier.gov/weighted.txt')
doc5.addText(u"This is my boom-stick.")
doc5.addHiddenText(u"eggs " * 30)
db.putDoc(doc5)

if 0:
    print doc5.encode('utf-8')
    # prints This is my boom-stick.

cond = HCondition(u'eggs')
results = db.search(cond)
if 0:
    for doc in results:
        print doc[u'@id']
    # prints 2, then 5

    # you can also do this another way, using pluck:

    print results.pluck(u'@id')
    # prints [u'5', u'2']

cond = HCondition(u'egg*')
results = db.search(cond)
if 0:
    print len(results)
    print results[0][u'@uri']

doc6 = HDocument(u'http://estraier.gov/spam.txt')
doc6.addText(u'spam and eggs')
db.putDoc(doc6)

if 0:
    # simple, intersection:
    print db.search(HCondition(u'spam* eggs*')).pluck(u'@id')
    # prints [u'6']

    # union
    print db.search(HCondition(u'eggs spam', matching='union')).pluck(u'@id')
    # prints [u'5', u'2', u'6']

    # unions with simple matching - you cannot use wildcard matches with
    # matching='union' but you can do so with '|' syntax
    print db.search(HCondition(u'egg* | spam')).pluck(u'@id')
    # prints [u'5', u'2', u'6']

words = [u'toast']
results = db.search(HCondition(u' '.join(words)))
hit = results[0]
if 0:
    print hit.teaser(words) # default is 'html'
    # prints ......

    # another way to get the original search words:
    words = results.hintWords()

    print hit.teaser(words, format='rst')
    # prints ......


cond = HCondition()
cond.addAttr(u'@id STREQ 5')

if 0:
    print db.search(cond)[0][u'@id']
    # prints 5

cond = HCondition()
cond.addAttr(u'@id STREQ 5')
if 0:
    print db.search(cond)[0][u'@id']
    # prints 5

# for clarity in the rest of these examples, I'll use this function:
def attrSx(expr):
    cond = HCondition()
    cond.addAttr(expr)
    return u' '.join(db.search(cond).pluck(u'@id'))

# give another document some interesting attributes
doc6[u'maxprice'] = u'100'
doc6[u'minprice'] = u'0'
doc5[u'date'] = u'2009-01-01'
doc6[u'date'] = u'2009-02-02'

# commit the documents again, so they can be searched.  Note that this has
# nothing to do with flush() - these changes only exist in memory until
# you commit them with putDoc() and flush() too.  In this case, we are
# still using autoflush.
db.putDoc(doc6)
db.putDoc(doc5)

if 0:
    # numeric searches

    print attrSx(u'maxprice NUMGE 50')
    # prints 6

    # NOTE: documents that don't have an attribute are treated as having it
    # set to "0" when doing a numeric comparison. therefore all the documents
    # match this one:
    print attrSx(u'minprice NUMLE 50')
    # prints 2 6 5
    # and two documents match this one:
    print attrSx(u'minprice NUMLE 0.99')
    # prints 2 5


    # date comparisons are numeric comparisons
    print attrSx(u'date NUMGE 2008-12-31')
    # prints 6 5
    print attrSx(u'date NUMGE 2009-01-30')
    # prints 6

    # regular expressions, why not

    print attrSx(u'@uri STRRX (pricelist.txt|spam.txt)')
    # prints 2 6

    # you can invert them, too, to get only documents not matching
    print attrSx(u'@uri !STRRX (pricelist.txt|spam.txt)')
    # prints 5

# and of course, you can use attribute searches in the same condition with
# phrase searches
cond = HCondition(u'spam')
cond.addAttr(u'minprice NUMLE 50')
if 0:
    print db.search(cond)[0][u'@id']
    # prints 6

if 0:
    print db.search(HCondition(u'e*')).pluck(u'@id')
    # prints [u'5', u'2', u'5']
    print db.search(HCondition(u'e*', max=2)).pluck(u'@id')
    # prints [u'5', u'2'] .. what did you expect?
    print db.search(HCondition(u'e*', skip=2)).pluck(u'@id')
    # prints [u'6']

cond = HCondition(u'e*')

if 0:
    # natural order
    print db.search(cond).pluck(u'@id')
    # prints [u'5', u'2', u'6']

    # numeric ascending
    cond.setOrder(u'@id NUMA')
    print db.search(cond).pluck(u'@id')
    # prints [u'2', u'5', u'6']

    # numeric descending
    cond.setOrder(u'@id NUMD')
    print db.search(cond).pluck(u'@id')
    # prints [u'6', u'5', u'2']

