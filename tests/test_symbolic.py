from exex.core.symbolic import Symbol


def test_symbol_str():
    x = Symbol('x')
    assert str(x) == 'x'

def test_symbol_type():
    x = Symbol('x')