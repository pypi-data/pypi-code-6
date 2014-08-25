from quant.djangoapp.apps.eui.views.base import QuantView
from dm.view.registry import RegistryNavigation
from dm.view.registry import RegistryFieldNames
from dm.view.registry import RegistryContextSetter
from dm.view.registry import RegistryView
from dm.view.registry import RegistryListView
from dm.view.registry import RegistryCreateView
from dm.view.registry import RegistryReadView
from dm.view.registry import RegistrySearchView
from dm.view.registry import RegistryFindView
from dm.view.registry import RegistryUpdateView
from dm.view.registry import RegistryDeleteView
from quant.contracttype.simple import Contract 

# Todo: Set navigation for extension contract types.

class SymbolNavigation(RegistryNavigation):

    def createMajorItem(self):
        return '/symbols/'

    def createMinorItem(self):
        return ''

    def createMinorItems(self):
        items = []
        items.append(
            {'title': 'Index', 'url': '/symbols/'}
        )
        items.append(
            {'title': 'New', 'url': '/symbols/create/'}
        )
        return items


class CodesNavigation(RegistryNavigation):

    def createMajorItem(self):
        return '/codes/'

    def createMinorItem(self):
        return ''

    def createMinorItems(self):
        items = []
        items.append(
            {'title': 'Price processes', 'url': '/priceProcesses/'}
        )
        items.append(
            {'title': 'Contract types', 'url': '/contractTypes/'}
        )
        items.append(
            {'title': 'Pricers', 'url': '/pricers/'}
        )
        items.append(
            {'title': 'Pricer preferences', 'url': '/pricerPreferences/'}
        )
        return items


class ContractTypeNavigation(CodesNavigation):

    def createMinorItem(self):
        return '/contractTypes/'


class PricerNavigation(CodesNavigation):

    def createMinorItem(self):
        return '/pricers/'


class PriceProcessNavigation(CodesNavigation):

    def createMinorItem(self):
        return '/priceProcesses/'


class PricerPreferenceNavigation(CodesNavigation):

    def createMinorItem(self):
        return '/pricerPreferences/'


class ImageNavigation(RegistryNavigation):

    def createMajorItem(self):
        return '/images/'

    def createMinorItem(self):
        return ''

    def createMinorItems(self):
        items = []
        items.append(
            {'title': 'Index', 'url': '/images/'}
        )
        items.append(
            {'title': 'New', 'url': '/images/create/'}
        )
        return items


class MarketNavigation(RegistryNavigation):

    def createMajorItem(self):
        return '/markets/'

    def createMinorItem(self):
        return ''

    def createMinorItems(self):
        items = []
        items.append(
            {'title': 'Index', 'url': '/markets/'}
        )
        items.append(
            {'title': 'New', 'url': '/markets/create/'}
        )
        return items


class TradesNavigation(RegistryNavigation):

    def createMajorItem(self):
        return '/trades/'

    def createMinorItem(self):
        return '/%s/' % self.view.getManipulatedObjectRegister().getDomainClass().getRegistryAttrName()

    def createMinorItems(self):
        items = []
        for contractType in self.view.registry.contractTypes:
            if contractType.canImportCode():
                registryAttrName = contractType.getExtensionRegistryAttrName()
                items.append({
                    'title': registryAttrName.capitalize(),
                    'url': '/%s/' % registryAttrName
                })
        return items


class BookNavigation(RegistryNavigation):

    def createMajorItem(self):
        return '/books/'

    def createMinorItem(self):
        return ''

    def createMinorItems(self):
        items = []
        items.append(
            {'title': 'Index', 'url': '/books/'}
        )
        items.append(
            {'title': 'New', 'url': '/books/create/'}
        )
        return items


class ResultNavigation(RegistryNavigation):

    def createMajorItem(self):
        return '/results/'

    def createMinorItem(self):
        return ''

    def createMinorItems(self):
        items = []
        items.append(
            {'title': 'Index', 'url': '/results/'}
        )
        items.append(
            {'title': 'New', 'url': '/results/create/'}
        )
        return items


