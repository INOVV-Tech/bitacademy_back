from decimal import Decimal

def quantize(value: Decimal) -> Decimal:
    return value.quantize(Decimal('1.000000'))

def is_decimal(value: str) -> bool:
    try:
        return value.isdecimal()
    except:
        return False
    
def not_decimal(value: str) -> bool:
    try:
        return not value.isdecimal()
    except:
        return True