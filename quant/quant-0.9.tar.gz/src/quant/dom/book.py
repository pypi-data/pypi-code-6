from quant.dom.base import SimpleObject, String, HasMany, AggregatesMany, HasA

class Book(SimpleObject):

    isUnique = False

    isTemporal = True

    title = String(isTemporal=True)
    results = AggregatesMany('Result', key='id')

    def getLabelValue(self):
        return self.title or self.id

    def getContracts(self):
        contracts = []
        for contractType in self.registry.contractTypes:
            register = contractType.getCodeClass().createRegister()
            contracts += register.findDomainObjects(book=self)
        return contracts

    def countContracts(self):
        return len(self.getContracts())

    def delete(self):
        for contract in self.getContracts():
            contract.book = None
            contract.save()
        super(Book, self).delete()

