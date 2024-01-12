from lark import Lark, Transformer
from lark.tree import Tree

from helpers.conversionRates import conversionRates
from helpers.conversionGrammar import conversionGrammar

class ConvertCurrency(Transformer):
    def start(self, items):
        amount = float(items[0])
        fromCurrency = items[1].upper()
        toCurrency = items[2].upper()
        rate = conversionRates[fromCurrency]['exchange'][toCurrency]
        convertedAmount = amount * rate
        tree = Tree('CONVERSION', [Tree('CANTIDAD:'.center(15), [amount]), Tree('ORIGEN:'.center(15), [fromCurrency]), Tree('DESTINO:'.center(15), [toCurrency]), Tree('RESULTADO:'.center(15), [convertedAmount])])
        return tree

conversionParser = Lark(conversionGrammar, parser='lalr', transformer=ConvertCurrency())
convertCurrency = conversionParser.parse