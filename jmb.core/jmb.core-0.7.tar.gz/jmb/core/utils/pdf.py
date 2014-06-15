# -*- coding: utf-8 -*-

from reportlab.lib import colors, pagesizes
from reportlab.lib.units import cm
from reportlab.platypus.frames import Frame
from reportlab.platypus.flowables import Spacer, KeepTogether
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.platypus import Table, TableStyle, FrameBreak
from reportlab.rl_config import defaultPageSize
import sys, os, time

class PortraitTemplate(BaseDocTemplate):
    _invalidInitArgs = ('pageTemplates',)

    def __init__(self, filename, titolo_report=None, frame=None, show_date=True, **kw):
        self.titolo_report = titolo_report
        self.show_date = show_date
        self.PAGE_HEIGHT = defaultPageSize[1]
        self.PAGE_WIDTH = defaultPageSize[0]
        if frame:
            frame1 = frame
        else:
            if not titolo_report:
                frame1 = Frame(0.5*cm,1.5*cm, self.PAGE_WIDTH - 1 *cm, self.PAGE_HEIGHT - 1.5 *cm, id='F1', showBoundary=0)
            else:
                frame1 = Frame(1*cm,1.5*cm, self.PAGE_WIDTH - 2 *cm, self.PAGE_HEIGHT - 3 *cm, id='F1', showBoundary=0)
        BaseDocTemplate.__init__(self, filename, **kw)
        template = PageTemplate('normal', [frame1], self.ReportPageFrame)
        self.addPageTemplates(template)

    def ReportPageFrame(self, canvas, doc):
        "The page frame used for all PDF documents."
        Title = self.titolo_report
        ora = time.strftime("%d-%b-%Y %H:%M",time.localtime())
        canvas.saveState()
        if Title:
            canvas.setFont('Times-Bold', 15)
            canvas.line(1*cm, self.PAGE_HEIGHT - 0.5*cm, self.PAGE_WIDTH - 1*cm, self.PAGE_HEIGHT - 0.5*cm)
            canvas.drawString(1*cm, self.PAGE_HEIGHT - 1*cm, Title)
            canvas.line(1*cm, self.PAGE_HEIGHT - 1.2*cm, self.PAGE_WIDTH - 1*cm, self.PAGE_HEIGHT - 1.2*cm)
        canvas.setFont('Times-Roman', 10)
        if self.show_date:
            canvas.drawString(cm, cm, ora)
        pageNumber = canvas.getPageNumber()
        canvas.drawString(self.PAGE_WIDTH /2, cm, str(pageNumber))
        canvas.restoreState()


class PdfReport:
    def generate_pdf(self):
        # Build story.
        story = []

        # Creo la struttura per creare il report pdf ciclando nell'iteratore del report
        #
        for flowable in self.getFlowables():
            story.append(flowable)

        # Creo il pdf vero e proprio
        #
        self.doc.multiBuild(story)