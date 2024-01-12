# La gramatica solo acepta la forma monto currency to currency 
# Por ej. 20 USD to LPS

# MONTO solo deben ser numeros ya sean enteros o decimales pero solo debe haber un punto.

# CURRENCY pueden ser letras en minusculas o en mayusculas con la abreviacion de los tipos de moneda a realizar la conversion.

conversionGrammar = """
    ?start: AMOUNT CURRENCY "to" CURRENCY
            | AMOUNT CURRENCY "TO" CURRENCY
            | AMOUNT CURRENCY "a" CURRENCY
            | AMOUNT CURRENCY "A" CURRENCY
            | AMOUNT CURRENCY "IN" CURRENCY
            | AMOUNT CURRENCY "in" CURRENCY
            | AMOUNT CURRENCY "en" CURRENCY
            | AMOUNT CURRENCY "EN" CURRENCY

    AMOUNT: /[0-9]+(\.[0-9]+)?/
    CURRENCY: /[A-Za-z]{3}/

    %import common.WS_INLINE
    %ignore WS_INLINE
"""