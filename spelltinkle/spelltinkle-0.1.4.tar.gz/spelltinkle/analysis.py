from spelltinkle.document import Document


class AnalysisDocument(Document):
    def __init__(self, session, doc):
        Document.__init__(self, actions=AnalysisActions())
        self.name = '[analysis]'
        lines = []
        self.change(0, 0, 0, 0, lines)
        self.view.move(0, 0)

        
class AnalysisActions:
    def enter(self, doc):
        r = doc.view.r
        