class QuantRegistryView(RegistryView, QuantView):

    domainClassName = ''
    manipulatedFieldNames = {
    }
    manipulators = {
    }
    redirectors = {
    }
    navigation = {
        'symbols/list':   SymbolNavigation,
        'symbols/create': SymbolNavigation,
        'symbols/read':   SymbolNavigation,
        'symbols/update': SymbolNavigation,
        'symbols/delete': SymbolNavigation,
        'priceProcesses/list':   PriceProcessNavigation,
        'priceProcesses/create': PriceProcessNavigation,
        'priceProcesses/read':   PriceProcessNavigation,
        'priceProcesses/update': PriceProcessNavigation,
        'priceProcesses/delete': PriceProcessNavigation,
        'pricerPreferences/list':   PricerPreferenceNavigation,
        'pricerPreferences/create': PricerPreferenceNavigation,
        'pricerPreferences/read':   PricerPreferenceNavigation,
        'pricerPreferences/update': PricerPreferenceNavigation,
        'pricerPreferences/delete': PricerPreferenceNavigation,
        'contractTypes/list':   ContractTypeNavigation,
        'contractTypes/create': ContractTypeNavigation,
        'contractTypes/read':   ContractTypeNavigation,
        'contractTypes/update': ContractTypeNavigation,
        'contractTypes/delete': ContractTypeNavigation,
        'images/list':   ImageNavigation,
        'images/create': ImageNavigation,
        'images/read':   ImageNavigation,
        'images/update': ImageNavigation,
        'images/delete': ImageNavigation,
        'markets/list':   MarketNavigation,
        'markets/create': MarketNavigation,
        'markets/read':   MarketNavigation,
        'markets/update': MarketNavigation,
        'markets/delete': MarketNavigation,
        'trades/list':   TradesNavigation,
        'trades/create': TradesNavigation,
        'trades/read':   TradesNavigation,
        'trades/update': TradesNavigation,
        'trades/delete': TradesNavigation,
        'pricers/list':   PricerNavigation,
        'pricers/create': PricerNavigation,
        'pricers/read':   PricerNavigation,
        'pricers/update': PricerNavigation,
        'pricers/delete': PricerNavigation,
        'books/list':   BookNavigation,
        'books/create': BookNavigation,
        'books/read':   BookNavigation,
        'books/update': BookNavigation,
        'books/delete': BookNavigation,
        'results/list':   ResultNavigation,
        'results/create': ResultNavigation,
        'results/read':   ResultNavigation,
        'results/update': ResultNavigation,
        'results/delete': ResultNavigation,
    }
    contextSetters = {
    }

    def getViewPosition(self):
        domainClass = self.getManipulatedObjectRegister().getDomainClass()
        if issubclass(domainClass, Contract):
            viewPosition = 'trades/' + self.getTemplatePathActionName()
        else:
            viewPosition = super(QuantRegistryView, self).getViewPosition()
        return viewPosition


class QuantRegistryListView(QuantRegistryView, RegistryListView):
    pass

class QuantRegistryCreateView(QuantRegistryView, RegistryCreateView):
    pass

class QuantRegistryReadView(QuantRegistryView, RegistryReadView):
    pass

class QuantRegistrySearchView(QuantRegistryView, RegistrySearchView):
    pass

class QuantRegistryFindView(QuantRegistryView, RegistryFindView):
    pass

class QuantRegistryUpdateView(QuantRegistryView, RegistryUpdateView):
    pass

class QuantRegistryDeleteView(QuantRegistryView, RegistryDeleteView):
    pass


def view(request, registryPath, actionName='', actionValue=''):
    pathNames = registryPath.split('/')
    pathLen = len(pathNames)
    if not actionName:
        if pathLen % 2:
            actionName = 'list'
        else:
            actionName = 'read'
    if actionName == 'list':
        viewClass = QuantRegistryListView
    elif actionName == 'create':
        viewClass = QuantRegistryCreateView
    elif actionName == 'read':
        viewClass = QuantRegistryReadView
    elif actionName == 'search':
        viewClass = QuantRegistrySearchView
    elif actionName == 'find':
        viewClass = QuantRegistryFindView
    elif actionName == 'update':
        viewClass = QuantRegistryUpdateView
    elif actionName == 'delete':
        viewClass = QuantRegistryDeleteView
    elif actionName == 'undelete':
        viewClass = QuantRegistryUndeleteView
    elif actionName == 'purge':
        viewClass = QuantRegisryPurgeView
    else:
        raise Exception("No view class for actionName '%s'." % actionName)
    view = viewClass(
        request=request,
        registryPath=registryPath,
        actionName=actionName,
        actionValue=actionValue
    )
    return view.getResponse()

