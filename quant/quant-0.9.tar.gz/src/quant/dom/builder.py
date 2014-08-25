import dm.dom.builder
from dm.dom.stateful import *

from dm.dom.apikey import ApiKey
from quant.dom.market import Exchange
from quant.dom.market import Symbol
from quant.dom.market import Image
from quant.dom.market import Market
from quant.dom.market import EuropeanOptionMarket
from quant.dom.market import Value
from quant.dom.market import Metric
from quant.contracttype.simple import OptionRight
from quant.contracttype.simple import FuturesRight
from quant.dom.book import Book
from quant.dom.result import Result, ResultLine
from quant.dom.extension import ContractType
from quant.dom.extension import PriceProcess
from quant.dom.extension import Pricer
from quant.dom.extension import PricerPreference

class ModelBuilder(dm.dom.builder.ModelBuilder):

    def loadImage(self):
        pass

    def construct(self):
        super(ModelBuilder, self).construct()
        # Core model.
        self.registry.registerDomainClass(ApiKey)
        self.registry.registerDomainClass(Exchange)
        self.registry.registerDomainClass(Symbol)
        self.registry.registerDomainClass(Market)
        self.registry.registerDomainClass(EuropeanOptionMarket)
        self.registry.registerDomainClass(Value)
        self.registry.registerDomainClass(Image)
        self.registry.registerDomainClass(Metric)
        self.registry.registerDomainClass(OptionRight)
        self.registry.registerDomainClass(FuturesRight)
        self.registry.registerDomainClass(Book)
        self.registry.registerDomainClass(ResultLine)
        self.registry.registerDomainClass(Result)
        self.registry.apiKeys = ApiKey.createRegister()
        self.registry.exchanges = Exchange.createRegister()
        Exchange.principalRegister = self.registry.exchanges
        self.registry.symbols = Symbol.createRegister()
        Symbol.principalRegister = self.registry.symbols
        self.registry.markets = Market.createRegister()
        Market.principalRegister = self.registry.markets
        self.registry.images = Image.createRegister()
        Image.principalRegister = self.registry.images
        self.registry.optionRights = OptionRight.createRegister()
        OptionRight.principalRegister = self.registry.optionRights
        self.registry.futuresRights = FuturesRight.createRegister()
        FuturesRight.principalRegister = self.registry.futuresRights
        self.registry.books = Book.createRegister()
        Book.principalRegister = self.registry.books
        self.registry.resultLines = ResultLine.createRegister()
        ResultLine.principalRegister = self.registry.resultLines
        self.registry.results = Result.createRegister()
        Result.principalRegister = self.registry.results
        # Extensions.
        self.registry.registerDomainClass(ContractType)
        self.registry.registerDomainClass(PriceProcess)
        self.registry.registerDomainClass(Pricer)
        self.registry.registerDomainClass(PricerPreference)
        self.registry.contractTypes = ContractType.createRegister()
        ContractType.principalRegister = self.registry.contractTypes
        self.registry.priceProcesses = PriceProcess.createRegister()
        PriceProcess.principalRegister = self.registry.priceProcesses
        self.registry.pricers = Pricer.createRegister()
        Pricer.principalRegister = self.registry.pricers
        self.registry.pricerPreferences = PricerPreference.createRegister()
        PricerPreference.principalRegister = self.registry.pricerPreferences
        #self.registry.loadBackgroundRegister(self.registry.contractTypes)
        #self.registry.loadBackgroundRegister(self.registry.priceProcesses)
        #self.registry.loadBackgroundRegister(self.registry.pricers)
        #self.registry.loadBackgroundRegister(self.registry.pricerPreferences)
        # Contracts from contract types.
        for contractType in self.registry.contractTypes:
            try:
                contractClass = contractType.getCodeClass()
            except ImportError, inst:
                # Todo: Write this to the logger.
                msg = "Error importing code for contract type '%s'." % contractType.getLabelValue()
                print msg
            else:
                self.registry.registerDomainClass(contractClass)
                registryAttrName = contractClass.getRegistryAttrName() 
                contractRegister = contractClass.createRegister()
                setattr(self.registry, registryAttrName, contractRegister)
                contractClass.principalRegister = contractRegister

