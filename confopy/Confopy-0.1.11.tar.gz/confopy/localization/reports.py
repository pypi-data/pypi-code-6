# coding: utf-8
'''
File: reports.py
Author: Oliver Zscheyge
Description:
    Implementation of all reports
'''

from confopy.analysis import Report, Analyzer, mean_stdev


METRIC_NAMES = [u"wordlength", u"spellcheck", u"lexicon", u"sentlength", u"personalstyle", u"impersonalstyle", u"simplepres", u"adverbmodifier", u"fillers", u"examplecount", u"sentlengthvar"]

class MultiDocReport(Report):
    """Overview/statistics for multiple documents.
    """
    def __init__(self):
        super(MultiDocReport, self).__init__(u"multidoc-de", u"de", u"Überblick über mehrere Dokumente")

    def execute(self, docs, args):
        output = list()
        metric_names = METRIC_NAMES
        A = Analyzer.instance()
        metrics = [A.get(metric=m) for m in metric_names]
        metrics = [m for m in metrics if m != None]
        corp = A.get(corpus=u"TIGER")
        results = list()
        for m in metrics:
            results.append([m.evaluate(d) for d in docs])
        stats = [mean_stdev(r, 2) for r in results]
        output.append(u"METRIC MEAN STDEV")
        for i in range(len(metrics)):
            output.append(u"%s %s %s" % (metric_names[i], stats[i][0], stats[i][1]))

        # Execute metrics on reference corpus
        output.append(u"")
        output.append(u"REFERENCE CORPUS")
        for m in metrics:
            val = m.evaluate(corp)
            output.append(u"%s %s" % (m.ID, val))

        output.append(u"")
        return u"\n".join(output)

    def _nltk_test(self, doc, corp):
        #sent_tokenizer = corp.sent_tokenizer()
        #sents = doc.sents(tokenizer=sent_tokenizer)
        #for s in sents:
        #    print u"SENTENCE"
        #    print s
        import sys
        #sys.exit(0)

Analyzer.register(MultiDocReport())

class DocumentComparison(Report):
    """Compares the metrics of 2 documents side by side
    """
    PAD = 2

    def __init__(self):
        super(DocumentComparison, self).__init__(u"doccomp-de", u"de", u"Vergleicht 2 Dokumente")

    def _compare(self, vals):
        return u"="

    def execute(self, docs, args):
        output = list()
        if len(docs) < 2 or len(docs) % 2 != 0:
            output.append(u"Error: Need an even number of documents (at least 2) for the document comparison report!")
        else:
            metric_names = METRIC_NAMES
            A = Analyzer.instance()
            metrics = [A.get(metric=m) for m in metric_names]
            metrics = [m for m in metrics if m != None]
            if len(docs) == 2:
                for m in metrics:
                    vals = [m.evaluate(doc) for doc in docs]
                    progress = u"="
                    if vals[0] > vals[1]:
                        progress = u"-"
                    elif vals[0] < vals[1]:
                        progress = u"+"
                    output.append(u"%s %.2f --> %.2f \t (%s)" % (m.ID, vals[0], vals[1], progress))

            else:
                half = len(docs) / 2
                output.append(u"m.ID + - =")
                for m in metrics:
                    results = list()
                    for i in range(half):
                        results.append((m.evaluate(docs[i]), m.evaluate(docs[i + half])))
                    counts = [0, 0, 0] # greater, less, equal
                    for r in results:
                        if r[0] > r[1]:
                            counts[1] += 1
                        elif r[0] < r[1]:
                            counts[0] += 1
                        else:
                            counts[2] += 1
                    output.append(u"%s %s %s %s" % (m.ID, counts[0], counts[1], counts[2]))
        return u"\n".join(output)

Analyzer.register(DocumentComparison())




class DocumentReport(Report):
    """Overview over a single document.
    """
    def __init__(self):
        super(DocumentReport, self).__init__(u"document", u"de", u"Überblick über ein einzelnes Dokument")

    def execute(self, docs, args):
        output = list()
        return u"\n".join(output)

Analyzer.register(DocumentReport())



class DocumentDetailedReport(Report):
    """Detailed analysis of a single document.
    """
    def __init__(self):
        super(DocumentDetailedReport, self).__init__(u"document-detail", u"de", u"Detaillierte Analyse eines Dokuments")

    def execute(self, docs, args):
        output = list()
        return u"\n".join(output)

Analyzer.register(DocumentDetailedReport())
